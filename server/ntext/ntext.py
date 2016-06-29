import nltk

class v_cmd:
    def __init__(self, kw, logic, cmd, exception=""):
        self.keys = kw;
        self.lg = logic;
        self.cmd = cmd;
        self.exp = exception;

#command = "mirror how do I look";

# Key base
key_w = "mirror"

# Input Cmd
command = "how should i dress today"

# Possible responce listening
out_cmd = [
    "I don't understand you",
    ""
]

# Commands model
# [keywords], (and/or), exp

# Possible comands list
in_cmd = [
    v_cmd(["look", "today"], "AND", "c1"),
    v_cmd(["dress", "today"], "AND", "c2"),
    v_cmd([""])
]

def get_command():
    tokens = nltk.word_tokenize(command)

    # if "mirror" in tokens:
    for c in in_cmd:
        print c.keys

get_command()
