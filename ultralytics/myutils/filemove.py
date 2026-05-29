import shutil
import os

# source_folder = r'D:\医学影像深度学习\脑肿瘤数据集\数据集1\archive\Train\Pituitary\labels'
# destination_folder = r'D:\医学影像深度学习\脑肿瘤数据集\数据集1\archive\Test\Pituitary\labels'
# folder_path = r'D:\医学影像深度学习\脑肿瘤数据集\数据集1\archive\Test\Pituitary\images'
# files_to_move = []
# for filename in os.listdir(folder_path):
#     # 构造完整的文件路径
#     files_to_move.append(filename.replace('.jpg', '.txt'))
#
# print(files_to_move)
#
# # 确保目标文件夹存在
# os.makedirs(destination_folder, exist_ok=True)
#
# for file in files_to_move:
#     source_file_path = os.path.join(source_folder, file)
#     destination_file_path = os.path.join(destination_folder, file)
#     if os.path.exists(source_file_path):
#         shutil.move(source_file_path, destination_file_path)
#         print(f"'{file}' has been moved from '{source_folder}' to '{destination_folder}'.")
#     else:
#         print(f"'{file}' does not exist in '{source_folder}'.")






source_folder = r'E:\yolov11\dataset1\Serrated adenoma\label'
destination_folder = r'E:\yolov11\dataset1\Serrated adenoma\test\label'
folder_path = r'E:\yolov11\dataset1\Serrated adenoma\test\image'
files_to_move = []
for filename in os.listdir(folder_path):
    # 构造完整的文件路径
    files_to_move.append(filename.replace('.png', '.txt'))

print(files_to_move)

# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

for file in files_to_move:
    source_file_path = os.path.join(source_folder, file)
    destination_file_path = os.path.join(destination_folder, file)
    if os.path.exists(source_file_path):
        shutil.move(source_file_path, destination_file_path)
        print(f"'{file}' has been moved from '{source_folder}' to '{destination_folder}'.")
    else:
        print(f"'{file}' does not exist in '{source_folder}'.")