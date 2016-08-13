from v_cmd import v_cmd

# Possible comands list
in_cmd = [
    v_cmd(["look", "today"], "AND", "cmp"), # Compliments
    v_cmd(["dress", "today"], "AND", "wardrobe_page"), # Stylist intro

    v_cmd(["what","about","weather"], "AND", "weather_warning"),
    # v_cmd(["calendar", "plans"], "OR", "c3"), # Calendar keywords
    # v_cmd(["weather", "jacket", "umbrella"], "OR", "c4"), # Weather keywords
    v_cmd(["next", "page"], "AND", "next_page"),
    v_cmd(["previous", "page"], "AND", "previous_page"),
    v_cmd(["go","right"], "AND", "right"),
    v_cmd(["go","left"], "AND", "left"),
    v_cmd([], "NUM", "fullscreen"),
    v_cmd(["close", "item"], "AND", "close_item"),
    v_cmd(["show", "stylist"], "AND", "wardrobe_page"),
    v_cmd(["show", "home"], "AND", "home_page"),
    v_cmd(["want", "wear", "today"], "AND", "item_worn"),
    v_cmd(["find"], "TAG", "search"),
    v_cmd(["show", "all"], "AND", "show_all"),

    v_cmd(["add","new"], "AND", "add_page"),

    v_cmd(["tag", "tags"], "TAG", "add_tags"),
    v_cmd(["save","confirm"], "OR", "save_tags"),
    v_cmd(["finish","quit"], "OR", "finish_tags"),
    v_cmd(["start","begin"], "OR", "start_cmd"),

    v_cmd(["edit","dresscode","code"], "TAG", "edit_dresscode"),
    v_cmd(["save","code"], "AND", "save_dc"),

    v_cmd(["help"], "OR", "list_vcmd"),
    v_cmd(["list", "close"], "AND", "list_vcmd_close"),

    v_cmd(["guide", "close"], "AND", "tutorial_close"),

]
