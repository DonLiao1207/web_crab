#!/bin/bash

# 查找當前目錄下所有包含空格的資料夾
for folder in *\ *; do
    if [ -d "$folder" ]; then
        # 去除空格
        new_name=$(echo $folder | tr -d ' ')
        git mv "$folder" "$new_name"
    fi
done

# 提交更改
git commit -m "批量去除資料夾名稱中的空格"
