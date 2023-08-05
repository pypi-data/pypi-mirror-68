from fisrt_shot.sub_1.helper import helper
from fisrt_shot.sub_1.mod_1 import fun_1_1

def func_2_1():
    print ('++++ func 2-1 started ')
    print ('calling func 1 -1 from mod1 of pack 1 ')
    fun_1_1()
    print('calling helper')
    helper()
    print ('++++That was func 2 -1  ')


if __name__ == '__main__':
    func_2_1()