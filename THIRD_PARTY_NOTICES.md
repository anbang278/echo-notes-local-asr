# 第三方来源与许可

项目原创文档、Spec、echo-notes-local-asr-development Skill、初始化辅助脚本和 tests 使用根目录 MIT License。模型与未来迁入的组件分别遵守其来源许可。

## Trellis 0.6.16

来源：[mindfold-ai/Trellis](https://github.com/mindfold-ai/Trellis)，本机 @mindfoldhq/trellis 0.6.16 的 init 生成。上游包标记 AGPL-3.0-only，许可全文保存在 [Trellis-LICENSE.txt](third_party/Trellis-LICENSE.txt)。不以本仓库 MIT 替换这些第三方内容的许可。

来源范围：`.trellis/scripts/`、`.trellis/agents/`、`.trellis/spec/guides/`、`.agents/skills/trellis-*/`、`.codex/`、`.pi/` 与生成模板的管理文件。`.trellis/workflow.md`、config 和 workspace 索引在 2026-10-16 按本项目分工与隐私约定作了修改。项目新增 Spec 与 tasks 是原创项目文档。模板哈希保留上游生成时的基线，后续更新应识别本地修改，不强制覆盖。

开发工具文件不进入未来 Mac 应用运行包。新增依赖或迁入源码时按组件记录许可、来源和修改范围。

## Echo Notes 既有实现

本次仅引用 anbang278/echo-notes 的提交 8eb08fc0481d794a62416d535c949c4a3ba9e8b1，未迁入其推理或控制台代码。M0 迁入前记录文件清单和版权，见 docs/SOURCES.md 与 M0 任务。
