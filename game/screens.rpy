style default:
    properties gui.text_properties()
    language "unicode"

default quick_menu = True

style button:
    background Solid("#332b4dcc")
    hover_background Solid("#6e5688dd")
    padding (28, 16)

style button_text:
    properties gui.button_text_properties("button")
    xalign 0.5

style bar:
    xsize 900
    ysize 24
    left_bar Solid(gui.accent_color)
    right_bar Solid("#555064")

screen say(who, what):
    window:
        id "window"
        background Solid("#151522dd")
        xalign 0.5
        yalign 1.0
        xsize 1680
        ysize 270
        padding (70, 48)

        if who is not None:
            text who:
                id "who"
                xpos 0
                ypos -10
                size gui.name_text_size
                color gui.accent_color

        text what:
            id "what"
            xpos 0
            ypos 58
            xsize 1520
            size gui.text_size

    use quick_menu

screen choice(items):
    style_prefix "choice"
    vbox:
        xalign 0.5
        ypos 800
        yanchor 1.0
        spacing 12
        for i in items:
            textbutton i.caption action i.action

style choice_button is button:
    xsize gui.choice_button_width
    background Solid("#28223ddd")
    hover_background Solid("#705a8ddd")

style choice_button_text is button_text:
    size gui.choice_button_text_size

screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            xalign 0.5
            yalign 0.985
            spacing 12
            textbutton "回退" action Rollback()
            textbutton "历史" action ShowMenu("history")
            textbutton "快进" action Skip() alternate Skip(fast=True, confirm=True)
            textbutton "自动" action Preference("auto-forward", "toggle")
            textbutton "保存" action ShowMenu("save")
            textbutton "读档" action ShowMenu("load")
            textbutton "状态" action Show("status_panel")
            textbutton "设置" action ShowMenu("preferences")

screen navigation():
    vbox:
        xpos 110
        yalign 0.52
        spacing 22
        if main_menu:
            text "平行世界线：只继承事业回顾，不继承恋爱。" size 24 color "#d5c6df" xsize 420
            textbutton "新篇：樱镜町" action Start("sequel_start")
            textbutton "旧篇：三个月，留下来" action Start("original_story_start")
        else:
            textbutton "返回游戏" action Return()
            textbutton "历史" action ShowMenu("history")
            textbutton "保存游戏" action ShowMenu("save")
        textbutton "读取游戏" action ShowMenu("load")
        textbutton "系统设置" action ShowMenu("preferences")
        if not main_menu:
            textbutton "返回主菜单" action MainMenu()
        textbutton "退出游戏" action Quit(confirm=not main_menu)

screen main_menu():
    tag menu
    add gui.main_menu_background
    add Solid("#11111c55")
    frame:
        background Solid("#171625bb")
        xsize 620
        yfill True
        padding (90, 90)
        vbox:
            spacing 28
            text config.name size 62 color "#ffffff"
            text "旺不稳的奇妙冒险，开始了。" size 30 color "#e6b7da"
            null height 50
            use navigation

screen game_menu(title, scroll=None, yinitial=0.0):
    tag menu
    add gui.game_menu_background
    use navigation
    text title:
        xpos 700
        ypos 70
        size 58
        color gui.accent_color
    frame:
        xpos 650
        ypos 160
        xsize 1160
        ysize 820
        background Solid("#242238dd")
        padding (45, 40)
        clipping True
        transclude

screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("第 {} 页"), auto=_("自动存档"), quick=_("快速存档"))
    use game_menu(title):
        vbox:
            spacing 24
            hbox:
                spacing 16
                textbutton "<" action FilePagePrevious()
                button:
                    xsize 460
                    key_events True
                    action page_name_value.Toggle()
                    input:
                        value page_name_value
                        xsize 420
                textbutton ">" action FilePageNext()
            grid 3 2:
                spacing 20
                for i in range(6):
                    $ slot = i + 1
                    button:
                        xsize 340
                        ysize 250
                        padding (12, 12)
                        action FileAction(slot)
                        vbox:
                            spacing 8
                            add FileScreenshot(slot) xsize 316 ysize 154
                            text FileTime(slot, format=_("%Y-%m-%d %H:%M"), empty=_("空存档")) size 20 xsize 316
                            text FileSaveName(slot) size 18 xsize 316

screen save():
    tag menu
    use file_slots(_("保存游戏"))

screen load():
    tag menu
    use file_slots(_("读取游戏"))

screen preferences():
    tag menu
    use game_menu(_("系统设置"), scroll="viewport"):
        vbox:
            spacing 28
            text "显示模式" size 36 color gui.accent_color
            hbox:
                spacing 18
                textbutton "窗口" action Preference("display", "window")
                textbutton "全屏" action Preference("display", "fullscreen")
            text "文字速度" size 36 color gui.accent_color
            bar value Preference("text speed")
            text "自动播放速度" size 36 color gui.accent_color
            bar value Preference("auto-forward time")

screen history():
    tag menu
    predict False
    use game_menu(_("历史记录"), scroll="viewport"):
        viewport:
            xsize 1060
            ysize 720
            mousewheel True
            draggable True
            scrollbars "vertical"
            yinitial 1.0
            vbox:
                spacing 18
                xfill True
                if not _history_list:
                    text "尚无对白记录。" color gui.idle_small_color
                for h in _history_list:
                    vbox:
                        xfill True
                        spacing 6
                        if h.who:
                            text h.who:
                                color gui.accent_color
                                xsize 1020
                        text h.what:
                            xsize 1020

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#11111cbb")
    frame:
        xalign 0.5
        yalign 0.5
        background Solid("#29243a")
        padding (70, 55)
        vbox:
            spacing 30
            text message xalign 0.5
            hbox:
                xalign 0.5
                spacing 25
                textbutton "确定" action yes_action
                textbutton "取消" action no_action

screen notify(message):
    zorder 300
    frame at notify_appear:
        xalign 0.98
        yalign 0.08
        background Solid("#342a4eee")
        padding (26, 18)
        text message size 26
    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1
    on hide:
        linear .35 alpha 0

screen v21_mirror_caption(message):
    zorder 50
    text message:
        xalign 0.5
        yalign 0.38
        xmaximum 1200
        text_align 0.5
        size 40
        color "#f7f4ff"
        outlines [(2, "#120e1acc", 0, 0)]
