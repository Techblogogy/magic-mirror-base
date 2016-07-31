from v_cmd import v_cmd

# Possible comands list
in_cmd = [
    v_cmd(["look", "today"], "AND", "cmp"), # Compliments
    v_cmd(["dress", "today"], "AND", "wardrobe_page"), # Stylist intro

    # v_cmd(["calendar", "plans"], "OR", "c3"), # Calendar keywords
    # v_cmd(["weather", "jacket", "umbrella"], "OR", "c4"), # Weather keywords

    v_cmd(["next", "page"], "AND", "next_page"),
    v_cmd(["previous", "page"], "AND", "previous_page"),

    v_cmd(["go","right"], "AND", "right"),
    v_cmd(["go","left"], "AND", "left"),

    v_cmd([], "NUM", "fullscreen"), # Number detection item

    v_cmd(["close", "image"], "AND", "close_item"),

    v_cmd(["tag", "tags"], "TAG", "add_tags"),

    v_cmd(["search"], "TAG", "search"),
    v_cmd(["find"], "TAG", "search"),

    v_cmd(["show", "stylist"], "AND", "wardrobe_page"),
    v_cmd(["show", "home"], "AND", "home_page"),
    v_cmd(["want", "wear", "today"], "AND", "item_worn"),

]
