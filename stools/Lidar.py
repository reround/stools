# 激光雷达的一些参数计算

import numpy as np
import matplotlib.pyplot as plt


def power_recv_ext(
    pt: float = 50e-3,
    R: float = 1,
    D: float = 0.01,
    rho_ext: float = 1,
    eta_a: float = 1,
    eta_s: float = 1,
) -> float:
    """计算扩展目标的接收信号功率（扩展目标雷达公式）

    Parameters
    ----------
    pt : float, optional
        发射功率(W), by default 50e-3
    R : float, optional
        目标距离(m), by default 1
    D : float, optional
        接收孔径(m), by default 0.01
    rho_ext : float, optional
        扩展目标的平均反射系数, by default 1
    eta_a : float, optional
        大气传输效率, by default 1
    eta_s : float, optional
        系统传输效率, by default 1

    Returns
    -------
    float
        接收信号功率
    """
    te = np.pi * pt * rho_ext * D**2 * eta_a * eta_s
    return te / ((4 * R) ** 2)


def distance_power_recv_ext(
    pr: float,
    pt: float = 50e-3,
    D: float = 0.01,
    rho_ext: float = 1,
    eta_a: float = 1,
    eta_s: float = 1,
):
    """计算扩展目标接收信号功率的距离

    Parameters
    ----------
    pr : float
        发射功率(W)
    pt : float, optional
        目标距离(m), by default 50e-3
    D : float, optional
        接收孔径(m), by default 0.01
    rho_ext : float, optional
        扩展目标的平均反射系数, by default 1
    eta_a : float, optional
        大气传输效率, by default 1
    eta_s : float, optional
        系统传输效率, by default 1

    Returns
    -------
    _type_
        距离
    """

    te = np.pi * pt * rho_ext * D**2 * eta_a * eta_s
    fourR_2 = te / pr
    fourR = np.sqrt(fourR_2)
    return fourR / 4


# 探测器参数计算
def cal_i_th_sq(B: float = 80e6, R_L: float = 50, T: float = 298.15) -> float:
    """计算热噪声电流的均方值, 单位 A^2

    Parameters
    ----------
    B : float, optional
        带宽, by default 80e6
    R_L : float, optional
        电阻, by default 50
    T : float, optional
        温度 (K), by default 298.15

    Returns
    -------
    float
        电流的均方值
    """
    return 4 * k * T * B / R_L


def cal_i_sh_sq(B: float = 80e6, R_L: float = 50, pl: float = 1e-3) -> float:
    """计算散粒噪声平方值, 单位 A^2

    Parameters
    ----------
    B : float, optional
        带宽, by default 80e6
    R_L : float, optional
        电阻, by default 50
    pl : float, optional
        本振光功率, by default 1e-3

    Returns
    -------
    float
        散粒噪声平方值
    """
    return 2 * q * R_L * pl**2 * B


if __name__ == "__main__":
    pass
    r = np.linspace(0.1, 40, 1000)
    pr = power_recv_ext(R=r)
    plt.plot(r, pr * 1e9)
    plt.xlabel("distance(m)")
    plt.ylabel("power(nW)")
    plt.show()
