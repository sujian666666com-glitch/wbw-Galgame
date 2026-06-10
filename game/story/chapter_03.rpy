label chapter_03:
    $ chapter_progress = 3
    $ notify_change("章节进度：第三章")

    scene bg meeting_room with fade
    show wangley serious
    show jianglin normal
    show xuwanqing normal

    narrator "会议室里，主管王磊正在分配任务。"
    wl "这次的新品推广活动，策划由许晚晴负责，执行和数据由江临配合。你们俩一组。"
    narrator "许晚晴看了江临一眼，没说话。江临点了点头。"
    show zhanghao smug
    zh "两个实习生做活动，能行吗？"

    scene bg convenience_store_night with dissolve
    show jianglin normal
    show xuwanqing serious

    narrator "深夜，便利店门口只有路灯亮着。两人坐在塑料凳上，拿着各自的笔记本，对着方案逐条过。"
    xw "标题我改了三版，你看看哪个切入点更准。"
    jl "第三版。但第一版的结构更好，可以结合起来。"
    xw "你倒是直接。"
    jl "你不是让我别说客气话吗？"
    show xuwanqing surprised
    xw "……我什么时候说的？"
    jl "天台上，你让我别替别人说好话。我也没打算对你客气。"
    narrator "许晚晴愣了一下，随即笑了。"
    show xuwanqing happy
    xw "行，那就别客气。你觉得投放预算分配有问题？"
    jl "对，主渠道投太多了，我查了用户画像，次渠道的转化率更高。"

    menu:
        "面对投放预算的问题，江临怎么建议？"

        "我把数据报告发你，你先看，明天咱们碰。":
            $ affection += 2
            $ ability += 1
            $ notify_change("许晚晴好感度 +2")
            $ notify_change("能力 +1")
            show xuwanqing happy
            xw "好，专业。"

        "要不现在就去公司跑一遍数据？":
            $ affection += 4
            $ ability += 2
            $ notify_change("许晚晴好感度 +4")
            $ notify_change("能力 +2")
            show xuwanqing surprised
            narrator "许晚晴看了他一眼。"
            show xuwanqing happy
            xw "……走啊。"
            scene bg office_night with dissolve
            show jianglin confident
            show xuwanqing serious
            narrator "两人回到公司，对着数据跑了两个小时，最终确定了新的投放方案。"

        "这个你比我懂，你定就行。":
            $ affection -= 2
            $ notify_change("许晚晴好感度 -2")
            show xuwanqing angry
            xw "我问你的意见，不是让你甩给我。"

    scene bg office with dissolve
    show jianglin normal
    show xuwanqing normal
    show wangley serious

    narrator "一周后的早晨，活动上线后数据一路上涨，最终成了当月的小爆款。王磊在早会上点名表扬。"
    wl "这次活动效果不错，许晚晴策划到位，江临数据分析很精准。"
    narrator "许晚晴在对面冲江临举了一下拳头，很小的一个动作，只有他看到。"
    $ side_project_ready = True
    $ notify_change("合作项目经验已准备")

    menu:
        "早会结束后，江临怎么回应这次成功？"

        "会后悄悄给她买一杯咖啡放在桌上。":
            $ affection += 3
            $ money -= 18
            $ notify_change("许晚晴好感度 +3")
            $ notify_change("资金 -18")
            narrator "许晚晴回来看到咖啡，嘴角微微上扬，没说话。"
            show xuwanqing happy

        "当面说：这次多亏你的策划。":
            $ affection += 2
            $ notify_change("许晚晴好感度 +2")
            show xuwanqing happy
            xw "别谦虚，你的数据才是关键。"

        "什么都没说，觉得这没什么。":
            $ notify_change("许晚晴好感度 +0")
            show xuwanqing normal
            xw "（内心）……这人，就这样？"

    scene bg company_street_night with dissolve
    show jianglin normal
    show xuwanqing normal

    narrator "公司楼下的街道上，夜色刚落。"
    xw "你有没有想过，如果这个活动失败了怎么办？"
    jl "没想过。"
    xw "骗人。"
    jl "……好吧，想过。最差就是被辞退，然后重新找。"
    show xuwanqing worried
    xw "你不怕？"
    jl "怕。但怕不是不做的理由。"
    narrator "许晚晴没有接话，走了几步之后忽然说——"
    show xuwanqing serious
    xw "我喜欢的不是你赢，是你明明快输了，还能冷静地找下一步。"
    jl "……"
    show xuwanqing happy
    xw "行了，别愣着，我请你吃饭。"

    menu:
        "江临怎么回答？"

        "你请？那我不客气了。":
            $ affection += 2
            $ notify_change("许晚晴好感度 +2")
            show xuwanqing happy
            xw "你终于不客气了。"

        "还是 AA 吧，我现在不富裕。":
            $ affection += 3
            $ money -= 50
            $ notify_change("许晚晴好感度 +3")
            $ notify_change("资金 -50")
            show xuwanqing surprised
            narrator "许晚晴看了他一眼。"
            show xuwanqing happy
            xw "……行，那下次我让你请。"

        "不用了，我回去还有事。":
            $ affection -= 1
            $ notify_change("许晚晴好感度 -1")
            show xuwanqing worried
            xw "哦。那好吧。"
            narrator "她的脚步慢了半拍。"

    jump chapter_04
