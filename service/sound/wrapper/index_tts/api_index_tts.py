# -*- coding: utf-8 -*-
from gradio_client import Client
from gradio_client import handle_file

import shutil
import os
from pathlib import Path

# ===================== 默认配置 不可更改 =====================
PYTHONPATH_ENV = os.getenv("PYTHONPATH", ".")
PSMS_ROOT = Path(PYTHONPATH_ENV.split(os.pathsep)[0])

# ===================== 自动配置（项目根目录） =====================
INIDEX_TTS_OUTPUTS_DIR = os.path.join(PSMS_ROOT, "service/sound/third/index_tts/outputs")
GRADIO_URL = "http://localhost:7860"
DEFAULT_REF_AUDIO = os.path.join(PSMS_ROOT, "service/sound/wrapper/index_tts/demo_voice.mp3")


# ===================== 核心公共API函数 =====================
def generate_tts(
    arg_prompt: str ,
    arg_text: str,
    arg_emo_ref_path: str,
    arg_emo_control_method:str="与音色参考音频相同",
    arg_output_path: str = ".",
    arg_output_filename: str = "tts_output",
    arg_gradio_url:str=GRADIO_URL,
    arg_auto_clean: bool = True,
    arg_verbose:bool = False,
    **kwargs
    ) -> str:
    """
    调用 IndexTTS 生成语音（完全开放原生接口所有参数）
    :param arg_prompt: 必选-参考音频路径
    :param arg_text: 必选-合成文本
    :param arg_emo_ref_path: 必选-音色参考音频路径。emo_control_method默认参考这个。
    :param arg_output_path: 可选-输出文件保存目录。结尾无“/”
    :param arg_output_filename: 可选-输出文件名（无后缀）
    :param arg_gradio_url: 可选-gradio服务地址
    :param arg_auto_clean: 可选-自动清理临时文件
    :param kwargs: 原生predict所有参数（emo_weight/vec1~vec8等任意传）
    :return: 生成音频的绝对路径
    """
    # 初始化客户端
    client = Client(arg_gradio_url)
    
    # 自动处理音频文件（核心封装能力）
    prompt_file = handle_file(arg_prompt)
    emo_ref_file = handle_file(arg_emo_ref_path)

    # 调用原生predict：固定必填参数 + 用户自定义参数（完全覆盖/扩展）
    result = client.predict(
        prompt=prompt_file,
        text=arg_text,
        emo_ref_path=emo_ref_file,
        emo_control_method=arg_emo_control_method,
        api_name="/gen_single" ,
        **kwargs  # 透传所有用户自定义参数，无任何限制
    )

    # 自动处理文件保存/格式适配（核心封装能力）
    temp_path = result["value"]
    ext = os.path.splitext(temp_path)[-1]
    output_path = os.path.join(arg_output_path, f"{arg_output_filename}{ext}")
    shutil.copy(temp_path, output_path)
    final_path = os.path.abspath(output_path)

    # 自动清理
    if arg_auto_clean:
        clean_index_tts_outputs_files(verbose=arg_verbose)
        clean_gradio_temp(verbose=arg_verbose)

    return final_path

def clean_index_tts_outputs_files(directory: str = INIDEX_TTS_OUTPUTS_DIR, extensions: list[str] = ["wav"],verbose=False):
    """
    清理指定目录下的文件
    :param directory: 要清理的文件夹路径
    :param extensions: 要删除的文件后缀列表。无需带"."，例如 ["wav", "mp4", "avi"]。
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录不存在：{directory}") if verbose else None
        return
    
    # 统一转为小写，避免大小写问题（如.WAV / .Wav）
    target_ext = {ext.lower() for ext in extensions}
    
    # 遍历目录文件
    for filename in os.listdir(directory):
        # 获取文件后缀（小写）
        file_ext = filename.split(".")[-1].lower() if "." in filename else ""
        # 判断后缀是否在删除列表中
        if file_ext in target_ext:
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"已删除：{file_path}") if verbose else None
            except Exception as e:
                print(f"删除失败 {file_path}：{e}") if verbose else None
def clean_gradio_temp(exclude_dirs: list[str] = ["vibe_edit_history"],verbose=False):
    """
    清理Gradio临时目录，排除指定的多个文件夹（自适应当前Windows用户）
    :param exclude_dirs: 要保留的文件夹名称列表，默认保留 ['vibe_edit_history']
    """
    try:
        # 自适应获取当前用户的 LocalAppData 路径
        local_appdata = os.environ.get("LOCALAPPDATA")
        if not local_appdata:
            print("无法获取用户目录")  if verbose else None
            return

        # 拼接 Gradio 临时文件夹完整路径
        gradio_temp_path = os.path.join(local_appdata, "Temp", "gradio")

        # 检查目录是否存在
        if not os.path.exists(gradio_temp_path):
            print(f"Gradio临时目录不存在：{gradio_temp_path}")  if verbose else None
            return

        print(f"正在清理目录：{gradio_temp_path}")  if verbose else None
        print(f"保留文件夹列表：{exclude_dirs}")  if verbose else None

        # 遍历所有子项
        for item in os.listdir(gradio_temp_path):
            item_path = os.path.join(gradio_temp_path, item)

            # 只处理【文件夹】，跳过文件 + 跳过排除列表中的文件夹
            if os.path.isdir(item_path) and item not in exclude_dirs:
                shutil.rmtree(item_path)
                print(f"已删除目录：{item}")  if verbose else None

        print("Gradio临时目录清理完成！")  if verbose else None

    except Exception as e:
        print(f"清理失败：{str(e)}")  if verbose else None

# ===================== 公共API导出 =====================
__all__ = [
    "generate_tts",
    "clean_index_tts_outputs_files",
    "clean_gradio_temp",
]

# ===================== 测试入口 =====================
if __name__ == "__main__":
    # 用法1：极简调用（用默认参数，和你原来一样）
    print("=== 极简模式调用 ===")
    path1 = generate_tts(arg_prompt=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
                         arg_text="溪柴火软蛮毡暖，我与狸奴不出门。",
                         arg_emo_ref_path=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
    )
    print(f"极简生成：{path1}")

    # 用法2：完全自定义参数（和原生predict一样，自由传所有参数）
    print("\n=== 完全自定义模式调用 ===")
    path2 = generate_tts(arg_prompt=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
                         arg_text="溪柴火软蛮毡暖，我与狸奴不出门。",
                         arg_emo_ref_path=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
                         arg_output_path=r"D:\testGit\psmstudio\temp",
                         arg_output_filename="hahagushi_2",
                         arg_verbose=True,
                         emo_weight=0.7,
                         vec1=0.1,
                         param_17=0.9
    )
    
    print(f"自定义生成：{path2}")