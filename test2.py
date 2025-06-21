import os
import time
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from threading import Thread

app = Flask(__name__)

# 模拟AI响应的预设回复
AI_RESPONSES = [
    "我理解你的问题，让我思考一下...",
    "这是一个很好的问题，我需要一些时间来组织答案。",
    "根据我的分析，这个问题可以从多个角度来看待。",
    "我建议你可以尝试...",
    "这是一个复杂的问题，不过我可以提供一些见解。",
    "很抱歉，我不理解这个问题。你可以换一种方式提问吗？",
    "这个问题超出了我的知识范围，不过我可以帮你查找相关信息。"
]

# 存储对话历史
chat_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({
            'success': False,
            'error': '请输入消息内容'
        })
    
    # 添加用户消息到历史
    chat_entry = {
        'user': user_message,
        'ai': '',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    chat_history.append(chat_entry)
    
    # 根据用户消息内容生成不同的回复
    if "你好" in user_message or "hi" in user_message.lower() or "hello" in user_message.lower():
        response = "你好！有什么我可以帮助你的吗？"
    elif "介绍" in user_message or "功能" in user_message:
        response = "我是一个基于人工智能的对话助手，可以回答问题、提供建议、进行闲聊等。请问有什么我可以帮助你的？"
    elif "时间" in user_message or "日期" in user_message:
        now = datetime.now()
        response = f"现在的时间是 {now.strftime('%Y年%m月%d日 %H:%M:%S')}"
    else:
        response = random.choice(AI_RESPONSES)
    
    # 模拟思考时间
    time.sleep(1)
    
    # 更新AI回复
    chat_entry['ai'] = response
    
    return jsonify({
        'success': True,
        'response': response,
        'timestamp': chat_entry['timestamp']
    })

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify({
        'success': True,
        'history': chat_history
    })

if __name__ == '__main__':
    # 创建模板文件夹
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 创建HTML模板文件
    template_path = os.path.join('templates', 'index.html')
    if not os.path.exists(template_path):
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI对话助手</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#165DFF',
                        secondary: '#0CB577',
                        neutral: {
                            100: '#F5F7FA',
                            200: '#E5E6EB',
                            300: '#C9CDD4',
                            400: '#86909C',
                            500: '#4E5969',
                            600: '#272E3B',
                            700: '#1D2129',
                        }
                    },
                    fontFamily: {
                        inter: ['Inter', 'system-ui', 'sans-serif'],
                    },
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer utilities {
            .content-auto {
                content-visibility: auto;
            }
            .scrollbar-hide {
                -ms-overflow-style: none;
                scrollbar-width: none;
            }
            .scrollbar-hide::-webkit-scrollbar {
                display: none;
            }
            .text-shadow {
                text-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .bg-gradient-chat {
                background: linear-gradient(180deg, rgba(245,247,250,1) 0%, rgba(255,255,255,1) 100%);
            }
            .message-appear {
                animation: fadeIn 0.3s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .typing-indicator {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 8px 16px;
                background: rgba(255,255,255,0.15);
                border-radius: 25px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                margin: 8px 0;
            }
            .typing-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: #4E5969;
                animation: typing-pulse 1.4s infinite ease-in-out both;
            }
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            .typing-dot:nth-child(3) { animation-delay: 0s; }
            @keyframes typing-pulse {
                0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
                40% { transform: scale(1.0); opacity: 1; }
            }
        }
    </style>
</head>
<body class="font-inter bg-neutral-100 text-neutral-700 min-h-screen flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-sm z-10">
        <div class="container mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                    <i class="fa fa-comments text-white text-xl"></i>
                </div>
                <h1 class="text-xl font-semibold text-neutral-700">AI对话助手</h1>
            </div>
            <div class="flex items-center space-x-4">
                <button class="text-neutral-500 hover:text-primary transition-colors duration-200">
                    <i class="fa fa-question-circle text-lg"></i>
                </button>
                <div class="w-8 h-8 rounded-full bg-neutral-200 overflow-hidden">
                    <img src="https://picsum.photos/200/200?random=user" alt="用户头像" class="w-full h-full object-cover">
                </div>
            </div>
        </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-grow flex flex-col max-w-6xl mx-auto w-full px-4 py-6">
        <!-- 对话历史区域 -->
        <div id="chat-history" class="flex-grow overflow-y-auto scrollbar-hide bg-white rounded-xl shadow-sm p-4 mb-6 max-h-[calc(100vh-200px)]">
            <!-- 欢迎消息 -->
            <div class="flex items-start mb-6 message-appear">
                <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                    <i class="fa fa-robot text-white"></i>
                </div>
                <div class="ml-3 bg-neutral-100 rounded-lg rounded-tl-none p-4 max-w-[80%]">
                    <p class="text-neutral-700">你好！我是AI对话助手，有什么可以帮助你的吗？</p>
                    <div class="text-xs text-neutral-400 mt-1 text-right">刚刚</div>
                </div>
            </div>
        </div>

        <!-- 输入区域 -->
        <div class="bg-white rounded-xl shadow-sm p-4">
            <div class="flex items-center space-x-3">
                <div class="flex-grow relative">
                    <textarea id="message-input" rows="1" placeholder="输入消息..." class="w-full resize-none border-0 focus:ring-0 py-2 px-4 bg-neutral-100 rounded-lg focus:bg-neutral-200 transition-colors duration-200 pr-10"></textarea>
                    <div class="absolute right-3 top-1/2 transform -translate-y-1/2 text-neutral-400">
                        <span id="char-count">0</span>/2000
                    </div>
                </div>
                <button id="send-button" class="p-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
                    <i class="fa fa-paper-plane"></i>
                </button>
            </div>
            <div class="mt-2 text-xs text-neutral-400 flex justify-between">
                <div>支持 Markdown 语法</div>
                <div>按 Enter 发送，Shift+Enter 换行</div>
            </div>
        </div>
    </main>

    <script>
        // 更新字符计数
        document.getElementById('message-input').addEventListener('input', function() {
            const count = this.value.length;
            document.getElementById('char-count').textContent = count > 2000 ? '2000' : count;
            if (count > 2000) {
                this.value = this.value.substring(0, 2000);
            }
        });

        // 发送消息
        document.getElementById('send-button').addEventListener('click', sendMessage);
        document.getElementById('message-input').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            if (!message) return;

            // 显示用户消息
            const chatHistory = document.getElementById('chat-history');
            const timestamp = new Date().toLocaleTimeString();
            
            const userMessageHtml = `
                <div class="flex items-start justify-end mb-6 message-appear">
                    <div class="mr-3 bg-primary text-white rounded-lg rounded-tr-none p-4 max-w-[80%]">
                        <p>${message}</p>
                        <div class="text-xs text-white/70 mt-1 text-right">${timestamp}</div>
                    </div>
                    <div class="w-10 h-10 rounded-full bg-neutral-200 overflow-hidden flex-shrink-0">
                        <img src="https://picsum.photos/200/200?random=user" alt="用户头像" class="w-full h-full object-cover">
                    </div>
                </div>
            `;
            
            chatHistory.insertAdjacentHTML('beforeend', userMessageHtml);
            chatHistory.scrollTop = chatHistory.scrollHeight;
            input.value = '';
            document.getElementById('char-count').textContent = '0';
            
            // 显示"正在输入"状态
            const typingHtml = `
                <div id="typing-indicator" class="flex items-start mb-6 message-appear">
                    <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                        <i class="fa fa-robot text-white"></i>
                    </div>
                    <div class="ml-3 bg-neutral-100 rounded-lg rounded-tl-none p-4 max-w-[80%] typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            `;
            
            chatHistory.insertAdjacentHTML('beforeend', typingHtml);
            chatHistory.scrollTop = chatHistory.scrollHeight;
            
            // 发送消息到服务器
            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            })
            .then(response => response.json())
            .then(data => {
                // 移除"正在输入"状态
                const typingIndicator = document.getElementById('typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                
                if (data.success) {
                    // 显示AI回复
                    const aiMessageHtml = `
                        <div class="flex items-start mb-6 message-appear">
                            <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                                <i class="fa fa-robot text-white"></i>
                            </div>
                            <div class="ml-3 bg-neutral-100 rounded-lg rounded-tl-none p-4 max-w-[80%]">
                                <p class="text-neutral-700">${data.response}</p>
                                <div class="text-xs text-neutral-400 mt-1 text-right">${data.timestamp}</div>
                            </div>
                        </div>
                    `;
                    
                    chatHistory.insertAdjacentHTML('beforeend', aiMessageHtml);
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                } else {
                    // 显示错误消息
                    alert(data.error);
                }
            })
            .catch(error => {
                // 移除"正在输入"状态
                const typingIndicator = document.getElementById('typing-indicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
                
                alert('发送消息时发生错误: ' + error.message);
            });
        }

        // 页面加载时获取历史消息
        window.addEventListener('load', function() {
            fetch('/get_history')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.history) {
                    const chatHistory = document.getElementById('chat-history');
                    // 清空欢迎消息
                    chatHistory.innerHTML = '';
                    
                    // 添加历史消息
                    data.history.forEach(entry => {
                        if (entry.user && entry.ai) {
                            // 添加用户消息
                            const userMessageHtml = `
                                <div class="flex items-start justify-end mb-6 message-appear">
                                    <div class="mr-3 bg-primary text-white rounded-lg rounded-tr-none p-4 max-w-[80%]">
                                        <p>${entry.user}</p>
                                        <div class="text-xs text-white/70 mt-1 text-right">${entry.timestamp}</div>
                                    </div>
                                    <div class="w-10 h-10 rounded-full bg-neutral-200 overflow-hidden flex-shrink-0">
                                        <img src="https://picsum.photos/200/200?random=user" alt="用户头像" class="w-full h-full object-cover">
                                    </div>
                                </div>
                            `;
                            
                            // 添加AI回复
                            const aiMessageHtml = `
                                <div class="flex items-start mb-6 message-appear">
                                    <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                                        <i class="fa fa-robot text-white"></i>
                                    </div>
                                    <div class="ml-3 bg-neutral-100 rounded-lg rounded-tl-none p-4 max-w-[80%]">
                                        <p class="text-neutral-700">${entry.ai}</p>
                                        <div class="text-xs text-neutral-400 mt-1 text-right">${entry.timestamp}</div>
                                    </div>
                                </div>
                            `;
                            
                            chatHistory.insertAdjacentHTML('beforeend', userMessageHtml);
                            chatHistory.insertAdjacentHTML('beforeend', aiMessageHtml);
                        }
                    });
                    
                    // 如果没有历史消息，添加欢迎消息
                    if (data.history.length === 0) {
                        const welcomeHtml = `
                            <div class="flex items-start mb-6 message-appear">
                                <div class="w-10 h-10 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
                                    <i class="fa fa-robot text-white"></i>
                                </div>
                                <div class="ml-3 bg-neutral-100 rounded-lg rounded-tl-none p-4 max-w-[80%]">
                                    <p class="text-neutral-700">你好！我是AI对话助手，有什么可以帮助你的吗？</p>
                                    <div class="text-xs text-neutral-400 mt-1 text-right">刚刚</div>
                                </div>
                            </div>
                        `;
                        chatHistory.insertAdjacentHTML('beforeend', welcomeHtml);
                    }
                    
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }
            })
            .catch(error => {
                console.error('获取历史消息时发生错误:', error);
            });
        });
    </script>
</body>
</html>""")
    
    print("服务器启动中，请访问 http://localhost:5000")
    app.run(debug=True)