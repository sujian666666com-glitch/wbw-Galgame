label sequel_ending_dana:
    $ sequel_chapter_progress = 7
    scene bg spring_garden with fade
    scene cg sequel_dana_spring with dissolve

    narrator "王不稳选择成为外来的稳定锚点。通往旧世界的门永久闭合，四季镜停止索取四位承载者的记忆。"
    narrator "一年后，废弃庭院和旧车站被改造成新居民互助站。每一个刚来樱镜町的人，都会先收到一张写有邻居姓名的卡片。"
    dana "哥哥，这次的新住户也迷路了。"
    wbw "你不是已经画了三版地图？"
    dana "地图只能告诉他怎么走，不能让他知道该去找谁呀。"
    narrator "Dana 跑向白栅栏外的陌生人，又在几步后回头，朝王不稳伸出手。"
    dana "一起去。以后每一次见面，我们都一起记住。"
    wbw "好。"
    narrator "她不再用热闹掩饰离别，也不再把留下谁当成自己一个人的责任。春风越过庭院，新的名字落在他们共同翻开的第一页。"
    narrator "——Dana 结局《春日归邻》"
    return


label sequel_ending_luna:
    $ sequel_chapter_progress = 7
    scene bg lighthouse_night with fade
    scene cg sequel_luna_tide with dissolve

    narrator "王不稳选择成为外来的稳定锚点。世界之间的门关闭，樱镜町的异常却第一次成为所有人都能查阅的数据。"
    narrator "Luna 把旧灯塔改造成公开观测站。潮汐、气温、记忆偏差和每一次四季镜波动，都由居民共同验证。"
    luna "三号节点比基准慢了零点七秒。"
    wbw "也可能是你的基准快了。"
    luna "你在质疑我？"
    wbw "我在执行你写的交叉验证制度。"
    narrator "Luna 看了他两秒，嘴角极轻地弯了一下。"
    luna "合格。那就陪我把下一组坐标算完。"
    narrator "海灯在远处逐一亮起。事实不再属于最聪明的那个人，而属于所有愿意检查它的人。两人的未来，也有了共同标记的坐标。"
    narrator "——Luna 结局《盛夏坐标》"
    return


label sequel_ending_irene:
    $ sequel_chapter_progress = 7
    scene bg archive_autumn with fade
    scene cg sequel_irene_archive with dissolve

    narrator "王不稳选择成为外来的稳定锚点。Irene 没有再关上档案馆最深处的门。"
    narrator "一年后，创始记录被放在大厅中央。每一页都有多个保管人，每一次删改都会留下公开痕迹。"
    irene "有人申请查阅我十二岁那年的原始记录。"
    wbw "你可以拒绝涉及个人隐私的部分。公开不等于交出自己。"
    irene "我知道。以前的我，大概不会分辨这两件事。"
    narrator "她合上申请表，把一枚新的铜钥匙放进王不稳手里。"
    irene "闭馆后还有一间屋子没有整理。作为平等的守护者，你不能提前下班。"
    wbw "这算邀请还是加班？"
    irene "今晚可以先算邀请。"
    narrator "红叶落在打开的窗台。被保存的不只是过去，也包括两个人终于允许彼此参与的以后。"
    narrator "——Irene 结局《秋实之书》"
    return


label sequel_ending_ruby:
    $ sequel_chapter_progress = 7
    scene bg sakurakagami_station_winter with fade
    scene cg sequel_ruby_name with dissolve

    narrator "王不稳选择成为外来的稳定锚点。Ruby 从冬之承载者变回了一个会被点名、会在照片里留下影子的人。"
    narrator "她留在旧车站，为曾被循环抹去的人整理来信。每年初雪，站台都会响起一遍完整的姓名。"
    ruby "最后一封读完了。"
    wbw "还有一封。"
    narrator "王不稳递给她一张没有邮戳的信纸。上面只有一句话：明年初雪，也请让我站在你身边。"
    ruby "这封信的收件人写错了。"
    wbw "哪里错？"
    ruby "不该只写明年。"
    narrator "Ruby 把两个人的名字并排写在信尾。耳坠轻轻一响，这一次保存的是他们亲自选择的未来。"
    narrator "——Ruby 结局《冬夜来信》"
    return


label sequel_ending_return:
    $ sequel_chapter_progress = 7
    scene bg city_anomaly with fade

    narrator "四季镜接受了王不稳离开的选择。四位承载者共同接管经过修正的本地协议，而他带着全部记录穿过银白光。"
    narrator "旧世界的雨滴继续落下。手机上的时间只走了一秒。"

    if sequel_origin_ending == "stable":
        narrator "公司门禁卡还在口袋里。那条熟悉的街道通向他已经承担两年的选择。"
    elif sequel_origin_ending == "rising":
        narrator "远方城市的列车提醒仍亮在屏幕上。他曾经选择出发，现在也仍会把路走完。"
    elif sequel_origin_ending == "startup":
        narrator "工作室群聊弹出一条新消息。那个由自己点亮的项目，还在等他回去继续。"
    else:
        narrator "旧世界没有替他写好答案。正如当年那三个月，答案仍要由他亲手完成。"

    narrator "行李不见了，手里却多出一本写满名字、潮汐和四季的笔记。最后一页有四种颜色的签名。"
    wbw "（内心）它们发生过。有人会记得，就不是梦。"
    narrator "他走回灯火之中。从此每逢雨夜，他都会在列车到站的风声里听见一声很轻的耳坠鸣响。"
    narrator "——返回结局《回到灯火》"
    return


label sequel_ending_true:
    $ sequel_chapter_progress = 7
    scene cg sequel_true_ending with fade

    narrator "所有证据彼此吻合，所有承担都有明确的名字。四季镜第一次找到旧规则之外的解。"
    narrator "记忆负荷化成无数微光，落进每一张自愿举起的姓名卡。没有人被抹去，也没有人被迫永远留下。"
    dana "花又开了！这次没有马上谢掉。"
    luna "潮汐时间恢复。十二个观测点全部一致。"
    irene "档案正在生成新的第一页。没有缺口。"
    ruby "门还在。它不再抓住谁，只会在四季交界时回应两边同时发出的邀请。"
    narrator "王不稳先回到旧世界。不是因为樱镜町不重要，而是因为真正的选择不该靠逃离另一份责任来证明。"
    narrator "他完成手头的承诺，也把那段无法公开验证的经历，按最熟悉的方式整理成一份完整记录。"
    narrator "一年后的春分，旧车站在雨声中再次亮起。"
    narrator "门的另一边，Dana 挥着新地图，Luna 抱着观测板，Irene 手里拿着开放档案的第一卷，Ruby 则撑着初见时那把旧伞。"
    ruby "欢迎回来，王不稳。"
    wbw "这次我的行李是自己的。"
    narrator "四个人同时笑了。春花、夏潮、秋叶和冬雪在同一片天空短暂交汇，却没有任何一季因此停下。"
    narrator "他们不再是被规则挑中的四季之女，而是共同写下新规则的人。王不稳也终于明白，留下来从来不是困在某个地方，而是愿意为自己的选择持续负责。"
    narrator "——真结局《四季同在》"
    return
