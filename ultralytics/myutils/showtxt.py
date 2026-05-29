import cv2
import numpy as np
import os
from pathlib import Path


def show_yolo_boxes(image_file: str, label_file: str = None):
    """
    快速显示YOLO标注框

    参数:
        image_file: 图像文件路径
        label_file: 标注文件路径 (可选，默认使用同名.txt文件)
    """
    # 读取图像
    img = cv2.imread(image_file)
    if img is None:
        print(f"错误: 无法读取图像 {image_file}")
        return

    h, w = img.shape[:2]

    # 确定标注文件
    if label_file is None:
        label_file = Path(image_file).with_suffix('.txt')

    if not os.path.exists(label_file):
        print(f"错误: 标注文件不存在 {label_file}")
        return

    # 读取标注
    boxes = []
    with open(label_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 5:
                    class_id = int(parts[0])
                    x_center = float(parts[1]) * w
                    y_center = float(parts[2]) * h
                    box_w = float(parts[3]) * w
                    box_h = float(parts[4]) * h

                    # 转换为左上角和右下角坐标
                    x1 = int(x_center - box_w / 2)
                    y1 = int(y_center - box_h / 2)
                    x2 = int(x_center + box_w / 2)
                    y2 = int(y_center + box_h / 2)

                    boxes.append((class_id, x1, y1, x2, y2))

    print(f"找到 {len(boxes)} 个标注框")

    # 绘制框
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]

    for class_id, x1, y1, x2, y2 in boxes:
        color = colors[class_id % len(colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, str(class_id), (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 显示
    cv2.imshow(f"YOLO标注 - {Path(image_file).name}", img)
    print("按任意键关闭...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 使用示例
if __name__ == "__main__":
    # 最简单用法: 图像和标注文件同名
    # show_yolo_boxes("example.jpg")

    # 或指定标注文件
    show_yolo_boxes("E:\yolov11\GTXC2110135-2-400-008.png", "E:\yolov11\GTXC2110135-2-400-008.txt")

