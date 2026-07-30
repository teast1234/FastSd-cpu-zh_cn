"""Simplified Chinese UI strings."""

MESSAGES = {
    # App
    "app.name": "FastSD CPU",
    "app.about_html": (
        "<h1>FastSD CPU {version}</h1>"
        "<h3>© 2023 - {year} Rupesh Sreeraman</h3>"
        "<h3>CPU 上的快速 Stable Diffusion</h3>"
        "<h3>基于 Latent Consistency Models</h3>"
        "<h3>GitHub：https://github.com/rupeshs/fastsdcpu/</h3>"
    ),
    # Tabs
    "tab.text_to_image": "文生图",
    "tab.image_to_image": "图生图",
    "tab.image_variations": "图像变体",
    "tab.upscaler": "放大",
    "tab.settings": "设置",
    "tab.lora": "LoRA 模型",
    "tab.controlnet": "ControlNet",
    "tab.about": "关于",
    # Text to image
    "prompt.placeholder": "例如：梦幻风景，夕阳光照，高清细节",
    "negative_prompt.label": "反向提示词（引导系数 > 1.0 时生效）：",
    "generate": "生成",
    "upscale": "放大",
    "open_output_folder": "打开输出文件夹",
    "please_wait": "请稍候…",
    "image_placeholder": "« 生成的图片 »",
    "control_image_placeholder": "« 控制图 »",
    # Settings
    "settings.lcm_model": "LCM 模型：",
    "settings.use_lcm_lora": "使用 LCM LoRA",
    "settings.lora_base_model": "LoRA 基础模型：",
    "settings.lcm_lora_model": "LCM LoRA 模型：",
    "settings.inference_steps": "推理步数：{value}",
    "settings.num_images": "生成张数：{value}",
    "settings.guidance_scale": "引导系数：{value}",
    "settings.clip_skip": "CLIP Skip：{value}",
    "settings.token_merging": "Token 合并：{value}",
    "settings.width": "宽度：",
    "settings.height": "高度：",
    "settings.use_seed": "使用随机种子",
    "settings.use_safety_checker": "启用安全检测",
    "settings.use_openvino": "使用 OpenVINO（Intel 加速）",
    "settings.openvino_model": "OpenVINO LCM 模型：",
    "settings.use_offline_model": "使用本地缓存/已下载模型（离线）",
    "settings.use_tae_sd": "使用 Tiny AutoEncoder（更快，质量中等）",
    "settings.output_path": "输出路径：",
    "settings.reset_all": "重置全部",
    "settings.select_folder": "选择文件夹",
    # Image to image
    "img2img.init_image": "初始图片：",
    "img2img.browse_tooltip": "浏览并选择初始图片",
    "img2img.strength": "去噪强度：{value}",
    "img2img.open_image": "打开图片",
    "img2img.image_filter": "图片文件 (*.png *.jpg *.bmp)",
    # Upscaler
    "upscaler.mode_label": "放大模式（2 倍）| AURA-SR（4 倍）：",
    # LoRA
    "lora.model": "LoRA 模型：",
    "lora.initial_weight": "初始权重：",
    "lora.load": "加载所选 LoRA",
    "lora.loaded": "已加载的 LoRA：",
    "lora.update_weights": "更新 LoRA 权重",
    "lora.tooltip": "将 LoRA 模型放入 <b>lora_models</b> 文件夹",
    "lora.error_openvino": "OpenVINO 模式暂不支持 LoRA。",
    "lora.error_invalid_path": "LoRA 模型路径无效！",
    "lora.error_pipeline": "管道尚未初始化，请先生成一张图片。",
    # ControlNet
    "controlnet.help_html": (
        "<p style='white-space:pre'>从 "
        "<a href='https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/tree/main'>"
        "ControlNet v1.1</a> 下载模型（约 723 MB）。<br>"
        "将模型放入 <b>controlnet_models</b> 文件夹。<br>"
        "安装新模型后请重启应用。</p>"
    ),
    "controlnet.enable": "启用 ControlNet",
    "controlnet.model": "ControlNet 模型：",
    "controlnet.conditioning_scale": "条件强度：",
    "controlnet.control_image": "控制图：",
    "controlnet.select_image_tooltip": "点击选择控制图",
    "controlnet.tooltip": "将 ControlNet 模型放入 <b>controlnet_models</b> 文件夹",
    "controlnet.open_image": "打开图片",
    "controlnet.image_filter": "图片文件 (*.png *.jpg *.bmp *.webp)",
    "preprocessor.canny": "Canny 边缘",
    "preprocessor.depth": "深度",
    "preprocessor.lineart": "线稿",
    "preprocessor.mlsd": "MLSD",
    "preprocessor.normalbae": "NormalBAE",
    "preprocessor.pose": "姿态",
    "preprocessor.softedge": "软边缘",
    "preprocessor.shuffle": "Shuffle",
    "preprocessor.none": "无",
    # Dialogs
    "dialog.error": "错误",
    # start.bat
    "start.launching": "正在启动 FastSD CPU…",
    "start.python_ok": "Python 检查：通过",
    "start.python_version": "Python 版本：{version}",
    "start.python_missing": "错误：未找到 Python，请安装 Python 3.10 或 3.11 后重试",
}

# Internal preprocessor keys used by the backend (do not translate)
PREPROCESSOR_KEYS = {
    "preprocessor.canny": "Canny",
    "preprocessor.depth": "Depth",
    "preprocessor.lineart": "Lineart",
    "preprocessor.mlsd": "MLSD",
    "preprocessor.normalbae": "NormalBAE",
    "preprocessor.pose": "Pose",
    "preprocessor.softedge": "SoftEdge",
    "preprocessor.shuffle": "Shuffle",
    "preprocessor.none": "None",
}
