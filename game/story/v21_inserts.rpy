# 产品转录：台词与分支条件按蓝本保留。
# 时段场景改为同底图的 v21_time_* 调色；镜面文字用 screen 叠加，并在下一句前 hide。
# cg v21_xuwanqing_rain_close 只在 affection >= 8；cg v21_ruby_ending_kiss 只在 Ruby 结局。

# v2.1 新增剧情 Ren'Py label 蓝本
# 实作：Claude Code / deepseek-flash[1m]
# 日期：2026-10-24
#
# 用途：供技术负责人转录到产品 .rpy。以下 23 个 label 均以 return 结束，
#       不含 menu、不含数值赋值、不写 persistent。条件只读取既有变量：
#       affection、ability、money、side_project_ready、dana_affection、
#       luna_affection、irene_affection、ruby_affection、sequel_insight、
#       sequel_resolve、spring_fragment、summer_fragment、autumn_fragment、
#       winter_fragment、sequel_luna_observation_outcome。
#
# 图像 ID 严格按 CONTRACT.md：
#   新增表情仅 dana worried / luna soft / irene shaken / irene relieved /
#   ruby resolute；既有表情仅王不稳 normal/confident、许晚晴
#   normal/happy/serious/worried/angry/surprised、四位续篇角色 normal。
#   新增背景仅 bg v21_train_interior_dusk / bg v21_old_house_mirror；
#   新增 CG 仅 cg v21_xuwanqing_rain_close / cg v21_ruby_ending_kiss。
#
# 接入方式：由技术负责人在指定位置 call 对应 label；label 结束自动 return。


# ─────────────────────────────────────────────────────────────
# 01. 原稿：【新增剧情 · 雨夜，第一笔账】
# 接入：序章 menu（选择 01）结束后、jump chapter_01 之前
# ─────────────────────────────────────────────────────────────
label v21_prologue:
    scene bg bedroom_night with fade
    show wangbuwen normal

    narrator "楼道里的感应灯坏了三盏。王不稳摸黑走上六楼，箱子轮子磕着每一级台阶，声音在狭窄的楼梯间里反复回荡。"
    narrator "房东把钥匙交给他时，只说了句“水电另算，押金不退”。他没有争辩，逐条拍下租约，确认后才签名。"
    narrator "手机里，母亲发来一句“到了没”。他拍了张只露出窗台的照片，回复“到了，住得不错”。照片之外，是墙角一块没有干透的水渍。"
    wbw "（内心）不是不能说实话。只是现在说出来，也只能让他们跟着担心。"
    narrator "他把今晚最后一瓶矿泉水放到桌上，写下三列标题：现金、时间、可证明的能力。"
    narrator "写到最后，他忽然想起地铁站那个点评他字迹的女孩。"
    wbw "……明明只见一面，嘴还挺毒。"
    narrator "窗外又下起雨。这一次，他没有关窗，而是听着雨声把明天六点半的闹钟设好。"

    return


# ─────────────────────────────────────────────────────────────
# 02. 原稿：【新增剧情 · 第一周的午餐】
# 接入：第一章 menu（选择 02）结束后、jump chapter_02 之前
# 条件：affection >= 3 播放完整互动；低值播放职业互助克制版
# ─────────────────────────────────────────────────────────────
label v21_chapter_01:
    scene bg pantry with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "午休只剩下二十分钟。王不稳抱着便利店饭团走进茶水间，看见许晚晴正对着微波炉发愁。"
    xw "它不转了。也许是不喜欢我的午饭。"
    wbw "你没关门。"
    narrator "许晚晴低头看了一眼没扣紧的门，沉默两秒。"

    if affection >= 3:
        xw "今天这件事，不许写进你的备忘录。"
        wbw "我只记重要的数据。"
        show xuwanqing surprised
        xw "那我是不是不重要？"
        narrator "王不稳险些呛到。她却轻轻笑出声，像是终于替枯燥的一天找到了乐趣。"
        show xuwanqing happy
        xw "放心，我也没打算让你现在回答。"
        narrator "后来他才发现，自己桌边多了一盒退热贴。盒底用细字写着：别把自己熬坏，记得好好吃饭。"
    else:
        show xuwanqing normal
        xw "谢谢。至少微波炉比人好懂。"
        wbw "把门扣上就行。"
        narrator "他伸手把微波炉门扣紧，又按了两下。机器重新转起来，两个人都没有再提刚才的停顿。"
        xw "午休还剩十二分钟。你不热饭？"
        wbw "不用，我站着吃完。"
        xw "那我帮你看着时间。下午例会要用数据，别迟到。"
        narrator "后来他才发现，自己桌边多了一盒退热贴。盒底写着：下午要用数据，别在会上出错。"
        narrator "字迹很轻，像是刻意把关心控制在同事之间。"

    return


