"""这是"nester.py" 模块，提供了一个名为print_lol()的函数，这个函数
的作用是打印列表，其中有可以能包含（也有可能不包含）嵌套列表。"""
def print_lol(the_list, level):
    """这个函数取一个位置参数，名为"the_list"，这可以是任何python
    列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项
    会（递归地）输出到屏幕上，个数据项各占一行。"""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
