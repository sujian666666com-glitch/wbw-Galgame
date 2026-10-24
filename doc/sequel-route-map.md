# 樱镜町续篇路线与状态对账

本文档以当前 `game/story/sequel_*.rpy` 与 `game/core/state.rpy` 为准，用于编剧、实现和测试对账。

## 入口与 label 链

```text
start
  → sequel_start
  → sequel_prologue
  → sequel_chapter_01
  → sequel_chapter_02_spring
  → sequel_chapter_03_summer
  → sequel_chapter_04_autumn
  → sequel_chapter_05_winter
  → sequel_finale
      ├─ sequel_ending_dana
      ├─ sequel_ending_luna
      ├─ sequel_ending_irene
      ├─ sequel_ending_ruby
      ├─ sequel_ending_return
      └─ sequel_ending_true
```

旧篇入口保留为 `original_story_start → prologue`。旧篇三个结局分别将 `persistent.old_ending_route` 写为 `stable`、`rising`、`startup`；`sequel_start` 将其读入 `sequel_origin_ending`，没有记录时使用 `unknown`。

## 章节进度

| `sequel_chapter_progress` | Label | 剧情段 |
|---:|---|---|
| 0 | `sequel_prologue` | 穿越序章 |
| 1 | `sequel_chapter_01` | 初遇与伪造身份 |
| 2 | `sequel_chapter_02_spring` | 春 / Dana |
| 3 | `sequel_chapter_03_summer` | 夏 / Luna |
| 4 | `sequel_chapter_04_autumn` | 秋 / Irene |
| 5 | `sequel_chapter_05_winter` | 冬 / Ruby |
| 6 | `sequel_finale` | 四季镜终章 |
| 7 | 六个 `sequel_ending_*` | 结局 |

## 状态变量

| 变量 | 初始值 | 正常流程最大值/终值 | 用途 |
|---|---:|---:|---|
| `story_arc` | `"old"` | 续篇入口设为 `"sequel"` | UI 与故事阶段区分 |
| `sequel_origin_ending` | `"unknown"` | `stable/rising/startup/unknown` | 序章与返回结局文本回调 |
| `ruby_affection` | 0 | 4 | Ruby 角色结局及真结局条件 |
| `dana_affection` | 0 | 3 | Dana 角色结局及真结局条件 |
| `luna_affection` | 0 | 3 | Luna 角色结局及真结局条件 |
| `irene_affection` | 0 | 3 | Irene 角色结局及真结局条件 |
| `sequel_insight` | 0 | 6 | 真相证据完整度；真结局要求 6 |
| `sequel_resolve` | 0 | 5 | 共同承担意志；真结局要求至少 4 |
| `spring_fragment` | `False` | `True` | 春章固定取得；真结局条件 |
| `summer_fragment` | `False` | `True` | 夏章固定取得；真结局条件 |
| `autumn_fragment` | `False` | `True` | 秋章固定取得；真结局条件 |
| `winter_fragment` | `False` | `True` | 冬章固定取得；真结局条件 |
| `sequel_route` | `""` | 六个路线字符串之一 | 记录最终选择 |

说明：`affection` 后缀沿用项目变量命名，续篇文本中的实际含义是信任、尊重与共同承担，不等同于即时恋爱关系。

## 全部 menu 与变量影响

### M00：序章检查陌生行李

所在 label：`sequel_prologue`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 逐项核对文件、日期和签名 | `sequel_insight +1` | 共同发现大学部材料、仿签与离线地图 |
| 先确认住处，避免继续淋雨 | 无 | 同上 |

### M01：向 Ruby 说明真实来历

所在 label：`sequel_chapter_01`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 坦白银光、陌生行李与非本人办理的身份 | `ruby_affection +1`、`sequel_resolve +1` | Luna 提议验证系统记录 |
| 暂时沿用材料中的转学生说法 | 无 | 同上；Ruby 保留距离 |

### M02：处理异常学籍

所在 label：`sequel_chapter_01`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 立即与 Luna 核对录入时间、账号和签名 | `sequel_insight +1` | Irene 登场并接收离线副本 |
| 先完成报到，拿到权限再查 | 无 | 同上；Luna 先保存原始记录 |

### M03：春庭现场分工

