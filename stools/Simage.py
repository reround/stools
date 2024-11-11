import json, os
import cv2
from PIL import Image


def get_file_name_from_dir_by_ext(dir_path: str, ext: str = None) -> list:
    """获取目录中所有扩展名为 ext 的文件名

    :param str dir_path: _description_
    :raises ValueError: _description_
    :return list: _description_
    """
    # 检查文件是否存在
    if not os.path.exists(dir_path):
        raise ValueError("dir_path is not valid")
    # 转换成绝对路径
    dir_path = os.path.join(os.getcwd(), dir_path)
    # 获取文件夹中的所有文件名
    file_names = os.listdir(dir_path)
    # 排序
    file_names.sort()
    if ext is not None:
        # 筛选扩展名为 ext 的文件
        file_names = [
            os.path.join(dir_path, file) for file in file_names if file.endswith(ext)
        ]
    return file_names


def is_image_solid_black(img: Image):
    """判断图片是否黑色且完全不透明

    :param Image img: 图片
    :return bool: 是否全黑
    """
    # # 打开图片
    # img = Image.open(png_path)
    # # 将图片转换为RGBA模式，以确保我们处理的是RGBA值
    # img = img.convert("RGBA")

    # 获取图片的尺寸
    width, height = img.size
    # 遍历图片的每个像素
    for x in range(width):
        for y in range(height):
            # 获取当前像素的RGBA值
            r, g, b, a = img.getpixel((x, y))
            # 如果像素不是黑色或者透明度不是完全不透明，则返回False
            if r != 0 or g != 0 or b != 0 or a != 255:
                return False
    # 如果所有像素都是纯黑色且完全不透明，则返回True
    return True


def is_image_black(img: Image):
    """判断图片是否全黑（不管透明度）

    :param Image img: 图片
    :return bool: 是否全黑
    """

    # 获取图片的尺寸
    width, height = img.size
    # 遍历图片的每个像素
    for x in range(width):
        for y in range(height):
            # 获取当前像素的RGBA值
            r, g, b, a = img.getpixel((x, y))
            # 如果像素不是黑色或者透明度不是完全不透明，则返回False
            if r != 0 or g != 0 or b != 0:
                return False
    # 如果所有像素都是纯黑色，则返回True
    return True


def del_end_black_frame(png_list: list):
    """删除PNG列表末尾的黑色帧

    :param list png_list: PNG 列表
    """
    while len(png_list) > 0 and is_image_black(Image.open(png_list[-1])):
        print("----")
        png_list.pop()


def convert_png_list_to_gif(png_list: list, output_file: str, duration=40):
    """将PNG队列转换为GIF (不能有透明度、否则会叠加)

    :param list png_list: PNG 列表
    :param str output_file: 输出GIF文件的路径
    :param int duration: GIF中每帧的持续时间（毫秒）, defaults to 40
    """
    images = []
    for p in png_list:
        img = Image.open(p)
        images.append(img)

    # 保存为GIF
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=duration,
        loop=0,
    )


def save_png_list_to_one_png(png_list: list, output_file: str):
    """将 png 列表转换为一个 png 文件, 保存到 output_file 文件夹中，并将关键信息保存到 json 文件中。

        例如：save_png_list_to_one_png(png_list, "img/out.png") 会生成如下结构：

        - img/out
            |- out.png
            |- out_info.json

    :param list png_list: png列表
    :param str output_file: 输出的文件名称
    """
    parent_dir = os.path.dirname(output_file)  # 获取父目录
    file_name = os.path.basename(output_file)  # 获取文件名
    file_split = file_name.split(".")  # 分割文件名和扩展名
    dir_name = os.path.join(parent_dir, file_split[0])  # 输出文件夹名
    if file_split[-1] != "png":
        raise ValueError("输出文件必须是png格式")
    os.makedirs(dir_name, exist_ok=True)
    output_info_file = os.path.join(
        dir_name, file_split[0] + "_info.json"
    )  # 输出信息文件名
    output_file = os.path.join(dir_name, file_name)  # 输出文件名

    del_end_black_frame(png_list)
    num = len(png_list)
    # 使用第一张图片的高度作为新图片的高度
    first_image = Image.open(png_list[0]).convert("RGBA")
    total_height = first_image.height
    total_width = num * first_image.width

    # 创建一个新的透明背景图像
    new_im = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # 将每张图片粘贴到新图像上
    x_offset = 0
    for img_path in png_list:
        img = Image.open(img_path).convert("RGBA")
        new_im.paste(img, (x_offset, 0))
        x_offset += first_image.width

    # 保存新图像
    new_im.save(output_file, "PNG")
    # 保存关键信息到 output_file.json
    info = {
        "Total_width": total_width,
        "Total_height": total_height,
        "Number_of_frames": num,
    }
    with open(output_info_file, "w") as f:
        json.dump(info, f)


if __name__ == "__main__":
    dir_path = "imgs/Elements - Explosion 004 Radial noCT noRSZ"
    save_png_list_to_one_png(
        get_file_name_from_dir_by_ext(dir_path, "png"),
        r"D:\Git\Sgame\pyglet\Explosion_004.png",
    )
