
def batch_list(lst, batch_size):
    print('-' * 30)
    for i in range(0, len(lst), batch_size):
        print(lst[i:i + batch_size])


# 使用示例
test_cases = [
    [],
    [1, ],
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
]
for tc in test_cases:
    batch_list(tc, 3)

