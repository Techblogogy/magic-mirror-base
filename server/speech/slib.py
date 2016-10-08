
import io, os, subprocess, wave, aifc, base64, sys
import math, audioop, collections, threading
import platform, stat, random, uuid
import json

import datetime

import httplib

import contextlib
from six.moves import queue

# from googleapiclient import discovery
# import httplib2
from oauth2client.client import GoogleCredentials

# from gcloud.credentials import get_credentials
# from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
# from grpc.beta import implementations

# from gcloud import credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations

SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'

import numpy, struct

from minfo import app_dir

try: # attempt to use the Python 2 modules
    from urllib import urlencode
    from urllib2 import Request, urlopen, URLError, HTTPError
except ImportError: # use the Python 3 modules
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

# define exceptions
class WaitTimeoutError(Exception): pass
class RequestError(Exception): pass
class UnknownValueError(Exception): pass

class AudioSource(object):
    def __init__(self):
        raise NotImplementedError("this is an abstract class")

    def __enter__(self):
        raise NotImplementedError("this is an abstract class")

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError("this is an abstract class")

class Microphone(AudioSource):
    """
    Creates a new ``Microphone`` instance, which represents a physical microphone on the computer. Subclass of ``AudioSource``.

    This will throw an ``AttributeError`` if you don't have PyAudio 0.2.9 or later installed.

    If ``device_index`` is unspecified or ``None``, the default microphone is used as the audio source. Otherwise, ``device_index`` should be the index of the device to use for audio input.

    A device index is an integer between 0 and ``pyaudio.get_device_count() - 1`` (assume we have used ``import pyaudio`` beforehand) inclusive. It represents an audio device such as a microphone or speaker. See the `PyAudio documentation <http://people.csail.mit.edu/hubert/pyaudio/docs/>`__ for more details.

    The microphone audio is recorded in chunks of ``chunk_size`` samples, at a rate of ``sample_rate`` samples per second (Hertz).

    Higher ``sample_rate`` values result in better audio quality, but also more bandwidth (and therefore, slower recognition). Additionally, some machines, such as some Raspberry Pi models, can't keep up if this value is too high.

    Higher ``chunk_size`` values help avoid triggering on rapidly changing ambient noise, but also makes detection less sensitive. This value, generally, should be left at its default.
    """
    def __init__(self, device_index = None, sample_rate = 16000, chunk_size = 1024):
        # set up PyAudio
        self.pyaudio_module = self.get_pyaudio()

        assert device_index is None or isinstance(device_index, int), "Device index must be None or an integer"
        if device_index is not None: # ensure device index is in range
            audio = self.pyaudio_module.PyAudio()
            try:
                count = audio.get_device_count() # obtain device count
            except:
                audio.terminate()
                raise
            assert 0 <= device_index < count, "Device index out of range ({0} devices available; device index should be between 0 and {1} inclusive)".format(count, count - 1)
        assert isinstance(sample_rate, int) and sample_rate > 0, "Sample rate must be a positive integer"
        assert isinstance(chunk_size, int) and chunk_size > 0, "Chunk size must be a positive integer"
        self.device_index = device_index
        self.format = self.pyaudio_module.paInt16 # 16-bit int sampling
        self.SAMPLE_WIDTH = self.pyaudio_module.get_sample_size(self.format) # size of each sample
        self.SAMPLE_RATE = sample_rate # sampling rate in Hertz
        self.CHUNK = chunk_size # number of frames stored in each buffer

        self.audio = None
        self.stream = None

    @staticmethod
    def get_pyaudio():
        """
        Imports the pyaudio module and checks its version. Throws exceptions if pyaudio can't be found or a wrong version is installed
        """
        try:
            import pyaudio
        except ImportError:
            raise AttributeError("Could not find PyAudio; check installation")
        from distutils.version import LooseVersion
        if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.9"):
            raise AttributeError("PyAudio 0.2.9 or later is required (found version {0})".format(pyaudio.__version__))
        return pyaudio

    @staticmethod
    def list_microphone_names():
        """
        Returns a list of the names of all available microphones. For microphones where the name can't be retrieved, the list entry contains ``None`` instead.

        The index of each microphone's name is the same as its device index when creating a ``Microphone`` instance - indices in this list can be used as values of ``device_index``.
        """
        audio = Microphone.get_pyaudio().PyAudio()
        try:
            result = []
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                result.append(device_info.get("name"))
        finally:
            audio.terminate()
        return result

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"
        self.audio = self.pyaudio_module.PyAudio()
        try:
            self.stream = Microphone.MicrophoneStream(
                self.audio.open(
                    input_device_index = self.device_index, channels = 1,
                    format = self.format, rate = self.SAMPLE_RATE, frames_per_buffer = self.CHUNK,
                    input = True, # stream is an input stream
                )
            )
        except:
            self.audio.terminate()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.stream.close()
        finally:
            self.stream = None
            self.audio.terminate()

    class MicrophoneStream(object):
        def __init__(self, pyaudio_stream):
            self.pyaudio_stream = pyaudio_stream

        def read(self, size):
            return self.pyaudio_stream.read(size, exception_on_overflow = False)

        def close(self):
            try:
                # sometimes, if the stream isn't stopped, closing the stream throws an exception
                if not self.pyaudio_stream.is_stopped():
                    self.pyaudio_stream.stop_stream()
            finally:
                self.pyaudio_stream.close()

