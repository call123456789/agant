from openai import OpenAI
from PIL import Image
import base64
import io
import os
from llm import LLM

# 压缩并调整图像大小（保持宽高比）
def compress_image(image_path, max_size_kb=900, max_width=1024):
    with Image.open(image_path) as img:
        # 转换为 RGB 避免透明通道问题（适用于 PNG/JPEG）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # 按比例缩小宽度至 max_width 以内
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # 使用 BytesIO 缓存压缩后的图像数据
        img_byte_arr = io.BytesIO()
        
        # 初始质量
        quality = 85
        
        # 循环压缩直到小于 max_size_kb
        while True:
            img_byte_arr.seek(0)
            img.save(img_byte_arr, format=img.format if img.format else "JPEG", quality=quality)
            size_kb = img_byte_arr.tell() / 1024
            if size_kb <= max_size_kb or quality <= 10:
                break
            quality -= 5

        img_byte_arr.seek(0)
        return base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")


def watch(args):
    file = args[0]
    base64_image = compress_image(file, max_size_kb=900, max_width=1024)
    llm = LLM()
    messages={
        "role": "user",
        "content": [
            {"type": "text", "text": args[1]},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ],
    }
    llm.messages.append(messages)
    response = llm.response()
            
    return response
if __name__ == '__main__':
    print(watch(('user/2025-06-23 15:25:49.png','分析一下这幅图的风格')))