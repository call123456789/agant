from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
import uuid
import datetime
from llm2 import LLM
from prompt import planner_prompt
from tool import tools
from knowledge import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'resources/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
knowledge_files = {}
app.config['KNOWLEDGE_BASE_FOLDER'] = 'resources/knowledge/user'
API_CONFIG_PATH = 'API.json'

# 存储对话历史
conversations = []
agent = LLM(task= planner_prompt, tools=tools)

@app.route('/')
def index():
    return render_template('index.html', conversations=conversations)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('message')
    files = request.files.getlist('file')
    
    # 保存上传的文件
    saved_files = []
    for file in files:
        if file.filename:
            filename = f"{datetime.now().strftime("%H:%M:%S")}_{uuid.uuid4().hex[:8]}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_files.append(filename)
    
    # 创建唯一的消息ID
    user_msg_id = str(uuid.uuid4())
    
    # 添加用户消息到对话历史
    user_entry = {
        'id': user_msg_id,
        'sender': 'user',
        'text': user_input,
        'files': saved_files,
        'time': datetime.now().strftime("%H:%M:%S")
    }
    conversations.append(user_entry)
    
    # 返回用户消息和AI消息的ID
    return jsonify({
        'user_message': user_entry,
        'ai_msg_id': str(uuid.uuid4())  # 为AI响应创建唯一ID
    })

@app.route('/stream_ai_response')
def stream_ai_response():
    """流式传输AI响应"""
    user_input = request.args.get('user_input', '')
    files = request.args.get('files', '')
    ai_msg_id = request.args.get('ai_msg_id', '')
    
    # 将文件字符串转换为列表
    files_list = files.split(',') if files else []
    if files_list:
        user_input += f"\n用户上传了 {len(files_list)} 个文件：{',  '.join(files_list)}"
    
    # 模拟AI流式响应
    response_fragments = agent.response(user_input)
    
    def generate():
        # 发送初始空消息以在UI中创建AI消息框
        yield f"event: start\ndata: \n\n"
        
        # 流式发送每个片段
        for fragment in response_fragments:
            # 将换行符替换为特殊标记
            escaped_fragment = fragment.replace('\n', '##NEWLINE##')
            yield f"data: {escaped_fragment}\n\n"
        
        # 发送结束信号
        yield f"event: end\ndata: \n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')
@app.route('/tools')
def tools():
    return render_template('tools.html')

# 构建知识库界面
@app.route('/build-knowledge')
def build_knowledge():
    return render_template('build-knowledge.html')

# 上传知识文件
@app.route('/upload_knowledge', methods=['POST'])
def upload_knowledge():
    files = request.files.getlist('knowledge_files')
    saved_files = []
    
    for file in files:
        if file.filename == '':
            continue
            
        # 生成安全的文件名
        filename = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_{file.filename}"
        file_path = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], filename)
        file.save(file_path)
        
        # 记录文件信息
        file_info = {
            'name': filename,
            'size': os.path.getsize(file_path),
            'status': 'processing'  # 初始状态为处理中
        }
        knowledge_files[filename] = file_info
        saved_files.append(file_info)
        
        # 这里调用你的知识库处理代码
        json_name = process_text(extract_text(file_path))
        
        # 模拟处理完成（实际应用中应异步处理）
        knowledge_files[filename]['status'] = 'completed'
        knowledge_files[filename]['json_name'] = json_name
    
    return jsonify({
        'status': 'success',
        'files': saved_files
    })

# 获取知识文件列表
@app.route('/get_knowledge_files', methods=['GET'])
def get_knowledge_files():
    # 获取文件系统中的实际文件列表
    actual_files = []
    if os.path.exists(app.config['KNOWLEDGE_BASE_FOLDER']):
        for filename in os.listdir(app.config['KNOWLEDGE_BASE_FOLDER']):
            file_path = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], filename)
            if os.path.isfile(file_path):
                # 使用存储的状态信息，如果不存在则创建
                if filename not in knowledge_files:
                    knowledge_files[filename] = {
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'status': 'completed'  # 假设已处理
                    }
                actual_files.append(knowledge_files[filename])
    
    return jsonify(actual_files)

# 删除知识文件
@app.route('/delete_knowledge_file', methods=['POST'])
def delete_knowledge_file():
    data = request.get_json()
    filename = data.get('filename')
    
    
    file_path = os.path.join(app.config['KNOWLEDGE_BASE_FOLDER'], filename)

    try:
        # 删除物理文件
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 从内存字典中移除记录
        if filename in knowledge_files:
            print(knowledge_files[filename])
            if 'json_name' in knowledge_files[filename]:
                if os.path.exists(knowledge_files[filename]['json_name']):
                    os.remove(knowledge_files[filename]['json_name'])

            del knowledge_files[filename]
            
        return jsonify({
            'status': 'success',
            'message': f'File {filename} deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete file: {str(e)}'
        }), 500

# 添加设置路由
@app.route('/setting', methods=['GET'])
def setting_page():
    """设置页面"""
    try:
        with open(API_CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except:
        config = {}
    
    return render_template('setting.html', config=config)

@app.route('/save_setting', methods=['POST'])
def save_setting():
    """保存API设置"""
    data = request.get_json()
    
    # 验证数据
    required_keys = ['talk-model', 'image-model', 'embedding-model', 
                     'api_key', 'base_url', 'temprature']
    if not all(key in data for key in required_keys):
        return jsonify({'status': 'error', 'message': '缺少必要的参数'}), 400
    
    # 保存到文件
    try:
        with open(API_CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)