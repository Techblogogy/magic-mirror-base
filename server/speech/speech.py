import slib as sr
from flask_socketio import emit

from ntext.ntext import get_command


import thread, platform, os



class Speech:

    def __init__(self, pserve, config, logger, appdir):
        self.pserve = pserve
        self._cfg = config
        self._log = logger
        self._appdir = appdir

        self._log.info("Initializing Speech Libraries")

        # Initialalize snowboy
        self.snowboy = self.import_snowboy()

        self.snowboy_trigger = self._cfg.getboolean("SPEECH", "snowboy_trigger")
        self.api_key = self._cfg.get("API KEYS", "bing_speech")

        self.s_sensitivity = self._cfg.getint("SPEECH", "snowboy_sensitivity")
        self.s_gain = self._cfg.getint("SPEECH", "snowboy_gain")

        self.adj_time = self._cfg.getint("SPEECH", "adjust_time")

        self._r = sr.Recognizer(self.pserve, self._log)
        # self._r.auth_google()
        # self._r.auth_google_grpc()
        self._r.dynamic_energy_threshold = self._cfg.getboolean("SPEECH", "dynamic_threshold") #False
        self._r.audio_gain = self._cfg.getint("SPEECH", "audio_gain")

        # Check if running
        self.running = True
        self.detected = False

        # Create microphone instance and ajust for noise
        self._log.info("Ajusting for ambient noise")

        self._m = sr.Microphone(
            device_index=self._cfg.getint("SPEECH", "device_index"),
            sample_rate=self._cfg.getint("SPEECH", "sample_rate")
        )

    	# print self._m.list_microphone_names()
        self.noise_adjust()

    def import_snowboy(self):
        try:
            import snowboydecoder
            return snowboydecoder
        except:
            self._log.exception("Snowboy Not Found :(")

        return None

    # Starts audio library
    def start(self):
        if self.snowboy_trigger:
            self._log.info("Starting snowboy")

            # Ajust for ambient noise
            self.running = True

            # Start snowboy thread
            self.dec = self.snowboy.HotwordDetector(
                os.path.join(self._appdir, "voice", "snowboy.umdl"),
                resource=os.path.join(self._appdir, "voice", "common.res"),
                sensitivity=self.s_sensitivity,
                audio_gain=self.s_gain

            )
            thread.start_new_thread( self.start_snowboy, () )

        else:
            self.stop_bing = self._r.listen_in_background(self._m,self.detect_bing)

    # Stops audio libarary
    def stop(self):
        self.running = False

    # Stops globally
    def stop_all(self):
        if not self.snowboy_trigger:
            self.stop_bing()
            self.snowboy_trigger = True
            self.start()


    # Starts snowboy voice thread
    def start_snowboy(self):

        self.dec.start(detected_callback=self.detected_snowboy,
                       interrupt_check=self.check_interrupt,
                       sleep_time=0.03)
        self.dec.terminate()

        self._log.info("Stopping snowboy")

        self._log.info("Starting Bing")

        if self.detected:
            self.bing_snowboy()

    # Check for interrupt
    def check_interrupt(self):
        return not self.running

    # Ajust for ambient noise
    def noise_adjust(self):
        with self._m as source:
            self._r.adjust_for_ambient_noise(source, duration=self.adj_time)

        if self._r.energy_threshold <= 300:
            self._r.energy_threshold = 300

    # Voice detection
    def detected_snowboy(self):
        self._log.info("SNOWBOY DETECTED")

        self.detected = True
        if self.pserve.is_sleeping:
            self.pserve.is_sleeping = False
            self.pserve.send("wake_up")
            try:
                thread.start_new_thread( self.pserve.sleep_state, (self,) )
                # self.pserve.sleep_state(voice)
            except:
                self._log.exception("Unable to start video thread")

        self.snowboy.play_audio_file( os.path.join(self._appdir, "voice", "dong.wav") )
        self.stop()

    def bing_snowboy(self):
        self.detected = False

        # Listen for phrase
        with self._m as source:
            audio = self._r.listen(source)

        # Send audio to bing
        self.detect_bing(self._r, audio)

        # Start snowboy in a thread
        self.start()

    def detect_bing(self,recon,audio):
        try:
            self.pserve.send("audio_uploading","")

            text = recon.recognize_google(audio)
            cmd = get_command(text)

            if cmd:
                self._log.debug("Item Number: %d", cmd[1])

                if cmd[0] == "add_tags" or cmd[0] == "edit_dresscode":
                    self.pserve.send(cmd[0], cmd[2])
                elif cmd[0] == "search":
                    self.pserve.send(cmd[0], cmd[2])
                else:
                    self.pserve.send(cmd[0], cmd[1])

                self.pserve.send("audio_detected",cmd[0])

                # Play Audio Ding
                try:
                    self.snowboy.play_audio_file( os.path.join(self._appdir, "voice", "ding.wav") )
                except:
                    self._log.exception("Snowboy error")

            else:
                self.pserve.send("audio_error", "unknown_command")

            self._log.debug("Speech: %s", text)

        except sr.UnknownValueError:
            self._log.info("Speech unrecognizable")
            self.pserve.send("audio_error", "unrecognizable")
        except sr.RequestError as e:
            self._log.error("Speech error; {0}".format(e))
            self.pserve.send("audio_error", "bing_error")
        except:
            self._log.exception("Speech unknown error")
            self.pserve.send("audio_error", "unknown")