# ─────────────────────────────────────────────────────────────
# 03. 原稿：【新增剧情 · 天台上的第二个秘密】
# 接入：第二章 menu（选择 04）结束后、jump chapter_03 之前
# 条件：affection >= 3 保留碰拳；低值改为克制的收手。职业动机全文保留。
# ─────────────────────────────────────────────────────────────
label v21_chapter_02:
    scene bg rooftop_night with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "天台的风把纸杯吹得滚到墙角。许晚晴没有去捡，只盯着夜空中缓慢靠近的乌云。"
    xw "你知道我为什么来这家公司吗？"
    wbw "为了工作。"
    xw "回答得真没水平。"
    narrator "她笑了一下，随后敛去笑意。"
    show xuwanqing serious
    xw "我家里觉得策划不算正经职业。他们替我安排了稳定的岗位，连报到日期都定好了。"
    wbw "你没去。"
    xw "我想至少试一次，看看自己到底有没有能力把喜欢的事情做好。"
    narrator "王不稳终于明白，她每次改方案到凌晨，不只是为了绩效。"
    wbw "那我们就把这次活动做好。至少结果可以由我们自己说了算。"
    xw "你是在安慰我？"
    show xuwanqing normal
    wbw "不是。是在邀请你跟我一起证明。"

    if affection >= 3:
        narrator "她伸出拳头。王不稳愣了半秒，才和她轻轻碰了一下。"
        show xuwanqing happy
    else:
        narrator "她抬起手，似乎想伸出拳头，最后只是把被风吹乱的头发别到耳后。"
        xw "方案还没做完。先回去吧。"
        wbw "好。"

    return


# ─────────────────────────────────────────────────────────────
# 04. 原稿：【新增剧情 · 伞下的距离】
# 接入：第三章 menu（选择 07）结束后、jump chapter_04 之前
# 条件：affection >= 8 使用 cg v21_xuwanqing_rain_close 并播放完整近距离版；
#       低值共用雨伞但保持距离，不播放 CG。
# ─────────────────────────────────────────────────────────────
label v21_chapter_03:
    scene bg v21_time_company_street_rain with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "散场时突然下起暴雨。许晚晴站在门口，打开一把只能勉强容下两人的折叠伞。"
    xw "走不走？再等地铁末班就没了。"
    wbw "你的伞有点小。"
    xw "嫌小就淋着。"

    if affection >= 8:
        scene cg v21_xuwanqing_rain_close with dissolve
        narrator "他走进伞下，肩膀不可避免地与她碰在一起。细密的雨滴顺着伞骨滴落，在两人鞋尖前溅成一圈圈碎光。"
        narrator "一辆电动车从身侧驶过，王不稳下意识把她拉向内侧。许晚晴扶住他的手臂，抬起头，鼻尖几乎碰到他的衣领。"
        xw "你心跳很快。"
        wbw "刚才车开得快。"
        xw "我说的是现在。"
        narrator "两人沉默着走完了那条街。临分别时，她替他把被雨打湿的领口理平，手指停留了短短一瞬。"
        xw "王不稳，别总让别人猜。想关心谁，就说出来。"
        wbw "那你呢？"
        xw "我已经说得够明显了。"
    else:
        narrator "他走进伞下，尽量把肩膀收在伞骨以内。雨点还是打湿了外侧的袖口。"
        narrator "一辆电动车从身侧驶过，王不稳往旁边让了一步，抬手示意她注意脚下。"
        xw "谢谢。"
        wbw "路滑，走里面。"
        narrator "两人沿着街边走到地铁口。她把伞往他那边偏了一点，又在进站前收回。"
        xw "王不稳，别总让别人猜。想关心谁，就说出来。"
        wbw "……我尽量。"
        xw "明天还要对数据。早点回去。"
        narrator "她说完便转身走向另一侧出口，没有再多留一步。"

    return


# ─────────────────────────────────────────────────────────────
# 05. 原稿：【新增剧情 · 失去的署名】
# 接入：第四章证据整理段之后、jump chapter_05 之前
# 条件：affection >= 8 播放原稿的并肩与手部相碰；低值保留共同取证、
#       删除身体接触。
# ─────────────────────────────────────────────────────────────
label v21_chapter_04:
    scene bg office_night with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "当天晚上，王不稳再次点开张浩发到群里的汇报文件，确认自己的名字确实从封面和修订记录摘要里消失了。"
    narrator "他没有立刻点击发送键。冷静不代表不委屈，只是他知道没有证据的愤怒会更快消耗自己。"
    narrator "许晚晴坐到他旁边，递来一只纸杯。咖啡已经凉了。"

    if affection >= 8:
        show xuwanqing serious
        xw "你不用在我面前装作无所谓。"
        wbw "我不想让你觉得我很狼狈。"
        xw "你以为我喜欢的是个永远不会出错的人？"
        narrator "她抽出笔，在白纸上写下“原始数据”“讨论纪要”“审批链”“交付节点”。"
        xw "你负责还原事实。我负责证明这些事实确实发生过。我们是同一组，不是吗？"
        wbw "嗯。"
        narrator "凌晨两点，空荡的办公室里只剩两台电脑的光。他们的手偶尔在鼠标旁相碰，再若无其事地移开。"
    else:
        show xuwanqing normal
        xw "文件名我核过了。署名确实被删了。"
        wbw "我留了原始版本。"
        xw "那就按证据走。你整理时间线，我核对审批链。"
        wbw "好。"
        narrator "她抽出笔，在白纸上写下“原始数据”“讨论纪要”“审批链”“交付节点”，把纸推到他面前。"
        xw "明天先交事实，不交情绪。"
        wbw "明白。"
        narrator "凌晨两点，空荡的办公室里只剩两台电脑的光。他们各自守着一份记录，偶尔交换一句确认，没有再谈委屈。"

    return


