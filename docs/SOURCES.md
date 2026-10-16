# 来源、基线与待验证项

核验日期：2026-10-16。来源用于支持架构和计划，不代表本项目已经执行安装或性能测试。

## S1 既有 Echo Notes 实现

仓库：[anbang278/echo-notes](https://github.com/anbang278/echo-notes)

原初始化资料引用的 GitHub 主分支核验提交：`8eb08fc0481d794a62416d535c949c4a3ba9e8b1`；该提交的 manifest 为 `0.4.40`。引用固定提交，避免把未来 main 的变化当作本次已经检查。

| 文件 | 本次设计使用的事实 | 不应推出的结论 |
|---|---|---|
| [本地服务说明](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr/README.md) | 已有 Apple Silicon 服务、任务协议、手动启停、模型缓存依赖 | 其他用户已能自动完成首次安装 |
| [service.py](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr/service.py) | Qwen3-ASR-0.6B-8bit、本地缓存路径、固定 FFmpeg 路径、offline 环境设置 | 已完成独立可移植打包或网络行为审计 |
| [模型清单](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr/model-manifest.json) | 模型 revision 与文件哈希，可用作迁移基线 | 新版模型可不经验证任意替换 |
| [deploy_service.py](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr/deploy_service.py) | 更新事务、备份和回退思路；要求已有运行环境 | 已支持零环境首次安装 |
| [package_service.py](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr/package_service.py) | 现有打包不包含解释器和模型缓存 | 该包已是普通用户可运行的完整安装器 |
| [本地客户端任务协议](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/src/providers/local-mlx-jobs.ts) | v1 与服务标识校验；专用端口判断为 18080/18081 | 只换端口或服务名就能继续恢复任务 |
| [本地模型文档](https://github.com/anbang278/echo-notes/blob/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/docs/local-model-transcription.md) | 仓库记录有部分自然会议测试，同时明确未做完整 3 小时真实推理验收 | 本次已独立复测或已支持所有长录音 |

原资料的读取方式为 GitHub 文档和代码核验。2026-10-16 本机初始化进一步只读核验了该 Git 提交与候选文件 blob，见 M0 research/baseline.md；没有运行旧服务或读取个人录音。代码移入新仓库时仍需重新检查版权、依赖、测试与当前状态。

## S2 MLX-Audio

- [上游项目](https://github.com/Blaizzy/mlx-audio)
- [Qwen3-ASR 模型说明](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/stt/models/qwen3_asr/README.md)

上游列有 Qwen3-ASR-0.6B-8bit、1.7B-8bit 与 ForcedAligner。该资料支持“可以复用 MLX-Audio 做推理”的选型，不代表本项目已经实现所有上游功能。依赖必须固定到验证过的版本，不在发布时自动取 latest。

## S3 Qwen 原始模型

- [Qwen3-ASR-0.6B 官方模型卡](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

原始模型卡列出 Apache-2.0。使用量化／转换模型前仍要核验该分发仓库、精确 revision、模型文件和附带说明；应用 MIT 许可证不能替代模型许可证。

## S4 Obsidian 社区目录政策

- [Developer policies](https://docs.obsidian.md/community-directory/developer-policies)

政策针对官方社区目录插件，禁止插件自行安装或更新自身及其依赖。这里采用独立应用承担安装与更新，减少插件职责混淆；不能将此架构决定写成已获得官方审核认可。模型资源和伴随应用的具体交互边界在插件提交前复核。

本计划不以“使用任意桌面 API 就必须改变整个插件的移动端支持状态”作未经核验的结论。桌面功能应有能力守卫，并对发布时的插件要求做针对性检查。

## S5 Apple Mac 软件分发

- [Notarizing macOS software before distribution](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- [Signing Mac Software with Developer ID](https://developer.apple.com/developer-id/)

官方文档支持签名、Hardened Runtime、公证和票据附加的发布流程。公证不等于 App Store 审核。本项目尚未确认签名凭据，也未产生通过公证的产物。

## S6 FFmpeg 分发条件

- [FFmpeg License and Legal Considerations](https://ffmpeg.org/legal.html)

不同编译选项会影响许可证义务；要核验实际分发的构建配置、许可证、源代码提供方式及相关义务。本计划不作“任意预编译 FFmpeg 均可直接附带发布”的假设。

## S7 可选 Swift 推理实现

- [MLX Audio Swift](https://github.com/Blaizzy/mlx-audio-swift)
- [Qwen3ASR 模型说明](https://github.com/Blaizzy/mlx-audio-swift/blob/main/Sources/MLXAudioSTT/Models/Qwen3ASR/README.md)

上游列出 Qwen3-ASR 与相关模型的 Swift 实现。仅作为 Python 打包路线需要替代时的候选，尚未评估与本项目长录音和任务协议的等价性。

## S8 GitHub 仓库初始化

- [GitHub CLI — gh repo create](https://cli.github.com/manual/gh_repo_create)

初始化脚本采用官方 `--public`、`--source`、`--remote` 和 `--push` 参数。脚本在原初始化包阶段仅做模拟测试；本次已通过认证 GitHub CLI 创建公开仓库、推送并读回核验，见 [初始化记录](INITIALIZATION.md)。
