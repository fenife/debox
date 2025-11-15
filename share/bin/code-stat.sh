#!/bin/bash

set -x

find ./ \
  -path "*/.git" -prune -o \
  -path "*/venv" -prune -o \
  -type f \
  -exec sh -c '
    for file do
      # 排除二进制文件（通过 MIME 编码判断）
      if file --mime-encoding "$file" | grep -q "binary"; then
        continue
      else
        wc -l "$file"  # 统计文本文件行数
      fi
    done
  ' sh {} + | sort -nr  # 排序（从多到少）
