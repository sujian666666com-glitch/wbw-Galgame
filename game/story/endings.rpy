label ending_stable:
    scene bg company_entrance_morning

    narrator "王不稳签了转正合同，走出会议室。许晚晴站在走廊尽头，看到他出来。"

    xw "定了？"

    wbw "定了。"

    xw "不后悔？"

    wbw "不后悔。"

    narrator "他走到她面前，停了一步的距离。"

    wbw "许晚晴。"

    xw "嗯？"

    if ability >= 7 and affection >= 15:
        wbw "下班一起吃饭？不是 AA。"

        narrator "许晚晴愣了一秒，然后笑了。"

        xw "你终于开窍了。"

        narrator "三个月后，王不稳留在了这座城市，也终于说出了那个早已藏不住的邀请。"
    else:
        wbw "下班一起吃饭？我请。"

        xw "行。庆祝你顺利转正。"

        narrator "他们并肩走向办公区。前路稳定，关系也在不急不缓地靠近。"

    call v21_ending_stable

    $ persistent.old_ending_route = "stable"
    if "stable" not in persistent.old_endings_seen:
        $ persistent.old_endings_seen = persistent.old_endings_seen + ["stable"]
    $ renpy.save_persistent()

    return


label ending_rising:
    scene bg train_platform

    narrator "王不稳接受了另一家公司的 offer，要去一个更大的城市。"

    xw "你真的要去？"

    wbw "嗯。"

    xw "那……什么时候走？"

    wbw "下周。"

    narrator "沉默了几秒。"

    xw "就你自己去？"

    wbw "……你呢？"

    if ability >= 9 and affection >= 12:
        xw "我没说我不去。"

        wbw "……"

        xw "我投了那边的公司，下周也有面试。"

        wbw "你什么时候投的？"

        xw "比你早三天。"

        narrator "王不稳看着她，说不出话。"

        xw "你以为就你有野心？走吧，一起。"

        narrator "列车进站时，他们看向同一座更大的城市，也看见了更远的未来。"
    else:
        xw "我暂时不去。不过，你到了那边别松懈。"

        wbw "不会。"

        xw "等你站稳了，记得告诉我。"

        narrator "列车进站。王不稳独自出发，但他们都知道，这不是告别。"

    call v21_ending_rising

    $ persistent.old_ending_route = "rising"
    if "rising" not in persistent.old_endings_seen:
        $ persistent.old_endings_seen = persistent.old_endings_seen + ["rising"]
    $ renpy.save_persistent()

    return


label ending_startup:
    scene bg startup_studio

    narrator "这是一间比出租屋大不了多少的工作室。两台电脑，一块白板，上面写满了方案。"
    narrator "王不稳拿起了企划书。"

    xw "你想好了？"

    wbw "没有。但先干了再说。"

    xw "……真够鲁莽的。"

    wbw "你不也在这吗？"

    xw "我在这是因为这个项目有前景，不是因为你在。"

    wbw "……那你为什么留到现在？"

    xw "……闭嘴干活。"

    narrator "她转过身，耳根有一点点红。"

    wbw "（内心）也许不稳定，但这是我们自己的路。"

    xw "第一个版本什么时候上线？"

    if side_project_ready and ability >= 8 and affection >= 15 and money >= 1800:
        wbw "明天。"

        xw "那今晚别睡了。"

        wbw "好。"

        xw "咖啡我去买。"

        wbw "AA？"

        xw "滚。"

        narrator "企划、启动资金和并肩的人都已就位。他们的第一个版本如期上线。"
    else:
        wbw "还需要一点时间。"

        xw "那就先把能做的做完。"

        wbw "好。"

        narrator "条件还不算充足，但这间小工作室已经亮起了第一盏灯。"

    call v21_ending_startup

    $ persistent.old_ending_route = "startup"
    if "startup" not in persistent.old_endings_seen:
        $ persistent.old_endings_seen = persistent.old_endings_seen + ["startup"]
    $ renpy.save_persistent()

    return
