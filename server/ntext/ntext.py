import nltk
item_number = 0

# import thread
# from thead import send_left

from v_cmd import v_cmd
from commands import in_cmd

# nltk.download()

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
num_dict = {}
i = 0
for i in range(len(n_units)):
    num_dict[n_units[i]] = i


n_tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
n_scales = ["hundred", "thousand", "million", "billion", "trillion"]

def get_numbers():
    pass

# Return command based on voice input
def get_command(cm):
    tokens = nltk.word_tokenize(cm)

    # print tokens
    # print pserve.test

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
        # Token compare for NUM
        elif c.lg == "NUM":
            br = False;
            for k in tokens:
                if k in num_dict:
                    global item_number
                    item_number = num_dict[k]
                    br = True

        # Output command
        if br:

            # try:
            #     thread.start_new_thread( send_left, (0,) )
            # except:
            #     print "Error: unable to start thread"

            # pserve.send()

            # pserve.socketio.emit("c2", "", namespace=pserve.IO_SPACE)
            # pserve.socketio.emit(c.cmd, "", namespace=pserve.IO_SPACE)
            print c.cmd
            return (c.cmd, item_number)
            break


get_command(" lucky silly ten ducks LSD")
print item_number
