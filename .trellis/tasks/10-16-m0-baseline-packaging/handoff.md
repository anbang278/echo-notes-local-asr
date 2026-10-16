# M0 交接

## 当前状态

- 规划准备完成；task 状态 planning。
- 初始化仓库与脚手架已获授权；M0 应用实施、应用原型及发布均未授权。
- 默认规划者 Codex、实施者 Pi；未自动发送消息，未启动 Pi。
- 当前没有本仓库应用包、真实模型、干净 Mac 或签名公证验收证据。

## 复制给 Pi Agent

```text
请接手 echo-notes-local-asr 的 M0 规划包。先读取仓库根 AGENTS.md、.agents/skills/echo-notes-local-asr-development/SKILL.md、docs/DEVELOPMENT.md，以及 .trellis/tasks/10-16-m0-baseline-packaging/ 下的 handoff.md、prd.md、design.md、implement.md、test-plan.md 和 JSONL 引用。
当前仅批准仓库／脚手架初始化和 M0 规划准备，尚未批准 M0 应用实施。请先只读核验交接，等待用户明确批准 M0 后再实现；生成此消息不代表你已开始。
获授权后，以本仓库 main 建立或接续 $HOME/.local/share/echo-notes-local-asr/worktrees/m0-baseline-packaging（pi/m0-baseline-packaging）。固定上游提交 8eb08fc0481d794a62416d535c949c4a3ba9e8b1，先核验必要源码与版权，再验证自包含 Python / MLX / 解码器、短录音、断网、跨路径、干净 Mac、支持矩阵、签名条件和数据目录。禁止修改旧 Echo Notes 仓库、旧服务或用户缓存。
持续完成已授权范围内的实现、修复、验证、本地功能分支提交与隔离测试交付。应用构建和打包命令由 M0 形成真实入口；不可套用 Obsidian 插件打包规则。交付包放新项目 deliveries，测试安装放 test-install，记录源码、版本、包 SHA-256、实际运行位置、人工启动步骤与未验证项。
人工仅验收当前测试应用及其对应证据；当前源码或包改变后重新验收。人工批准当前交付前，不合并 main、不 push、Tag 或 Release；证书或干净设备缺失要准确报告阻塞，不宣称签名、公证或新机验收通过。
```

本节为公开可移植消息；向当前用户交付时由 Codex 展开本机真实任务与 handoff 绝对路径，实际路径不提交公开仓库。
