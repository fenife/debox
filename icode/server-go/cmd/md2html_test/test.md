
## 冒泡排序
比较相邻的元素，如果前面的比后面的大，则交换。
假设数组长度为n，对第0个到第n-1个做同样的操作。

```python
def bubble_sort(lst: list):
    """冒泡排序"""

    # 获取数组长度
    n = len(lst)

    # 重复n次
    for i in range(n):
        # 每一轮都比较相邻的元素，'冒泡'找到最大的元素
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                # 交换
                lst[j], lst[j+1] = lst[j+1], lst[j]

    return lst
```
复杂度分析：

- 时间复杂度：O(n^2)
- 空间复杂度：O(1)
- 稳定性：稳定

## table

| Name  | Age |
|-------|------|
|  Bob  | 27 |
| Alice | 23 |

## 参考
1. [python排序算法](https://cloud.tencent.com/developer/article/2117904)
