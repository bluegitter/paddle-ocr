# Paddle-OCR Web Service

这是一个基于 PaddleOCR 封装的简单 Web 服务应用。该应用能够接受图片的 `base64` 编码，并返回识别出的文字结果。通过使用 Flask 框架，提供一个易于集成的 HTTP 接口。

## 目录

- [功能介绍](#功能介绍)
- [安装步骤](#安装步骤)
- [使用指南](#使用指南)
- [测试方法](#测试方法)


## 功能介绍

- **OCR 识别**：能够对传入的图片进行文字识别，并返回文本内容。
- **支持多种图片格式**：支持 `data:image/png;base64,...` 和其他 `base64` 编码格式的图片。
- **Flask Web 服务**：提供一个基于 HTTP 协议的 RESTful API 接口，方便集成到前端或其他系统中。

## 安装步骤

请按照以下步骤安装 Paddle-OCR 项目的依赖环境。

1. 创建新的 conda 虚拟环境并激活：

    ```bash
    conda create -n paddlex python=3.8
    conda activate paddlex
    ```

2. 安装 PaddleX 依赖库：

    ```bash
    pip install https://paddle-model-ecology.bj.bcebos.com/paddlex/whl/paddlex-3.0.0b1-py3-none-any.whl
    ```

3. 安装其他必要的依赖库：

    ```bash
    pip install paddlepaddle paddleocr ujson -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip install  flask flask-cors -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

    如果系统提示: 
    Error: Your machine doesn't support AVX, but the installed PaddlePaddle is avx core, you should reinstall paddlepaddle with no-avx core.
    ```bash
    pip install paddlepaddle==2.3.2 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/noavx/stable.html --no-index --no-deps
    ```

## 使用指南

1. **启动服务**：

   在项目根目录下执行以下命令：

    ```bash
    python app.py
    ```

2. **测试 OCR 服务**：

   启动成功后，服务会在 `http://127.0.0.1:5000/ocr` 端口监听。可以使用 `curl` 或 Postman 发送请求进行测试。

## 测试方法

以下是一个简单的测试命令，演示如何使用 `curl` 命令发送带有 `base64` 图片内容的请求：

1. **使用 curl 进行测试**：

   方式1: 将以下内容替换为实际的 `base64` 图片内容（`data:image/png;base64,...` 格式）：

    ```bash
    curl -X POST http://127.0.0.1:5000/ocr \
    -H "Content-Type: application/json" \
    -d '{
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAL8AAAAcCAYAAAAwYm5GAAAAAXNS..."
    }'
    ```

   方式2: 以文件方式识别
   ```bash
   curl -X POST http://192.168.14.48:5000/ocr -F file=@test.png
   ```
2. **成功响应示例**：

    如果图片中包含 "Hello OCR" 字样，响应可能会类似以下 JSON：

    ```json
    {
      "text": "Hello OCR"
    }
    ```

3. **错误响应示例**：

    如果请求格式不正确或图片解析失败，返回如下错误响应：

    ```json
    {
      "error": "Image data not provided"
    }
    ```