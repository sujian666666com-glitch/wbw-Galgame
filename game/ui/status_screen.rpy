screen status_panel():
    modal True
    zorder 200

    add Solid("#11111cdd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 780
        ysize 610
        background Solid("#29243aee")
        padding (64, 54)

        vbox:
            spacing 30
            text "王不稳的三个月" size 52 color "#f4cfe8" xalign 0.5
            null height 8
            text "章节进度：[chapter_progress] / 6"
            text "许晚晴好感度：[affection]（[affection_level()]）"
            text "能力值：[ability]"
            text "可用金钱：[money] 元"
            textbutton "返回":
                xalign 0.5
                action Hide("status_panel")
