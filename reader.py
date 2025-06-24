import os
import docx
import pdfplumber

def extract_text(filename):
    """
    从txt, docx或pdf文件中提取文本，保留原始格式
    
    参数:
        filename (str): 文件路径
        
    返回:
        str: 提取的文本内容
        
    异常:
        ValueError: 不支持的文件格式
        FileNotFoundError: 文件不存在
    """
    # 检查文件是否存在
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"文件不存在: {filename}")
    
    # 获取文件扩展名
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    # 处理不同文件格式
    if ext == '.txt':
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
            
    elif ext == '.docx':
        doc = docx.Document(filename)
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        
    elif ext == '.pdf':
        full_text = []
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                # 提取页面文本（保留布局）
                text = page.extract_text()
                if text:  # 确保页面有文本内容
                    full_text.append(text)
        return '\n'.join(full_text)
        
    else:
        raise ValueError(f"不支持的文件格式: {ext}。支持格式: .txt, .docx, .pdf")

# 使用示例
if __name__ == "__main__":
    try:
        text = extract_text("resources/knowledge/user/1.docx")
        print("提取内容:")
        print(text)
    except Exception as e:
        print(f"错误: {e}")