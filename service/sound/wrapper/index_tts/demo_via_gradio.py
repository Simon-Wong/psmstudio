from gradio_client import Client as gclient
from gradio_client import file as gFile

import shutil
import os
from pathlib import Path

PYTHONPATH_ENV = os.getenv("PYTHONPATH", ".")
PSMS_ROOT = Path(PYTHONPATH_ENV.split(os.pathsep)[0])
# 需要清理wav文件的目录
OUTPUTS_DIR=os.path.join(PSMS_ROOT, "service/sound/third/index_tts/outputs")

# 连接到正在运行的 webui.py 服务
client = gclient("http://localhost:7860")
# 查看可用的端点/函数名称
#print(client.view_api())

#输出的文件名
outfilename="hahagushi"

audiopathfile = r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3"

result=client.predict(emo_control_method="与音色参考音频相同",  # 情感控制方式索引
                            prompt=gFile(audiopathfile), # 音色参考音频路径
                            text="溪柴火软蛮毡暖，我与狸奴不出门。",      # 目标文本
                            emo_ref_path=gFile(audiopathfile),             # 情感参考音频路径
                            api_name="/gen_single" )
temp_audio_path=result["value"]
file_ext = os.path.splitext(temp_audio_path)[-1]

my_output_path =f"{outfilename}{file_ext}"
shutil.copy(temp_audio_path, my_output_path)
print(f"语音已生成并保存到：{os.path.abspath(my_output_path)}")


def clean_outputs_files(directory: str, extensions: list[str] = ["wav"]):
    """
    清理指定目录下的文件
    :param directory: 要清理的文件夹路径
    :param extensions: 要删除的文件后缀列表。无需带"."，例如 ["wav", "mp4", "avi"]。
    """
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"目录不存在：{directory}")
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
                print(f"已删除：{file_path}")
            except Exception as e:
                print(f"删除失败 {file_path}：{e}")


def clean_gradio_temp(exclude_dirs: list[str] = ["vibe_edit_history"]):
    """
    清理Gradio临时目录，排除指定的多个文件夹（自适应当前Windows用户）
    :param exclude_dirs: 要保留的文件夹名称列表，默认保留 ['vibe_edit_history']
    """
    try:
        # 自适应获取当前用户的 LocalAppData 路径
        local_appdata = os.environ.get("LOCALAPPDATA")
        if not local_appdata:
            print("无法获取用户目录")
            return

        # 拼接 Gradio 临时文件夹完整路径
        gradio_temp_path = os.path.join(local_appdata, "Temp", "gradio")

        # 检查目录是否存在
        if not os.path.exists(gradio_temp_path):
            print(f"Gradio临时目录不存在：{gradio_temp_path}")
            return

        print(f"正在清理目录：{gradio_temp_path}")
        print(f"保留文件夹列表：{exclude_dirs}")

        # 遍历所有子项
        for item in os.listdir(gradio_temp_path):
            item_path = os.path.join(gradio_temp_path, item)

            # 只处理【文件夹】，跳过文件 + 跳过排除列表中的文件夹
            if os.path.isdir(item_path) and item not in exclude_dirs:
                shutil.rmtree(item_path)
                print(f"已删除目录：{item}")

        print("Gradio临时目录清理完成！")

    except Exception as e:
        print(f"清理失败：{str(e)}")



# 执行清理
clean_outputs_files(OUTPUTS_DIR)
clean_gradio_temp()