# ─────────────────────────────────────────────────────────────
# 06. 原稿：【新增剧情 · 胜利不是终点】
# 接入：第五章天台对话结束后、jump chapter_06 之前
# 条件：affection >= 15 保留牵手与“顺便站你这边”；低值只保留职业互助
#       和克制收束。
# ─────────────────────────────────────────────────────────────
label v21_chapter_05:
    scene bg company_street_night with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "复盘会后，王不稳被单独留下。王磊承认流程有漏洞，也承诺重新核定项目署名，却没有一句正式道歉。"
    narrator "这不是电影里的大获全胜。张浩仍坐在原来的工位，客户也仍要求周五前完成补救。"
    narrator "许晚晴在楼下等他，手里拿着两罐刚从自动售货机取出的苏打水。"
    xw "你现在开心吗？"
    wbw "说不上。只是觉得应该做的事做完了。"
    xw "这就够了。剩下的交给时间。"

    if affection >= 15:
        narrator "她靠近时，一缕发丝擦过他的手背。王不稳这次没有避开，而是轻轻握住她拿着饮料的手。"
        wbw "谢谢你站在我这边。"
        xw "我站在事实那边。"
        narrator "她嘴上说得干脆，却没有把手抽走。"
        show xuwanqing happy
        xw "……当然，也顺便站你这边。"
    else:
        narrator "她把另一罐苏打水递给他，拉环已经替他打开。"
        wbw "谢谢。"
        xw "我站在事实那边。"
        wbw "我知道。"
        xw "明天客户那边还要收尾。"
        narrator "两人站在自动售货机旁把水喝完。她没有问更多，他也没有把疲惫说成胜利。"
        show xuwanqing normal
        xw "回去把复盘写完。别再一个人扛到凌晨。"
        wbw "你也是。"

    return


# ─────────────────────────────────────────────────────────────
# 07. 原稿：【新增剧情 · 三封未发出的消息】
# 接入：第六章“那就看远一点。”之后、最终 menu（选择 10）之前
# 条件：affection >= 15 保留“我们以后还有没有可能”的关系问句；
#       低值不提出关系确认，只保留选择前的克制对话。
# ─────────────────────────────────────────────────────────────
label v21_chapter_06:
    scene bg bedroom_night with fade
    show wangbuwen normal
    show xuwanqing normal

    narrator "桌上的三个选项，没有一个能保证未来。公司转正意味着熟悉的机会与限制；更大的平台意味着离开；项目企划则可能让他失去已经攒下的一切。"
    narrator "王不稳打开与许晚晴的聊天框，打下“你会希望我留下吗”，又逐字删掉。"
    narrator "许晚晴看见他的动作，直接把手机推回去。"
    xw "别让我替你选人生。要是以后不开心，你就会把今天的心软当成遗憾。"
    wbw "那如果我走了？"
    xw "我会难过。但那是我需要面对的事，不是绑住你的理由。"
    narrator "两人隔着一张狭小书桌相望。灯光落在她的眼睫上，让她难得显出一丝不设防的疲倦。"

    if affection >= 15:
        wbw "我想，无论选哪一条，都认真问你一句：我们以后，还有没有可能？"
        xw "这个问题，你可以等做完选择，再当面问我一次。"
        show xuwanqing happy
        narrator "她没有催他，只把桌上的三份文件重新摆正。"
    else:
        wbw "……我会认真选。"
        xw "好。选完再告诉我。"
        show xuwanqing serious
        narrator "王不稳把手机扣在桌上，没有重新输入那句已经删掉的问题。两人只继续讨论三条路各自的代价。"
        narrator "窗外的车流声盖过了短暂的沉默。"

    return


# ─────────────────────────────────────────────────────────────
# 08. 原稿：【新增后日谈 · 稳定线】
# 接入：ending_stable 条件分支结束后、结局持久化记录写入之前
# 条件：沿用原有理想条件 ability >= 7 and affection >= 15；
#       否则播放普通版，不确认牵手。
# ─────────────────────────────────────────────────────────────
label v21_ending_stable:
    scene bg v21_time_company_street_dusk with fade
    show wangbuwen normal
    show xuwanqing normal

    if ability >= 7 and affection >= 15:
        narrator "转正后的第一个周五，王不稳比约定早到了十五分钟。他在餐厅门口练习过两次开场白，最终一个字也没记住。"
        show xuwanqing happy
        xw "你在背什么？"
        wbw "菜单。"
        xw "菜单拿反了。"
        narrator "她握住他的手，笑得眼睛弯起。繁忙的城市仍然没有为任何人停下脚步，但这一次，他们不用独自穿过人潮。"
    else:
        narrator "转正后的第一个周五，他们约在公司附近的小餐馆。王不稳提前到了，把菜单看了两遍。"
        xw "你到得挺早。"
        wbw "怕排队。"
        xw "这家店我常来。招牌菜不难吃。"
        narrator "他们聊项目、聊转正后的排班，也聊哪条地铁线晚上更挤。关系没有突然越过什么，但下一次见面已经约在了下周五。"
        show xuwanqing happy
        xw "下次你请。"
        wbw "好。"

    return


