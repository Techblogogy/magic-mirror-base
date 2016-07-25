import nltk

from server_public import socketio
from server_public import IO_SPACE
from flask_socketio import emit

from v_cmd import v_cmd
from commands import in_cmd

nltk.download()

# Key base
key_w = "mirror"

# Input Cmd
# command = "how do i look today"

# Number Units
n_units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
n_tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
n_scales = ["hundred", "thousand", "million", "billion", "trillion"]

def get_numbers():
    pass

# Return command based on voice input
def get_command(cm):
    # print IO_SPACE
    # socketio.emit('right', "", namespace=IO_SPACE)
    tokens = nltk.word_tokenize(cm)

    print tokens

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
        elif c.lg == "OR":
            br = False;
            for k in c.keys:
                if k in tokens:
                    br = True

        # Output command
        if br:
            socketio.emit(c.cmd, "", namespace=IO_SPACE)
            print c.cmd;
            break;


# get_command("i pick number twenty two please")
