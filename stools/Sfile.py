import os, shutil
from pathlib import Path


def get_file_list_with_end_str(
    dir_path: str, end_str: str = None, with_ext: bool = False, ext: str = None
) -> list:
    """获取目录中以指定字符串结尾的文件列表

    :param str dir_path: 目录路径
    :param str end_str: 结尾字符串, defaults to None
    :param bool with_ext: 结尾字符串是否包含扩展名, defaults to False
    :param str ext: 扩展名, defaults to "txt"
    :return list: 以指定字符串结尾的文件列表
    """
    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"create dir: {dir_path}")
    # 转换成绝对路径
    dir_path = os.path.join(os.getcwd(), dir_path)
    # 获取文件夹中的所有文件名
    file_names = os.listdir(dir_path)
    if ext is not None:  # 筛选扩展名为 ext 的文件
        if not ext[0] == ".":
            ext = "." + ext
        file_names = [os.path.join(dir_path, f) for f in file_names if f.endswith(ext)]
    if not with_ext:  # 筛选不带扩展名的文件
        file_names = [
            os.path.join(dir_path, f)
            for f in file_names
            if f.split(".")[0].endswith(end_str)
        ]
    else:  # 筛选扩展名为 ext 的文件
        if end_str is not None:
            file_names = [
                os.path.join(dir_path, f) for f in file_names if f.endswith(end_str)
            ]
    return file_names


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


def loop_touch(
    dir_path: str = "",
    prefix: str = "",
    suffix: str = "",
    start: int = 1,
    end: int = 10,
    ext: str = "txt",
):
    """批量创建文件

    :param str dir_path: 输出路径, defaults to ""
    :param str prefix: 文件名前缀, defaults to ""
    :param str suffix: 文件名后缀, defaults to ""
    :param int start: 序号起始值, defaults to 1
    :param int end: 序号结束值, defaults to 10
    :param str ext: 扩展名, defaults to "txt"
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"create dir: {dir_path}")
    for i in range(start, end + 1):
        file_name = os.path.join(dir_path, prefix + f"{i:03d}" + suffix + "." + ext)
        Path(file_name).touch()
        print(f"create file: {file_name}")


if __name__ == "__main__":
    xx = get_file_list_with_end_str("stools/assets/test", "for_test")
    move_file_list_to_dir("test", xx)
