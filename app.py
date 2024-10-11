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
def ocr_base64():
    # 从请求中提取 base64 字符串
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "Image data not provided"}), 400

    image_base64 = data['image']

    try:
        # 如果 base64 字符串是 data URI 格式，去除前缀 "data:image/png;base64,"
        if image_base64.startswith("data:image"):
            image_base64 = image_base64.split(",")[1]

        # 解码 base64 图片
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

        # 将 PIL 图像转换为 OCR 可识别的 numpy 格式
        image_np = np.array(image)

        # 执行 OCR 识别
        result = ocr.ocr(image_np, cls=True)

        texts = []
        for res in result:
            for line in res:
                text = line[1][0]  # 提取每一行识别的文字
                texts.append(text)

        # 将所有文字拼接为一个字符串
        final_text = "\n".join(texts)

        return jsonify({"text": final_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
