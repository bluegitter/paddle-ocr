import base64
import io
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from paddleocr import PaddleOCR

# 初始化 PaddleOCR（使用中文模型）
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)


@app.route('/ocr', methods=['POST'])
def ocr_handler():
    if request.content_type.startswith('multipart/form-data'):
        # 文件上传处理
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        image = Image.open(file.stream)
    else:
        # 处理 base64 字符串
        data = request.get_json()
        if 'image' not in data:
            return jsonify({"error": "Image data not provided"}), 400

        image_base64 = data['image']
        if image_base64.startswith("data:image"):
            image_base64 = image_base64.split(",")[1]

        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

    # 将 PIL 图像转换为 OCR 可识别的 numpy 格式
    image_np = np.array(image)

    # 执行 OCR 识别
    result = ocr.ocr(image_np, cls=True)

    if result is None:
        return jsonify({"error": "OCR failed, result is None"}), 500

    # 修改提取文字的逻辑，防止 NoneType 错误
    texts = [line[1][0] for res in result if res is not None for line in res]
    return jsonify({"text": "\n".join(texts)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