class AudioFile(AudioSource):
    """
    Creates a new ``AudioFile`` instance given a WAV/AIFF/FLAC audio file `filename_or_fileobject`. Subclass of ``AudioSource``.

    If ``filename_or_fileobject`` is a string, then it is interpreted as a path to an audio file on the filesystem. Otherwise, ``filename_or_fileobject`` should be a file-like object such as ``io.BytesIO`` or similar.

    Note that functions that read from the audio (such as ``recognizer_instance.record`` or ``recognizer_instance.listen``) will move ahead in the stream. For example, if you execute ``recognizer_instance.record(audiofile_instance, duration=10)`` twice, the first time it will return the first 10 seconds of audio, and the second time it will return the 10 seconds of audio right after that. This is always reset to the beginning when entering an ``AudioFile`` context.

    WAV files must be in PCM/LPCM format; WAVE_FORMAT_EXTENSIBLE and compressed WAV are not supported and may result in undefined behaviour.

    Both AIFF and AIFF-C (compressed AIFF) formats are supported.

    FLAC files must be in native FLAC format; OGG-FLAC is not supported and may result in undefined behaviour.
    """

    def __init__(self, filename_or_fileobject):
        if str is bytes: # Python 2 - if a file path is specified, it must either be a `str` instance or a `unicode` instance
            assert isinstance(filename_or_fileobject, (str, unicode)) or hasattr(filename_or_fileobject, "read"), "Given audio file must be a filename string or a file-like object"
        else: # Python 3 - if a file path is specified, it must be a `str` instance
            assert isinstance(filename_or_fileobject, str) or hasattr(filename_or_fileobject, "read"), "Given audio file must be a filename string or a file-like object"
        self.filename_or_fileobject = filename_or_fileobject
        self.stream = None
        self.DURATION = None

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"
        try:
            # attempt to read the file as WAV
            self.audio_reader = wave.open(self.filename_or_fileobject, "rb")
            self.little_endian = True # RIFF WAV is a little-endian format (most ``audioop`` operations assume that the frames are stored in little-endian form)
        except wave.Error:
            try:
                # attempt to read the file as AIFF
                self.audio_reader = aifc.open(self.filename_or_fileobject, "rb")
                self.little_endian = False # AIFF is a big-endian format
            except aifc.Error:
                # attempt to read the file as FLAC
                if hasattr(self.filename_or_fileobject, "read"):
                    flac_data = self.filename_or_fileobject.read()
                else:
                    with open(self.filename_or_fileobject, "rb") as f: flac_data = f.read()

                # run the FLAC converter with the FLAC data to get the AIFF data
                flac_converter = get_flac_converter()
                process = subprocess.Popen([
                    flac_converter,
                    "--stdout", "--totally-silent", # put the resulting AIFF file in stdout, and make sure it's not mixed with any program output
                    "--decode", "--force-aiff-format", # decode the FLAC file into an AIFF file
                    "-", # the input FLAC file contents will be given in stdin
                ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                aiff_data, stderr = process.communicate(flac_data)
                aiff_file = io.BytesIO(aiff_data)
                try:
                    self.audio_reader = aifc.open(aiff_file, "rb")
                except aifc.Error:
                    assert False, "Audio file could not be read as WAV, AIFF, or FLAC; check if file is corrupted"
                self.little_endian = False # AIFF is a big-endian format
        assert 1 <= self.audio_reader.getnchannels() <= 2, "Audio must be mono or stereo"
        self.SAMPLE_WIDTH = self.audio_reader.getsampwidth()

        # 24-bit audio needs some special handling for old Python versions (workaround for https://bugs.python.org/issue12866)
        samples_24_bit_pretending_to_be_32_bit = False
        if self.SAMPLE_WIDTH == 3: # 24-bit audio
            try: audioop.bias(b"", self.SAMPLE_WIDTH, 0) # test whether this sample width is supported (for example, ``audioop`` in Python 3.3 and below don't support sample width 3, while Python 3.4+ do)
            except audioop.error: # this version of audioop doesn't support 24-bit audio (probably Python 3.3 or less)
                samples_24_bit_pretending_to_be_32_bit = True # while the ``AudioFile`` instance will outwardly appear to be 32-bit, it will actually internally be 24-bit
                self.SAMPLE_WIDTH = 4 # the ``AudioFile`` instance should present itself as a 32-bit stream now, since we'll be converting into 32-bit on the fly when reading

        self.SAMPLE_RATE = self.audio_reader.getframerate()
        self.CHUNK = 4096
        self.FRAME_COUNT = self.audio_reader.getnframes()
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)
        self.stream = AudioFile.AudioFileStream(self.audio_reader, self.little_endian, samples_24_bit_pretending_to_be_32_bit)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not hasattr(self.filename_or_fileobject, "read"): # only close the file if it was opened by this class in the first place (if the file was originally given as a path)
            self.audio_reader.close()
        self.stream = None
        self.DURATION = None

    class AudioFileStream(object):
        def __init__(self, audio_reader, little_endian, samples_24_bit_pretending_to_be_32_bit):
            self.audio_reader = audio_reader # an audio file object (e.g., a `wave.Wave_read` instance)
            self.little_endian = little_endian # whether the audio data is little-endian (when working with big-endian things, we'll have to convert it to little-endian before we process it)
            self.samples_24_bit_pretending_to_be_32_bit = samples_24_bit_pretending_to_be_32_bit # this is true if the audio is 24-bit audio, but 24-bit audio isn't supported, so we have to pretend that this is 32-bit audio and convert it on the fly

        def read(self, size = -1):
            buffer = self.audio_reader.readframes(self.audio_reader.getnframes() if size == -1 else size)
            if not isinstance(buffer, bytes): buffer = b"" # workaround for https://bugs.python.org/issue24608

            sample_width = self.audio_reader.getsampwidth()
            if not self.little_endian: # big endian format, convert to little endian on the fly
                if hasattr(audioop, "byteswap"): # ``audioop.byteswap`` was only added in Python 3.4 (incidentally, that also means that we don't need to worry about 24-bit audio being unsupported, since Python 3.4+ always has that functionality)
                    buffer = audioop.byteswap(buffer, sample_width)
                else: # manually reverse the bytes of each sample, which is slower but works well enough as a fallback
                    buffer = buffer[sample_width - 1::-1] + b"".join(buffer[i + sample_width:i:-1] for i in range(sample_width - 1, len(buffer), sample_width))

            # workaround for https://bugs.python.org/issue12866
            if self.samples_24_bit_pretending_to_be_32_bit: # we need to convert samples from 24-bit to 32-bit before we can process them with ``audioop`` functions
                buffer = b"".join("\x00" + buffer[i:i + sample_width] for i in range(0, len(buffer), sample_width)) # since we're in little endian, we prepend a zero byte to each 24-bit sample to get a 32-bit sample
            if self.audio_reader.getnchannels() != 1: # stereo audio
                buffer = audioop.tomono(buffer, sample_width, 1, 1) # convert stereo audio data to mono
            return buffer

class AudioData(object):
    def __init__(self, frame_data, sample_rate, sample_width):
        assert sample_rate > 0, "Sample rate must be a positive integer"
        assert sample_width % 1 == 0 and 1 <= sample_width <= 4, "Sample width must be between 1 and 4 inclusive"
        self.frame_data = frame_data
        self.sample_rate = sample_rate
        self.sample_width = int(sample_width)

    def get_raw_data(self, convert_rate = None, convert_width = None):
        """
        Returns a byte string representing the raw frame data for the audio represented by the ``AudioData`` instance.

        If ``convert_rate`` is specified and the audio sample rate is not ``convert_rate`` Hz, the resulting audio is resampled to match.

        If ``convert_width`` is specified and the audio samples are not ``convert_width`` bytes each, the resulting audio is converted to match.

        Writing these bytes directly to a file results in a valid `RAW/PCM audio file <https://en.wikipedia.org/wiki/Raw_audio_format>`__.
        """
        assert convert_rate is None or convert_rate > 0, "Sample rate to convert to must be a positive integer"
        assert convert_width is None or (convert_width % 1 == 0 and 1 <= convert_width <= 4), "Sample width to convert to must be between 1 and 4 inclusive"

        raw_data = self.frame_data

        # make sure unsigned 8-bit audio (which uses unsigned samples) is handled like higher sample width audio (which uses signed samples)
        if self.sample_width == 1:
            raw_data = audioop.bias(raw_data, 1, -128) # subtract 128 from every sample to make them act like signed samples

        # resample audio at the desired rate if specified
        if convert_rate is not None and self.sample_rate != convert_rate:
            raw_data, _ = audioop.ratecv(raw_data, self.sample_width, 1, self.sample_rate, convert_rate, None)

        # convert samples to desired sample width if specified
        if convert_width is not None and self.sample_width != convert_width:
            if convert_width == 3: # we're converting the audio into 24-bit (workaround for https://bugs.python.org/issue12866)
                raw_data = audioop.lin2lin(raw_data, self.sample_width, 4) # convert audio into 32-bit first, which is always supported
                try: audioop.bias(b"", 3, 0) # test whether 24-bit audio is supported (for example, ``audioop`` in Python 3.3 and below don't support sample width 3, while Python 3.4+ do)
                except audioop.error: # this version of audioop doesn't support 24-bit audio (probably Python 3.3 or less)
                    raw_data = b"".join(raw_data[i + 1:i + 4] for i in range(0, len(raw_data), 4)) # since we're in little endian, we discard the first byte from each 32-bit sample to get a 24-bit sample
                else: # 24-bit audio fully supported, we don't need to shim anything
                    raw_data = audioop.lin2lin(raw_data, self.sample_width, convert_width)
            else:
                raw_data = audioop.lin2lin(raw_data, self.sample_width, convert_width)

        # if the output is 8-bit audio with unsigned samples, convert the samples we've been treating as signed to unsigned again
        if convert_width == 1:
            raw_data = audioop.bias(raw_data, 1, 128) # add 128 to every sample to make them act like unsigned samples again

        return raw_data

    def get_wav_data(self, convert_rate = None, convert_width = None):
        """
        Returns a byte string representing the contents of a WAV file containing the audio represented by the ``AudioData`` instance.

        If ``convert_width`` is specified and the audio samples are not ``convert_width`` bytes each, the resulting audio is converted to match.

        If ``convert_rate`` is specified and the audio sample rate is not ``convert_rate`` Hz, the resulting audio is resampled to match.

        Writing these bytes directly to a file results in a valid `WAV file <https://en.wikipedia.org/wiki/WAV>`__.
        """
        raw_data = self.get_raw_data(convert_rate, convert_width)
        sample_rate = self.sample_rate if convert_rate is None else convert_rate
        sample_width = self.sample_width if convert_width is None else convert_width

        # generate the WAV file contents
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            try: # note that we can't use context manager, since that was only added in Python 3.4
                wav_writer.setframerate(sample_rate)
                wav_writer.setsampwidth(sample_width)
                wav_writer.setnchannels(1)
                wav_writer.writeframes(raw_data)
                wav_data = wav_file.getvalue()
            finally:  # make sure resources are cleaned up
                wav_writer.close()
        return wav_data

    def get_aiff_data(self, convert_rate = None, convert_width = None):
        """
        Returns a byte string representing the contents of an AIFF-C file containing the audio represented by the ``AudioData`` instance.

        If ``convert_width`` is specified and the audio samples are not ``convert_width`` bytes each, the resulting audio is converted to match.

        If ``convert_rate`` is specified and the audio sample rate is not ``convert_rate`` Hz, the resulting audio is resampled to match.

        Writing these bytes directly to a file results in a valid `AIFF-C file <https://en.wikipedia.org/wiki/Audio_Interchange_File_Format>`__.
        """
        raw_data = self.get_raw_data(convert_rate, convert_width)
        sample_rate = self.sample_rate if convert_rate is None else convert_rate
        sample_width = self.sample_width if convert_width is None else convert_width

        # the AIFF format is big-endian, so we need to covnert the little-endian raw data to big-endian
        if hasattr(audioop, "byteswap"): # ``audioop.byteswap`` was only added in Python 3.4
            raw_data = audioop.byteswap(raw_data, sample_width)
        else: # manually reverse the bytes of each sample, which is slower but works well enough as a fallback
            raw_data = raw_data[sample_width - 1::-1] + b"".join(raw_data[i + sample_width:i:-1] for i in range(sample_width - 1, len(raw_data), sample_width))

        # generate the AIFF-C file contents
        with io.BytesIO() as aiff_file:
            aiff_writer = aifc.open(aiff_file, "wb")
            try: # note that we can't use context manager, since that was only added in Python 3.4
                aiff_writer.setframerate(sample_rate)
                aiff_writer.setsampwidth(sample_width)
                aiff_writer.setnchannels(1)
                aiff_writer.writeframes(raw_data)
                aiff_data = aiff_file.getvalue()
            finally:  # make sure resources are cleaned up
                aiff_writer.close()
        return aiff_data

    def get_flac_data(self, convert_rate = None, convert_width = None):
        """
        Returns a byte string representing the contents of a FLAC file containing the audio represented by the ``AudioData`` instance.

        Note that 32-bit FLAC is not supported. If the audio data is 32-bit and ``convert_width`` is not specified, then the resulting FLAC will be a 24-bit FLAC.

        If ``convert_rate`` is specified and the audio sample rate is not ``convert_rate`` Hz, the resulting audio is resampled to match.

        If ``convert_width`` is specified and the audio samples are not ``convert_width`` bytes each, the resulting audio is converted to match.

        Writing these bytes directly to a file results in a valid `FLAC file <https://en.wikipedia.org/wiki/FLAC>`__.
        """
        assert convert_width is None or (convert_width % 1 == 0 and 1 <= convert_width <= 3), "Sample width to convert to must be between 1 and 3 inclusive"

        if self.sample_width > 3 and convert_width is None: # resulting WAV data would be 32-bit, which is not convertable to FLAC using our encoder
            convert_width = 3 # the largest supported sample width is 24-bit, so we'll limit the sample width to that

        # run the FLAC converter with the WAV data to get the FLAC data
        wav_data = self.get_wav_data(convert_rate, convert_width)
        flac_converter = get_flac_converter()
        process = subprocess.Popen([
            flac_converter,
            "--stdout", "--totally-silent", # put the resulting FLAC file in stdout, and make sure it's not mixed with any program output
            "--best", # highest level of compression available
            "-", # the input FLAC file contents will be given in stdin
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        flac_data, stderr = process.communicate(wav_data)
        return flac_data

class Recognizer(AudioSource):
    def __init__(self, pserve, logger):
        """
        Creates a new ``Recognizer`` instance, which represents a collection of speech recognition functionality.
        """
        self.energy_threshold = 300 # minimum audio energy to consider for recording
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8 # seconds of non-speaking audio before a phrase is considered complete
        self.phrase_threshold = 0.3 # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        self.non_speaking_duration = 0.5 # seconds of non-speaking audio to keep on both sides of the recording
        self.audio_gain = 10

        self.pserve = pserve
        self._log = logger

        self._running_voice = False
        self._running_stream = False

    def google_grpc_channel(self, host, port):
        """Creates an SSL channel with auth credentials from the environment."""
        # In order to make an https call, use an ssl channel with defaults
        ssl_channel = implementations.ssl_channel_credentials(None, None, None)

        # Grab application default credentials from the environment
        creds = GoogleCredentials.from_stream(os.path.join(app_dir,"audio_creds.json")).create_scoped([SPEECH_SCOPE])

        # Add a plugin to inject the creds into the header
        auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token)
        auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds')

        # compose the two together for both ssl and google auth
        composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)

        return implementations.secure_channel(host, port, composite_channel)


    def adjust_for_ambient_noise(self, source, duration = 1):
        """
        Adjusts the energy threshold dynamically using audio from ``source`` (an ``AudioSource`` instance) to account for ambient noise.

        Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.

        The ``duration`` parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.
        """
        assert isinstance(source, AudioSource), "Source must be an audio source"
        assert source.stream is not None, "Audio source must be entered before adjusting, see documentation for `AudioSource`; are you using `source` outside of a `with` statement?"
        assert self.pause_threshold >= self.non_speaking_duration >= 0

        seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
        elapsed_time = 0

        # adjust energy threshold until a phrase starts
        while True:
            elapsed_time += seconds_per_buffer
            if elapsed_time > duration: break
            buffer = source.stream.read(source.CHUNK)

            # Amplify volume
            # buffer = numpy.fromstring(buffer, numpy.int16) * self.audio_gain # half amplitude
            # buffer = struct.pack('h'*len(buffer), *buffer)
            buffer = self.amplify(buffer, self.audio_gain)

            energy = audioop.rms(buffer, source.SAMPLE_WIDTH) # energy of the audio signal

            # dynamically adjust the energy threshold using assymmetric weighted average
            damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
            target_energy = energy * self.dynamic_energy_ratio
            self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

    def amplify(self, buff, gain):
        amp_b = numpy.fromstring(buff, numpy.int16) * gain # half amplitude
        amp_b = struct.pack('h'*len(amp_b), *amp_b)
        return amp_b

    def listen_trigger(self, source, timeout):
        assert isinstance(source, AudioSource), "Source must be an audio source"
        assert source.stream is not None, "Audio source must be entered before listening, see documentation for `AudioSource`; are you using `source` outside of a `with` statement?"
        assert self.pause_threshold >= self.non_speaking_duration >= 0

        seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
        pause_buffer_count = int(math.ceil(self.pause_threshold / seconds_per_buffer)) # number of buffers of non-speaking audio before the phrase is complete
        phrase_buffer_count = int(math.ceil(self.phrase_threshold / seconds_per_buffer)) # minimum number of buffers of speaking audio before we consider the speaking audio a phrase
        non_speaking_buffer_count = int(math.ceil(self.non_speaking_duration / seconds_per_buffer)) # maximum number of buffers of non-speaking audio to retain before and after

        # read audio input for phrases until there is a phrase that is long enough
        elapsed_time = 0 # number of seconds of audio read

        frames = collections.deque()

        self._log.info("Energy threshold %d", (self.energy_threshold))

        # store audio input until the phrase starts
        while True:
            elapsed_time += seconds_per_buffer
            if timeout and elapsed_time > timeout: # handle timeout if specified
                raise WaitTimeoutError("listening timed out")

            buffer = source.stream.read(source.CHUNK)

            # Amplify volume
            buffer = self.amplify(buffer, self.audio_gain)

            if len(buffer) == 0: break # reached end of the stream
            frames.append(buffer)

            if len(frames) > non_speaking_buffer_count: # ensure we only keep the needed amount of non-speaking buffers
                frames.popleft()

            # detect whether speaking has started on audio input
            energy = audioop.rms(buffer, source.SAMPLE_WIDTH) # energy of the audio signal
            if energy > self.energy_threshold: break

            # dynamically adjust the energy threshold using assymmetric weighted average
            if self.dynamic_energy_threshold:
                damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
                target_energy = energy * self.dynamic_energy_ratio
                self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)

        frame_data = b"".join(list(frames))
        return frame_data


    def listen(self, source, buff, timeout = None):
        """
        Records a single phrase from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.

        This is done by waiting until the audio has an energy above ``recognizer_instance.energy_threshold`` (the user has started speaking), and then recording until it encounters ``recognizer_instance.pause_threshold`` seconds of non-speaking or there is no more audio input. The ending silence is not included.

        The ``timeout`` parameter is the maximum number of seconds that it will wait for a phrase to start before giving up and throwing an ``speech_recognition.WaitTimeoutError`` exception. If ``timeout`` is ``None``, it will wait indefinitely.
        """

        self._log.debug("Microphone capturing thread started")

        # Tab left for entire function -->
        while self._running_stream:
            # elapsed_time += seconds_per_buffer
            # if timeout and elapsed_time > 5: # handle timeout if specified
            #     break;

            buffer = source.stream.read(source.CHUNK)

            # Amplify volume
            buffer = self.amplify(buffer, self.audio_gain)

            if len(buffer) == 0: # reached end of the stream
                buff.put(None)
                break

            buff.put(buffer)

        self._log.debug("Microphone capturing thread stopped")


    @contextlib.contextmanager
    def listen_thread(self, source):
        assert isinstance(source, AudioSource), "Source must be an audio source"
        # running = [True]

        buff = queue.Queue()

        # source.__enter__()

        mic_thread = threading.Thread(
            target=self.listen,
            args=(source, buff))
        mic_thread.start()

        yield self.g_audio_data_generator(buff)

        # source.__exit__()
        mic_thread.join()


    def listen_in_background(self, source, callback):
        assert isinstance(source, AudioSource), "Source must be an audio source"

        # running = [True]

        def threaded_listen():
            with cloud_speech.beta_create_Speech_stub(self.google_grpc_channel('speech.googleapis.com', 443)) as service:
                with source as s:
                    while self._running_voice:
                        try: # listen for 1 second, then check again if the stop function has been called
                            init_buff = self.listen_trigger(s, 1)
                        except WaitTimeoutError: # listening timed out, just try again
                            pass
                        else:
                            self.g_stream_loop(service, source, init_buff, callback)
        def stopper():
            self._running_voice = False
            listener_thread.join() # block until the background thread is done, which can be up to 1 second

        self._running_voice = True
        listener_thread = threading.Thread(target=threaded_listen)
        # listener_thread.daemon = True
        listener_thread.start()

        return stopper

    def g_stream_loop(self, service, source, init_buff, callback):

            self._running_stream = True
            with self.listen_thread(source) as buffered_audio_data:

                requests = self.g_request_steam(buffered_audio_data, source.SAMPLE_RATE, init_buff)
                recon_stream = service.StreamingRecognize(requests, 60 * 3 + 5)

                try:
                    self.g_print_loop(recon_stream, callback)
                    recon_stream.cancel()
                except:
                    self._log.exception("Printer error")

                self._log.debug("Exited stream")

            self._log.debug("Exited everything")


    def g_audio_data_generator(self,buff):
        while True:
            chunk = buff.get()
            if not chunk:
                self._log.debug("No Data in buffer")
                continue

            data = [chunk]

            while True:
                try:
                    data.append(buff.get(block=False))
                except queue.Empty:
                    break
            yield b''.join(data)

    def g_request_steam(self, data_stream, rate, init_buff=None):

        r_config = cloud_speech.RecognitionConfig(
            encoding='LINEAR16',
            sample_rate=rate,
            language_code='en-US',
            speech_context= cloud_speech.SpeechContext(
                phrases=["mirror", "add", "item", "help", "close", "clothes", "tag", "tags", "find", "number 1", "wear", "start", "stop", "stylist", "wardrobe", "exit", "1", "2", "3", "4", "5", "6", "7", "8"]
            )
        )
        r_stream_config = cloud_speech.StreamingRecognitionConfig(
            config=r_config,
            single_utterance=False,
            interim_results=False)

        yield cloud_speech.StreamingRecognizeRequest(
            streaming_config=r_stream_config)

        if init_buff:
            yield cloud_speech.StreamingRecognizeRequest(audio_content=init_buff)

        for data in data_stream:
            yield cloud_speech.StreamingRecognizeRequest(audio_content=data)

    def g_print_loop(self, recognize_stream, callback):
        # self._log.info("Streaming")
        for resp in recognize_stream:
            self._log.info(resp)

            if resp.error.code != code_pb2.OK:
                self._running_stream = False
                self._log.exception("Recognition Error")
                break

                # recon_stream = service.StreamingRecognize(requests, 60 * 3 + 5)

            if resp.endpointer_type == 1:
                self._log.debug("Speech Started\n")
                self.pserve.send("audio_found","")
            elif resp.endpointer_type == 2:
                self._log.debug("Speech Ended\n")
                self.pserve.send("audio_uploading","")
            elif resp.endpointer_type == 3:
                self._log.debug("Audio Ended. Restarting stream\n")
                # recon_stream = service.StreamingRecognize(requests, 60 * 3 + 5)

            for result in resp.results:
                for alt in result.alternatives:
                    # self._log.info(alt.transcript)
                    callback(alt.transcript)


