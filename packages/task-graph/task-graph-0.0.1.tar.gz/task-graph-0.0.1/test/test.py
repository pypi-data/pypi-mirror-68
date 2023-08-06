from task_graph import TaskGraph

tg = TaskGraph()


def add(a, b):
    print("add", a, b)
    return a + b


def sub(a, b):
    print("sub", a, b)
    return a - b

ret1 = tg(add)(1, 2)
ret2 = tg(add)(3, ret1)
ret3 = tg(add)(4, ret2)
ret4 = tg(sub)(ret3, 0)
ret5 = tg(print)(ret4)

final = tg.add_task('to_list')(ret1, ret2, ret3, ret4)

final.print()  # same as print(final.compute())

tg.update_task(ret3)(add)(5, ret2)

final.print()  # same as print(final.compute())
