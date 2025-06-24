import pyaudio
import numpy as np
import wave
import os

def record_and_save_audio(output_file="recording.wav", duration=10):
    # 录音参数
    chunk = 1024  # 每个缓冲区的帧数
    sample_format = pyaudio.paInt16  # 采样格式
    channels = 1  # 声道
    fs = 44100  # 采样率 (Hz)
    seconds = duration  # 录音时长（秒）

    # 打开录音设备
    p = pyaudio.PyAudio()  # 创建PyAudio实例
    print("开始录音...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # 存储录音数据的列表

    # 录音过程
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    print("录音结束.")

    # 停止并关闭流
    stream.stop_stream()
    stream.close()
    # 关闭PyAudio实例
    p.terminate()

    # 保存录音到WAV文件
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"录音已保存到 {output_file}")

if __name__ == "__main__":
    # 设置录音时长（秒）和输出文件名
    record_duration = 5  # 录音5秒
    output_filename = "recording.wav"

    # 调用函数开始录音
    record_and_save_audio(output_file=output_filename, duration=record_duration)