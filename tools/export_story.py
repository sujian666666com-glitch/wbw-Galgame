from __future__ import annotations

import ast
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date


ROOT = Path(__file__).resolve().parents[1]
import argparse
parser = argparse.ArgumentParser(description="Export all playable story branches as readable UTF-8 text.")
parser.add_argument('--output', type=Path, default=ROOT / 'releases/v2.1.0')
args = parser.parse_args()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
VERSION = re.search(r'config.version = "([^"]+)"', (ROOT / 'game/options.rpy').read_text()).group(1)
MANIFEST_PATH = ROOT / 'doc/collaboration/v2.1/story/manifest.json'
INSERT_TITLES = {item['target_label']: item['source_heading'] for item in json.loads(MANIFEST_PATH.read_text())} if MANIFEST_PATH.exists() else {}
QUOTE = r'"(?:\\.|[^"\\])*"'
SPEAKERS = {
    'narrator': '旁白', 'wbw': '王不稳', 'xw': '许晚晴',
    'wl': '王磊', 'zh': '张浩', 'relative': '亲戚',
    'dana': 'Dana', 'luna': 'Luna', 'irene': 'Irene', 'ruby': 'Ruby',
}
TITLES = {
    'prologue': '序章：地铁站',
    'chapter_01': '第一章：初到城市',
    'chapter_02': '第二章：第一次反打',
    'chapter_03': '第三章：并肩合作',
    'chapter_04': '第四章：被打压',
    'chapter_05': '第五章：正式翻盘',
    'chapter_06': '第六章：选择',
    'ending_stable': '旧篇结局一：稳定',
    'ending_rising': '旧篇结局二：上升',
    'ending_startup': '旧篇结局三：创业',
    'sequel_prologue': '穿越序章：消失的街头',
    'sequel_chapter_01': '初遇：被写好的身份',
    'sequel_chapter_02_spring': '春之章：一夜盛开的庭院',
    'sequel_chapter_03_summer': '夏之章：逆流的海灯',
    'sequel_chapter_04_autumn': '秋之章：红蔷薇的旧档案',
    'sequel_chapter_05_winter': '冬之章：被忘记的名字',
    'sequel_finale': '镜室终章：没有人必须被忘记',
    'sequel_ending_dana': '续篇结局一：Dana《春日归邻》',
    'sequel_ending_luna': '续篇结局二：Luna《盛夏坐标》',
    'sequel_ending_irene': '续篇结局三：Irene《秋实之书》',
    'sequel_ending_ruby': '续篇结局四：Ruby《冬夜来信》',
    'sequel_ending_return': '续篇结局五：返回现实《回到灯火》',
    'sequel_ending_true': '续篇真结局：《四季同在》',
}
SCENES = {
    'bg subway_exit_rain': '雨后的地铁站出口',
    'cg subway_meeting': '地铁初遇（剧情 CG）',
    'bg bedroom_small_day': '小出租屋（日间）',
    'bg bedroom_night': '出租屋（夜间背景）',
    'bg office': '公司办公区',
    'bg office_night': '公司办公区（夜间）',
    'bg meeting_room': '公司会议室',
    'bg rooftop_night': '公司天台（夜间）',
    'bg rooftop_sunset': '公司天台（黄昏）',
    'bg pantry': '公司茶水间',
    'bg convenience_store_night': '便利店门口（夜间）',
    'bg company_street_night': '公司楼下街道（夜间）',
    'bg corridor': '公司走廊',
    'bg company_entrance_morning': '公司入口（清晨背景）',
    'bg train_platform': '列车站台',
    'bg startup_studio': '创业工作室',
    'cg four_friends_living_room': '四人客厅合影（剧情 CG）',
    'bg city_anomaly': '原世界的城市异象',
    'bg sakurakagami_station_rain': '樱镜町车站（雨夜）',
    'bg old_house_day': '旧宅（日间）',
    'bg academy_courtyard': '樱镜学园庭院',
    'bg spring_garden': '春庭',
    'bg lighthouse_night': '海岸灯塔（夜间）',
    'bg archive_autumn': '秋季档案馆',
    'bg sakurakagami_station_winter': '樱镜町车站（冬季）',
    'bg mirror_chamber': '四季镜室',
    'cg sequel_four_meeting': '四人同场（实际复用四人客厅合影 CG）',
    'cg sequel_dana_spring': 'Dana 春之章 CG',
    'cg sequel_luna_tide': 'Luna 夏之章 CG',
    'cg sequel_irene_archive': 'Irene 秋之章 CG',
    'cg sequel_ruby_name': 'Ruby 冬之章 CG',
    'cg sequel_mirror_finale': '四季镜终局 CG',
    'cg sequel_true_ending': '四季同在后日谈 CG',
    'bg v21_train_interior_dusk': '列车车厢（黄昏）',
    'bg v21_old_house_mirror': '旧宅镜面近景',
    'cg v21_xuwanqing_rain_close': '许晚晴雨伞亲近 CG',
    'cg v21_ruby_ending_kiss': 'Ruby 冬夜亲吻 CG',
    'bg v21_time_old_house_night': '旧宅（夜间）',
    'bg v21_time_spring_garden_dusk': '春庭（黄昏）',
    'bg v21_time_spring_garden_evening': '春庭（傍晚）',
    'bg v21_time_lighthouse_deep_night': '海岸灯塔（深夜）',
    'bg v21_time_lighthouse_dawn': '海岸灯塔（黎明）',
    'bg v21_time_archive_evening': '档案馆（傍晚）',
    'bg v21_time_archive_night': '档案馆（夜间）',
    'bg v21_time_company_street_dusk': '公司楼下街道（黄昏）',
    'bg v21_time_company_street_rain': '公司楼下街道（雨夜）',
    'bg v21_time_startup_morning': '创业工作室（清晨）',
    'bg v21_time_station_first_snow': '樱镜町车站（初雪）',
    'bg v21_time_city_street_morning': '原世界城市街道（清晨）',
    'bg v21_time_station_boundary': '旧车站（四季交界）',
}
TRUTH = '春、夏、秋、冬四枚碎片全部取得，四位女孩的信任均至少为 3，洞察至少为 6，共同意志至少为 4'
CONDITIONS = {
    'not evidence_ready': '尚未准备好关键证据',
    'evidence_ready': '已准备好关键证据',
    'ability >= 7 and affection >= 15': '能力至少为 7，且许晚晴好感度至少为 15',
    'ability >= 9 and affection >= 12': '能力至少为 9，且许晚晴好感度至少为 12',
    'side_project_ready and ability >= 8 and affection >= 15 and money >= 1800':
        '已准备好副业项目，能力至少为 8，许晚晴好感度至少为 15，资金至少为 1800',
    'sequel_origin_ending == "stable"': '最近完成的旧篇结局是“稳定”',
    'sequel_origin_ending == "rising"': '最近完成的旧篇结局是“上升”',
    'sequel_origin_ending == "startup"': '最近完成的旧篇结局是“创业”',
    'sequel_truth_ready()': TRUTH,
    **{f'{c}_affection >= 3': f'{c.title()} 信任至少为 3' for c in ('dana', 'luna', 'irene', 'ruby')},
}
CONDITIONS.update({
    'affection >= 3': '许晚晴好感度至少为 3',
    'affection >= 8': '许晚晴好感度至少为 8',
    'affection >= 15': '许晚晴好感度至少为 15',
    'sequel_luna_observation_outcome == "paper_tape"': '此前按方案带回了原始纸带',
    'sequel_luna_observation_outcome == "aborted"': '此前冒险靠近三号设备后中止行动',
    'sequel_luna_observation_outcome == "evacuated"': '此前选择立即撤离',
    'sequel_luna_observation_outcome == "unknown"': '旧存档未记录本次观测行动',
})
END_CONDITIONS = {
    'sequel_ending_dana': 'Dana 信任至少为 3，且在终章选择与 Dana 留下。',
    'sequel_ending_luna': 'Luna 信任至少为 3，且在终章选择与 Luna 留下。',
    'sequel_ending_irene': 'Irene 信任至少为 3，且在终章选择与 Irene 留下。',
    'sequel_ending_ruby': 'Ruby 信任至少为 3，且在终章选择与 Ruby 留下。',
    'sequel_ending_return': '终章始终可以选择返回原世界。',
    'sequel_ending_true': TRUTH + '，且在终章选择让整个樱镜町共同记住四季。',
}


