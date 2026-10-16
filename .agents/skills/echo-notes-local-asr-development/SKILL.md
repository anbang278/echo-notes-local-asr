---
name: echo-notes-local-asr-development
description: "Echo Notes Local ASR 独立 Mac 助手的项目研发入口；用于本项目规划、实现、调试、测试交付和发布。保留 Codex 规划、Pi 实施、人工验收的分工，不适用于 Echo Notes 插件安装或审核。"
---

# Echo Notes Local ASR 研发入口

1. 读取根目录 AGENTS、README、`.trellis/workflow.md` 和指定任务。用 Git 与实际文件核对当前状态，不把计划当作实现。
2. 识别执行者与批准范围。Codex 默认规划并生成 Pi 交接；Pi 仅实施已授权任务；人工批准当前交付后，才进入应用发布。初始化仓库授权不包含 M0 实施。
3. 按下表加载相关 Spec，并读取任务 JSONL 的有效引用。

| 任务 | 必读入口 |
| --- | --- |
| Mac 应用、进程与数据目录 | `.trellis/spec/runtime/index.md` |
| Python、MLX、音频解码与取消 | `.trellis/spec/inference/index.md` |
| 模型安装、下载与运行时交付 | `.trellis/spec/models/index.md` |
| 配对、鉴权、本地协议、诊断 | `.trellis/spec/protocol-security/index.md` |
| 验证、测试交付、签名、公证与发布 | `.trellis/spec/quality-release/index.md` |

4. 使用 `bash scripts/check.sh` 验证初始化治理工件；它不验证 ASR 或 Mac 应用。应用构建和测试命令必须由 M0 实验产生，并记录于 `docs/DEVELOPMENT.md`。
5. 更新 README、研发计划和任务证据。Codex 完成或修订计划时，维护 handoff 的“复制给 Pi Agent”并在回复中附完整接手消息；批准证据变化时同步刷新。没有 Pi 接收证据就保持待接手。

公开文档使用仓库相对路径或 `$HOME`，项目工件以本仓库为真源。此 Skill 不依赖用户私有的中央 Obsidian 插件工作流；迁移机器可直接使用项目工件。Codex hooks 的宿主信任与 `/hooks` 批准由用户管理，未启用时手动读取本 Skill；不替用户修改全局信任设置。
