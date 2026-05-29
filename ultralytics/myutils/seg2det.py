import os
import glob
import shutil

# 分割标注转成目标检测框
# 转换思路
# 读：读取 txt 文件里的 所有坐标点。
# 算：找出这些点的 x_min, x_max, y_min, y_max，得到外接矩形。
# 转：把矩形转成 YOLO 要的格式：class_id center_x center_y width height（全部归一化到 0~1）。
def convert_segmentation_to_bbox(seg_txt_path, bbox_txt_path):
    """
    将实例分割标注转换为目标检测标注（外接矩形）

    Args:
        seg_txt_path: 输入的分割标注文件路径
        bbox_txt_path: 输出的目标检测标注文件路径
    """
    with open(seg_txt_path, 'r') as f:
        lines = f.readlines()

    bbox_lines = []

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue

        # 第一个值是类别ID
        class_id = parts[0]

        # 剩余的是分割点的坐标 (归一化的 x1, y1, x2, y2, ...)
        points = list(map(float, parts[1:]))

        if len(points) < 6:  # 至少需要3个点(6个坐标值)才能形成多边形
            continue

        # 找到所有x坐标和y坐标
        x_coords = points[0::2]  # 所有x坐标
        y_coords = points[1::2]  # 所有y坐标

        # 计算外接矩形
        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)

        # 计算中心点坐标和宽高
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        # 以像素点过滤,只有几个像素点的过滤掉
        if width * height < 0.005:
            continue

        # 确保坐标在[0,1]范围内
        x_center = max(0, min(1, x_center))
        y_center = max(0, min(1, y_center))
        width = max(0, min(1, width))
        height = max(0, min(1, height))

        # 格式: class_id x_center y_center width height
        bbox_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        bbox_lines.append(bbox_line)

    # 写入新的标注文件
    with open(bbox_txt_path, 'w') as f:
        f.writelines(bbox_lines)


def copy_image_and_convert_annotation(seg_file, output_folder):
    """
    复制图片文件并转换对应的标注文件

    Args:
        seg_file: 分割标注文件路径
        output_folder: 输出文件夹路径
    """
    # 获取文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(seg_file))[0]

    # 查找对应的图片文件
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP']
    img_path = None

    for ext in img_extensions:
        potential_img_path = os.path.join(os.path.dirname(seg_file), base_name + ext)
        if os.path.exists(potential_img_path):
            img_path = potential_img_path
            break

    if img_path is None:
        print(f"警告: 未找到 {base_name} 对应的图片文件")
        return False

    try:
        # 复制图片文件到输出路径
        img_output_path = os.path.join(output_folder, os.path.basename(img_path))
        shutil.copy2(img_path, img_output_path)

        # 转换标注文件到输出路径
        bbox_output_path = os.path.join(output_folder, base_name + ".txt")
        convert_segmentation_to_bbox(seg_file, bbox_output_path)

        print(f"处理完成: {os.path.basename(seg_file)} -> 图片和标注已保存到输出路径")
        return True

    except Exception as e:
        print(f"错误: 处理 {base_name} 时发生异常: {str(e)}")
        return False


def batch_convert_with_output(input_folder, output_folder):
    """
    批量转换文件夹中的所有分割标注文件，并复制图片到指定输出路径

    Args:
        input_folder: 输入文件夹路径（包含图片和标注文件）
        output_folder: 输出文件夹路径
    """
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出文件夹: {output_folder}")

    # 查找所有的分割标注文件
    seg_files = glob.glob(os.path.join(input_folder, "*.txt"))

    converted_count = 0
    total_files = len(seg_files)

    print(f"找到 {total_files} 个标注文件，开始处理...")

    for i, seg_file in enumerate(seg_files):
        print(f"处理进度: {i + 1}/{total_files}", end='\r')

        if copy_image_and_convert_annotation(seg_file, output_folder):
            converted_count += 1

    print(f"\n\n转换完成！共成功处理了 {converted_count} 个文件。")
    print(f"输出路径: {output_folder}")
    print(f"包含: {converted_count} 个图片文件和 {converted_count} 个标注文件")


if __name__ == "__main__":
    # 输入文件夹路径（包含所有实例分割标注文件和图片的目录）
    input_folder = r"E:\yolov11\数据集\数据集2\dataset2\labels\test"

    # 输出文件夹路径
    output_folder = r"E:\yolov11\数据集\数据集2\dataset2\labels\test1"

    if not os.path.exists(input_folder):
        print("输入文件夹不存在，请检查路径！")
    else:
        batch_convert_with_output(input_folder, output_folder)