label chapter_04:
    $ chapter_progress = 4
    $ notify_change("章节进度：第四章")

    scene bg meeting_room with fade

    narrator "月度汇报会上，张浩拿着王不稳做了一周的方案，在所有人面前侃侃而谈。"

    zh "这次活动的数据分析和优化方案是我主导的，效果大家也看到了。"

    narrator "王不稳坐在角落，手指微微收紧，但没有说话。许晚晴在另一边，脸色变了。"

    wl "不错不错，张浩辛苦了。"

    narrator "王不稳看着张浩把自己的成果说成他的功劳，安静地记下了这一刻。"

    scene bg corridor with dissolve

    xw "那个方案明明是你做的。"

    wbw "我知道。"

    xw "你不打算说点什么？"

    menu:
        "不是不说，是时候没到。我已经保留了所有的原始文件和时间记录。":
            $ affection += 5
            $ ability += 2
            $ evidence_ready = True
            $ notify_change("许晚晴好感度 +5")
            $ notify_change("能力 +2")
            $ notify_change("关键证据已保留")

            narrator "许晚晴看着他，眼神变了。"
            xw "……你一直在等？"
            wbw "急什么，让他先拿着。"

        "说了又怎样？主管会信我还是信他？":
            $ affection += 1
            $ ability += 1
            $ notify_change("许晚晴好感度 +1")
            $ notify_change("能力 +1")

            narrator "许晚晴沉默了一下。"
            xw "……也是。"

        "无所谓，方案能跑通就行。":
            $ affection -= 1
            $ notify_change("许晚晴好感度 -1")

            xw "……你不在意自己的东西被拿走吗？"

    call v21_chapter_04

    scene bg bedroom_night with dissolve

    narrator "深夜，电脑屏幕的光照着王不稳的脸。"
    narrator "王不稳打开文件夹，里面是完整的工作记录：每一次数据修改的时间戳、每一版方案的对比、和许晚晴的讨论记录。"

    wbw "（内心）不是不气。但气没有用。"

    narrator "他把所有证据整理好，存了两份备份，然后关上电脑。"

    if not evidence_ready:
        $ evidence_ready = True
        $ notify_change("关键证据已整理完毕")

    jump chapter_05