def get_flac_converter():
    # determine which converter executable to use
    system = platform.system()
    path = os.path.dirname(os.path.abspath(__file__)) # directory of the current module file, where all the FLAC bundled binaries are stored
    flac_converter = shutil_which("flac") # check for installed version first
    if flac_converter is None: # flac utility is not installed
        compatible_machine_types = ["i686", "i786", "x86", "x86_64", "AMD64"] # whitelist of machine types our bundled binaries are compatible with
        if system == "Windows" and platform.machine() in compatible_machine_types:
            flac_converter = os.path.join(path, "flac-win32.exe")
        elif system == "Linux" and platform.machine() in compatible_machine_types:
            flac_converter = os.path.join(path, "flac-linux-x86")
        elif system == "Darwin" and platform.machine() in compatible_machine_types:
            flac_converter = os.path.join(path, "flac-mac")
        else:
            raise OSError("FLAC conversion utility not available - consider installing the FLAC command line application using `brew install flac` or your operating system's equivalent")

    # mark FLAC converter as executable if possible
    try:
        stat_info = os.stat(flac_converter)
        os.chmod(flac_converter, stat_info.st_mode | stat.S_IEXEC)
    except OSError: pass

    return flac_converter

def shutil_which(pgm):
    """Python 2 backport of ``shutil.which()`` from Python 3"""
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
