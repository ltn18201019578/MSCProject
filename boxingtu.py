import librosa
import librosa.display
import matplotlib.pyplot as plt

# 文件路径
file_path = r'C:\Users\18201\OneDrive\桌面\study\final project\trainData4\20170001P00001I0001.wav'

# 加载音频文件
y, sr = librosa.load(file_path, sr=None)

# 绘制波形图
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Waveform of 20170001P00002A0056.wav')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()