# ─────────────────────────────────────────────────────────────
# 09. 原稿：【新增后日谈 · 上升线】
# 接入：ending_rising 条件分支结束后、结局持久化记录写入之前
# 条件：沿用原有理想条件 ability >= 9 and affection >= 12；
#       理想版同车，普通版异地；普通版只约下次吃饭，不确认约会关系。
# ─────────────────────────────────────────────────────────────
label v21_ending_rising:
    scene bg v21_train_interior_dusk with fade
    show wangbuwen normal

    if ability >= 9 and affection >= 12:
        show xuwanqing normal
        narrator "启程后，两人并排坐在同一节车厢。窗外的站台向后退去，黄昏把座椅染成暖色。"
        narrator "王不稳收到一条消息：到了以后，发一张你窗外的照片。发送人是许晚晴。"
        wbw "你就坐我旁边。"
        show xuwanqing happy
        xw "先练习一下异地也适用的沟通方式。"
        narrator "他对着车窗拍下远去的站台，想了想，又补上另一句。"
        wbw "到站以后，我想认真和你约会。"
        xw "可以。不过先陪我去看房子，约会排在后面。"
        narrator "消息发出的一刻，他第一次觉得远方并不只意味着分别。"
    else:
        narrator "启程后，王不稳独自坐在车厢里。窗外的站台向后退去，黄昏把空着的邻座照得很亮。"
        narrator "手机震了一下：到了以后，发一张你窗外的照片。发送人是许晚晴。"
        narrator "他对着车窗拍下远去的站台，想了想，又补上另一句。"
        wbw "下次见面，我请你吃饭。到时候再听你说说最近的事。"
        narrator "消息发出的一刻，他第一次觉得远方并不只意味着分别。"
        narrator "她回：好。别挑太贵的店。"

    return


# ─────────────────────────────────────────────────────────────
# 10. 原稿：【新增后日谈 · 创业线】
# 接入：ending_startup 条件分支结束后、结局持久化记录写入之前
# 条件：沿用原有理想条件 side_project_ready and ability >= 8 and
#       affection >= 15 and money >= 1800；普通版明确“晚了几个月才上线”。
# ─────────────────────────────────────────────────────────────
label v21_ending_startup:
    scene bg v21_time_startup_morning with fade
    show wangbuwen normal
    show xuwanqing normal

    if side_project_ready and ability >= 8 and affection >= 15 and money >= 1800:
        narrator "第一个版本上线时，服务器连续报警三次。两人并肩修到天亮，最后一条错误日志消失，许晚晴累得靠在他肩上。"
        show xuwanqing happy
        xw "我现在怀疑你当初是在骗我来打工。"
        wbw "你可以辞职。"
        xw "不辞。还有，等用户破一千，你得带我出去约会。不能带电脑。"
        narrator "王不稳将这句要求写进项目里程碑，优先级标成最高。"
    else:
        narrator "第一个版本比原计划晚了几个月才上线。服务器仍然连续报警，两人修到天亮，最后一条错误日志终于消失。"
        narrator "许晚晴没有靠过来，只把椅子往后一推，长长地呼出一口气。"
        xw "我现在怀疑你当初是在骗我来打工。"
        wbw "你可以辞职。"
        xw "不辞。还有，等用户破一千，你得请我吃顿饭。不能带电脑。"
        wbw "记下了。"
        narrator "王不稳将这条要求写进项目里程碑，优先级标成最高。"
        narrator "窗外天已经亮了。第一个版本迟到了几个月，但总算真正上线。"

    return


# ─────────────────────────────────────────────────────────────
# 11. 原稿：【新增剧情 · 失效的钟】
# 接入：穿越序章最后一句王不稳内心独白之后、jump sequel_chapter_01 之前
# 说明：镜面提示与银铃首次出现；其同源含义在冬之章回收。
# ─────────────────────────────────────────────────────────────
label v21_sequel_prologue:
    scene bg v21_old_house_mirror with fade
    show wangbuwen normal

    narrator "旧宅的走廊有一面全身镜。王不稳把行李搬进去时，镜中的自己比现实里的动作慢了半秒。"
    wbw "错觉？"
    narrator "他抬手、停顿、再抬手。第三次，倒影先于他做出了动作。"
    show screen v21_mirror_caption("请不要独自记住")
    narrator "镜面上浮出一行浅得几乎看不清的字：请不要独自记住。"
    hide screen v21_mirror_caption
    narrator "字很快消失。他在纸上画出镜子的轮廓，标注时间，并把纸压在床头。"
    narrator "凌晨两点，窗外传来轻轻的敲击声。院门外没有人，白色栅栏上却挂着一枚银色铃铛。"
    narrator "他没有碰铃铛。直到天亮，铃声仍在没有风的屋檐下轻响。"

    return