所在 label：`sequel_chapter_02_spring`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 先问 Dana 需要什么，再按她的方案分工 | `dana_affection +2` | 共同核对失踪见证者 |
| 直接接过名单，替 Dana 指挥所有人 | 无 | Dana 拒绝被替换，主线回收 |
| 建议立刻解散活动，各自回家 | 无 | Dana 改为集体撤至入口，主线回收 |

### M04：保存春庭记忆

所在 label：`sequel_chapter_02_spring`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 每位见证者保存一小段并互相核对 | `dana_affection +1`、`sequel_insight +1`、`sequel_resolve +1` | 固定取得春之碎片 |
| 全部记录交给 Dana 一人保管 | 无 | Dana 主动改为分布保存，固定取得碎片 |
| 王不稳建立唯一总档案 | 无 | Dana 与 Luna 改为分布保存，固定取得碎片 |

### M05：逆流现场行动

所在 label：`sequel_chapter_03_summer`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 执行 Luna 分组方案，带回二号点纸带 | `luna_affection +2`、`sequel_insight +1` | 共同确认记录被自动覆盖 |
| 离开安全绳，冲向三号设备 | 无 | Luna 阻止冒险，主线回收 |
| 立即撤离，放弃全部现场数据 | 无 | Luna 保留残缺离线日志，主线回收 |

### M06：公开夏季异常

所在 label：`sequel_chapter_03_summer`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 公开可复核证据并邀请见证者补充 | `luna_affection +1`、`sequel_resolve +1` | 固定取得夏之碎片 |
| 立即上传全部原始资料 | 无 | Luna 改为发布已验证资料，固定取得碎片 |
| 封锁消息，只让五人保留 | 无 | Luna 改为邀请自愿见证者保存，固定取得碎片 |

### M07：面对 Irene 的隐瞒

所在 label：`sequel_chapter_04_autumn`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 让她说完，再逐页核对证据 | `irene_affection +2`、`sequel_insight +1` | Irene 打开铁盒中的创始记录 |
| 指出她无权替所有人决定 | 无 | Irene 仍打开铁盒，主线回收 |

### M08：秋季承载选择

所在 label：`sequel_chapter_04_autumn`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 拒绝未经本人和众人同意的牺牲 | `irene_affection +1`、`sequel_resolve +1` | Irene 开放档案，固定取得秋之碎片 |
| 接受她独自承担以先稳定小镇 | 无 | 其余三人到场阻止，固定取得碎片 |

### M09：保存 Ruby 的名字

所在 label：`sequel_chapter_05_winter`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 请她亲手写下名字和意愿，让所有人共同读出 | `ruby_affection +2`、`sequel_insight +1` | 全镇广播共同念出 Ruby 的名字 |
| 承诺自己永远不会忘记她 | 无 | Ruby 仍亲手写名，主线回收 |

### M10：冬之钥印承担方式

所在 label：`sequel_chapter_05_winter`

| 选项 | 变量影响 | 回收 |
|---|---|---|
| 尊重 Ruby 决定，与其他三人共同扶住钥印 | `ruby_affection +1`、`sequel_resolve +1` | 固定取得冬之碎片 |
| 抢过钥印，替她成为承载者 | 无 | Ruby 拒绝被代替，众人共同分担并取得碎片 |

### M11：四季镜最终选择

所在 label：`sequel_finale`

| 选项 | 显示条件 | 变量影响与跳转 |
|---|---|---|
| 让整个樱镜町共同记住四季 | `sequel_truth_ready()` | `sequel_route = "true"` → `sequel_ending_true` |
| 与 Dana 留下 | `dana_affection >= 3` | `sequel_route = "dana"` → `sequel_ending_dana` |
| 与 Luna 留下 | `luna_affection >= 3` | `sequel_route = "luna"` → `sequel_ending_luna` |
| 与 Irene 留下 | `irene_affection >= 3` | `sequel_route = "irene"` → `sequel_ending_irene` |
| 与 Ruby 留下 | `ruby_affection >= 3` | `sequel_route = "ruby"` → `sequel_ending_ruby` |
| 返回原世界 | 始终显示 | `sequel_route = "return"` → `sequel_ending_return` |

所有剧情型菜单都会在当前 label 内回收；只有 M11 跳入互斥结局。

## 理想路线数值对账

