label chapter_06:
    $ chapter_progress = 6
    $ notify_change("章节进度：第六章")

    scene bg bedroom_night with fade

    narrator "傍晚，桌上摊着三样东西：公司发的转正通知、另一家公司的 offer 邮件、自己的项目企划书。"
    narrator "门响了，许晚晴站在门外。"

    xw "听说你在纠结？"

    wbw "你怎么知道的。"

    xw "猜的。你这几天眉头都没松开过。"

    narrator "她走进来，看到桌上的三样东西，没有说话。"

    xw "你不用考虑我。这是你的选择。"

    wbw "我知道。"

    xw "那你纠结什么？"

    wbw "……我在想，哪条路能看到更远的地方。"

    xw "那就看远一点。"

    menu:
        "签下公司的转正通知。":
            $ ending_route = "stable"
            jump ending_stable

        "接受另一家公司的 offer。":
            $ ending_route = "rising"
            jump ending_rising

        "拿起自己的项目企划书。":
            $ ending_route = "startup"
            $ side_project_ready = True
            $ notify_change("副业项目企划已准备就绪")
            jump ending_startup