# ─────────────────────────────────────────────────────────────
# 12. 原稿：【新增剧情 · 四个人的不同距离】
# 接入：初遇章 Dana“跟好。春庭的路可不在你的离线地图里。”之后、
#       jump sequel_chapter_02_spring 之前
# 条件：无。初遇时 dana_affection 仍为 0，不设信任分支；
#       Dana 保持体贴但尊重距离，亲密阈值从春之章起使用。
# ─────────────────────────────────────────────────────────────
label v21_sequel_chapter_01:
    scene bg academy_courtyard with fade
    show wangbuwen normal
    show dana normal

    narrator "去春庭的路上，Dana 一边领路，一边指给他看学园食堂。她说话总是很快，仿佛慢一点，身边的人便会突然消失。"
    dana "你喜欢甜的还是咸的？对了，你有没有忌口？不喜欢太吵的位置也可以告诉我。"
    wbw "我只是来报到，你不用替我安排全部生活。"
    show dana worried
    dana "……习惯了。"
    narrator "她第一次没有立刻接话。"

    show dana normal
    dana "那午饭我就不替你安排了。食堂二楼靠窗，人少一些。你饿了再去，不用勉强。"
    wbw "谢谢。我会自己安排。"
    narrator "Dana 点点头，把还想说的话咽了回去。她仍走在半步之前，只在路口停下时回头确认他有没有跟上。"

    hide dana
    show luna normal
    narrator "Luna 在后面记录异常学籍，发现王不稳鞋底的泥土不属于樱镜町任何常见土层。"
    show irene normal
    irene "同一份记录只留一个副本，等于只留一次被改写的可能。"
    hide luna
    hide irene
    show ruby normal
    narrator "Ruby 静静走在最后。王不稳回头时，她正望向自己被阳光拉长的影子。"
    ruby "还好。你有影子。"
    wbw "没有会怎么样？"
    ruby "有些人来到这里以后，先失去的不是名字。"

    return


# ─────────────────────────────────────────────────────────────
# 13. 原稿：【新增剧情 · 春庭的约定】
# 接入：春之章 Luna 说完“可以。但到了现场，必须遵守我的安全方案。”之后、
#       “夜色落下前，一行人向海边灯塔出发。”之前（仍在 jump 前）
# 条件：Dana 信任 >= 3 保留握手与单独看花的约定；低值保留角色表达，
#       不确认恋情。
# ─────────────────────────────────────────────────────────────
label v21_sequel_chapter_02_spring:
    scene bg v21_time_spring_garden_evening with fade
    show wangbuwen normal
    show dana normal

    narrator "危机解除的傍晚，王不稳回到庭院，发现 Dana 还在一盏盏检查路灯。她双手沾着泥，袖口卷到手肘，和白天笑着迎人的模样判若两人。"
    wbw "不休息？"
    dana "还有二十七份记录要核对。我怕今晚睡一觉，明天又少了一个名字。"
    wbw "我帮你。"
    narrator "他把水桶搬到墙边，把纸质名单按签字顺序排好。Dana 终于停下来，看着两人并排的影子。"
    show dana worried
    dana "你知道吗？我有时候笑得那么大声，是因为我怕大家看不见我也在害怕。"
    wbw "现在我看见了。"

    if dana_affection >= 3:
        show dana normal
        narrator "Dana 伸出沾着泥的手，又有点不好意思地收回。王不稳没有笑话她，只轻轻握住她的指尖。"
        dana "等一切结束，我想和你单独来这里看花。那时候不用数人，也不用确认谁消失了。"
        wbw "约好了。"
    else:
        show dana normal
        narrator "Dana 把手在围裙上擦了擦，没有伸过来。"
        dana "谢谢。剩下的我自己来。"
        wbw "记录可以分我一半。"
        dana "好。那就按签字顺序。"
        narrator "她仍然笑着，但那个笑容不再需要撑给谁看。"
        dana "等一切结束，我想把这里重新种满花。你要是还在，就来帮忙。"
        wbw "我会来。"

    return


