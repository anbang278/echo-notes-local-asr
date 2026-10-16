# Echo Notes Local ASR

面向 Mac 用户的本地语音转写助手：把运行环境、模型下载与本机服务管理封装起来，让用户不必配置 Python、终端或 API 地址，就能在 Echo Notes 中使用本地 ASR。

> **当前状态：设计与研发准备阶段。** 本仓库初始化内容包含设计文档、研发计划、验收标准及建库辅助脚本；尚未迁入 ASR 应用源码，没有可下载的应用安装包，也没有本仓库版本的 Mac 实机验收结果。文中“目标”“计划”不代表已实现。

## 项目定位

Echo Notes 插件负责录音、笔记关联、转写任务、Markdown 及后续知识处理；本项目负责本机模型的安装、运行、资源释放与服务接口。两者通过版本化本地协议协作，各自独立发布，不把模型权重放入 Obsidian Vault。

首先解决：**一台没有预装 Python、Homebrew、FFmpeg 和模型的新 Mac，能够通过图形界面完成安装，并在断网后完成录音转写。**

## 首期范围

| 项目 | 首期决定 |
|---|---|
| 平台 | macOS Apple Silicon（arm64）；Intel Mac 暂不承诺 |
| 首轮基准设备 | M2 / 16GB；其他芯片和内存档位按实测扩充支持矩阵 |
| 最低 macOS 版本 | 待 M0 确认所选 MLX、Python 运行时与签名包的共同下限 |
| 默认模型 | `mlx-community/Qwen3-ASR-0.6B-8bit`，固定经过验证的 revision |
| 转写方式 | 已完成录音的文件转写；首期不做实时听写 |
| 应用形态 | 原生 Mac 控制台／菜单栏应用 + 隔离的本地推理进程 |
| 交付形态 | 目标为签名、公证的 `.app` / `.dmg`，运行时随包交付，模型单独下载 |
| 默认联网策略 | 下载模型由用户触发；转写不调用云端；不自动回退云端 |
| 后续能力 | 1.7B、说话人分离、精细时间对齐；不作为首期完成条件 |

## 设计入口

- [设计理念与产品边界](docs/DESIGN.md)
- [技术架构与集成契约](docs/ARCHITECTURE.md)
- [研发计划、里程碑与任务](docs/DEVELOPMENT_PLAN.md)
- [验收标准与测试证据](docs/ACCEPTANCE.md)
- [既有实现与一手资料](docs/SOURCES.md)
- [交给 Codex 的执行说明](docs/CODEX_HANDOFF.md)
- [研发与测试交付约定](docs/DEVELOPMENT.md)
- [工程规范导航](.trellis/spec/index.md)
- [M0 任务与 Pi 交接](.trellis/tasks/10-16-m0-baseline-packaging/handoff.md)
- [第三方来源与许可](THIRD_PARTY_NOTICES.md)
- [协作约束](AGENTS.md)

## 现有基础，而非本仓库已完成项

可复用来源是 [Echo Notes](https://github.com/anbang278/echo-notes) 的 `integrations/local-mlx-asr/`。本次核验基线为提交 `8eb08fc0481d794a62416d535c949c4a3ba9e8b1`。该目录已有 MLX 推理服务、本地任务协议及 Swift 控制台；仍需要解除对既有开发环境的依赖，并完成独立打包、首次安装及安全集成。来源和限制见 [SOURCES](docs/SOURCES.md)。

## 项目进度

| 里程碑 | 状态 | 完成依据／阻塞 |
|---|---|---|
| M0：基线与打包可行性 | 待开始 | 文档已准备；干净 Mac、签名条件、最低系统版本尚未核实 |
| M1：可移植本地服务 | 待开始 | 未迁入源码，未完成新进程的协议和鉴权测试 |
| M2：Mac 安装与模型管理 | 待开始 | 尚无 `.app`、运行时包与模型安装向导 |
| M3：Echo Notes 配对与自动配置 | 待开始 | 需要另行授权修改主插件仓库并开展联调 |
| M4：可分发测试版 | 待开始 | 尚无真实 Mac 测试矩阵和签名、公证产物 |

**下一步行动：**评审并批准 M0 任务，再由 Pi 在独立持久 worktree 开始基线与打包实验。M0 当前为 planning，尚未授权应用实施；真实模型、干净 Mac、签名与公证均未验证。

每次研发交付必须同步更新本节的当前进度、证据、下一步行动和阻塞。完整任务见 [研发计划](docs/DEVELOPMENT_PLAN.md)。

## 研发脚手架

已生成 Trellis 0.6.16 native 工作流和 Codex / Pi 配置，建立五类工程规范、项目开发 Skill 与 M0 完整计划包。默认 Codex 规划、Pi 实施与测试交付、人工验收后发布；创建交接消息不自动启动 Pi。

```bash
bash scripts/check.sh
```

本入口检查公开清单、文档、初始化脚本模拟和任务引用，不安装 ASR，不验证模型或 Mac 应用。应用构建命令由 M0 实验确定。个人身份与 journals、运行态、原始 ZIP／汇总资料保留本地并被忽略。Codex hooks 是否启用仍取决于宿主信任和人工批准。

**初始化已完成：**[GitHub 公开仓库](https://github.com/anbang278/echo-notes-local-asr)，默认分支 main；首个提交 `ef79de94e290ebc46cebe80c983dfd2d4335069c` 已读回核验，[首次 GitHub Actions](https://github.com/anbang278/echo-notes-local-asr/actions/runs/38864939703) 通过。本地 17 项测试、公开文件检查、文档与任务校验通过，独立复核通过。详见 [初始化验收记录](docs/INITIALIZATION.md)。

初始化完成只代表仓库和研发流程就绪；应用 M0 仍待实施授权。后续提交的检查结果见仓库 Actions。

## 首次建库脚本（已执行）

目标仓库标识：`anbang278/echo-notes-local-asr`。本仓库已创建，以下命令仅记录首次建库流程，当前目录不要重复执行 --publish。辅助脚本拒绝既有 Git 元数据，不用于安装 ASR。

```bash
# 在已安装并登录 GitHub CLI 的环境中执行。
# 默认只显示发布清单；不会访问 GitHub 或创建仓库。
bash scripts/create-github-repo.sh

# 检查清单后创建 PUBLIC 仓库，并推送初始化文档。
bash scripts/create-github-repo.sh --publish
```

脚本只提交白名单中的初始化文件，拒绝覆盖已有 Git 仓库或同名远端仓库，并核验登录账号、公开状态与提交 SHA。缺少 GitHub CLI 时，按照 [GitHub CLI 官方说明](https://cli.github.com/)安装并登录，不要将访问令牌写进文档或脚本。

## 许可证与隐私

本项目原创文档和代码使用 [MIT License](LICENSE)，随仓库提供的 Trellis 工具文件保留其上游许可，详见 [第三方来源与许可](THIRD_PARTY_NOTICES.md)。模型、运行库和音频解码组件遵循各自许可证；正式分发前应完成组件清单与再分发条件检查。不要把本许可证理解为对所有模型权重的统一授权。

不收集音频、转写正文或客户端遥测。模型安装完成后的本机 ASR 与 Echo Notes 的云端分析、校对、Memory 是不同数据链路；“本地 ASR”不等于整条知识处理链路均离线。
