from v_cmd import v_cmd

# Possible comands list
in_cmd = [
    v_cmd(["look", "today"], "AND", "cmp"), # Compliments
    v_cmd(["dress", "today"], "AND", "c2"), # Stylist intro
    v_cmd(["calendar", "plans"], "OR", "c3"), # Calendar keywords
    v_cmd(["weather", "jacket", "umbrella"], "OR", "c4") # Weather keywords
]
