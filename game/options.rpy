define config.name = _("旺不稳的奇妙冒险")
define config.version = "2.1.0"
define build.name = "three_months_to_stay"

define config.has_sound = False
define config.has_music = False
define config.has_voice = False

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.after_load_transition = dissolve
define config.end_game_transition = fade

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

define config.history_length = 250

default preferences.text_cps = 35
default preferences.auto_forward_time = 10

define config.save_directory = "three-months-to-stay-1"

init python:
    # 第一次命中生效，排除写在归档之前。
    # 规则只扫项目目录。引擎由 SDK 的 renpy_patterns 另包，
    # 不调用 classify_renpy，也不把 renpy/ 或 lib/ 排除。
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)

    build.classify("doc/**", None)
    build.classify("image/**", None)
    build.classify("ik.md", None)
    build.classify("**/ik.md", None)
    build.classify("tools/**", None)
    build.classify("game/testcases.rpy", None)
    build.classify("game/testcases.rpyc", None)
    build.classify("game/testcases.rpymc", None)

    build.classify("game/cache/**", None)
    build.classify("**/__pycache__/**", None)
    build.classify("**.pyc", None)
    build.classify("game/saves/**", None)
    build.classify("**/saves/**", None)
    build.classify("**.save", None)
    build.classify("**.log", None)
    build.classify("log/**", None)
    build.classify("**/log.txt", None)
    build.classify("**/errors.txt", None)
    build.classify("**/traceback.txt", None)
    build.classify(".work/**", None)
    build.classify("**/.work/**", None)
    build.classify("**/renpy-sdk/**", None)
    build.classify("**/renpy-*-sdk/**", None)

    build.classify("THIRD_PARTY_NOTICES.txt", "all")
    build.classify("licenses/**", "all")

    build.classify("game/fonts/**", "archive")
    build.classify("game/**.ttf", "archive")
    build.classify("game/**.otf", "archive")
    build.classify("game/**.rpy", "archive")
    build.classify("game/**.rpyc", "archive")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.jpeg", "archive")
    build.classify("game/**.webp", "archive")
