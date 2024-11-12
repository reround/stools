import os, shutil
from pathlib import Path


def get_file_list(dir_path: str, join_path: bool = False) -> list[str]:
    """获取文件列表

    :param str dir_path: 目录路径
    :param bool join_path: 返回列表是否添加目录路径
    :return List[str]: 文件列表
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


def get_dir_list(dir_path: str, join_path: bool = False) -> list[str]:
    """获取目录列表

    :param str dir_path: 目录路径
    :param bool join_path: 返回列表是否添加目录路径
    :return List[str]: 目录列表
    """
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"dir not found: {dir_path}")

    if join_path:
        return [
            os.path.join(dir_path, d)
            for d in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, d))
        ]
    else:
        return [
            d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))
        ]


def get_file_list_with_str(
    dir_path: str,
    start_str: str = "",
    end_str: str = "",
    with_ext: bool = False,
    ext: str = None,
) -> list:
    """获取目录中以指定字符串结尾的文件列表

    :param str dir_path: 目录路径
    :param str start_str: 起始字符串, defaults to ""
    :param str end_str: 结尾字符串, defaults to ""
    :param bool with_ext: 结尾字符串是否包含扩展名, defaults to False
    :param str ext: 扩展名, defaults to "txt"
    :return list: 以指定字符串结尾的文件列表
    """
    file_list = get_file_list(dir_path)
    if start_str != "":  # 筛选起始字符串为 start_str 的文件
        file_list = [f for f in file_list if f.startswith(start_str)]

    if ext is not None:  # 筛选扩展名为 ext 的文件
        if not ext[0] == ".":
            ext = "." + ext
        file_list = [f for f in file_list if f.endswith(ext)]
    if not with_ext:  # 筛选不带扩展名的文件,以 end_str 结尾的文件
        file_list = [
            os.path.join(dir_path, f)
            for f in file_list
            if f[: f.rfind(".")].endswith(end_str)
        ]
    else:  # 筛选带扩展名为 ext ,以 end_str 结尾的文件
        if end_str != "":
            file_list = [
                os.path.join(dir_path, f) for f in file_list if f.endswith(end_str)
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
    return [os.path.join(dir_path, d) for d in dir_list if d.endswith(end_str)]


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
        shutil.move(f, dir_path)
        print(f"move file: {f} to dir: {dir_path}")


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
    # xx = get_file_list_with_end_str("stools/assets/test", "for_test")
    # move_file_list_to_dir("test", xx)

    # dirs = get_dir_list("stools/assets/test")
    # print(dirs)
    # batch_touch("stools/assets/test", suffix="dfsfa")
    # xx = get_file_list_with_end_str("stools/assets/test", "dfsfa")
    # copy_file_list_to_dir("./test", xx)
    # print(get_file_list("stools/assets/test"))
    # print(get_dir_list("stools/assets/test"))
    # print(get_file_list_with_end_str("stools/assets/test", "dfsfa"))
    # print(get_dir_list_with_str("stools/assets/test", start_str="w", end_str=")"))
    dl = get_dir_list("stools/assets")
    print(dl)
    for d in dl:
        print(get_file_list("stools/assets/test"))
    # if "xxcc".startswith("xx"):
    #     print("yes")
    # else:
    #     print("no")
    pass
