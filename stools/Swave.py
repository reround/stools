"""

TODO: 包含一些常用的波形

"""

import numpy as np


def sine(
    freq: float = 10,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成正弦波

    Parameters
    ----------
    freq : float, optional
        频率 (单位: Hz), by default 10
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，正弦波形
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = amp * np.sin(2 * np.pi * freq * t)
    return (t, s)


def cosine(
    freq: float = 10,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成余弦波

    Parameters
    ----------
    freq : float, optional
        频率 (单位: Hz), by default 10
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，余弦波形)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = amp * np.cos(2 * np.pi * freq * t)
    return (t, s)


def square(
    freq: float = 10,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成方波

    Parameters
    ----------
    freq : float, optional
        频率 (单位: Hz), by default 10
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，方波形)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = amp * np.sign(np.sin(2 * np.pi * freq * t))
    return (t, s)


def triangle(
    freq: float = 10,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成三角波

    Parameters
    ----------
    freq : float, optional
        频率 (单位: Hz), by default 10
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，三角波形)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = np.arcsin(np.sin(2 * np.pi * freq * t))
    # 纠正幅度到 amp
    s = s / (np.pi / 2) * amp

    return (t, s)


def sawtooth(
    freq: float = 10,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成锯齿波

    Parameters
    ----------
    freq : float, optional
        频率 (单位: Hz), by default 10
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，锯齿波形)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = 2 * np.pi * freq * t % (2 * np.pi)
    # 纠正幅度到 amp
    s = s / (2 * np.pi) * amp
    return (t, s)


def chirp(
    start_freq: float = 10,
    end_freq: float = 100,
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成线性振荡

    Parameters
    ----------
    start_freq : float, optional
        起始频率 (单位: Hz), by default 10
    end_freq : float, optional
        终止频率 (单位: Hz), by default 100
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，线性振荡)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = amp * np.sin(2 * np.pi * (start_freq + (end_freq - start_freq) * t) * t)
    return (t, s)


def noise(
    time: float = 1,
    fs: int = 1000,
    amp: float = 1.0,
    t: np.ndarray = None,
) -> (np.ndarray, np.ndarray):
    """生成随机噪声

    Parameters
    ----------
    time : float, optional
        时间长度 (单位: s), by default 1
    fs : int, optional
        采样率 (单位: Hz), by default 1000
    amp : float, optional
        振幅 (单位: V), by default 1.0
    t : np.ndarray, optional
        时间序列, by default None

    Returns
    -------
    (np.ndarray, np.ndarray)
        (时间序列，随机噪声)
    """
    if t is None:
        t = np.arange(0, time, 1 / fs)
    s = amp * np.random.randn(len(t))
    return (t, s)


import matplotlib.pyplot as plt

if __name__ == "__main__":
    pass

    t = np.arange(0, 2, 0.01)
    t, s = sine(freq=10, amp=1)
    plt.plot(t, s)
    plt.show()
