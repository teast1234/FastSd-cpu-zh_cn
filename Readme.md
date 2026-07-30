# 🎨 FastSD CPU — CPU 快速 AI 生图（Windows 中文 Fork）

**语言 / Languages:** **简体中文** | [上游英文文档](https://github.com/rupeshs/fastsdcpu/blob/main/Readme.md)

在 **CPU** 上快速运行 Stable Diffusion 的工具：基于 [Latent Consistency Models (LCM)](https://github.com/luosiallen/latent-consistency-model) 与 [OpenVINO](https://github.com/openvinotoolkit/openvino) 加速，无需独立显卡也能在数秒～数分钟内出图。

本仓库基于上游 [rupeshs/fastsdcpu](https://github.com/rupeshs/fastsdcpu) 修改：**修复 Windows 官方安装后无法启动的问题**，并将桌面 GUI 汉化。上游英文原版说明仍可参考官方仓库；**本文件记录 Fork 改动与完整中文使用说明**。

> ⭐ **如果这个项目帮到你，欢迎去仓库点个 Star 支持一下～**  
> 你的一颗星，是个人开发者继续更新的最大动力 ❤️

| | |
|---|---|
| 上游项目 | [github.com/rupeshs/fastsdcpu](https://github.com/rupeshs/fastsdcpu) |
| Releases | [官方 Releases](https://github.com/rupeshs/fastsdcpu/releases) |
| 协议 | [MIT](./LICENSE) |
| 作者 | abbuibuibui |
| 联系 | [3244940576@qq.com](mailto:3244940576@qq.com) |

### ✨ 演示：桌面 GUI / Web UI

上游项目截图（本 Fork 桌面 GUI 已汉化，布局一致）：

![FastSD CPU Desktop GUI](docs/images/fastsdcpu-gui.jpg)

![FastSD CPU WebUI](docs/images/fastsdcpu-webui.png)

---

## 📌 项目介绍

| 能力 | 说明 |
|------|------|
| CPU 生图 | 无需 NVIDIA/AMD 独显，LCM / OpenVINO / GGUF 多模式推理 |
| 桌面 GUI | Qt 界面；**本 Fork 已汉化**（文生图、设置、LoRA、ControlNet 等） |
| Web UI | Gradio 高级界面（英文）：文生图、图生图、LoRA、设置等 |
| 多模型 | LCM、标准 SD1.5/SDXL、LCM-LoRA、OpenVINO、GGUF（Flux） |
| LoRA | 标准风格 LoRA + LCM-LoRA 加速适配器（最多 5 个叠加） |
| ControlNet | LCM-LoRA 模式下支持姿势 / 线稿等控制 |
| 本 Fork 修复 | Windows 依赖锁定、安装校验、安装脚本补齐 torchvision |

**限制与注意：**

- ⚠️ 有强力 NVIDIA 显卡时，建议改用 ComfyUI / WebUI Forge，速度更快；本项目优势在 **CPU / Intel AI PC** 场景
- 首次生成会从 Hugging Face 下载模型（约数 GB），请保持网络畅通；国内可设镜像（见下文 FAQ）
- WebUI、命令行、`install.bat` 安装过程仍为英文；桌面 GUI（`start.bat`）已汉化

---

## 🔀 本 Fork 与原版差异

原版在 Windows 上**按官方流程安装后仍可能无法启动**：虚拟环境 `env\` 里装到的依赖版本与项目预期不一致，导致 DLL 加载失败或程序崩溃。

### 原版典型报错

| 报错信息 | 原因 |
| --- | --- |
| `OSError: Error loading c10.dll`（WinError 1114） | 安装了 `torch 2.13.0`，而非项目要求的 `2.8.0` |
| 程序闪退 / access violation | `torchvision` 与 `torch` 版本不匹配，或 `sentencepiece 0.2.2` 导入崩溃 |
| `ImportError: DLL load failed ... onnxruntime` | `onnxruntime 1.26.0` 在部分 Windows 上 DLL 初始化失败 |
| `numpy.core.multiarray failed to import` | 依赖安装过程中 `numpy` 被升到 2.x，与 `opencv-python` 不兼容 |

### 错误环境 vs 项目声明（实测对比）

| 包 | 原版 `install.bat` / `requirements.txt` 声明 | 错误环境中实际出现 | 后果 |
| --- | --- | --- | --- |
| **torch** | `2.8.0` | **2.13.0** | `c10.dll` 加载失败 |
| **torchvision** | 未在 Windows 的 `install.bat` 中安装 | **0.28.0**（随 torch 升级） | 与 torch 2.8 不匹配，导入 diffusers 崩溃 |
| **sentencepiece** | 未锁定 | **0.2.2** | 原生 DLL 导入 access violation |
| **onnxruntime** | `1.26.0` | 1.26.0 | 本机 Windows DLL 初始化失败 |
| **numpy** | `1.26.4` | 被解析升到 **2.x** | opencv 无法导入 |

### 原版设计 / 安装流程的缺陷

1. **`install.bat` 只装了 `torch`，没装 `torchvision`**（Linux 的 `install.sh` 两者都装）
2. **`requirements.txt` 未锁定 torch / torchvision / sentencepiece**，后续解析可能自动升级
3. **`onnxruntime==1.26.0` 在部分 Windows 环境不兼容**
4. **安装后无校验步骤**，双击 `start.bat` 才发现崩溃

### 本 Fork 做了哪些修改？

#### 1. 依赖与安装脚本（核心修复）

| 文件 | 原版 | 本 Fork |
| --- | --- | --- |
| `install.bat` | 仅 `torch==2.8.0` | 同时安装 `torch==2.8.0` + `torchvision==0.23.0` |
| `install.bat` | 装完即结束 | 安装后**回钉关键版本**，防止二次升级 |
| `install.bat` | 无校验 | 末尾自动 `Dependency check: OK` 导入测试 |
| `requirements.txt` | `onnxruntime==1.26.0` | `onnxruntime==1.19.2`（Windows 实测稳定） |
| `requirements.txt` | 无 sentencepiece / protobuf 锁定 | 增加 `sentencepiece==0.2.0`、`protobuf==4.25.9` |
| `install.sh` / `install-mac.sh` | 无回钉与校验 | 同步增加回钉与依赖校验 |

**本 Fork 已验证可用的 Windows 依赖版本：**

```text
torch==2.8.0+cpu
torchvision==0.23.0+cpu
numpy==1.26.4
Pillow==9.4.0
onnxruntime==1.19.2
sentencepiece==0.2.0
protobuf==4.25.9
```

#### 2. 中文界面（桌面 GUI）

| 文件 | 改动 |
| --- | --- |
| 新增 `src/frontend/i18n/` | 轻量翻译模块（`tr()` + `zh_CN.py`） |
| `src/frontend/gui/*.py` | 标签页、按钮、设置项、错误提示等改为中文 |
| `start.bat` | 控制台启动提示改为中文 |

#### 3. 未改动的部分

- 核心业务逻辑、模型推理代码（`src/backend/` 等）
- WebUI（Gradio）界面
- 默认模型 ID、配置文件结构
- 上游功能特性（LCM / OpenVINO / LoRA / ControlNet 等）

### 遇到问题怎么办？

| 情况 | 处理 |
| --- | --- |
| `start.bat` 无法启动 | 删除 `env\`，重新运行 `install.bat`，等待 `Dependency check: OK` |
| 安装校验失败 | 检查 Python 3.10/3.11 和 uv，确认网络可访问 PyTorch / HuggingFace |
| 曾手动 `pip install torch` 升级过 | 不要手动升级 `env` 内包，删 `env` 重装 |
| 首次生成很慢 | 正常，需从 HuggingFace 下载模型（约 1～2 GB），之后会缓存 |

---

## 🏗️ 项目架构

```text
用户（提示词 / 参考图）
      │
      ▼
┌─────────────────────────────────────┐
│  前端                                │
│  Desktop GUI（Qt，本 Fork 已汉化）    │
│  WebUI（Gradio）· CLI               │
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  推理后端                            │
│  LCM · LCM-LoRA · OpenVINO · GGUF   │
│  LoRA / ControlNet / Upscaler       │
└─────────────────────────────────────┘
      │
      ▼
┌──────────────┐     ┌──────────────────────────┐
│  results/    │     │  HuggingFace 缓存 / 本地  │
│  生成图片    │     │  模型 · LoRA · ControlNet │
└──────────────┘     └──────────────────────────┘
```

**它适合谁：**

- 没有 NVIDIA/AMD 独显，但想在本地跑 Stable Diffusion
- 有 Intel AI PC / NPU，想用 OpenVINO 加速
- 想要 1～3 步快速出图（LCM 模式）
- 想用 Civitai / Hugging Face 上下载的 LoRA 微调风格

**目录结构（核心）：**

```text
fastsdcpu/
├── install.bat                 # Windows 安装（本 Fork 已加固）
├── start.bat                   # 启动中文桌面 GUI
├── start-webui.bat             # 启动 Web UI
├── requirements.txt            # 依赖（含锁定版本）
├── results/                    # ★ 生成图片默认输出
├── lora_models/                # ★ LoRA（.safetensors）
├── controlnet_models/          # ★ ControlNet（.safetensors）
├── models/gguf/                # ★ GGUF 相关模型
│   ├── diffusion/
│   ├── llm/
│   └── vae/
├── configs/
│   ├── settings.yaml           # 用户设置（gitignore，不入库）
│   ├── lcm-models.txt
│   ├── openvino-lcm-models.txt
│   ├── stable-diffusion-models.txt
│   └── lcm-lora-models.txt
├── env/                        # 虚拟环境（gitignore，install.bat 创建）
├── src/
│   ├── frontend/
│   │   ├── gui/                # 桌面 GUI（已汉化）
│   │   ├── i18n/               # ★ 本 Fork 新增中文翻译
│   │   └── webui/
│   └── backend/                # 推理流水线
├── docs/images/                # 文档截图
├── LICENSE
└── README.md                   # 本文件（中文 Fork 说明）
```

---

## 🛠️ 技术栈与依赖

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.10+（推荐 3.10 / 3.11） |
| 包管理 | [uv](https://docs.astral.sh/uv/) |
| 推理 | PyTorch CPU（锁定 `2.8.0`）+ Diffusers |
| 加速 | LCM / LCM-LoRA · OpenVINO · GGUF（stable-diffusion.cpp） |
| 桌面 UI | Qt（PySide） |
| Web UI | Gradio |
| 本 Fork 锁定 | torchvision `0.23.0` · onnxruntime `1.19.2` · sentencepiece `0.2.0` · protobuf `4.25.9` · numpy `1.26.4` |

---

## 🚀 快速开始

### 1. 环境要求

- Windows 10 / 11
- Python **3.10 或 3.11**（勾选 **Add Python to PATH**）
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 包管理器
- （建议）内存 **16GB+**；OpenVINO / Flux 场景需要更多

验证：

```powershell
python --version
uv --version
```

安装 uv（若尚未安装）：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装后**重开终端**再验证。

### 2. 获取代码

```powershell
# 克隆本 Fork（将 URL 换成你的仓库地址）
git clone <你的仓库地址>
cd fastsdcpu
```

或从上游 Release 下载 zip 后，使用本 Fork 的安装脚本与依赖锁定版本。

### 3. 安装依赖 ⚙️

在项目根目录双击 **`install.bat`**，或：

```powershell
.\install.bat
```

脚本会：

- 检查 Python / uv
- 创建虚拟环境 `env\`
- 安装 CPU 版 PyTorch + torchvision 与全部依赖
- **回钉关键版本**并执行导入校验

> 安装约 5～20 分钟。完成后应看到 **`Dependency check: OK`**。

### 4. 启动程序 🎬

| 方式 | 命令 | 说明 |
|------|------|------|
| 桌面 GUI（推荐新手） | 双击 `start.bat` | **已汉化**，Qt 窗口 |
| Web UI（功能更全） | 双击 `start-webui.bat` | 浏览器打开 <http://127.0.0.1:7860>（英文） |

Web UI 主要标签：

- **Text-to-Image** 文生图
- **Image-to-Image** 图生图
- **LoRA Models** LoRA 管理
- **Settings** 模型与推理参数

### 5. 第一次生图 🔗

1. 启动 Web UI 或桌面 GUI
2. **Model** 选择：
   - 最快出图 → **LCM** + `SimianLuo/LCM_Dreamshaper_v7` 等
   - SD1.5 基模 + LoRA → **LCM-LoRA**
   - Intel CPU/NPU → **OpenVINO**
3. 输入 Prompt，例如：

```text
a cute corgi sitting in a meadow, golden hour, photorealistic, 8k
```

4. 可选 Negative prompt：

```text
blurry, low quality, deformed, extra limbs
```

5. 参数建议：
   - **Width / Height**：512×512 起步，CPU 上不建议超过 768×768
   - **Inference steps**：LCM 1～4 步；普通模式 20～25 步
   - **Guidance scale**：LCM 通常 1.0～2.0
   - **Seed**：`-1` 随机，或填固定值复现
6. 点击 **Generate** / 「生成」

---

## 🧩 模型类型与用法

FastSD CPU 的核心是 **LCM**：目标 1～4 步出图。普通 SD 模型原本要 20～50 步，在 CPU 上过慢，因此需要 LCM / LCM-LoRA 加速。

### 5 类支持的模型

| 模型类型 | 配置文件 | 使用模式 | 举例 |
|---------|---------|---------|------|
| **LCM 模型** | `configs/lcm-models.txt` | LCM | SDXS-512-0.9、SDXL-Lightning、Hyper-SD |
| **标准 SD 基模 / 微调** | `configs/stable-diffusion-models.txt` | **LCM-LoRA** | SD1.5、SDXL、Civitai checkpoint |
| **LCM-LoRA 适配器** | `configs/lcm-lora-models.txt` | LCM-LoRA | lcm-lora-sdv1-5、lcm-lora-sdxl |
| **OpenVINO 模型** | `configs/openvino-lcm-models.txt` | OpenVINO | Intel 优化模型，CPU 最快 |
| **GGUF 模型** | `models/gguf/` | GGUF | Flux.1-schnell（内存约 12GB） |

### 关键概念：基模 + LCM-LoRA = 快速出图

```text
普通 SD 基模（提供画风/内容）
        +
LCM-LoRA 适配器（提供 1～4 步快速推理）
        ↓
   1～4 步出图
```

**三层模型关系：**

```text
基模 (SD1.5 / SDXL checkpoint)   ← 决定画风基础
   └─ LCM-LoRA 适配器              ← 让它跑得快（CPU 上必需）
       └─ 风格 LoRA (.safetensors)  ← 微调人物/画风（可选，最多 5 个）
```

Civitai 上的 SD1.5 / SDXL checkpoint 完全可用：把路径写入 `configs/stable-diffusion-models.txt`，在 **LCM-LoRA** 模式下选择基模 + 对应适配器即可。

### 使用 Civitai 普通 SD checkpoint

1. 下载 `.safetensors`（如 `dreamshaper_8.safetensors`）
2. 写入 `configs/stable-diffusion-models.txt` 完整本地路径，例如：

```text
D:\models\dreamshaper_8.safetensors
```

3. Web UI 模式选 **LCM-LoRA**
4. Model settings：
   - **Stable diffusion model** → 本地模型
   - **LCM-Lora model** → SD1.5 配 `lcm-lora-sdv1-5`；SDXL 配 `lcm-lora-sdxl`
5. 正常生成

也可直接写 Hugging Face ID（如 `Lykon/dreamshaper-8`），程序会自动下载。

### 推荐组合

| 想要 | 基模 | LCM-LoRA 适配器 | 步数 |
|------|------|---------------|------|
| 最快出图（1 步） | `runwayml/stable-diffusion-v1-5` | `rupeshs/hypersd-sd1-5-1-step-lora` | 1 |
| 二次元 | `stablediffusionapi/anything-v5` | `lcm-lora-sdv1-5` | 3～4 |
| 高质量写实 | `Lykon/dreamshaper-8` | `lcm-lora-sdv1-5` | 3～4 |
| SDXL 高清 | `stabilityai/stable-diffusion-xl-base-1.0` | `lcm-lora-sdxl` | 2～4 |
| Intel CPU 极速 | OpenVINO：`rupeshs/sd-turbo-openvino` | — | 1 |

### 模型模式速查

| 模式 | 速度 | 适用 | 备注 |
|------|------|------|------|
| **LCM** | 极快（1～4 步） | 最快出图 | 需 LCM 专用模型 |
| **LCM-LoRA** | 极快 | 普通 SD1.5/SDXL + LoRA | 支持反向提示词；**Civitai 模型必选** |
| **OpenVINO** | 最快（Intel CPU） | Intel 平台 | **不支持 LoRA** |
| **GGUF** | 中 | Flux 等 | 通过 stable-diffusion.cpp |

---

## 🎭 使用风格 LoRA

| 类型 | 用途 | 模式 |
|------|------|------|
| **标准 LoRA** | Civitai/HF 风格微调 | LCM 或 LCM-LoRA |
| **LCM-LoRA** | 让普通 SD 获得 1～4 步能力 | LCM-LoRA |

### 1. 下载与放置

- [Civitai](https://civitai.com/) · [Hugging Face](https://huggingface.co/)
- 将 `.safetensors` 放入 **`lora_models/`**（支持子目录，递归扫描）

```text
fastsdcpu/
└── lora_models/
    ├── my_style.safetensors
    └── anime/
        └── anime_style.safetensors
```

### 2. Web UI 使用

1. 模式切到 **LCM-LoRA**
2. 选基模 + LCM-LoRA 适配器
3. **LoRA Models** 标签：选文件 → weight（常用 0.6～0.9）→ Load
4. 回到文生图生成（最多 **5 个** LoRA）

### 3. CLI 示例

```powershell
.\src\frontend\cli.py --base_model_id runwayml/stable-diffusion-v1-5 `
    --use_lcm_lora `
    --lora_path lora_models/my_style.safetensors `
    --lora_weight 0.8 `
    --prompt "a cute corgi, photorealistic" `
    --inference_steps 4 `
    --guidance_scale 1.5
```

| 参数 | 说明 |
|------|------|
| `--use_lcm_lora` | 启用 LCM-LoRA |
| `--use_openvino` | 启用 OpenVINO |
| `--lora_path` / `--lora_weight` | LoRA 路径与权重 0.0～1.0 |
| `--prompt` / `--negative_prompt` | 正 / 反向提示词 |
| `--image_height` / `--image_width` | 分辨率 |
| `--inference_steps` | 步数（LCM 1～4） |
| `--guidance_scale` | 引导强度 |
| `--seed` | 随机种子 |

离线使用 LCM-LoRA：下载后把本地文件夹路径写入 `configs/lcm-lora-models.txt`，重启即可在下拉框选择。

---

## 📁 目录与文件说明

### 生成图片保存在哪里？

| 项目 | 说明 |
| --- | --- |
| **默认输出** | `results\` |
| **如何修改** | 桌面 GUI → **设置** → **输出路径** |
| **配置记录** | `configs/settings.yaml` → `generated_images.path` |

| 文件 | 说明 |
| --- | --- |
| `{随机ID}-1.png` | 生成图片（多张为 `-2.png` …） |
| `{随机ID}.json` | 同次生成参数（prompt、步数、模型等） |
| `{原名}_2x_upscale_{时间戳}.png` | 放大输出，仍在 `results\` |

默认格式 **PNG**，可在 `settings.yaml` 的 `generated_images.format` 修改。

### 各类模型放哪？

项目**不附带**权重。主模型首次从 HuggingFace 自动下载到 `%USERPROFILE%\.cache\huggingface\hub\`；扩展模型需手动放入：

| 模型类型 | 存放路径 | 格式 |
| --- | --- | --- |
| LCM / OpenVINO 主模型 | 无需手动放置 | 首次生成自动下载 |
| LoRA | `lora_models\` | `.safetensors` |
| ControlNet | `controlnet_models\` | `.safetensors`（放入后**重启**） |
| GGUF 扩散 / LLM / VAE | `models\gguf\diffusion\` · `llm\` · `vae\` | `.gguf` / `.safetensors` |

ControlNet 可参考：[ControlNet v1.1 fp16](https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/tree/main)（约 723 MB）。

模型列表配置（`configs\`，一行一个 HF ID 或本地绝对路径）：

| 文件 | 用途 |
| --- | --- |
| `lcm-models.txt` | LCM 主模型 |
| `openvino-lcm-models.txt` | OpenVINO 模型 |
| `stable-diffusion-models.txt` | LCM-LoRA 基础 SD（含 Civitai 路径） |
| `lcm-lora-models.txt` | LCM-LoRA 适配器 |

离线：GUI **设置** 勾选「使用本地缓存/已下载模型（离线）」，并把路径写入上述 `.txt`。

---

## ❓ 常见问题

**Q: 启动报错 `python not found`？**  
A: 重装 Python 时勾选 Add to PATH，或手动加入系统环境变量。

**Q: 下载模型很慢 / 卡住？**  
A: 国内可设置 Hugging Face 镜像后再启动：

```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"
.\start-webui.bat
```

**Q: LoRA 加载后没效果？**  
A: ① 确认 **LCM 或 LCM-LoRA** 模式（OpenVINO 不支持 LoRA）；② 调高 weight 到 0.8～1.0；③ 确认基模与 LoRA 兼容（SD1.5 LoRA 不能用于 SDXL）。

**Q: 出图慢？**  
A: 用 LCM、步数 2～4、分辨率 512×512；Intel CPU 可切 OpenVINO；关闭其他占 CPU 程序。

**Q: 内存不足？**  
A: 降低分辨率，或使用 GGUF 量化模型。

**Q: `start.bat` 仍无法启动？**  
A: 删除 `env\`，重新 `install.bat`，确认出现 `Dependency check: OK`；勿手动升级 `env` 内包。

---

## 🔗 参考链接

- 上游主页：<https://github.com/rupeshs/fastsdcpu>
- Releases：<https://github.com/rupeshs/fastsdcpu/releases>
- LoRA / 模型：<https://civitai.com/> · <https://huggingface.co/>
- uv 安装：<https://docs.astral.sh/uv/getting-started/installation/>
- 上游详细文档（英文）：<https://deepwiki.com/rupeshs/fastsdcpu>

---

## 💬 反馈与贡献

如果这个项目对你有帮助，拜托：

1. ⭐ 去仓库点个 **Star**
2. 🐛 遇到问题提 Issue（请附上 Windows 版本、Python 版本、完整报错）
3. ✉️ 想交流可发邮件：[3244940576@qq.com](mailto:3244940576@qq.com)（作者：abbuibuibui）

也欢迎提交 Pull Request（请先说明改动目的与测试方式）～

上游原作者与维护者：[Rupesh Sreeraman](https://github.com/rupeshs)。本 Fork 仅在其基础上做 Windows 依赖修复与中文 GUI。

---

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源（与上游一致）。

```text
Copyright (c) abbuibuibui
```

使用第三方模型与数据源时，请自行遵守对方服务条款与许可；本项目仅供学习与研究，不对生成内容作保证。用户须遵守当地法律并负责任地使用。
