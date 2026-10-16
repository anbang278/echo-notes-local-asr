# 上游基线核验

核验日期：2026-10-16。仓库：https://github.com/anbang278/echo-notes 。固定提交：`8eb08fc0481d794a62416d535c949c4a3ba9e8b1`。本轮使用本机 Git 对象核验提交存在、目录清单和下表 blob，并只读查看 README；未运行旧服务、未迁入应用源码，也未完成逐个模块的 M0 深入分析。

| 候选来源 | Git blob |
| --- | --- |
| `integrations/local-mlx-asr/README.md` | `824dd4d347a574af911c2c200a543f3e057ebe84` |
| `integrations/local-mlx-asr/requirements.lock` | `f26670a626271b24c3298a0ac105a39d5f920fd0` |
| `integrations/local-mlx-asr/service.py` | `01c83b07f4ba52c8d34c5c296a237d670733ca41` |
| `integrations/local-mlx-asr/bounded_audio.py` | `43278173f0868efead7a10a7cdd47e495a4ee6b7` |
| `integrations/local-mlx-asr/bounded_worker.py` | `e5b7df63a61bf49f4218e471176ccfd36af97d39` |
| `integrations/local-mlx-asr/job_store.py` | `632ac19cf8d6a687395c3aca32c9dbac45999ec7` |
| `integrations/local-mlx-asr/multipart_stream.py` | `f66f9e1cba4eb89807b6d518eef218f08f7d3e48` |
| `integrations/local-mlx-asr/control.py` | `a09a9ec658f78aaa785d0aec23c3b7502c2e1c13` |
| `integrations/local-mlx-asr/package_service.py` | `86fdc8ef90d0d3653048fd15ba17565ea492a327` |
| `integrations/local-mlx-asr/model-manifest.json` | `d4f05c2c150b883dc7434a91fa919dc395147d26` |
| `integrations/local-mlx-asr/controller/ASRControl.swift` | `4cba7566bd4150c5147cf08684b0459178025d20` |
| `integrations/local-mlx-asr/controller/build.sh` | `9e0b79ba617534ad674d1cdf32113e11ea8cd1ce` |

已有说明确认：现有服务依赖预置的本地环境及模型缓存，默认加载三套模型；控制台和打包工具是迁移候选。普通转写脱离说话人与对齐依赖、解释器与解码器自包含、运行路径可移植、签名及鉴权都需要进一步验证。

现有 README 还声明跨实例共享 MLX 推理锁；M0 必须查证实际锁行为，避免与旧服务冲突。来源的接口容量、格式和取消描述不构成本项目实测承诺。

M0-01 将逐文件读取实际源码与测试后，把候选清单收敛为正式 SOURCE_BASELINE；不可把上表当作批准迁入全部文件。源码与协议参考：[固定提交目录](https://github.com/anbang278/echo-notes/tree/8eb08fc0481d794a62416d535c949c4a3ba9e8b1/integrations/local-mlx-asr)。
