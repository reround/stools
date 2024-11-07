"""

TODO: 针对 matplotlib 做的一些调整
    
1. 设置中文字体为宋体
2. 用来正常显示负号
3. 设置字体大小为 14

"""

import matplotlib.pyplot as plt
import matplotlib


matplotlib.rcParams["font.family"] = ["SimSun"]  # 设置中文字体为宋体
matplotlib.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号
matplotlib.rcParams["font.size"] = 14.5  # 设置字体大小为 14.5


def set_font_family(family: str):
    """设置字体

    :param str family: 字体名
    """

    matplotlib.rcParams["font.family"] = [family]


def set_label_font_size(size: float):
    """设置标签字体大小

    :param float size: 字体大小
    """
    matplotlib.rcParams["font.size"] = size


if __name__ == "__main__":
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.xlabel("横坐标")
    plt.ylabel("纵坐标")
    plt.title("标题")
    plt.show()
