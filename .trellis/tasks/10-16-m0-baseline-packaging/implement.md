# M0 实施步骤

状态：待实施授权；本清单不是启动批准。

1. 读取 AGENTS、项目 Skill、全部任务工件和 JSONL 引用，核实本次授权与主分支。建立持久 worktree：`$HOME/.local/share/echo-notes-local-asr/worktrees/m0-baseline-packaging`，分支 `pi/m0-baseline-packaging`；已有同用途 worktree 则核验后接续。
2. 核验固定上游提交与 research/baseline.md。列出普通 ASR 必需模块、间接依赖、可复用测试、需要解除的路径和可剔除的说话人依赖；记录版权。不得修改原 Echo Notes 仓库。
3. 实测首轮设备和可用签名条件；建立 test-data、test-install、deliveries 等隔离目录。仅使用许可明确音频，不读取用户录音或扫描缓存以假定模型可用。
4. 选择并固定自包含解释器及依赖，制作最小运行实验。将实际构建、运行、依赖校验命令写入 docs/DEVELOPMENT.md；避免给尚未成立的入口填假成功实现。
5. 执行 test-plan 中真实短音频、跨路径、断网、缺模型及干净设备验证，保留具体失败和阻塞。无签名或干净设备时仍完成其他可独立验证项。
6. 形成组件清单、支持矩阵、数据目录 ADR 和路线结论，更新 README 与研发计划。新增脚本及依赖运行相应测试，再运行 `bash scripts/check.sh` 并更新公开白名单。
7. 在本地功能分支保存实现与证据提交，生成绑定 commit、版本、包 SHA-256 和安装位置的交付记录。将已验证开发包交付新项目 test-install，提供人工启动步骤；若运行包不可用则报告失败，不能宣称交付就绪。
8. 等待人工验收。人工批准当前产物前不合并、推送、Tag 或 Release。失败只清理本任务拥有的测试产物，先确认来源；保留源码、复现命令与失败证据，不修改旧正式服务或模型缓存。
