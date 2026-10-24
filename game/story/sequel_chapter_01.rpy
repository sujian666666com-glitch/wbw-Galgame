label sequel_chapter_01:
    $ story_arc = "sequel"
    $ sequel_chapter_progress = 1
    $ notify_change("续篇进度：初遇")

    scene bg old_house_day with fade
    show wangbuwen normal

    narrator "第二天清晨，王不稳在旧宅二楼醒来。"
    narrator "昨晚那把钥匙确实打开了白色栅栏后的房门。屋里没有灰尘，冰箱里甚至放着刚好够三天的食物。"
    narrator "卧室书桌上摆着一张入住清单，末尾仍是那个像他、却不属于他的签名。"
    wbw "准备得越周全，越说明不是意外。"
    narrator "他把录取材料、租约和照片各做了一份备份，随后才推门出去。"

    show dana normal

    dana "早上好！你就是昨晚搬来的新邻居吧？"
    narrator "粉棕色双马尾的女孩站在隔壁院门前，怀里抱着一盆刚发芽的花。"
    wbw "消息传得这么快？"
    dana "不是消息快，是这栋房子空了很久。突然亮灯，整条巷子都看得见。"
    dana "我叫 Dana，樱镜学园大学部一年级。你今天也要去报到吧？"
    wbw "材料上是这么写的。"
    dana "材料上？你说话好奇怪。"
    wbw "我对这里还不熟。"
    dana "那正好，我带路。离线地图在旧街经常会绕远，你跟我走不会迟到。"
    narrator "Dana 没有追问，主动走在前面。她一路和每个遇见的邻居打招呼，连对方家门口新换的花盆都记得。"
    wbw "你认识整条街的人？"
    dana "差不多吧。只要一直记得，大家就不会真的变成陌生人。"
    narrator "她说完笑了笑，像是随口一句玩笑。"

    scene bg academy_courtyard with dissolve
    show wangbuwen normal
    show dana normal

    narrator "樱镜学园是一所包含大学部的综合学院。大学部学生全部成年，只在典礼和学生会值勤时穿统一制服。"
    narrator "这解释了录取材料上的年龄，却解释不了那份提前三个月出现的学籍。"

    hide dana
    show luna normal

    luna "王不稳，二十二岁，大学部转入生。系统显示你应该在三个月前完成报到。"
    narrator "青绿色短发的女孩抱着平板站在庭院入口，声音冷静得像在核对一张清单。"
    wbw "但我是昨晚第一次到这里。"
    luna "那就有矛盾。"
    dana "Luna，你别一见面就审人嘛。"
    luna "我负责学生会学籍协查。发现矛盾是工作，不是审问。"
    wbw "录入账号能查到吗？"
    luna "正在查。"

    hide luna
    show ruby normal

    ruby "昨晚车站的人。"
    narrator "Ruby 从教学楼方向走来。她看到王不稳时先是一怔，随后望向他身边的行李文件袋。"
    wbw "你果然也在这里。"
    dana "你们认识？"
    ruby "昨晚见过一面。我给他指了去旧宅区的路。"
    narrator "她没有提自己曾经说过‘我知道你的名字’，却明显在等王不稳如何回答。"

    menu:
        "面对 Ruby 的试探，王不稳决定——"

        "坦白自己是被银光带来，身份材料也不是本人办理。":
            $ ruby_affection += 1
            $ sequel_resolve += 1
            $ notify_change("Ruby 信任 +1")
            $ notify_change("共同意志 +1")
            wbw "昨晚以前，我不知道樱镜町，也没有申请这里的学籍。"
            wbw "我在另一个城市被一团银光卷进来，醒来时行李和材料就在脚边。"
            narrator "Dana 收起笑意，Luna 立刻在平板上新建记录。Ruby 则像终于等到这句话，慢慢松开攥紧的手。"
            ruby "至少你没有把材料里的故事当成自己的记忆。"
            wbw "所以你知道它们是假的。"
            ruby "我只知道，这座镇子有时会替新来的人写好一个身份。"

        "暂时沿用材料中的转学生说法。":
            wbw "昨晚刚到，很多手续还没来得及确认。"
            narrator "Ruby 看了他几秒，没有拆穿。"
            ruby "原来如此。那你最好亲自核对每一页。"
            narrator "她的语气仍然温和，两人之间却多了一层没有说破的距离。"

    luna "不管来历是哪一种，系统记录本身都可以验证。"

    menu:
        "王不稳要如何处理异常学籍？"

        "立即与 Luna 核对录入时间、账号和签名。":
            $ sequel_insight += 1
            $ notify_change("洞察 +1")
            narrator "王不稳把昨晚拍下的材料并排放在 Luna 的平板旁。"
            narrator "纸质回执和系统学籍都创建于三个月前的同一分钟，录入账号却不属于任何教职员工。"
            luna "系统日志里没有登录过程，只有完成后的结果。"
            wbw "像是有人跳过了过程，直接把结果写进现实。"
            narrator "两份签名的收笔角度完全相同，也保留着同一处模仿错误。"
            luna "结论：这不是你的签名，而且伪造者使用了同一个样本。"

        "先完成报到，等拿到更多权限再查。":
            wbw "现在能看到的只是表面记录。先完成报到，别让系统把我挡在外面。"
            luna "务实。"
            narrator "Luna 为他办理临时通行权限，同时把异常学籍标为禁止自动覆盖。"
            luna "原始记录我会离线保存。等权限开放，再查录入源。"

    hide ruby
    show irene normal

    irene "把原始记录交给我一份。学生会服务器会忘记，但旧档案室不会。"
    narrator "白金色盘发的女人从回廊下走来。她没有穿学生制服，胸前别着大学部档案馆的工作证。"
    dana "Irene 学姐！"
    irene "我已经毕业两年了，不必再叫学姐。"
    luna "Irene，二十四岁，大学部档案馆助理，前学生会长。她有权限调阅旧制学籍。"
    irene "介绍得很完整。"
    narrator "Irene 接过材料，没有先看文字，而是看向文件袋上的樱花镜纹。"
    irene "这个纹章已经十二年没有出现在正式文件上。"
    ruby "十二年……"
    narrator "Ruby 耳垂上的水晶耳坠泛起微弱白光。Dana 怀中的嫩芽忽然舒展，Luna 的平板温度骤升，Irene 的黑色耳环则映出一片红叶。"

    scene cg sequel_four_meeting with dissolve

    narrator "四种光在庭院中央短暂交汇，又同时熄灭。"
    dana "刚才那是什么？"
    luna "不是设备投影。平板记录到四个不同温区。"
    irene "春、夏、秋、冬。"
    wbw "四个季节，和昨晚银光里的一样。"
    ruby "所以，它真的把你带来了。"
    narrator "所有人的目光落在 Ruby 身上。她沉默片刻，最终没有逃开。"
    ruby "我不知道完整答案。但最近每次下雨，我都会梦见一个站在银光外的人。"
    irene "这里不是谈这件事的地方。"
    dana "那先去春庭吧。那里今天有大学部和居民一起参加的复兴活动，人多，也不会有人觉得我们在秘密开会。"
    luna "春庭昨晚出现异常生长记录，值得调查。"
    wbw "那就从能验证的异常开始。"
    narrator "Dana 抱紧花盆，率先走向庭院外。"
    dana "跟好。春庭的路可不在你的离线地图里。"

    jump sequel_chapter_02_spring