@dataclass
class Node:
    text: str
    location: str
    children: list[Node] = field(default_factory=list)


def parse(path: Path) -> list[Node]:
    records = [(len(line) - len(line.lstrip()), line.strip(), f'{path.relative_to(ROOT)}:{i}')
               for i, line in enumerate(path.read_text().splitlines(), 1)
               if line.strip() and not line.lstrip().startswith('#')]

    def block(index: int, indent: int) -> tuple[list[Node], int]:
        nodes = []
        while index < len(records):
            level, text, location = records[index]
            if level < indent:
                break
            assert level == indent, (location, level, indent)
            node = Node(text, location)
            index += 1
            if index < len(records) and records[index][0] > level:
                assert text.endswith(':'), location
                node.children, index = block(index, records[index][0])
            nodes.append(node)
        return nodes, index

    nodes, end = block(0, 0)
    assert end == len(records)
    return nodes


emitted = []
counts = Counter()
menu_number = 0
label_nodes = {}
called_labels = set()


def decode(literal: str, kind: str) -> str:
    value = ast.literal_eval(literal)
    emitted.append((kind, value))
    counts[kind] += 1
    return value


def line(text: str, depth: int = 0) -> list[str]:
    return ['  ' * depth + text, '']


def render(nodes: list[Node], depth: int = 0) -> list[str]:
    global menu_number
    out = []
    i = 0
    while i < len(nodes):
        node = nodes[i]
        text = node.text
        i += 1
        dialogue = re.fullmatch(r'(\w+)\s+(' + QUOTE + ')', text)
        if dialogue:
            who, literal = dialogue.groups()
            assert who in SPEAKERS, node.location
            out += line(f'{SPEAKERS[who]}：{decode(literal, "dialogue")}', depth)
        elif text.startswith('label '):
            name = text[6:-1]
            counts['labels'] += 1
            out += ['─' * 36, TITLES[name], '─' * 36, '']
            if name in END_CONDITIONS:
                out += line('【进入条件】' + END_CONDITIONS[name])
            out += render(node.children, depth)
        elif text == 'menu:':
            menu_number += 1
            counts['menus'] += 1
            out += line(f'【选择 {menu_number:02d}】', depth)
            option_index = 0
            for child in node.children:
                option = re.fullmatch('(' + QUOTE + r')(?: if (.+))?:', child.text)
                if option:
                    literal, condition = option.groups()
                    option_index += 1
                    value = decode(literal, 'option')
                    out += line(f'{chr(64 + option_index)}．{value}', depth + 1)
                    if condition:
                        out += line('【显示条件】' + CONDITIONS[condition], depth + 2)
                    out += render(child.children, depth + 2)
                else:
                    assert re.fullmatch(QUOTE, child.text), child.location
                    out += line(decode(child.text, 'prompt'), depth)
            out += line('【选择分支结束；未跳转至结局时，继续以下共同剧情】', depth)
        elif text.startswith('if '):
            chain = [node]
            while i < len(nodes) and (nodes[i].text.startswith('elif ') or nodes[i].text == 'else:'):
                chain.append(nodes[i])
                i += 1
            rendered = []
            for branch in chain:
                body = render(branch.children, depth + 1)
                if not body:
                    continue
                if branch.text == 'else:':
                    title = '【否则：以上条件均不满足】'
                else:
                    condition = branch.text.split(' ', 1)[1][:-1]
                    title = '【条件分支】' + CONDITIONS[condition]
                rendered += line(title, depth) + body
            if rendered:
                out += rendered + line('【条件分支结束】', depth)
        elif text.startswith('$ notify_change('):
            match = re.fullmatch(r'\$ notify_change\((' + QUOTE + r')\)', text)
            assert match, node.location
            out += line('【系统提示】' + decode(match.group(1), 'notification'), depth)
        elif text.startswith('$ '):
            assert not node.children, node.location
        elif text.startswith('scene '):
            image_name = text[6:].split(' with ', 1)[0].split(' at ', 1)[0]
            out += line('【画面】' + SCENES[image_name], depth)
            counts['scenes'] += 1
        elif text.startswith(('show ', 'hide ')):
            assert not node.children, node.location
        elif text.startswith('call '):
            target = text[5:].split(' from ', 1)[0]
            if target in called_labels:
                raise ValueError(f'Duplicate or recursive story insert: {target}')
            called_labels.add(target)
            out += line(INSERT_TITLES.get(target, '【剧情片段】' + target), depth)
            counts['labels'] += 1
            out += render(label_nodes[target].children, depth)
        elif text.startswith('jump '):
            target = text[5:]
            out += line('【转至】' + TITLES[target], depth)
            counts['jumps'] += 1
        elif text == 'return':
            counts['returns'] += 1
        else:
            raise ValueError(f'Unhandled script statement at {node.location}: {text}')
    return out


