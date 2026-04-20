# PSMStudio

Persional Sound and Movie Studio

```
git clone git@github.com:Simon-Wong/psmstudio.git
```

## 环境

wsl2 ubuntu24.04

miniforge3

python=3.12

gradio=6.12.0

```
conda create -n envPMMS python=3.12
```

## 拉取子模块

```
GIT_LFS_SKIP_SMUDGE=1 git submodule update --init --recursive
```

## 子模块组成

**由于不同的组件需要的环境不同，可能要拉取多份代码，在不同的地方部署。**

index_tts：个人感觉在Windows上部署方便

wan2.2：个人感觉在wsl上部署方便

### Sound

#### service/sound/third/index_tts

子模块，来自开源项目https://github.com/index-tts/index-tts

根据index-tts的要求配置好后，应能独立运行。

这个用Windows跑。

##### 专用环境

```
D:
cd D:\testGit\psmstudio\service\sound\third\index_tts

conda create -n envTools python=3.12
conda activate envTools

pip uninstall torch torchvision torchaudio
conda uninstall pytorch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130

pip install -U uv
uv sync --extra webui --default-index "https://mirrors.aliyun.com/pypi/simple"

uv tool install "modelscope"
```

##### 下载模型

```
modelscope download --model IndexTeam/IndexTTS-2 --local_dir D:\modelscope_stuff\IndexTeam_IndexTTS-2
```

##### 检测GPU可用

```
uv run tools/gpu_check.py
```

（也可以调试）

正常会显示

```
(envTools) D:\testGit\psmstudio\service\sound\third\index_tts>uv run tools/gpu_check.py
warning: Ignoring `SSL_CERT_DIR`. No certificates found in: C:\Users\thbyt\.conda\envs\envTools\Library\ssl\certs.
Scanning for PyTorch hardware acceleration devices...

PyTorch: NVIDIA CUDA / AMD ROCm is available!
  * Number of CUDA devices found: 1
  * Device 0: "NVIDIA GeForce RTX 5080"
PyTorch: No devices found for Intel XPU backend.
PyTorch: No devices found for Apple MPS backend.

Hardware acceleration detected. Your system is ready!

(envTools) D:\testGit\psmstudio\service\sound\third\index_tts>
```

##### 运行

```
set HF_HUB_DISABLE_SSL_VERIFY=true
set HF_ENDPOINT=https://hf-mirror.com
uv run webui.py --model_dir D:\modelscope_stuff\IndexTeam_IndexTTS-2
```

打开

```
http://localhost:7860
```

#### service/sound/wrapper/index_tts

对service/sound/third/index_tts的封装，提供一个API，使其可以在一个新的环境里运行，不必考虑index_tts项目的环境。要求index_tts的服务是运行的。

##### 测试

在envPMMS环境下，demo_via_gradio.py是一个调用index_tts的例子。

```
D:
cd D:\testGit\psmstudio\service\sound\wrapper\index_tts

conda activate envPMMS
python demo_via_gradio.py
```

或者直接在vscode里用envPMMS环境运行api_index_tts.py文件。

```
conda activate envPMMS
python D:\testGit\psmstudio\service\sound\wrapper\index_tts\api_index_tts.py
```

##### 调试

可以提前向index-tts的webui.py里增加“show_error=True”，以打开gradio的报错信息。

```
if __name__ == "__main__":
    demo.queue(20)
    demo.launch(server_name=cmd_args.host, server_port=cmd_args.port,show_error=True)
```

### Video

#### service/video/third/wan2.2

子模块，来自开源项目https://github.com/Wan-Video/Wan2.2

根据Wan2.2的要求配置好后，应能独立运行。

这个用wsl ubuntu24.04跑。（虽然我在Windows上成功的编译了flash_attention，但是还有triton等要处理）

##### 专用环境

```
cd /home/thbytwo/testGit/psmstudio/service/video/third/wan2.2

conda create -n envWan2_2 python=3.10 -y

conda activate envWan2_2
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-13-0

pip install psutil
pip install -r requirements.txt --no-build-isolation -vvv
pip install -r requirements_s2v.txt 
pip install ninja
pip install sam2 --no-build-isolation --extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple
#注释掉requirements_animate里的sam2
pip install -r requirements_animate.txt --no-build-isolation -vvv
```

##### 下载模型

```
modelscope download --model Wan-AI/Wan2.2-TI2V-5B --local_dir /mnt/d/modelscope_stuff/Wan2.2-TI2V-5B
```

##### 测试

```
python generate.py --task ti2v-5B --size 1280*704 --frame_num=29 --ckpt_dir /mnt/d/modelscope_stuff/Wan2.2-TI2V-5B --offload_model True --convert_model_dtype --t5_cpu --prompt "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage" --save_file "/home/thbytwo/testGit/psmstudio/testwan22-2.mp4"
```

##### 可能遇到的报错

###### killed

如果遇到“killed”，可以用下面的命令看原因。

```
dmesg -T | grep -i "killed process"
```

一般来讲是内存爆了。修改参数，降低质量。分别是：分辨率、帧数、采样。

```
--size 1280*704 --frame_num 24 --sample_steps 5
```

或者用WSL Settings修改配置。例如内存改成20480

###### CUDA版本不匹配

需要根据具体的显卡重新研究配置环境。

```
# 检查PyTorch版本和CUDA可用性
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda}'); print(f'GPU型号: {torch.cuda.get_device_name(0)}')"

# 检查NVIDIA驱动版本
nvidia-smi
```


