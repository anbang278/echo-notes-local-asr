# Codex 移交说明

## 任务背景

Echo Notes 是 Obsidian 录音转写与知识处理插件。用户已经在自己的 Mac 上使用本地 ASR，现在希望其他 Mac 用户也能无需技术配置地完成本地部署和转写。

新项目名为 **Echo Notes Local ASR**，公开仓库 `anbang278/echo-notes-local-asr` 已创建，默认 main，初始化工件已推送并真实读回。当前交付包含文档、研发脚手架、检查与 M0 规划，尚无应用实现。

## 当前内容与阅读顺序

先读 `README.md`、`AGENTS.md`、`docs/DESIGN.md`、`docs/ARCHITECTURE.md`、`docs/DEVELOPMENT_PLAN.md`、`docs/ACCEPTANCE.md`。上游基线与资料位于 `docs/SOURCES.md`。

仓库与脚手架初始化已执行：首个提交 `ef79de94e290ebc46cebe80c983dfd2d4335069c`；[首次 CI](https://github.com/anbang278/echo-notes-local-asr/actions/runs/38864939703) 通过。完整范围和未验证项见 [初始化记录](INITIALIZATION.md)。已有仓库不要重复执行建库脚本；后续按当前任务的授权更新和推送。

## 本项目研发脚手架

本次初始化按用户批准方案建立 Trellis 0.6.16 native 工作流，启用 Codex / Pi。研发分工、文件路由和测试交付以 AGENTS、项目开发 Skill 与 [研发约定](DEVELOPMENT.md) 为准。M0 已准备 [完整计划与交接](../.trellis/tasks/10-16-m0-baseline-packaging/handoff.md)，状态 planning，等待应用实施授权。

统一检查入口：`bash scripts/check.sh`。它覆盖初始化治理，不覆盖实际模型、干净 Mac 或签名公证。GitHub 创建与推送状态以 README 的真实读回证据为准；建库脚本仅适用于首次初始化，已有 .git 时拒绝重复执行。

## 后续研发任务的起点

收到明确的应用研发授权后，从 M0 开始。首要目标是在干净 Apple Silicon Mac 上跑通最小可分发程序，而不是先做完整设置 UI 或同时支持多个平台。

默认复用主插件仓库 `integrations/local-mlx-asr/` 中必要的推理、任务与控制台代码。基线固定为 `8eb08fc0481d794a62416d535c949c4a3ba9e8b1`，迁入前核验本地获取内容。保留版权和来源，排除个人路径、私有录音、日志、`.venv` 和模型权重。

## 已选择的产品边界

首期支持经过验证的 Apple Silicon Mac；默认 Qwen3-ASR-0.6B-8bit；文件录音转写；原生轻量应用加独立推理进程；独立应用安装并管理模型，插件只连接服务与处理笔记；不默认运行 pip、Homebrew、远程 shell 安装脚本；不自动回退云端。

暂不做 Windows、Intel Mac、实时录音、多模型融合、1.7B、说话人分离和精细时间对齐。只预留适配边界，不提前实现这些功能。

## 关键待验证问题

1. 自包含 Python／MLX／解码器包能否在不同 Mac 和目录中运行，并完成签名、公证。
2. 最低 macOS、可用内存和原生库版本组合；不要仅按参数量或模型文件大小估算。
3. 本地令牌、配对、进程身份、任务所有权与取消终态的安全性。
4. 不改变旧主服务和缓存的隔离验证方式。
5. 真实长录音质量与资源占用，及客户端重载／服务重启的恢复差异。

## 授权与交付要求

建库和文档初始化不包含修改旧主插件仓库、部署用户正式 Mac 服务、关闭旧进程、删除缓存或发布安装包的授权。后续任务明确授权哪些部分，就推进哪些部分；不要以“自动化研发”为由扩大操作范围。

每阶段返回变更范围、执行与验证记录、未验证内容、阻塞、下一步。未访问 Mac 时只能报告静态／模拟测试；未读回远端时不得说“已推送”；未测试真实模型时不得说“本地转写已通过”。
