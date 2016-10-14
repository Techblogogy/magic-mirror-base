from v_cmd import v_cmd

# Possible comands list
in_cmd = [

    # --- Close commands
    v_cmd(["close", "exit", "quit"], "OR", "exit_context"), # To replace close_item, list_vcmd_close, tutorial_close


    # --- Opens Wardrobe Page
    v_cmd(["I", "dress"], "AND", "wardrobe_page"), # Stylist intro
    v_cmd(["stylist", "styles", "wardrobe"], "OR", "wardrobe_page"),

    # --- Wardrobe Page Controls
    v_cmd([], "NUM", "fullscreen"),

    v_cmd(["next", "more"], "OR", "next_page"),
    v_cmd(["previous", "less", "back"], "OR", "previous_page"),

    v_cmd(["wear"], "AND", "item_worn"),

    v_cmd(["find"], "TAG", "search"),

    v_cmd(["add","new"], "AND", "add_page"),

    v_cmd(["show", "all"], "AND", "show_all"),

    # v_cmd(["close", "item"], "AND", "close_item"),


    # --- Adding Page Commands
    v_cmd(["tag", "tags"], "TAG", "add_tags"),
    v_cmd(["save","confirm"], "OR", "save_tags"),
    v_cmd(["finish","quit"], "OR", "finish_tags"),

    v_cmd(["start","begin"], "OR", "start_cmd"),
    v_cmd(["stop","begin"], "OR", "stop_cmd"),

    v_cmd(["edit","dresscode","code"], "TAG", "edit_dresscode"),
    v_cmd(["save","code"], "AND", "save_dc"),


    # --- Opens Home Page
    v_cmd(["home"], "AND", "home_page"),


    # -- Home Page
    v_cmd(["what","about","weather"], "AND", "weather_warning"),

    v_cmd(["more", "plans"], "AND", "next_plans_page"),
    v_cmd(["current", "plans"], "AND", "prev_plans_page"),


    # --- General help
    v_cmd(["help"], "OR", "list_vcmd")

    # v_cmd(["list", "close"], "AND", "list_vcmd_close"),
    # v_cmd(["guide", "close"], "AND", "tutorial_close"),


]