| 来源 | Ruby | Dana | Luna | Irene | 洞察 | 共同意志 |
|---|---:|---:|---:|---:|---:|---:|
| 序章检查文件 | 0 | 0 | 0 | 0 | 1 | 0 |
| 初遇坦白 | 1 | 0 | 0 | 0 | 0 | 1 |
| 初遇核对学籍 | 0 | 0 | 0 | 0 | 1 | 0 |
| 春章两次理想选择 | 0 | 3 | 0 | 0 | 1 | 1 |
| 夏章两次理想选择 | 0 | 0 | 3 | 0 | 1 | 1 |
| 秋章两次理想选择 | 0 | 0 | 0 | 3 | 1 | 1 |
| 冬章两次理想选择 | 3 | 0 | 0 | 0 | 1 | 1 |
| **最大值** | **4** | **3** | **3** | **3** | **6** | **5** |

四枚碎片均在相应章节固定取得，因此正常完整流程抵达 `sequel_finale` 时碎片数为 4。

真结局要求共同意志至少 4，而最大值为 5，允许玩家在五次共同承担选择中错过一次；洞察要求恰好达到最大值 6，因此六次证据型理想选择必须全部完成。

## 六个结局显示条件

| 结局 | `sequel_route` | 菜单显示条件 |
|---|---|---|
| Dana《春日归邻》 | `dana` | `dana_affection >= 3` |
| Luna《盛夏坐标》 | `luna` | `luna_affection >= 3` |
| Irene《秋实之书》 | `irene` | `irene_affection >= 3` |
| Ruby《冬夜来信》 | `ruby` | `ruby_affection >= 3` |
| 返回《回到灯火》 | `return` | 始终显示 |
| 真结局《四季同在》 | `true` | 四信任均 ≥3、`sequel_insight >= 6`、`sequel_resolve >= 4`、四碎片全为真 |

角色结局菜单在代码中只直接检查对应信任值；正常 label 链会固定取得四碎片。若测试直接跳进 `sequel_finale`，应自行准备章节状态。

## 全部运行时 image id

### 背景 `scene bg`

| Image id | 使用位置 |
|---|---|
| `bg city_anomaly` | 穿越序章、返回结局 |
| `bg sakurakagami_station_rain` | 穿越后的雨夜车站 |
| `bg old_house_day` | 初遇章旧宅清晨 |
| `bg academy_courtyard` | 初遇、春章回收 |
| `bg spring_garden` | 春章、Dana 结局 |
| `bg lighthouse_night` | 夏章、Luna 结局 |
| `bg archive_autumn` | 秋章、Irene 结局 |
| `bg sakurakagami_station_winter` | 冬章、Ruby 结局 |
| `bg mirror_chamber` | 四季镜终章 |

### 剧情 CG `scene cg`

| Image id | 使用位置 |
|---|---|
| `cg sequel_four_meeting` | 四人庭院初次同框 |
| `cg sequel_dana_spring` | 春庭共同记忆、Dana 结局复用 |
| `cg sequel_luna_tide` | 夏夜逆流、Luna 结局复用 |
| `cg sequel_irene_archive` | 秋季档案真相、Irene 结局复用 |
| `cg sequel_ruby_name` | 冬夜写名、Ruby 结局复用 |
| `cg sequel_mirror_finale` | 镜室共同承担 |
| `cg sequel_true_ending` | 真结局群像 |

### 角色立绘 `show`

| Image id | 角色 |
|---|---|
| `wangbuwen normal` | 王不稳 |
| `ruby normal` | Ruby |
| `dana normal` | Dana |
| `luna normal` | Luna |
| `irene normal` | Irene |

当前续篇剧本只引用上述普通立绘，没有引用未登记的表情变体。

## 测试用最短状态

| 目标 | 建议直达状态 |
|---|---|
| Dana 结局 | `dana_affection = 3`，从 `sequel_finale` 进入 |
| Luna 结局 | `luna_affection = 3`，从 `sequel_finale` 进入 |
| Irene 结局 | `irene_affection = 3`，从 `sequel_finale` 进入 |
| Ruby 结局 | `ruby_affection = 3`，从 `sequel_finale` 进入 |
| 返回结局 | 无前置状态，从 `sequel_finale` 进入 |
| 真结局 | 四信任均为 3 或更高、洞察 6、共同意志 4 或更高、四碎片为真 |

完整流程测试仍应从 `sequel_start` 开始，以验证旧结局回顾、全部局部分支回收、碎片获取和真结局解锁。