parts = [
    ('第一部 · 三个月，留下来', ['prologue', *[f'chapter_{i:02d}' for i in range(1, 7)], 'endings']),
    ('第二部 · 樱镜町·四季镜', ['sequel_prologue', 'sequel_chapter_01',
       'sequel_chapter_02_spring', 'sequel_chapter_03_summer',
       'sequel_chapter_04_autumn', 'sequel_chapter_05_winter', 'sequel_finale', 'sequel_endings']),
]
files = [ROOT / 'game/story' / (name + '.rpy') for _, names in parts for name in names]
all_files = sorted((ROOT / 'game/story').glob('*.rpy'))
for path in all_files:
    for node in parse(path):
        assert node.text.startswith('label '), node.location
        name = node.text[6:-1]
        assert name not in label_nodes, name
        label_nodes[name] = node
commit = subprocess.check_output(['git', 'rev-parse', '--short=7', 'HEAD'], cwd=ROOT, text=True).strip()
output = [
    '旺不稳的奇妙冒险', f'v{VERSION} 完整剧本 · 全分支阅读版', '',
    f'整理日期：{date.today().isoformat()}　来源提交：{commit}',
    '正文依据当前游戏实际执行的剧情脚本整理，旁白、对白、菜单文字和系统提示均保留原文。',
    '覆盖旧篇与续篇、全部选择及九类结局。旧篇的普通／理想结局表现也分别收录。', '',
    '阅读方法',
    '1．同一组选择下的 A、B、C 等内容互斥，实际游玩只会经过所选分支。',
    '2．条件分支按标明的条件择一阅读；结束标记之后回到共同剧情。',
    '3．“转至结局”表示离开当前主线，请跳读文中同名结局。',
    '4．画面名称与条件说明为阅读注释；剧情正文使用原句。', '',
    '目录',
    '第一部：序章、第一至第六章、稳定／上升／创业结局。',
    '第二部：穿越序章、初遇、春／夏／秋／冬之章、镜室终章、六个结局。', '',
]
for title, names in parts:
    menu_number = 0
    output += ['═' * 36, title, '═' * 36, '']
    if title.startswith('第一部'):
        output += ['【初始状态】许晚晴好感度 0，能力 2，资金 2300；证据与副业项目尚未准备。', '']
    else:
        output += ['【初始状态】四位女孩信任、洞察、共同意志均为 0，四季碎片均未取得。',
                   '【旧篇接续】序章按最近完成的旧篇结局展示对应回顾；没有记录时展示中性回顾。', '']
    for name in names:
        for node in parse(ROOT / 'game/story' / (name + '.rpy')):
            output += render([node])
            if 'ending_' in node.text:
                output += line('【本结局结束】')
                counts['endings'] += 1

