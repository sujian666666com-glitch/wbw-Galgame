label sequel_chapter_03_summer:
    $ story_arc = "sequel"
    $ sequel_chapter_progress = 3
    $ notify_change("续篇进度：夏之章")

    scene bg lighthouse_night with fade
    show luna normal
    show wangbuwen normal

    narrator "入夜后，樱镜町海岸仍残留着白天的热意。"
    narrator "试运行的海灯沿防波堤依次亮起，灯塔则像一枚钉子，把深蓝色夜空固定在海面上。"
    narrator "Luna 在三个观测点布置离线记录器，又给每个人分配明确区域。"
    luna "Dana 负责疏散入口，Ruby 留在高处观察光色，Irene 去灯塔旧档案室。"
    luna "王不稳跟我核对主观测点。任何人都不准脱离联络范围。"
    wbw "如果设备记录和肉眼不同？"
    luna "两者都保留，不急着宣布谁错。"
    narrator "她递给王不稳一份纸质潮汐表。表上的今晚高潮时间被人用红笔改过三次。"
    wbw "谁改的？"
    luna "每一次都是我。因为每次复查，原始数据都会变成另一个结果。"
    wbw "所以你改在纸上。"
    luna "纸也会变。我只是在测试它多久开始忘记。"

    show dana normal
    dana "入口已经清空，居民都到高处了。还有两盏海灯没收回来。"
    luna "灯可以丢，人不可以回去。"
    hide dana
    narrator "她话音刚落，远处海面忽然安静下来。"
    narrator "浪声消失，悬在空中的海灯同时熄灭。下一秒，潮水沿着陡峭礁石向上爬升。"
    dana "真的倒着流了……"
    narrator "不是浪涌。整片海像一张被人倒放的影像，水流越过重力，朝灯塔顶端汇聚。"

    scene cg sequel_luna_tide with dissolve

    narrator "逆流海潮在灯塔外盘旋，盛夏的光从水中透出。Luna 站在主观测台前，手中的仪器不断报警。"
    luna "三号设备失联，主设备还有九十秒覆盖旧数据。"
    wbw "你的方案？"
    luna "我留在这里导出原始日志。你沿安全绳去二号点取纸带，必须在六十秒内返回。"

    menu:
        "潮水逼近观测台，王不稳决定——"

        "执行 Luna 的分组方案，带回二号点原始纸带。":
            $ luna_affection += 2
            $ sequel_insight += 1
            $ notify_change("Luna 信任 +2")
            $ notify_change("洞察 +1")
            wbw "六十秒。超过时间我就放弃设备，按原路撤回。"
            luna "复述正确。行动。"
            narrator "王不稳扣紧安全绳，没有偏离 Luna 标出的路线。"
            narrator "他在纸带被水卷走前取下整卷记录，并按约定时间回到主观测台。"
            luna "时间五十八秒。数据完整。"
            wbw "你的判断也完整。"

        "离开安全绳，直接冲向更近的三号设备。":
            wbw "三号点更近，我去那里。"
            luna "距离近不等于路线安全！"
            narrator "逆流在礁石间突然转向，迫使王不稳退回观测台。"
            narrator "Luna 及时切断三号设备电源，避免短路波及灯塔。"
            luna "调查不是证明个人胆量。下一次先服从现场方案。"

        "立即撤离，放弃全部现场数据。":
            wbw "数据可以重做，先撤。"
            luna "人员撤离优先，但主设备可以远程导出。"
            narrator "两人退到安全线内。Luna 一边撤离，一边完成了残缺日志的离线备份。"
            luna "不完整，但至少没有拿人去换设备。"

    narrator "九十秒后，逆流骤然落回海面。浪声重新出现，所有电子设备上的异常曲线却开始变平。"
    show luna normal
    show wangbuwen normal
    narrator "只有纸带和分散在众人手里的副本保留了原貌。"
    luna "和春庭一样。系统会自动生成一个‘从未异常’的结果。"
    wbw "但这次它没能同时改掉所有见证者。"

    hide wangbuwen
    show irene normal
    irene "灯塔旧档案里有一套相同的潮汐曲线，日期是十二年前。"
    narrator "Irene 把一页泛黄记录放在地上。记录末尾写着：夏季承载完成，异常归零。"
    luna "承载者姓名被删除了。"
    irene "不是自然褪色，是后来的人主动刮掉。"
    ruby "海里还有一个声音。它在问，这次由谁来记住。"
    dana "我们都在这里。为什么一定只能选一个人？"
    narrator "Luna 看向手中的多份记录，第一次没有立刻回答。"

    menu:
        "应该如何向居民说明今晚的异常？"

        "公开可复核证据，并邀请见证者补充各自记录。":
            $ luna_affection += 1
            $ sequel_resolve += 1
            $ notify_change("Luna 信任 +1")
            $ notify_change("共同意志 +1")
            wbw "先公布时间、观测点和原始纸带，不替大家下结论。"
            luna "每项证据标明来源和缺失部分，让见证者自行确认。"
            narrator "Luna 建立公开记录页，把不同人的观察并列保存，而不是压成唯一答案。"

        "立刻上传全部原始资料，让异常引发全镇关注。":
            wbw "越多人看到，越不容易被删掉。"
            luna "没有说明来源的碎片只会制造恐慌。"
            narrator "她拦下未经整理的数据包，保留副本后，只发布已经完成交叉验证的部分。"
            luna "公开不是把风险推给不知情的人。"

        "暂时封锁消息，只让五个人保留记录。":
            wbw "知道的人越少，越容易控制。"
            luna "也越容易一次性被改写。"
            narrator "Luna 想起春庭的分散记录，最终邀请当晚所有自愿见证者各自保存一份。"
            luna "控制信息不能解决单点失效。"

    narrator "公开记录完成后，海面下升起一枚炽蓝色光片。"
    narrator "它穿过水面落在 Luna 掌心，像盛夏正午被压进一块透明镜片。"
    $ summer_fragment = True
    $ notify_change("已取得夏之碎片")

    luna "春庭的碎片回应共同记忆，海里的碎片回应共同见证。"
    wbw "这套机制未必要求牺牲。它只是在寻找能让世界稳定下来的承载方式。"
    irene "你们看到的是结果，不是全部规则。"
    narrator "Irene 的声音很轻。她盯着那页十二年前的记录，脸色比海灯熄灭时更冷。"
    luna "这份记录使用了你的旧学生会权限编号。"
    dana "十二年前你才十二岁。"
    ruby "Irene，你是不是记得上一次发生了什么？"
    narrator "海风吹动泛黄纸页。Irene 沉默许久，终于将它收回档案袋。"
    irene "明天来旧档案馆。我会告诉你们秋天拿走了什么。"
    wbw "这次不会再只由一个人保存答案。"
    irene "希望你听完以后，还能这么说。"
    narrator "她转身走下灯塔。远处海面已经恢复平静，仿佛逆流从未发生。"
    narrator "但春与夏的两枚碎片仍在黑暗中发光，证明这个夜晚无法再被彻底抹去。"

    jump sequel_chapter_04_autumn