# ─────────────────────────────────────────────────────────────
# 14. 原稿：【新增剧情 · 灯塔里的温差】
# 接入：夏之章“但春与夏的两枚碎片仍在黑暗中发光……”之后、
#       jump sequel_chapter_04_autumn 之前
# 条件：动作回忆只读 sequel_luna_observation_outcome
#       （paper_tape / aborted / evacuated / unknown），不由好感推断；
#       收束阶段 Luna 信任 >= 3 才播放软化的亲密表达。
# ─────────────────────────────────────────────────────────────
label v21_sequel_chapter_03_summer:
    scene bg lighthouse_night with fade
    show wangbuwen normal
    show luna normal

    narrator "其他人去收拾仪器后，Luna 仍坐在监测台前。她把湿透的外套挂在椅背，肩膀因为寒冷微微发抖。"
    wbw "再测一次也不会改变已经发生的事。"
    luna "我知道。但如果漏掉一个变量，下次有人会因此受伤。"
    narrator "王不稳把备用毯子放到她肩上。Luna 没有拒绝，却也没有回头。"
    luna "我以前以为，只要数据足够完整，就不需要信任别人。"
    wbw "现在呢？"

    if sequel_luna_observation_outcome == "paper_tape":
        luna "现在我发现，你会在约定的六十秒内主动回来。这个行为比口头保证更可靠。"
        wbw "听上去像一份测试报告。"
        luna "对你而言，这是很高的评价。"
    elif sequel_luna_observation_outcome == "aborted":
        luna "现在我发现，你会在判断失误后服从现场方案。至少下一次，我还能把后背交给你。"
        wbw "这个评价听起来不太像表扬。"
        luna "是记录。也是我暂时能给出的信任。"
    elif sequel_luna_observation_outcome == "evacuated":
        luna "现在我发现，你把人员撤离放在设备之前。这个顺序正确。"
        wbw "数据可以重做。"
        luna "人不行。这个结论我同意。"
    else:
        luna "现在我发现，你至少会听我把话说完。先保持这个标准。"
        wbw "听上去门槛不高。"
        luna "那就从能验证的部分开始。"

    if luna_affection >= 3:
        narrator "灯塔外的夏潮终于恢复正常。Luna 抬头与他对视，认真补上一句。"
        show luna soft
        luna "另外，我也很高兴你回来。这个结论不需要更多样本。"
    else:
        narrator "灯塔外的夏潮终于恢复正常。Luna 把毯子往上拉了拉。"
        show luna normal
        luna "另外，今晚谢谢你留下来收尾。明天九点，观测站重新校准。"
        wbw "我会到。"
        narrator "她没有再说多余的话。"

    return


# ─────────────────────────────────────────────────────────────
# 15. 原稿：【新增剧情 · 秋日未寄出的信】
# 接入：秋之章取得秋之碎片（autumn_fragment = True）并重新显示档案馆场景之后、
#       Irene 说“最后一页只记了一个称谓：冬之承载者。”之前；
#       即“Ruby 只剩一夜”警告之前，保留一小段休息。
# 条件：Irene 信任 >= 3 保留靠肩与玩笑；低值保留角色表达，
#       以共同归档收束，不确认恋情。
# ─────────────────────────────────────────────────────────────
label v21_sequel_chapter_04_autumn:
    scene bg v21_time_archive_evening with fade
    show wangbuwen normal
    show irene normal

    narrator "档案公开后，Irene 独自留下整理散乱的纸页。她打开一个封存了十二年的盒子，里面有一封写给母亲却从未寄出的信。"
    show irene shaken
    irene "我已经记不清她的声音了。连这封信是谁教我写的，也不确定。"
    wbw "你可以不告诉我。"
    irene "我想告诉你。只是以前没有人问过，我自己愿不愿意说。"
    narrator "王不稳坐到她身旁，没有去碰那封泛黄的纸。"
    irene "我一直告诉自己，成熟就是替别人决定，再独自承担后果。听上去很可靠，对吧？"
    wbw "听上去很孤独。"

    if irene_affection >= 3:
        narrator "Irene 沉默了许久，忽然靠过来，把额头轻轻抵在他的肩头。"
        irene "就一分钟。档案馆助理偶尔也会累。"
        wbw "时间到了我会提醒你。"
        irene "……你要是敢真的计时，我就把你的借阅证停掉。"
        show irene relieved
        narrator "两个人都笑了。这是王不稳第一次见她笑得毫无防备。"
    else:
        narrator "Irene 沉默了很久，最后把信重新折好，放进一只标着日期的档案袋。"
        wbw "信要放回原处吗？"
        irene "不。既然拿出来了，就给它一个能被找到的位置。"
        narrator "她第一次没有把疲惫藏进工作流程里。两人并肩把散乱的纸页按年份归档，直到闭馆灯亮起。"
        irene "开放档案还要继续整理。你如果来，我会给你留一副手套。"
        wbw "好。"
        show irene relieved

    return


