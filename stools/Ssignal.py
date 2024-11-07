"""

一些信号处理的工具函数

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
from scipy.signal import stft


def smooth(x: np.ndarray, M: int) -> np.ndarray:
    """平滑函数

    Parameters
    ----------
    x : np.ndarray
        需要平滑的数组
    M : int
        平滑点数

    Returns
    -------
    np.ndarray
        平滑后的数组
    """

    K = round(M / 2 - 0.1)  # M应为奇数，如果是偶数，则取大1的奇数
    lenX = len(x)
    if lenX < 2 * K + 1:
        print("数据长度小于平滑点数")
    else:
        y = np.zeros(lenX)
        for NN in range(0, lenX, 1):
            startInd = max([0, NN - K])
            endInd = min(NN + K + 1, lenX)
            y[NN] = np.mean(x[startInd:endInd])
    ##    y[0]=x[0]       #首部保持一致
    ##    y[-1]=x[-1]     #尾部也保持一致
    return y


def abs_roc(sig: np.ndarray) -> np.ndarray:
    """使信号按的变化率（"rate of change"）的绝对值变\n
    对信号求 dy -> 对 dy 取绝对值 -> 累加 abs(dy)

    Parameters
    ----------
    sig : np.ndarray
        信号序列

    Returns
    -------
    np.ndarray
        按变化率绝对值变化的信号
    """
    ds = []  # 变化率序列
    for i in range(1, len(t)):
        ds.append((sig[i] - sig[i - 1]))
    ds_abs = np.abs(ds)  # 变化率序列取绝对值
    ds_E = [0]  # 变化率绝对值变化
    for i in range(0, len(ds_abs)):
        ds_E.append(ds_E[i] + ds_abs[i])
    return np.array(ds_E)


def compare_sig_peaks(
    sig1: np.ndarray,
    sig2: np.ndarray,
    x: np.ndarray = None,
    start: int = 0,
    end: int = None,
    **kwargs,
):
    """绘图对比两个信号的峰值

    Parameters
    ----------
    sig1 : np.ndarray
        信号1
    sig2 : np.ndarray
        信号2
    x : np.ndarray
        共同的时间序列, by default None
    start : int, optional
        开始位置, by default 0
    end : int, optional
        结束位置, by default None
    ylim : tuple, optional
        y轴范围, by default None
    xlim : tuple, optional
        x轴范围, by default None
    """
    if x is None:
        x = np.arange(len(sig1))
    xlabel = kwargs.get("xlabel", "")
    label1 = kwargs.get("label1", "signal 1")
    label2 = kwargs.get("label2", "signal 2")
    title = kwargs.get("title", "")
    ylim = kwargs.get("ylim", None)
    xlim = kwargs.get("xlim", None)
    plt.figure(figsize=(10, 5))
    plt.plot(x[start:end], sig1[start:end], color="blue", label=label1)
    plt.plot(x[start:end], sig2[start:end], color="red", label=label2)
    # plt.grid()
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=16)
    plt.legend(fontsize=16)

    # 寻找峰值
    peaks, _ = find_peaks(sig1[start:end])
    for i in peaks:
        plt.annotate(
            str(x[i]),  # 注释文本
            (x[i], sig1[i]),  # 被标记的点的坐标
            textcoords="offset points",  # 文本偏移量
            xytext=(0, 10),  # 文本偏移的方向和距离
            arrowprops=dict(arrowstyle="->"),
            color="blue",
            fontsize=16,
        )  # 箭头的样式

    # 寻找峰值
    peaks, _ = find_peaks(sig2[start:end])
    for i in peaks:
        plt.annotate(
            str(x[i]),  # 注释文本
            (x[i], sig2[i]),  # 被标记的点的坐标
            textcoords="offset points",  # 文本偏移量
            xytext=(0, 10),  # 文本偏移的方向和距离
            arrowprops=dict(arrowstyle="->"),
            color="red",
            fontsize=16,
        )  # 箭头的样式
    plt.show()


def pectrum(signal: np.ndarray, sample_interval: int, isdB: bool = False):
    """绘制 signal 的傅里叶变换频谱图

    Parameters
    ----------
    signal : np.ndarray
        信号序列
    sample_interval : int
        采样间隔 ( 1/fs)
    isdB : bool, optional
        dB 显示, by default False
    """
    length = len(signal)
    if isdB:
        s_fft = 10 * np.log10(fftpack.fft(signal))
        f = fftpack.fftfreq(length, sample_interval)
    else:
        # 频域
        s_fft = fftpack.fft(signal)
        f = fftpack.fftfreq(length, sample_interval)
    mask = f > 0
    plt.plot(f[mask], abs(s_fft[mask]))
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()


def pspectrum(
    x: np.ndarray,
    fs: float,
    window="hamming",
    nperseg=256,
    noverlap=128,
    figsize=(10, 6),
    shading="gouraud",
    title="STFT Magnitude",
    *args,
    **kwargs,
):
    """绘制短时傅里叶变换图

    Parameters
    ----------
    x : np.ndarray
        信号
    fs : float
        采样率
    window : str, optional
        窗型, by default "hamming"
    nperseg : int, optional
        窗长, by default 256
    noverlap : int, optional
        重叠样本数, by default 128
    figsize : tuple, optional
        画布尺寸, by default (10, 6)
    shading : str, optional
        颜色的填充方式, by default "gouraud"
    title : str, optional
        标题, by default "STFT Magnitude"
    ylabel : str, optional
        纵轴标签, by default "Frequency [Hz]"
    xlabel : str, optional
        横轴标签, by default "Time [sec]"
    label_fontsize : str, optional
        坐标轴字体尺寸, by default 17
    tick_fontsize : str, optional
        刻度字体尺寸, by default 16
    """
    ylabel = kwargs.get("ylabel", "Frequency [Hz]")
    xlabel = kwargs.get("xlabel", "Time [sec]")
    label_fontsize = kwargs.get("label_fontsize", 17)
    tick_fontsize = kwargs.get("tick_fontsize", 16)

    plt.figure(figsize=figsize)
    freq_stft, t, Zxx = stft(x, fs, window=window, nperseg=nperseg, noverlap=noverlap)
    freq_stft = np.abs(freq_stft)
    plt.pcolormesh(t, freq_stft, np.abs(Zxx), shading=shading)
    plt.ylabel(ylabel, fontsize=label_fontsize)
    plt.xlabel(xlabel, fontsize=label_fontsize)
    plt.title(title)
    plt.colorbar(label="Magnitude")
    plt.tick_params(
        axis="both", which="major", labelsize=tick_fontsize
    )  # 设置major ticks的字体大小
    plt.tick_params(
        axis="both", which="minor", labelsize=tick_fontsize
    )  # 设置minor ticks的字体大小
    plt.show()


if __name__ == "__main__":
    pass
    a = np.array([1, 2, 3, 4, 5, 3, 2, 1, 2, 3])
    b = np.array([1, 2, 3, 4, 1, 2, 1, 1, 1, 1])
    compare_sig_peaks(a, b, ylim=(-1, 6))
