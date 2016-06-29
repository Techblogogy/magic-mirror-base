import nltk

from server import socketio
from server import IO_SPACE

from flask_socketio import emit
from v_cmd import v_cmd
from commands import in_cmd

# Key base
key_w = "mirror"

# Input Cmd
command = "how do i look today"

# Possible responce listening
# out_cmd = [
#     "I don't understand you",
#     ""
# ]

def get_command(cm):
    tokens = nltk.word_tokenize(cm)

    # Iriterate over all commands
    for c in in_cmd:
        # Initrate Keys
        br = True;

        # Token compare for AND
        if c.lg == "AND":
            for k in c.keys:
                if k in tokens:
                    pass
                else:
                    br = False
        # Token compare for OR
        elif v_cmd.logic == "OR":
            br = False;
            for k in c.keys:
                if k in tokens:
                    br = True;

        # Output command
        if br:
            socketio.emit(c.cmd, "", namespace=IO_SPACE)
            print c.cmd;
            break;


get_command(command)