# Verify every displayed source string independently, including all alternate branches.
expected = []
source_counts = Counter()
for path in all_files:
    for raw in path.read_text().splitlines():
        text = raw.strip()
        match = re.fullmatch(r'(\w+)\s+(' + QUOTE + ')', text)
        if match and match.group(1) in SPEAKERS:
            expected.append(('dialogue', ast.literal_eval(match.group(2))))
        elif match := re.fullmatch(r'\$ notify_change\((' + QUOTE + r')\)', text):
            expected.append(('notification', ast.literal_eval(match.group(1))))
        elif match := re.fullmatch('(' + QUOTE + r')(?: if .+)?:', text):
            expected.append(('option', ast.literal_eval(match.group(1))))
        elif re.fullmatch(QUOTE, text):
            expected.append(('prompt', ast.literal_eval(text)))
        if text == 'menu:': source_counts['menus'] += 1
        if text.startswith('label '): source_counts['labels'] += 1
        if text.startswith('scene '): source_counts['scenes'] += 1
        if text.startswith('jump '): source_counts['jumps'] += 1
        if text == 'return': source_counts['returns'] += 1

assert Counter(expected) == Counter(emitted), (Counter(expected) - Counter(emitted), Counter(emitted) - Counter(expected))
for key, value in source_counts.items():
    assert counts[key] == value, (key, counts[key], value)
assert counts['menus'] == 22
assert counts['endings'] == 9
text = '\n'.join(output).rstrip() + '\n'
for _, original in expected:
    assert original in text
target = OUT / f'旺不稳的奇妙冒险-v{VERSION}-完整剧本.txt'
target.write_text(text, encoding='utf-8-sig')
report = {'source_commit': commit, 'source_files': len(all_files), 'counts': dict(counts),
          'source_text_preserved': True, 'output': str(target), 'output_bytes': target.stat().st_size, 'called_insert_count': len(called_labels)}
(OUT / 'script-export-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
