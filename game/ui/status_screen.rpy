screen status_panel():
    modal True
    zorder 200

    add Solid("#11111cdd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 820
        background Solid("#29243aee")
        padding (64, 54)

        vbox:
            spacing 18

            if story_arc == "sequel":
                text "樱镜町的四季" size 52 color "#f4cfe8" xalign 0.5
                null height 4
                text "章节进度：[sequel_chapter_progress]"

                if sequel_route:
                    text "当前路线：[sequel_route]"
                else:
                    text "当前路线：共通线"

                if sequel_origin_ending == "stable":
                    text "事业回顾：稳定结局"
                elif sequel_origin_ending == "rising":
                    text "事业回顾：上升结局"
                elif sequel_origin_ending == "startup":
                    text "事业回顾：创业结局"
                else:
                    text "事业回顾：未带入"

                text "Ruby 信任：[ruby_affection]"
                text "Dana 信任：[dana_affection]"
                text "Luna 信任：[luna_affection]"
                text "Irene 信任：[irene_affection]"
                text "洞察：[sequel_insight]    共同意志：[sequel_resolve]"
                text "四季碎片：[fragment_count()] / 4"

                if sequel_truth_ready():
                    text "真相条件：已满足" color "#bdecc8"
                else:
                    text "真相条件：尚未满足" color "#e8c7a1"
            else:
                text "王不稳的三个月" size 52 color "#f4cfe8" xalign 0.5
                null height 8
                text "章节进度：[chapter_progress] / 6"
                text "许晚晴好感度：[affection]（[affection_level()]）"
                text "能力值：[ability]"
                text "可用金钱：[money] 元"

            textbutton "返回":
                xalign 0.5
                action Hide("status_panel")
