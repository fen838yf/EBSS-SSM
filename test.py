from ultralytics import YOLO

if __name__ == '__main__':
    # 模型验证
    model = YOLO('runs/detect/yolo11-C2PSAMamba-HAFB-WiseInnerMPDIoU-train/weights/best.pt')
    model.val(data='ultralytics/datasets/mydata.yaml', batch=16, split='test')