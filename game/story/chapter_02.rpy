label chapter_02:
    $ chapter_progress = 2
    $ notify_change("章节进度：第二章")

    scene bg office_night with fade
    show jianglin normal

    narrator "办公区只剩几盏灯亮着。江临一个人坐在工位前，对着电脑屏幕。"
    narrator "主管让江临整理活动报名数据，他一边整理一边发现异常——两组数据的用户增长曲线完全不合理，像是被人为修改过的。"
    jl "（内心）这个数据不对……如果按这个投放下去，这周末的活动会出大问题。"

    menu:
        "发现数据异常后，江临准备怎么做？"

        "直接给主管发消息，报告数据异常。":
            $ ability += 1
            $ evidence_ready = True
            $ notify_change("许晚晴好感度 +0")
            $ notify_change("能力 +1")
            $ notify_change("数据异常证据已留存")
            show wangley serious
            wl "你确定？别瞎说。"
            narrator "王磊半信半疑，但最终核实后发现江临是对的。"

        "先自己跑一遍完整数据验证，确认后再汇报。":
            $ affection += 2
            $ ability += 2
            $ evidence_ready = True
            $ notify_change("许晚晴好感度 +2")
            $ notify_change("能力 +2")
            $ notify_change("完整数据证据已准备")
            narrator "江临花了两小时跑完数据，拿着完整报告找王磊。"
            show wangley serious
            narrator "王磊的脸色变了。"

        "发到工作群里公开指出问题。":
            $ affection += 1
            $ ability += 1
            $ evidence_ready = True
            $ notify_change("许晚晴好感度 +1")
            $ notify_change("能力 +1")
            $ notify_change("数据异常证据已公开留存")
            narrator "办公室气氛紧张起来。"
            show zhanghao normal
            narrator "张浩脸色难看，因为数据是他负责的。"
            show wangley serious
            wl "为什么不先跟我说？"

    scene bg office with dissolve
    show jianglin normal

    narrator "第二天，消息传开了——实习生发现了一个数据漏洞，帮公司避免了一次活动事故。"
    show zhanghao normal
    zh "一个实习生，多管闲事。"
    narrator "但其他同事看江临的眼神变了。"

    scene bg rooftop_night with dissolve
    show jianglin normal
    show xuwanqing normal

    narrator "公司天台上风有点大。许晚晴站在栏杆边。"
    narrator "江临推开天台的门，看到许晚晴正对着远处的高楼发呆。"
    xw "听说你昨天发现了数据的问题？"
    jl "碰巧看到的。"
    xw "碰巧？别人天天看那些数据都没发现，你来了三天就看到了。"
    jl "……可能是他们太忙了。"
    show xuwanqing serious
    xw "你不用替他们说话。"
    narrator "她转过身，看着江临。"
    xw "你那个备忘录还记得吗？三个月，留下来。"
    jl "记得。"
    xw "现在几天了？"
    jl "第四天。"
    show xuwanqing happy
    xw "还不错，没被赶走。"

    menu:
        "江临怎么回答？"

        "才第四天，急什么。":
            $ affection += 3
            $ notify_change("许晚晴好感度 +3")
            show jianglin confident
            show xuwanqing happy
            narrator "江临笑着回应。"
            xw "行，那我等着看。"

        "你一直在观察我？":
            $ affection += 2
            $ notify_change("许晚晴好感度 +2")
            show xuwanqing surprised
            narrator "许晚晴顿了一下。"
            xw "……观察算不上，就是觉得你挺有意思的。"

        "被赶走也不怕，大不了换个地方。":
            $ affection += 1
            $ notify_change("许晚晴好感度 +1")
            show xuwanqing happy
            xw "嘴硬。"

    jump chapter_03