# ─────────────────────────────────────────────────────────────
# 16. 原稿：【新增剧情 · Ruby 的真心】
# 接入：冬之章“那就去把规则改掉。”之后、jump sequel_finale 之前
# 条件：Ruby 信任 >= 3 才摘耳坠、播放脸颊吻（立绘与文字，不用 CG），
#       吻后把耳坠递还并戴好；低值保留角色表达，不摘耳坠、不确认恋情。
# 回收：本段明确旧宅镜面与银铃都是四季镜提醒众人共同保存记忆的信号；
#       银铃不是水晶耳坠，不新增另一套魔法设定。
# ─────────────────────────────────────────────────────────────
label v21_sequel_chapter_05_winter:
    scene bg sakurakagami_station_winter with fade
    show wangbuwen normal
    show ruby normal

    narrator "Ruby 把先前取下的水晶耳坠重新戴回耳边，听着广播里仍在延续的姓名。"
    narrator "通向镜室的门出现后，其他人先行检查阶梯。Ruby 却留在站台，注视着玻璃上自己刚刚写下的名字。"
    ruby "我第一次看见你的时候，其实很害怕。"
    wbw "怕我？"
    ruby "怕你和以前那些人一样，最后只会把我当作需要拯救的东西。"
    narrator "王不稳想起旧宅走廊那面慢半拍的镜子，也想起站台玻璃上刚刚恢复的名字。"
    wbw "旧宅的镜子和这里的门，是同一面四季镜投出的信号？"
    ruby "是。银铃也是。铃响不是在挑选新的承载者，只是在提醒所有人：不要独自记住。"
    wbw "那银铃和你的耳坠……"
    ruby "不是同一件东西。耳坠保存名字，银铃只负责提醒。它们都来自四季镜，不是另一套规则。铃响一次，就是镜在问，有没有人愿意一起记住。"

    if ruby_affection >= 3:
        narrator "她把水晶耳坠摘下来，放进他手心。没有耳坠遮挡，她的耳朵被冬夜冻得微红。"
        show ruby resolute
        ruby "我不是因为能听见镜的声音才值得留下。我也会嫉妒，会任性，会想在下雪的夜里被人牵着手走回家。"
        wbw "那是你本来就可以拥有的生活。"
        ruby "如果你留下，能不能偶尔只陪我，不谈拯救世界？"
        wbw "能。"
        narrator "Ruby 踮起脚，在他脸颊上落下一个很轻的吻，随即退开半步。"
        ruby "那这个，不算冬之承载者的谢礼。只是 Ruby 自己想做。"
        narrator "王不稳把水晶耳坠递还给她。Ruby 接过去，重新戴好，水晶在冬夜里轻轻响了一声。"
    else:
        show ruby resolute
        ruby "我不是因为能听见镜的声音才值得留下。我也会嫉妒，会任性，会想在下雪的夜里被人记住。"
        wbw "那是你本来就可以拥有的生活。"
        narrator "Ruby 抬手碰了碰耳坠，最终没有摘下来。"
        ruby "这个先放在我这里。等我确认自己不是一时害怕，再决定要不要交给你。"
        wbw "好。"
        ruby "如果你留下，能不能偶尔只陪我走一段路，不谈拯救世界？"
        wbw "能。"
        ruby "那先记住这句话。别急着证明。"
        narrator "她抬手把耳坠扶正，玻璃上的名字仍清晰。两个人隔着半步的距离，一起看向通往镜室的门。"

    return


# ─────────────────────────────────────────────────────────────
# 17. 原稿：【新增剧情 · 最后的独处】
# 接入：镜室终章“裂纹间开始推演几条仍可执行的道路。”之后、
#       最终 menu（选择 12）之前
# 条件：四位角色各自在对应信任 >= 3 时使用原稿表达；
#       低值使用不确认恋情的克制版。
# ─────────────────────────────────────────────────────────────
label v21_sequel_finale:
    scene bg mirror_chamber with fade
    show wangbuwen normal

    narrator "镜面推演停止的间隙，四人依次走到王不稳身边。她们不再以承载者的身份请求保护，而是各自陈述想要的未来。"

    show dana normal
    if dana_affection >= 3:
        dana "我想把春庭修成真正的花园。你来不来都可以，但我希望你知道我会在那里。"
    else:
        dana "春庭的修复计划不会停。你要是还留在镇上，欢迎来帮忙。"
    hide dana

    show luna normal
    if luna_affection >= 3:
        show luna soft
        luna "我会继续记录世界的异常。不过，如果有人愿意和我一起确认日出时间，我不会再把它视作无效变量。"
    else:
        luna "我会继续记录世界的异常。观测站欢迎任何愿意按流程复核的人。"
    hide luna

    show irene normal
    if irene_affection >= 3:
        show irene relieved
        irene "档案会被公开，我也想学着为自己保留一些私人时间。也许还有一个愿意听我说废话的人。"
    else:
        irene "档案会被公开。我也会保留必要的个人时间，这一点不需要再向谁申请。"
    hide irene

    show ruby normal
    if ruby_affection >= 3:
        ruby "我想每年都写信。不管我们相隔多远，都让彼此知道，今天我仍然是我。"
    else:
        ruby "我会继续替需要被记住的人保存来信。每一封都会留下可查的日期。"
    hide ruby

    narrator "王不稳意识到，任何选择都不该把某个人变成奖品。真正值得珍惜的，是她们各自完整的生活，与彼此自愿靠近的机会。"

    return


# ─────────────────────────────────────────────────────────────
# 18. 原稿：【新增后日谈 · Dana 线】
# 接入：sequel_ending_dana 最终叙述之后、结局 marker
#       “——Dana 结局《春日归邻》”之前
# 条件：该结局入口已要求 dana_affection >= 3；此处播放完整后日谈。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_dana:
    scene bg v21_time_spring_garden_evening with fade
    show wangbuwen normal
    show dana normal

    narrator "春日庆典收摊后，Dana 把写着“明年也要见面”的纸卡偷偷塞进王不稳口袋。"
    wbw "不用偷放。你可以直接说。"
    dana "那我就说了。我想明年、后年，以后每年都和你一起种花。"
    narrator "他牵住她的手。暖风经过新栽的枝叶，两人都没有急着松开。"

    return


