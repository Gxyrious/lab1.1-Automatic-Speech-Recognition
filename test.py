import wave
import speech_recognition as sr

# Working with audio files
r = sr.Recognizer()
speech = sr.AudioFile('audio.wav')
with speech as source:
    audio = r.record(source)
print(r.recognize_sphinx(audio))

# Working with Microphones
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)
    print("请开始讲话：")
    audio = r.listen(source)
    print("识别结果：")
    text = r.recognize_sphinx(audio)
    print(text)
    
    # 保存录音文件
    with wave.open("audio.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(audio.sample_width)
        f.setframerate(audio.sample_rate)
        f.writeframes(audio.get_raw_data())