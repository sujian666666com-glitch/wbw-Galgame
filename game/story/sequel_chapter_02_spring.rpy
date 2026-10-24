label sequel_chapter_02_spring:
    $ story_arc = "sequel"
    $ sequel_chapter_progress = 2
    $ notify_change("续篇进度：春之章")

    scene bg spring_garden with fade
    show dana normal
    show wangbuwen normal

    narrator "春庭位于学园与旧街之间，曾经是全镇共同照料的花园。"
    narrator "荒废多年后，Dana 发起复兴活动，把大学部学生和附近居民重新召集到一起。"
    dana "工具按颜色放，年纪大的居民负责播种，搬土和修水渠交给我们。别逞强，也别抢活。"
    narrator "她拿着名单穿梭在人群里，准确叫出每个人的名字，也记得谁对花粉过敏、谁的腰不能久弯。"
    wbw "你准备了多久？"
    dana "名单做了一周，挨家挨户敲门用了三天。"
    wbw "不是临时起意。"
    dana "当然。让大家重新说上话，比种花难多了。"

    show ruby normal
    show luna normal

    luna "昨晚的监测记录显示，这里的土壤温度在十分钟内经历了四个月的变化。"
    ruby "我听见花下面有人说话。"
    dana "Ruby，别吓第一次来的志愿者。"
    ruby "不是吓人。它们在重复名字。"
    hide ruby
    hide luna
    narrator "王不稳蹲下检查刚翻开的泥土。里面没有机械，也没有人为加热的痕迹。"
    narrator "一名居民把种子埋进土里。几乎就在手掌离开的瞬间，嫩芽破土而出。"
    narrator "嫩芽抽枝、结苞、盛开，随后在所有人面前迅速枯萎。"
    narrator "整个过程不到一分钟。"
    dana "大家先停下！离花床远一点，按名单到入口集合！"
    narrator "她没有慌乱，立刻把人群带离异常区域。"

    menu:
        "Dana 一个人同时清点人员、安抚居民并封锁花床，王不稳选择——"

        "先问 Dana 需要什么，再按她的方案分工。":
            $ dana_affection += 2
            $ notify_change("Dana 信任 +2")
            wbw "你负责人的情况，我负责现场记录。还缺什么？"
            dana "让 Luna 备份监测数据，请 Ruby 听清那些名字。然后帮我核对名单。"
            wbw "明白。你继续指挥。"
            narrator "Dana 看了他一眼，用力点头。王不稳没有接管她的工作，而是把她的方案变成可执行的步骤。"

        "直接接过名单，替 Dana 指挥所有人。":
            wbw "名单给我，你先休息。"
            dana "我没有需要被替换。"
            narrator "她抽回名单，语气仍然温和，却没有退让。"
            dana "你可以帮忙记录，但这里每个人的情况只有我清楚。听我的安排。"

        "建议立刻解散活动，所有人各自回家。":
            wbw "异常原因不明，最安全的做法是先撤离。"
            dana "撤到入口可以，不能让大家独自回去。"
            narrator "Dana 指向名单。"
            dana "刚才有个人还在帮我们搬花盆，现在已经没人记得他住在哪里了。"

    narrator "重新清点时，名单上有二十七个名字，现场却只有二十六个人。"
    narrator "空出来的位置旁放着一副沾满泥土的手套。所有居民都看见过它，却没人能说出手套属于谁。"
    dana "我记得有人。"
    wbw "名字呢？"
    dana "想不起来。但我记得他把水递给我时，手在发抖。"
    narrator "Dana 用力按住太阳穴。她能感到被抹去的人留下的情绪，却抓不住具体身份。"
    ruby "花下面念的就是那个名字。可是每念一遍，声音都会更轻。"
    luna "监测数据也在自动减少。再过几分钟，异常曲线会变成正常值。"
    wbw "先离线保存，再让每个人说出自己还记得的细节。不要等完整答案。"

    scene cg sequel_dana_spring with dissolve

    narrator "枯萎的春庭中央，Dana 站到所有人面前，举起那副陌生手套。"
    dana "我们可能不记得他的名字，但这不代表他没有来过。"
    dana "请每个人说一件刚才发生过的事。哪怕只记得有人扶过花盆、递过水，也请说出来。"
    narrator "零碎的声音逐渐连成一条线。有人记得灰色袖口，有人记得低沉笑声，有人记得水渠边多出的一道脚印。"

    menu:
        "这些记忆正在迅速消退，应该由谁保存？"

        "让每位见证者各自保存一小段，再互相核对。":
            $ dana_affection += 1
            $ sequel_insight += 1
            $ sequel_resolve += 1
            $ notify_change("Dana 信任 +1")
            $ notify_change("洞察 +1")
            $ notify_change("共同意志 +1")
            wbw "不要把所有记忆压在一个人身上。每人写下一段，交换副本，定期互相确认。"
            dana "这样就算一个人忘了，其他人也能把那一段还给他。"
            narrator "她把名单拆成多份，让每位居民签下自己愿意保留的那一小段。"

        "把全部记录交给 Dana，由她一个人保管。":
            wbw "你记得最多，集中给你最有效率。"
            dana "也最容易一次全部丢掉。"
            narrator "Dana 摇头，把手中的记录分给居民。"
            dana "我可以负责联系大家，但不能替所有人承担记忆。"

        "由王不稳建立一份唯一的总档案。":
            wbw "我是外来者，也许不会被这里改写。交给我保存。"
            luna "单一档案同样可能损坏。"
            dana "而且这是大家共同经历的事，不能只留在一个陌生人的手机里。"
            narrator "在 Dana 的坚持下，总档案被复制给每一位自愿参与的见证者。"

    narrator "当最后一份记录完成，枯萎花床里升起一枚嫩绿色的光片。"
    narrator "它像一片刚展开的叶，又像镜子缺失的一角，映出方才所有人彼此确认姓名的画面。"
    dana "它没有拿走任何人的记忆。"
    ruby "因为这一次，记忆没有只放在一个人身上。"
    luna "共同存储降低了单点消失的风险。这个机制可以验证。"
    narrator "Dana 伸手触碰光片。春色沿着她的指尖亮起，随即安静下来。"
    $ spring_fragment = True
    $ notify_change("已取得春之碎片")

    scene bg academy_courtyard with dissolve
    show luna normal
    show dana normal
    show wangbuwen normal

    narrator "回到学园后，Luna 把春庭记录与近期环境数据交叉比对。"
    luna "同样的时间回卷还出现在海岸。今晚海灯祭试运行，潮汐预测却出现了向陆地方向倒流的数据。"
    dana "海水还能倒着走？"
    luna "正常情况下不能。所以我要亲眼确认。"
    wbw "我和你一起去。带上离线记录设备，也带上春庭的分布式副本。"
    luna "可以。但到了现场，必须遵守我的安全方案。"
    call v21_sequel_chapter_02_spring
    narrator "夜色落下前，一行人向海边灯塔出发。"

    jump sequel_chapter_03_summer