# ─────────────────────────────────────────────────────────────
# 19. 原稿：【新增后日谈 · Luna 线】
# 接入：sequel_ending_luna 最终叙述之后、结局 marker
#       “——Luna 结局《盛夏坐标》”之前
# 条件：该结局入口已要求 luna_affection >= 3；此处播放完整后日谈。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_luna:
    scene bg v21_time_lighthouse_dawn with fade
    show wangbuwen normal
    show luna soft

    narrator "观测站第一次开放夜间参观，工作终于在凌晨结束。Luna 把仪器关掉，主动靠近王不稳。"
    luna "今晚我没有安排额外实验。"
    wbw "那安排什么？"
    luna "一场约会。从这里开始，走到太阳升起来。"
    narrator "她伸出手，像提出一项经过周密考虑、却仍有些紧张的请求。"
    narrator "王不稳握住她的手。海风从灯塔外吹进来，天边已经有一点发白。"

    return


# ─────────────────────────────────────────────────────────────
# 20. 原稿：【新增后日谈 · Irene 线】
# 接入：sequel_ending_irene 最终叙述之后、结局 marker
#       “——Irene 结局《秋实之书》”之前
# 条件：该结局入口已要求 irene_affection >= 3；此处播放完整后日谈。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_irene:
    scene bg v21_time_archive_night with fade
    show wangbuwen normal
    show irene normal

    narrator "档案馆闭馆后的灯光比白天柔和。Irene 把一份空白表格推给王不稳，上面写着“私人时间安排”。"
    wbw "需要签字吗？"
    irene "不需要审批。我只是想知道，你明晚愿不愿意陪我去看红叶。"
    show irene relieved
    narrator "他说愿意。Irene 难得没有追问依据，只轻轻吻了他的额头。"

    return


# ─────────────────────────────────────────────────────────────
# 21. 原稿：【新增后日谈 · Ruby 线】
# 接入：sequel_ending_ruby 最终叙述之后、结局 marker
#       “——Ruby 结局《冬夜来信》”之前
# 条件：该结局入口已要求 ruby_affection >= 3；专属 CG
#       cg v21_ruby_ending_kiss 只用于本结局的唇吻。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_ruby:
    scene bg v21_time_station_first_snow with fade
    show wangbuwen normal
    show ruby normal

    narrator "初雪夜，Ruby 把那封没有邮戳的信收进怀里，伸手勾住王不稳的小指。"
    ruby "现在这个瞬间，也会被镜子记录吗？"
    wbw "可能会。"
    ruby "那我想留下一个只有我们知道的版本。"
    scene cg v21_ruby_ending_kiss with dissolve
    narrator "她靠近他，轻轻吻了吻他的唇。"
    narrator "远处的站钟重新开始走动，没有任何人因此被遗忘。"

    return


# ─────────────────────────────────────────────────────────────
# 22. 原稿：【新增后日谈 · 返回现实线】
# 接入：sequel_ending_return 最终叙述之后、结局 marker
#       “——返回结局《回到灯火》”之前
# 条件：无信任门槛；邮件只作为未证实线索，不开启真结局。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_return:
    scene bg city_anomaly with fade
    show wangbuwen normal

    narrator "后来王不稳把樱镜町的故事写成了一本小说，却始终没有公开那几张字迹不同的姓名卡。"
    narrator "某个雨夜，他收到一封没有发件地址的邮件。正文只有四个字：春天见面。"
    narrator "邮件没有可验证的邮戳。它不能证明门再次打开，只能证明有人还记得那个约定。"
    narrator "他望向窗外，第一次没有急着解释一切，只安静地把信保存下来，并在文件夹上写下“未证实”。"

    return


# ─────────────────────────────────────────────────────────────
# 23. 原稿：【新增后日谈 · 真结局】
# 接入：sequel_ending_true 最终叙述之后、结局 marker
#       “——真结局《四季同在》”之前
# 条件：门只在四季交界、双方同时发出邀请时回应；本后日谈承接
#       四碎片、四位信任 >= 3、洞察 >= 6、共同意志 >= 4 的真结局。
# ─────────────────────────────────────────────────────────────
label v21_sequel_ending_true:
    scene bg v21_time_station_boundary with fade
    show wangbuwen normal

    narrator "重逢的当天，五人在车站旁开了一场小小的欢迎会。没有仪式，也没有拯救世界的任务，只有热茶、点心和对彼此近况的追问。"
    narrator "这一天正好是四季交界。门没有主动抓住任何人，只回应了两边同时发出的邀请。"
    show dana normal
    dana "这次你要住多久？"
    wbw "先住到下个节日。"
    hide dana
    show luna normal
    luna "期限不明确。"
    hide luna
    show irene normal
    irene "别审问他。门不会强迫谁留下。"
    irene "下个四季交界，两边都可以再发出邀请。"
    hide irene
    show ruby normal
    ruby "那就慢慢决定。"
    hide ruby
    narrator "王不稳把曾写着“三个月，留下来”的笔记翻到新的一页。他没有再写期限，只写下五个人的名字，以及一句话：今天，我们都在。"

    return
