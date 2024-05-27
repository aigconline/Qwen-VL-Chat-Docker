# Qwen-VL-Chat-Docker
## Qwen-VL-Chat 模型下载[下载全部文件]
```shell
https://huggingface.co/Qwen/Qwen-VL-Chat/tree/main
```
## docker镜像构建
```shell
docker build --platform linux/amd64 -t="qwen-vl-chat:v1.0.0" .
```
## 运行
```shell
docker run -d --restart=always --runtime=nvidia --gpus='"device=1"' -p 25000:5000 --name chat qwen-vl-chat:v1.0.0
```

## 测试
```shell
curl -X POST -H "Content-Type: application/json" http://0.0.0.0:25000/qwen/vl/chat -d '{"image": ["test.png"], "text": "照片里面有什么?来自什么电影里面的？"}'
```