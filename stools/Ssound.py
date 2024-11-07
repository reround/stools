import matplotlib.pyplot as plt
import matplotlib as mpl
import wave
import pyaudio
import numpy as np


class Sound:
    """声音类，用于处理音频流。

    Attributes
    ----------
    p : PyAudio
        PyAudio 实例。
    rate : int
        采样速率。
    chunk : int
        块大小。
    format : int
        音频格式。
    channal : int
        声道数。
    """

    def __init__(
        self,
        rate: int = 44100,
        chunk: int = 1024,
        format_=pyaudio.paInt16,
        channal: int = 1,
    ):
        """初始化音频数据

        Parameters
        ----------
        rate : int, optional
            采样速率, by default 44100
        chunk : int, optional
            块大小, by default 1024
        format_ : _type_, optional
            格式, by default pyaudio.paInt16
        channal : int, optional
            声道数, by default 1
        """
        self.p = pyaudio.PyAudio()  # 实例化PyAudio类
        self.rate = rate  # 采样速率
        self.chunk = chunk  # 块大小
        self.format = format_  # 格式
        self.channal = channal  # 声道数

    def open_stream(self, write=False):
        """打开流

        Parameters
        ----------
        write : bool, optional
            是否能够写入, by default False
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
        """_summary_
        播放 np.ndarray 形式的音频
        目前是整体处理，文件肯定不能特别大

        Parameters
        ----------
        array : np.ndarray
            np.ndarray 序列
        rate : int
            采样速率
        level : float, optional
            声音等级(0-30), 0 为不做变化, by default 1.0
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

        Parameters
        ----------
        array : np.ndarray
            转换的 np.ndarray
        filename : str
            目标文件名称
        level : float, optional
            声音等级(0-30), 0 为不做变化, by default 1.0
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
        目前是整体处理，文件肯定不能特别大


        Parameters
        ----------
        filename : str
            保存的文件名
        record_seconds : int
            录音时间
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

    def create_f_voice(
        self,
        fv: float = 440,
        filename: str = None,
        sec: float = 2,
        fs: int = 22050,
        level: float = 1.0,
    ):
        """生成指定频率，指定长度的音频

        Parameters
        ----------
        fv : float, optional
            频率, by default 440
        filename : str, optional
            文件名, by default None
        sec : float, optional
            时间 (s), by default 200
        fs : int, optional
            音频采样率, by default 22050
        level : float, optional
            声音等级(0<level<=30),by default 1.0
        """
        x = np.linspace(0, sec, int(22050 * sec))
        b = np.sin(2 * np.pi * fv * x) * 1000 * level
        s = Sound(rate=fs)
        if filename is None:
            filename = f"sin_{fv}Hz.wav"
        s.to_wav_from_ndarray(b, filename, level=level)

    def create_wave_voice(
        self,
        wave_form,
        rate: int = 44100,
        filename: str = None,
        level: float = 10.0,
    ):
        pass

    @staticmethod
    def load_wav(filename: str) -> tuple:
        """加载 wav 文件

        Parameters
        ----------
        filename : str
            文件名

        Returns
        -------
        tuple
            (音频数据, 采样率)
        """

        print(filename)
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

    def test(self, t: str = "Test function", a: int = 0) -> int:
        """测试函数

        :param str t: 测试字符串超长注释版，用来看看输出的效果，这个是不带换行的, defaults to "Test function"
        :param int a: 测试数字, defaults to 0
        :return int: 测试数字
        """
        print("------------ Test ------------")
        return a + 1


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
