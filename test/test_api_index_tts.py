import sys
import os
from pathlib import Path

PYTHONPATH_ENV = os.getenv("PYTHONPATH", ".")
PSMS_ROOT = Path(PYTHONPATH_ENV.split(os.pathsep)[0])
sys.path.insert(0, str(PSMS_ROOT))

from service.sound.wrapper.index_tts.api_index_tts import generate_tts


path= generate_tts(arg_prompt=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
                     arg_text="溪柴火软蛮毡暖，我与狸奴不出门。",
                     arg_emo_ref_path=r"D:\testGit\psmstudio\service\sound\wrapper\index_tts\demo_voice.mp3",
                     arg_output_path=r"D:\testGit\psmstudio\temp",
                     arg_output_filename="hahagushi_3",
                     arg_verbose=True,
                     emo_weight=0.9,vec1=0.1,param_17=0.9
                     )
    
print(f"自定义生成：{path}")