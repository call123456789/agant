import speech_recognition as sr

def recognize_speech(file_path):
    try:
        # 创建一个识别器实例
        recognizer = sr.Recognizer()

        # 将音频文件加载到识别器中
        with sr.AudioFile(file_path) as source:
            # 读取音频数据
            audio_data = recognizer.record(source)
            # 使用Google Web Speech API识别，这需要网络连接
            text = recognizer.recognize_google(audio_data, language="zh-CN")  # 可以修改为其他语言
            print(f"识别的文本: {text}")
            return f"识别的文本: {text}"

    except sr.UnknownValueError:
        print("无法识别音频中的语音。")
        return "无法识别音频中的语音。"
    except sr.RequestError as e:
        print(f"请求识别服务时出错; {e}")
        return f"请求识别服务时出错; {e}"
    except Exception as e:
        print(file_path)
        print(f"处理音频时出错: {e}")
        return f"处理音频时出错: {e}"

if __name__ == "__main__":
    # 替换为你的音频文件路径
    file_path = "resources/uploads/recording_20250622_224354_fa561b54.wav"
    recognize_speech(file_path)