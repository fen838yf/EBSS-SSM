# # 获取csv文件中几个列的值写入新的文件
# import pandas as pd
# # 步骤2: 读取CSV文件
# df = pd.read_csv('results.csv')
# # 步骤3: 选择特定的列，例如选择列A和列B
# selected_columns = df[['epoch', 'metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)']]
# # 步骤4: 将选定的列写入新的CSV文件
# selected_columns.to_csv('results-yolo11.csv', index=False)  # index=False表示不将索引写入文件


# # 打开文件
# with open('results-yolo11.csv', 'r', encoding='utf-8') as file:
#     # 读取文件内容
#     content = file.read()
# # 替换内容
# content = content.replace(',', ' ')
# # 将修改后的内容写回文件
# with open('results-yolo11-new.csv', 'w', encoding='utf-8') as file:
#     file.write(content)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file_list = ['results-ours-new.csv', 'results-yolo11-new.csv']
    names = ['Ours', 'YOLO11n']
    # ap = ['0.673', '0.639', '1']

    plt.figure(figsize=(6, 6))
    for i in range(len(file_list)):
        data = pd.read_csv(file_list[i], sep=' ')
        epoch, R = np.array(data.iloc[:, 0]), np.array(data.iloc[:, 4])
        plt.plot(epoch, R, label=f'{names[i]}')

    plt.xlabel('Epoch')
    plt.ylabel('mAP@0.5:0.95')
    # plt.ylabel('Precision')
    # plt.title('R Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('mAP@0.5-0.95.png')