import os

def rename_images_in_subfolders(parent_dir):
    # 遍歷父資料夾中的所有子資料夾
    for subdir in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir)
        print(subdir_path)
        # 確認該路徑是資料夾
        if os.path.isdir(subdir_path):
            # 初始化計數器
            count = 1

            # 遍歷子資料夾中的所有 jpg 文件
            for filename in os.listdir(subdir_path):
                if filename.endswith(".jpeg"):
                    # 構建舊文件路徑
                    old_file_path = os.path.join(subdir_path, filename)

                    # 構建新文件名，格式為 "子資料夾名稱_{num}.jpg"
                    new_filename = f"{subdir}_{count}.jpg"
                    new_file_path = os.path.join(subdir_path, new_filename)

                    # 重命名文件
                    os.rename(old_file_path, new_file_path)

                    # 增加計數器
                    count += 1

if __name__ == "__main__":
    # 設置父資料夾為 upload_pic
    parent_directory = "upload_pic"
    
    # 開始重命名
    rename_images_in_subfolders(parent_directory)
