# 存档语句身份映射

本目录保存 Ren’Py 官方 old-game 编译映射，使干净构建保留存档依赖的语句身份。不能把它当作可随意删除的缓存。

v2.1.0 映射由通过 lint 的同源隔离项目生成，继承 commit 1737ed6 对应四份自然游玩 v2.0 存档的编译身份。原种子校验值见 doc/collaboration/v2.1/v20-compiled-lineage.json，当前26份产品映射及对应源码校验值见 compiled-lineage.json；测试和验收 observer 不纳入。

产品源码变化后，先用本目录种子在隔离工程编译并验证，再运行 tools/freeze_statement_ids.py <compiled-project> 更新映射并提交。打包工具检查源码与映射哈希，避免使用过期编译身份。源代码 ZIP 保留本目录，运行包排除。

已验证旧档来自固定编译 lineage；没有原始编译映射的任意旧开发快照，不能承诺恢复所有语句。不得用清除个人存档或猜测剧情状态代替兼容修复。
