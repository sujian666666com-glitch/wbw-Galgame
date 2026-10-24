label sequel_prologue:
    $ story_arc = "sequel"
    $ sequel_chapter_progress = 0
    $ notify_change("续篇进度：穿越序章")

    scene bg city_anomaly with fade
    show wangbuwen normal

    narrator "那三个月之后，王不稳为自己的选择走了整整两年。"

    if sequel_origin_ending == "stable":
        narrator "他留在最初的公司，从实习生变成了能够独立负责项目的人。"
        narrator "熟悉的办公室没有让他停下，他仍旧把每一次判断和结果记进那本旧笔记。"
    elif sequel_origin_ending == "rising":
        narrator "他去了更大的城市，也站上了更高的平台。"
        narrator "新的节奏更快，要求更高，但他已经学会在压力里找出下一步。"
    elif sequel_origin_ending == "startup":
        narrator "他把第一版产品做了出来，随后是第二版、第三版。"
        narrator "创业没有让生活变得轻松，却让每一次成败都真正属于自己。"
    else:
        narrator "有人选择留下，有人选择远行，也有人从零开始。"
        narrator "无论那时走上哪条路，王不稳都已经学会为自己的决定负责。"

    narrator "这天深夜，他结束工作，独自走过一条刚下过雨的街。"
    narrator "霓虹映在柏油路面上，像两年前第一次来到大城市的那个傍晚。"
    wbw "（内心）又下雨了。"
    narrator "他下意识摸了摸随身的笔记本。封面已经磨旧，里面那行字仍然清楚。"
    wbw "（内心）三个月，留下来。"
    narrator "街道尽头忽然亮起一团银白色的光。"
    narrator "它不像车灯，也不像广告牌，更像一面被风吹皱的镜子，把四种不属于同一时节的颜色叠在一起。"
    wbw "什么东西……"
    narrator "他没有贸然靠近，而是拿出手机，先拍下光芒出现的位置和时间。"
    narrator "照片刚刚保存，屏幕上的街道便开始扭曲。"
    narrator "春花从积水里盛开，盛夏的海潮声越过高楼，枯叶贴着路面旋转，雪落在他的肩上。"
    wbw "四个季节？"
    narrator "银光猛然扩散。建筑、路灯和脚下的地面像被擦去的铅笔线，依次消失。"
    narrator "王不稳后退一步，鞋底却没有碰到地面。"
    wbw "这是——"

    scene bg sakurakagami_station_rain with fade

    narrator "黑暗之后，先回来的是雨声。"
    narrator "王不稳睁开眼，发现自己站在一座老旧车站的屋檐下。"
    narrator "没有高楼，没有霓虹。昏黄路灯照着窄窄的站前路，远处传来海浪声。"
    narrator "手机没有网络，时间停在银光吞没街道的那一分钟。"
    narrator "他的脚边却多出一只从未见过的深色行李箱。"
    wbw "不是我的。"
    narrator "箱锁没有密码，轻轻一拨便开了。里面是合身的衣物、旧宅钥匙和一个印着樱花镜纹的文件袋。"

    menu:
        "面对来历不明的行李，王不稳决定——"

        "逐项核对文件、日期和签名。":
            $ sequel_insight += 1
            $ notify_change("洞察 +1")
            narrator "他先拍下箱内原状，再按文件顺序逐页检查。"
            narrator "录取通知、租约和学籍回执的签发日期完全相同——都在三个月前。"
            narrator "三份文件上的签名都像他的字，却在落笔习惯上差了同一个细节。"
            wbw "有人知道我的名字，也见过我的字，但这个人不是我。"

        "先确认住处，避免继续淋雨。":
            narrator "他没有久留，只把文件摊开拍照，再收进贴身的背包。"
            wbw "先找到一个能关门的地方，再慢慢核对。"

    narrator "文件最上方写着：樱镜学园大学部，二十二岁转入生，王不稳。"
    narrator "租约上的地址与录取材料一致，签名却依旧像一份刻意临摹的赝品。"
    narrator "手机虽然没有信号，地图应用里却预先缓存了车站到旧宅区的离线路线。"
    wbw "行李、住处、学籍、地图……这里早就替我准备好了身份。"
    narrator "他把这个判断记进手机备忘录，没有把它当成事实，只标成了待验证。"

    show ruby normal

    narrator "雨幕里，一名银白色低双马尾的女孩撑伞走来。"
    narrator "她在看见行李箱上的樱花镜纹时，脚步明显停了一瞬。"
    ruby "你在找旧宅区吗？"
    wbw "你怎么知道？"
    ruby "这个时间来到车站，又带着那里的钥匙……不难猜。"
    narrator "她的语气很轻，红棕色的眼睛却始终没有离开那只陌生行李箱。"
    wbw "往哪边走？"
    ruby "沿着站前路直走，第二个路口左转。最里面那栋有白色栅栏。"
    wbw "谢谢。你叫什么？"
    ruby "Ruby。"
    narrator "她说出名字时，车站玻璃上的倒影迟了半拍。"
    wbw "王不稳。"
    ruby "……我知道。"
    narrator "Ruby 像是说漏了什么，立刻垂下目光。"
    ruby "录取材料上写着。明天你会去学园，对吧？"
    wbw "如果那份材料是真的。"
    ruby "那就明天见。今晚别在车站停太久。"
    wbw "为什么？"
    ruby "这里的雨，会让人忘记刚才看见的东西。"
    narrator "她没有继续解释，转身走进雨里。"
    narrator "王不稳看着她远去，又看了一眼手机中刚拍下的文件。照片仍在。"
    wbw "（内心）先验证身份，再弄清楚她为什么认识我。"

    jump sequel_chapter_01
