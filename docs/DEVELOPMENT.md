# 研发与测试交付约定

## 当前工具与能力

Trellis 0.6.16，native 工作流，Codex + Pi；项目规则由 AGENTS、项目开发 Skill、Spec 和任务共同提供。Python 3.11 是初始化 CI 的检查版本，不是应用内嵌 Python 版本承诺。

```bash
bash scripts/check.sh
python3 .trellis/scripts/task.py list
python3 .trellis/scripts/task.py validate .trellis/tasks/10-16-m0-baseline-packaging
python3 .trellis/scripts/get_context.py --mode packages
```

Codex hooks 文件已生成，但宿主启用、项目信任及 `/hooks` 批准不是本轮自动修改内容。未启用时手动读项目 Skill、workflow 和任务即可；不把文件存在报告成已受信任运行。Pi 配置指向仓库内扩展与 prompts，没有自动启动 Pi。

## 五阶段责任与批准

| 阶段 | 责任 | 出口 |
| --- | --- | --- |
| 规划 | Codex | 需求、设计、实施、测试与 handoff 齐全，关键决定已确认 |
| 实施 | Pi | 获授权后，在持久 worktree 完成本地源码提交与验证 |
| 测试交付 | Pi | 构建、版本、包与隔离安装核验一致，提供操作步骤 |
| 人工验收 | 用户 | 启动当前测试应用确认体验；批准绑定当前交付 |
| 正式发布 | Codex 或 Pi 单一执行者 | 核实批准后合并、推送、签名公证、发布及资产读回 |

本轮初始化由用户明确授权 Codex 实施并公开推送治理工件；M0 仍是 planning，尚未授权应用实现。后续“继续”不改变默认执行者。交接消息不自动发送给 Pi。

## 持久目录与隔离

本机工作根：`$HOME/.local/share/echo-notes-local-asr/`。

| 子目录 | 用途 |
| --- | --- |
| worktrees/ | Pi 持久功能 worktree；建议 M0 分支 pi/m0-baseline-packaging |
| deliveries/ | 按任务、版本、源码提交保存包与脱敏证据 |
| backups/ | 测试交付备份与回退材料 |
| test-install/ | 与正式应用隔离的待人工测试应用 |
| test-data/ | 明确许可的测试音频与隔离运行数据 |

这些是约定，本次不创建安装或启动服务。公开文档使用 `$HOME`；详细机器输出与完整本地路径放被忽略的 local-evidence/。真实应用数据目录、隔离端口、解释器版本、构建及安装命令由 M0 实验后固化，不提前提供虚假的可用命令。

## 应用交付与失败恢复

Pi 获 M0 实施授权后，在新命名空间持久 worktree 中核对主分支与计划版本，完成必要实验。生成组件清单、运行包、测试说明和失败证据，逐步确立后续应用构建、打包、部署与回退入口。不得使用旧插件的三文件覆盖或 Obsidian 重载作为本应用部署。

交付至少记录任务、源码 commit、版本、包 SHA-256、依赖／模型 revision、实际测试安装位置、测试结果和人工操作步骤。无证书可验证开发运行包，但不得生成“已签名公证”结论。M0 可以失败并给出可复现的失败与替代路线证据，不能用空壳应用掩盖运行时问题。

人工批准前保留 worktree 与交付，不合并应用主分支、不 push、tag 或 Release。失败先恢复已验证的测试布局；不得停止或替换旧服务。M3 涉及主插件修改时，单独安排相应仓库授权与回归。

## 文件路由

README 维护状态和证据入口；docs 保存正式设计、架构、计划、验收和来源；Spec 保存跨任务约束；任务目录保存本次需求、实现步骤、研究与交接。原始输入只读保存并忽略，不维护另一套正文。
