label sequel_chapter_05_winter:
    $ sequel_chapter_progress = 5
    $ notify_change("新篇进度：冬之章")

    scene bg sakurakagami_station_winter with fade

    narrator "当晚，樱镜町在没有预报的情况下入了冬。雨丝在半空凝成冰晶，车站的时钟停在王不稳到来的那一分钟。"
    narrator "他赶到站台时，Ruby 正站在最初相遇的路灯下。银白色低双马尾几乎融进大雪，脚边散着一叠空白照片。"
    show ruby normal

    ruby "你还记得我吗？"
    wbw "Ruby。雨夜给我指路的人。你看见了行李上的冬纹，却没有告诉我。"
    ruby "……还好。"
    narrator "她捡起一张照片。画面里 Dana、Luna 和 Irene 并肩站着，原本属于 Ruby 的位置只剩一片不自然的光。"
    ruby "从下午开始，老师点名时会跳过我。邻居说那栋房子一直没人住。再过一会儿，连她们也会忘记。"
    wbw "你的耳坠在保存名字。"
    ruby "每响一次，就能替一个人多留一会儿。可它保存不了我自己。"
    narrator "Ruby 取下水晶耳坠。里面传出极轻的声音，像许多人隔着漫长冬夜依次报出姓名。"
    ruby "十二年前，四季镜选择了 Irene。现在它选择我。"
    ruby "我在镜里听见了四个人的求救，也看见另一个世界里不受这里改写的人。是我们的愿望把你拉了过来。"
    wbw "所以银白光不是谁设下的陷阱。"
    ruby "是镜在执行求救，也是它在寻找新的承载者。你身边那只行李、租约和学籍，都是它为了让你留下而补出的身份。"
    wbw "我的签名为什么像真的？"
    ruby "因为镜读到了你的记忆，却学不会你写字时最后那一下停顿。"
    narrator "王不稳想起旧世界备忘录里那行并不好看的字。再完美的伪造，也留下了可验证的破绽。"

    menu:
        "当 Ruby 的名字开始从世界上消失，王不稳选择——"

        "请她亲手写下名字和意愿，让所有人共同读出。":
            $ ruby_affection += 2
            $ sequel_insight += 1
            $ notify_change("Ruby 信任 +2")
            $ notify_change("洞察 +1")
            wbw "只靠我记住你，还是把责任交给一个人。"
            wbw "写下来。写你是谁，也写你愿不愿意继续承担。我们让全镇一起读。"
            ruby "如果他们害怕呢？"
            wbw "那也该由他们知道以后自己决定。"
            narrator "Ruby 在结霜的候车室玻璃上，一笔一画写下自己的名字。"

        "承诺无论发生什么，自己都不会忘记她。":
            wbw "我不会忘记你。"
            ruby "这句话很温柔。可如果只有你记得，我还是会变成只属于你的影子。"
            narrator "她仍然在玻璃上写下名字，只是没有把耳坠交出来。"

    narrator "Dana 把写有居民姓名的卡片送到车站；Luna 接通全镇广播；Irene 打开档案馆的旧录音。"
    narrator "一个又一个声音念出 Ruby 的名字。玻璃上的字不再结霜，照片里的空白也短暂恢复了轮廓。"
    ruby "镜在下面。站台尽头那扇从来打不开的门，就是入口。"
    narrator "冬之钥印在她掌心亮起。寒意沿着手臂向上蔓延，像要把她整个人变成透明的冰。"

    menu:
        "钥印要求一名承载者独自接住全部冬夜。"

        "尊重 Ruby 的决定，与其他三人共同扶住钥印。":
            $ ruby_affection += 1
            $ sequel_resolve += 1
            $ notify_change("Ruby 信任 +1")
            $ notify_change("共同意志 +1")
            wbw "决定权在你。无论你选什么，我们都不会让你一个人接住。"
            ruby "我不想消失。"
            ruby "也不想用别人的消失换我留下。请和我一起。"
            narrator "四只手先后落在钥印边缘。王不稳最后托住最下方，寒意被分成五道微弱的光。"

        "抢过钥印，试图代替她成为承载者。":
            wbw "我是外来者，镜本来就在找我。由我承担更合适。"
            ruby "你又在替我决定。"
            narrator "她没有松手。Dana、Luna 和 Irene 同时扶住钥印，强行把集中的寒意分开。"

    scene cg sequel_ruby_name with dissolve
    narrator "冻结的雨夜车站里，Ruby 的倒影一度从镜面消失。她把自己的名字写在结霜玻璃上，身后四个人的手同时按住那道即将闭合的光。"
    ruby "这一次，我要作为 Ruby 留下来。不是冬之女，也不是谁的代价。"

    $ winter_fragment = True
    $ notify_change("获得冬之碎片")

    scene bg sakurakagami_station_winter with dissolve
    show ruby normal
    narrator "站台尽头传来机关转动的声音。封闭多年的门向下开启，露出一段被四种季节同时照亮的阶梯。"
    ruby "镜室醒了。"
    wbw "那就去把规则改掉。"

    call v21_sequel_chapter_05_winter

    jump sequel_finale
