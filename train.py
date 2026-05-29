import torch
from ultralytics import YOLO


if __name__ == '__main__':
   # 使用yaml配置文件来创建模型,并导入预训练权重.
   # 不使用预训练权重，从零开始训练（如果对网络结构进行了修改，推荐从零开始训练）·
   model = YOLO('ultralytics/cfg/models/11/yolo11n-C2PSAMamba-HLGFusion.yaml')
   model.load('ultralytics/weights/yolo11n.pt')
   model.train(cfg="ultralytics/cfg/default.yaml", data="ultralytics/datasets/mydata.yaml",
               epochs=600, batch=8, workers=2, amp=False, patience=100)





