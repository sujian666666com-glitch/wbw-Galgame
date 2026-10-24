label sequel_finale:
    $ sequel_chapter_progress = 6
    $ notify_change("新篇进度：终章")

    scene bg mirror_chamber with fade
    narrator "车站下方没有铁轨，只有一座悬在黑暗中的圆形镜室。春花、夏潮、秋叶和冬雪在同一片空气里缓慢旋转。"
    narrator "四枚碎片脱离众人掌心，嵌入中央那面布满裂纹的古镜。"

    show dana normal
    dana "外面的人都到广播点了。每个人手里都有一张名字卡。"
    hide dana
    show luna normal
    luna "观测数据已经公开。任何变化都会由十二个独立节点同时记录，不会再只有一个人掌握真相。"
    hide luna
    show irene normal
    irene "档案馆的门全部打开了。被删掉的名字、被改写的年份，都有人自愿读下去。"
    hide irene
    show ruby normal
    ruby "耳坠里保存的声音，也接入了广播。"
    hide ruby

    narrator "镜面亮起，一段没有感情的文字浮现在裂纹之间。"
    narrator "维持樱镜町需要稳定记忆。旧规则提供三种方案：四名承载者各失去一段核心记忆；外来见证者失去原世界；关闭镜面，让本世界停止。"
    wbw "这不是神谕，只是一套用了太久的应急规则。"
    luna "规则的目标函数是用最少承载者维持最多生命。它从未计算自愿分担。"
    irene "因为过去的人没有把那条路写进记录。"
    dana "那我们现在写。"
    ruby "用所有愿意记住的人，一起写。"

    scene cg sequel_mirror_finale with dissolve
    narrator "四位女孩围住破裂的四季镜。广播里，居民依次读出自己愿意保存的名字与记忆。无数微小光点从小镇升起，在镜室上空连成一张网。"
    narrator "王不稳把一路留下的文件、时间戳、潮汐日志、创始记录和姓名卡按顺序排开。"
    wbw "请求修改协议：记忆负荷不再强制集中。每一份承担都必须知情、自愿、可撤回，也必须留下多人可复核的记录。"
    narrator "镜面沉默了很久。裂纹间开始推演几条仍可执行的道路。"

    menu:
        "四季镜等待王不稳给出最后的选择。"

        "让整个樱镜町共同记住四季。" if sequel_truth_ready():
            $ sequel_route = "true"
            jump sequel_ending_true

        "留下来，与 Dana 一起守住每一次相遇。" if dana_affection >= 3:
            $ sequel_route = "dana"
            jump sequel_ending_dana

        "留下来，与 Luna 一起建立公开的观测坐标。" if luna_affection >= 3:
            $ sequel_route = "luna"
            jump sequel_ending_luna

        "留下来，与 Irene 一起重写不再封闭的档案。" if irene_affection >= 3:
            $ sequel_route = "irene"
            jump sequel_ending_irene

        "留下来，陪 Ruby 记住每一个冬夜的名字。" if ruby_affection >= 3:
            $ sequel_route = "ruby"
            jump sequel_ending_ruby

        "回到原来的世界，带走这里真实存在过的证据。":
            $ sequel_route = "return"
            jump sequel_ending_return
