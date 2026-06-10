label chapter_01:
    $ chapter_progress = 1
    $ notify_change("章节进度：第一章")

    scene bg bedroom_small_day with fade
    show jianglin normal

    narrator "一间不足十平米的小房间，一张床、一张桌、一把椅子。窗外是嘈杂的街道。"
    narrator "江临把行李箱打开，里面的东西不多——几件换洗衣服、一台旧笔记本电脑、一个笔记本。"
    $ money -= 1200
    $ notify_change("支付首月房租 -1200")
    jl "（内心）够了。"

    scene bg office with dissolve
    show jianglin normal
    show wangley serious

    narrator "开放式办公区里工位密集，键盘声此起彼伏。"
    narrator "江临被带到工位前，主管王磊扫了一眼他的简历。"
    wl "实习生是吧，先把这些表格整理了。"
    narrator "一摞厚厚的打印资料被推过来。"
    jl "好的。"
    narrator "江临接过资料，没有多说。"

    show zhanghao smug
    zh "又一个来打杂的，现在的实习生什么都不会。"
    narrator "江临没有回应。他开始整理表格，但同时在看每个数据背后的逻辑。"

    scene bg pantry with dissolve
    show jianglin normal
    show xuwanqing happy

    narrator "公司茶水间里，咖啡机嗡嗡响。"
    narrator "江临倒水的时候，许晚晴端着杯子走进来。"
    xw "地铁站那位——字丑的那个。"
    jl "……你还记得。"
    xw "你那几个字确实挺难看的。你也在这家公司？"
    jl "运营部实习生。"
    xw "巧了，我也是。策划方向的。"
    narrator "她靠在台面上，打量了他一眼。"
    xw "第一天就被派了杂活？"
    jl "正常。"

    menu:
        "江临怎么回应？"

        "没事，我正好趁这个机会看看公司的数据。":
            $ affection += 3
            $ ability += 1
            $ notify_change("许晚晴好感度 +3")
            $ notify_change("能力 +1")
            show jianglin confident
            show xuwanqing happy
            xw "你倒是挺会找机会。"

        "杂活也得有人干，先干着呗。":
            $ notify_change("许晚晴好感度 +0")
            show xuwanqing normal
            xw "嗯，也对。"
            narrator "她语气平淡，转身离开。"

        "别提了，烦得要死。":
            $ affection -= 2
            $ notify_change("许晚晴好感度 -2")
            show xuwanqing serious
            xw "那你当初来干嘛？"
            narrator "她微微皱眉。"

    jump chapter_02
