label sequel_chapter_04_autumn:
    $ sequel_chapter_progress = 4
    $ notify_change("新篇进度：秋之章")

    scene bg archive_autumn with fade
    show irene normal

    narrator "旧档案馆藏在学园大学部最北侧。窗外的红叶贴着玻璃打转，像一封封没有寄出的信。"
    narrator "Luna 从海灯祭带回的日志摊在桌上。所有被删除的访问记录，都指向同一个账号。"
    luna "账号的最后使用人，是 Irene。"
    irene "准确地说，是十二年前的我。"
    narrator "Irene 摘下黑色耳环，放在一本褪色的学生名册旁。耳环背面刻着一枚细小的秋叶纹。"
    wbw "你十二岁时就经历过一次循环？"
    irene "那一年，小镇连续过了三个秋天。第四次红叶落下时，所有人都忘了我母亲的名字。"
    irene "我成了秋之承载者。镜从我这里拿走一部分记忆，换来其他人继续生活。"
    narrator "她说得平静，手指却一直压着名册里一处被水洇开的空白。"
    irene "后来我当上学生会长，毕业后留在档案馆。不是为了监督谁，而是为了把每一次被改写前的记录留下。"
    wbw "你为什么删掉 Luna 查到的日志？"
    irene "因为被镜认定为知情者的人越多，它能索取的记忆也越多。至少，我一直是这么相信的。"

    menu:
        "面对 Irene 隐瞒的十二年，王不稳决定——"

        "让她把所有经过说完，再逐页核对证据。":
            $ irene_affection += 2
            $ sequel_insight += 1
            $ notify_change("Irene 信任 +2")
            $ notify_change("洞察 +1")
            wbw "先把你的版本说完。然后我们只相信能彼此印证的部分。"
            irene "你不打算先指责我？"
            wbw "指责不能补回缺页。证据可以。"
            narrator "Irene 沉默片刻，把书架最深处的一只铁盒推到桌面中央。"

        "当面指出她没有权力替所有人决定。":
            wbw "不管理由是什么，你都没有权力替所有人决定他们该知道什么。"
            irene "你说得对。但如果再来一次，我当时仍会先阻止更多人被卷进来。"
            narrator "她打开铁盒，却没有再解释自己的伤口。"

    narrator "铁盒里放着四季镜的创始记录。第一页写着镇民熟知的句子：四人献出记忆，四季得以轮转。"
    narrator "Irene 将一张被撕掉的半页拼回去。断口严丝合缝，原句终于完整。"
    irene "四季由众人共同记忆。"
    wbw "后半句从来不是献祭。"
    irene "是后来的人为了方便管理，把全镇的责任集中到了四个承载者身上。应急方案被用久了，就变成了传说。"
    narrator "窗外忽然刮起一阵风。红叶穿过没有打开的窗，悬停在 Irene 身边。"
    irene "镜已经在催我。只要我重新接过秋印，它就会暂时稳定。你也能被送回原来的世界。"

    menu:
        "Irene 准备再次独自承担秋季代价。"

        "拒绝未经本人和众人同意的牺牲。":
            $ irene_affection += 1
            $ sequel_resolve += 1
            $ notify_change("Irene 信任 +1")
            $ notify_change("共同意志 +1")
            wbw "我拒绝的不是你的勇气，是这套从来没有征求过所有人同意的办法。"
            wbw "把档案公开。代价如果真实存在，就让每一个可能承担的人先知道真相。"
            irene "你知道那会有多乱吗？"
            wbw "知道。所以我们一起把它变成能执行的方案。"
            narrator "Irene 看着他，像是第一次允许另一个人站到那扇锁了十二年的门里。"

        "接受她的安排，先让小镇稳定下来。":
            wbw "如果这是眼下风险最低的办法……"
            irene "理性的选择。也是我最不希望再听见的答案。"
            narrator "她拿起秋印，却在触碰之前停住了。Dana、Luna 和 Ruby 已经站在门口。"

    scene cg sequel_irene_archive with dissolve
    narrator "红叶从旧档案的每一道缝隙里涌出。Irene 没有独自握住那枚钥印，而是将创始记录摊开，让所有人看清被撕去的半句话。"
    irene "我隐瞒了十二年。今天起，档案向所有愿意承担后果的人开放。"
    narrator "秋叶纹从她的耳环上脱落，化成一枚温暖的琥珀色碎片。"

    $ autumn_fragment = True
    $ notify_change("获得秋之碎片")

    scene bg archive_autumn with dissolve
    show irene normal
    call v21_sequel_chapter_04_autumn
    scene bg archive_autumn with dissolve
    show irene normal
    irene "最后一页只记了一个称谓：冬之承载者。"
    wbw "Ruby。"
    irene "如果镜开始收回她的名字，我们剩下的时间不会超过一夜。"

    jump sequel_chapter_05_winter
