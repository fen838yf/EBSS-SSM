import cv2
import numpy as np
from PIL import Image
import os

from matplotlib import pyplot as plt
# 语义分割中将图片mask标签改为可以用于yolo训练的txt标签文件格式
def convert(source_path, target_path):
    image_names = os.listdir(source_path)
    for image_name in image_names:
        # 读取 图像
        image_path = os.path.join(source_path, image_name)
        image = Image.open(image_path)

        # 将图像转换为 NumPy 数组并转为灰度图
        image_array = np.array(image.convert('L'))

        # 将图像转换为二值图像（假设标签是0和非0值）
        binary_image = image_array*255

        # 找到连通区域的轮廓
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 确保输出文件夹存在
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # 保存多边形的坐标到文件
        output_file = os.path.join(target_path, os.path.splitext(image_name)[0] + '.txt')

        # 遍历每个轮廓，生成多边形坐标并保存为 .txt 文件
        for i, contour in enumerate(contours):
            # 近似多边形轮廓（可选，降低点的数量,越小点越多）
            epsilon = 0.002 * cv2.arcLength(contour, True)
            epsilon = 0
            approx_polygon = cv2.approxPolyDP(contour, epsilon, True)
            # 剔除特别小的点
            if len(approx_polygon) <3:
                continue
            # 获取图像的高度和宽度
            height, width = image_array.shape


            with open(output_file, 'a') as f:
                # 保存每个多边形的类别ID（假设为0）和坐标，坐标需要归一化
                f.write(f"5 ")
                for point in approx_polygon:
                    # 每个点的坐标归一化到[0, 1]范围
                    x_normalized = point[0][0] / width
                    y_normalized = point[0][1] / height
                    f.write(f"{x_normalized} {y_normalized} ")
                f.write("\n")

            print(f"Polygon {i} saved to {output_file}")

        print("多边形标签已生成并保存为 TXT 文件。")


if __name__ == '__main__':
    source_path = r"E:\yolov11\数据集\数据集2\dataset2\labels\test\Serrated adenoma\label"
    target_path =r"E:\yolov11\数据集\数据集2\dataset2\labels\test\Serrated adenoma\label"
    convert(source_path=source_path, target_path=target_path)


