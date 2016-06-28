import nltk

#command = "mirror how do I look";
command = "mirror what should i dress today";

# Possible responce listening
out_cmd = [
    "I don't understand you",
    ""
]

# Possible comands list
in_cmd = [
    ["do", "i", "need", "an", "umbrella", "today"],
    ["how", "do", "i", "look"],
    ["how", "should", "i", "dress", "today"],
    ["does", "she", "love", "me"]
]

def get_command():
    tokens = nltk.word_tokenize(command)
    tags = nltk.pos_tag(tokens)

    print tokens
    print tags

    if "mirror" in tokens:
        print "yes"

get_command()
