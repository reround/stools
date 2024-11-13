import os, shutil
from pathlib import Path


def get_file_list(dir_path: str, join_path: bool = False) -> list:
    """获取文件列表

    :param str dir_path: 目录路径
    :param bool join_path: 返回列表是否添加目录路径
    :return list: 文件列表

    >>> dir_path = os.path.dirname(__file__)
    >>> f_list = get_file_list(os.path.join(dir_path, "test"), join_path=True)
    >>> len(f_list)
    5
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"dir not found: {dir_path}")

    if join_path:
        return [
            os.path.join(dir_path, d)
            for d in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, d))
        ]
    else:
        return [
            d for d in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, d))
        ]


def get_dir_list(dir_path: str, join_path: bool = False) -> list:
    """获取目录列表

    :param str dir_path: 目录路径
    :param bool join_path: 返回列表是否添加目录路径
    :return list: 目录列表

    >>> dir_path = os.path.dirname(__file__)
    >>> d_list = get_dir_list(os.path.join(dir_path, "test"), join_path=True)
    >>> len(d_list)
    5
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"dir not found: {dir_path}")

    if join_path:
        return [
            str(Path(os.path.join(dir_path, d)))
            for d in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, d))
        ]
    else:
        return [
            str(Path(d))
            for d in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, d))
        ]


def add_parent_name_to_file_list(file_list: list, mod: str = "prefix"):
    """重命名文件列表，给文件列表添加父目录名

    :param list file_list: 文件列表
    :param str mod: 添加方式, "prefix" 或 "suffix", defaults to "prefix"
    :raises ValueError: ValueError
    """
    for f in file_list:
        parent_dir = os.path.dirname(f)
        f_basename = os.path.basename(f)
        parent_name = os.path.basename(os.path.dirname(f))
        if mod == "prefix":
            new_name = os.path.join(parent_dir, parent_name + "_" + f_basename)
        elif mod == "suffix":
            new_name = os.path.join(parent_dir, f_basename + "_" + parent_name)
        else:
            raise ValueError(f"mod must be 'prefix' or 'suffix', but got {mod}")

        # 重命名文件
        try:
            os.rename(f, new_name)
            print(f"file: {f} renamed to: {new_name}")
        except OSError as e:
            print(e)


def get_file_list_with_str(
    dir_path: str,
    start_str: str = "",
    end_str: str = "",
    with_ext: bool = False,
) -> list:
    """获取目录中以指定字符串结尾的文件列表

    :param str dir_path: 目录路径
    :param str start_str: 起始字符串, defaults to ""
    :param str end_str: 结尾字符串, defaults to ""
    :param bool with_ext: 结尾字符串是否包含扩展名, defaults to False
    :return list: 以指定字符串结尾的文件列表
    """
    file_list = get_file_list(dir_path)
    if start_str != "":  # 筛选起始字符串为 start_str 的文件
        file_list = [str(Path(f)) for f in file_list if f.startswith(start_str)]

    if not with_ext:  # 筛选不带扩展名的文件,以 end_str 结尾的文件
        file_list = [
            str(Path(os.path.join(dir_path, f)))
            for f in file_list
            if f[: f.rfind(".")].endswith(end_str)
        ]
    else:  # 筛选带扩展名为 ext ,以 end_str 结尾的文件
        if end_str != "":
            file_list = [
                str(Path(os.path.join(dir_path, f)))
                for f in file_list
                if f.endswith(end_str)
            ]
    return file_list


def get_dir_list_with_str(
    dir_path: str, start_str: str = "", end_str: str = ""
) -> list:
    """获取目录中以指定字符串结尾的目录列表

    :param str dir_path: 目录路径
    :param str start_str: 起始字符串, defaults to ""
    :param str end_str: 结尾字符串, defaults to ""
    :return list: 以指定字符串结尾的目录列表
    """
    dir_list = get_dir_list(dir_path)
    if end_str != "":  # 筛选起始字符串为 start_str 的文件
        dir_list = [d for d in dir_list if d.startswith(start_str)]
    return [
        str(Path(os.path.join(dir_path, d))) for d in dir_list if d.endswith(end_str)
    ]


def get_file_list_with_ext(dir_path: str, ext: str, join_path: bool = False) -> list:
    """获取目录中以指定扩展名结尾的文件列表

    :param str dir_path: 目录路径
    :param str ext: 扩展名
    :param bool join_path: 返回列表是否添加目录路径
    :return list: 以指定扩展名结尾的文件列表
    """
    file_list = get_file_list(dir_path, join_path=join_path)
    return [str(Path(f)) for f in file_list if f.split(".")[-1] == ext]


def move_file_list_to_dir(dir_path: str, file_list: list):
    """将文件列表移动到指定目录

    :param str dir_path: 目标目录路径
    :param list file_list: 文件列表
    """
    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"create dir: {dir_path}")
    # 移动文件
    for f in file_list:
        try:
            shutil.move(f, dir_path)
            print(f"move file: {f} to dir: {dir_path}")
        except Exception as e:
            print(e)


def copy_file_list_to_dir(dir_path: str, file_list: list):
    """将文件列表复制到指定目录

    :param str dir_path: 目标目录路径
    :param list file_list: 文件列表
    """
    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"create dir: {dir_path}")
    # 复制文件
    for f in file_list:
        shutil.copy(f, dir_path)
        print(f"copy file: {f} to dir: {dir_path}")


def batch_touch(
    dir_path: str = "./",
    prefix: str = "",
    suffix: str = "",
    start: int = 1,
    end: int = 10,
    step: int = 1,
    ext: str = "txt",
):
    """批量创建文件

    :param str dir_path: 输出路径, defaults to "./"
    :param str prefix: 文件名序号前缀, defaults to ""
    :param str suffix: 文件名序号后缀, defaults to ""
    :param int start: 序号起始值, defaults to 1
    :param int end: 序号结束值, defaults to 10
    :param int step: 序号步长, defaults to 1
    :param str ext: 扩展名, defaults to "txt"
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"create dir: {dir_path}")
    for i in range(start, end + 1, step):
        file_name = os.path.join(dir_path, prefix + f"{i:03d}" + suffix + "." + ext)
        Path(file_name).touch()
        print(f"create file: {file_name} in dir: {dir_path}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # dir_path = os.path.dirname(__file__)
    # print(dir_path)
    # f_list = get_file_list(os.path.join(dir_path, "test"), join_path=True)
    # print(len(f_list))
    # f_li = get_file_list_with_ext("./assets/test", "png", join_path=True)
    # for f in f_li:
    #     print(type(f))
    # # print(get_file_list_with_str("./assets/test", end_str=".txt", with_ext=False))
    # pass
