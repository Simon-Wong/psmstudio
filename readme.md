# PSMStudio

Persional Sound and Movie Studio

## 环境

python=3.12

gradio=6.12.0

## 组成

### 声音

#### service/sound/third/index_tts

子模块，来自开源项目https://github.com/index-tts/index-tts

根据index-tts的要求配置好后，应能独立运行。

#### service/sound/wrapper/index_tts

封装index_tts的功能，提供一个API。

demo_via_gradio.py是一个调用index_tts的例子。这个例子要求index_tts的服务是运行的。

调试时，可以提前向index-tts的webui.py里增加“show_error=True”，以打开gradio的报错信息。

```
if __name__ == "__main__":
    demo.queue(20)
    demo.launch(server_name=cmd_args.host, server_port=cmd_args.port,show_error=True)
```

