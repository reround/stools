import matplotlib.pyplot as plt
import matplotlib as mpl
import wave
import pyaudio
import numpy as np


class Sound:
    """声音类，用于处理音频流

    :param int rate: PyAudio 实例, defaults to 44100
    :param int chunk: 块大小, defaults to 1024
    :param _type_ format_: 音频格式, defaults to pyaudio.paInt16
    :param int channal: 声道数, defaults to 1
    """

    def __init__(
        self,
        rate: int = 44100,
        chunk: int = 1024,
        format_=pyaudio.paInt16,
        channal: int = 1,
    ):
        self.p = pyaudio.PyAudio()  # 实例化PyAudio类
        self.rate = rate  # 采样速率
        self.chunk = chunk  # 块大小
        self.format = format_  # 格式
        self.channal = channal  # 声道数

    def open_stream(self, write=False):
        """打开流

        :param bool write: 是否能够写入, defaults to False
        """
        self.stream = self.p.open(
            format=self.format,
            channels=self.channal,
            rate=self.rate,
            output=True,
            input=write,
        )

    def close_stream(self):
        """关闭流"""
        self.stream.stop_stream()
        self.stream.close()

    def play_ndarray(self, array: np.ndarray, rate: int = 44100, level: float = 1.0):
        """播放 np.ndarray 形式的音频,目前是整体处理，文件肯定不能特别大

        :param np.ndarray array: np.ndarray 序列
        :param int rate: 采样速率, defaults to 44100
        :param float level: 声音等级(0-30), 0 为不做变化, defaults to 1.0
        """
        assert level >= 0 and level <= 30, "声音等级必须在 0-30 之间"
        if level > 0:
            # 归一化
            array = array / np.max(array)
            array = array * 1e3 * level
        self.rate = rate
        array_bytes = array.astype(np.int16).tobytes()
        self.open_stream()
        self.stream.write(array_bytes)
        self.close_stream()
        # self.p.terminate()

    @staticmethod
    def to_wav_from_ndarray(
        array: np.ndarray,
        filename: str,
        level: float = 5.0,
        rate: int = 44100,
        format_=pyaudio.paInt16,
        channal: int = 1,
    ):
        """将一个 np.ndarray 保存为 wav 音频文件

        :param np.ndarray array: 转换的 np.ndarray
        :param str filename: 目标文件名称
        :param float level: 声音等级(0-30), 0 为不做变化, defaults to 5.0
        :param int rate: 采样率, defaults to 44100
        :param _type_ format_: 数据格式, defaults to pyaudio.paInt16
        :param int channal: 通道数, defaults to 1
        """
        assert level >= 0 and level <= 30, "声音等级必须在 0-30 之间"
        if level > 0:
            # 归一化
            array = array / np.max(array)
            array = array * 1e3 * level
        if filename.split(".")[-1] != "wav":
            filename += ".wav"
        array_bytes = array.astype(np.int16).tobytes()

        wf = wave.open(filename, "wb")
        wf.setnchannels(channal)
        # wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format_))
        wf.setframerate(rate)
        wf.writeframes(array_bytes)
        wf.close()

    def record(self, filename: str, record_seconds: int):
        """记录声音

        :param str filename: 保存的文件名
        :param int record_seconds: 录音时间
        """
        frames = []
        self.open_stream(input_=True)

        print("Record start ...")
        for i in range(0, int(self.rate / self.chunk * record_seconds)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        print("Record end.")
        self.close_stream()
        self.p.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channal)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(frames))
        wf.close()

    @staticmethod
    def load_wav(filename: str) -> tuple:
        """加载 wav 文件，返回 np.ndarray 数据和采样率

        :param str filename: 文件名
        :raises ValueError: _description_
        :return tuple: (音频数据, 采样率)
        """
        # 打开WAV文件
        with wave.open(filename, "rb") as wav_file:
            # 获取音频文件参数
            # n_channels: 音频文件的通道数，比如单声道（1）或立体声（2）。
            # sample_width: 每个样本的字节宽度。例如，8位音频是1字节，16位音频是2字节。
            # frame_rate: 帧率，即每秒的帧数（帧/秒），等同于采样率。
            # n_frames: 音频文件中的总帧数。
            # comptype: 压缩类型，对于未压缩的WAV文件通常是'NONE'。
            # compname: 压缩名称，对于未压缩的WAV文件通常是'not compressed'。
            n_channels, sample_width, frame_rate, n_frames, comptype, compname = (
                wav_file.getparams()
            )

            # 读取音频文件的帧数据
            frames = wav_file.readframes(n_frames)

            # 将帧数据转换为numpy数组
            # dtype根据sample_width选择，这里假设是16位PCM数据
            if sample_width == 2:
                dtype = np.int16
            elif sample_width == 4:
                dtype = np.int32
            else:
                raise ValueError("Unsupported sample width")

            audio_data = np.frombuffer(frames, dtype=dtype)

            # 如果是立体声，需要将数据reshape成2D数组
            if n_channels == 2:
                audio_data = audio_data.reshape(-1, 2)

            return audio_data, frame_rate


import matplotlib.pyplot as plt

if __name__ == "__main__":
    pass
    a, r = Sound.load_wav("./assets/notsay.wav")

    # plt.plot(a[:, 0])
    # plt.show()
    # s = Sound(rate=r)
    start = 900000
    last = 2000000
    # s.play_ndarray(a[start:last, 0], level=10)
    Sound.to_wav_from_ndarray(a[start:last, 0], "cc.wav", rate=r)

    # print(a.shape)
    # s = Sound()
    # fv = 440  # 振动频率
    # fs = 22050
    #     # sec = 2e2  # 时间 s
    #     # # x = np.linspace(0, sec, 22050 * sec)
    #     # # b = np.sin(2 * np.pi * fv * x) * 10000
    #     # # b = np.array(b)

    #     # # s.play_ndarray(b)
    # s.create_f_voice(fv, level=30)
#     # # s.creat_wav_with_ndarray(b, "xx.wav")
#     # # s.record("hello.wav", 3)
