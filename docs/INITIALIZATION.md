# 仓库与研发脚手架初始化验收

日期：2026-10-16。执行范围来自用户完整引用并要求实施的初始化方案；本轮应用开发未启动。

## 真实结果

| 检查 | 结果与证据 |
| --- | --- |
| 原始输入 | ZIP 及汇总 Markdown 原样保留并忽略；前后 SHA-256 一致 |
| 初始文件 | 释放 14 个初始化文件到仓库根层，无覆盖冲突 |
| Trellis | 0.6.16 native，Codex + Pi，session_auto_commit=false，Codex inline |
| 工程规范 | Mac 进程、Python/MLX、模型、协议隐私、测试发布五类 Spec |
| 本地统一检查 | bash scripts/check.sh 通过；17 项单元／模拟测试、公开清单、文档和任务上下文通过 |
| 独立复核 | 只读复核通过，无阻塞公开初始化的 P0–P2 问题 |
| 远端 | [anbang278/echo-notes-local-asr](https://github.com/anbang278/echo-notes-local-asr)，PUBLIC，默认 main |
| 首提交读回 | `ef79de94e290ebc46cebe80c983dfd2d4335069c`，创建后本地 HEAD 与远端 main 一致 |
| 首次 CI | [Repository checks](https://github.com/anbang278/echo-notes-local-asr/actions/runs/38864939703)，completed / success，绑定上述首提交 |
| 后续提交 | 本记录及初始化归档通过正常后续提交同步；最新状态以 GitHub Actions 和 git log 为准 |
| M0 | planning，implementation_approved=false，implementation_started=false，待 Pi 接手 |

GitHub 首次检查通过后提示旧 Action Node 运行时退役和 ubuntu-latest 即将迁移；后续配置固定 ubuntu-24.04，并使用官方 API 核验的 checkout v7.0.1、setup-python v7.0.0（均 Node 24）对应完整 commit，保持检查环境明确。

## 原始资料指纹

- 本地ASR初始化.zip：`0dba3021e812842f0288090f9c1997434c72c1f49118206f2ec327035ee26031`
- 本地ASR设计与研发计划.md：`a10ca19c3bf140e20352640e2573d02a0a4fa0f3b3443b46b6200ab06c705ef7`

旧 Echo Notes 工作区的 Git 状态与开始时一致；本任务未编辑其文件。原始资料、个人身份与 journal、运行态、音频、模型、凭据与详细本地证据不在公开清单中。初始化脚本仅提交显式白名单，既有仓库和同名远端不会被覆盖。

## 未验证与下一步

尚无本仓库的应用源码迁移、模型推理、干净 Mac、长音频、签名公证或测试安装证据。Codex hooks 是否启用与受信任由用户宿主决定，本轮未修改全局配置或自动批准 hooks，也未启动 Pi。

[M0 交接](../.trellis/tasks/10-16-m0-baseline-packaging/handoff.md) 已准备。用户批准 M0 实施后，由 Pi 在新项目持久 worktree 推进运行时与打包实验。

## 本轮复盘

- 保留初始化顺序：先完成工件和清单检查，再由首次建库脚本初始化 Git、创建远端并推送。
- 模型缓存的忽略规则使用根路径，避免把工程规范中的 models 目录一并忽略。
- macOS Bash 3.2 中紧邻中文标点的变量使用花括号，保证错误账号分支输出合法文本。
- 本轮经验仅写入项目验收记录，未写入长期记忆或升级全局技能。
