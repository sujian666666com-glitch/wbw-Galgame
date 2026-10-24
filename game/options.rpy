define config.name = _("旺不稳的奇妙冒险")
define config.version = "2.0.0"
define build.name = "three_months_to_stay"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = dissolve
define config.end_game_transition = fade

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

default preferences.text_cps = 35
default preferences.auto_forward_time = 10

define config.save_directory = "three-months-to-stay-1"

init python:
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("game/**.rpy", "archive")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.webp", "archive")
