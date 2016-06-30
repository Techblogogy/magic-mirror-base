# Commands model
# [keywords], (and/or), exp
class v_cmd:
    def __init__(self, kw, logic, cmd, exception=""):
        self.keys = kw;
        self.lg = logic;
        self.cmd = cmd;
        self.exp = exception;
