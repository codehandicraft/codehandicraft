import cv2
import os
import re

def pointDrawingProcess(str):
    print(f"point drawing {str}")
    return "ok"


dd = {"点画":"pointDrawing"}
print(eval(dd["点画"]+"Process")(dd["点画"]))

file_path='./sis_out.jpg'

file_list = ['./sis_out.jpg', './sis_out.jpg', './sis_out.jpg', './sis_out.jpg', './sis_out.jpg', './sis_out.jpg', './sis_out.jpg', './sis_out.jpg', ]


def str_to_int(input_str):  
    # 使用正则表达式匹配数字部分  
    numbers = re.findall(r'\d+', input_str)  
      
    # 如果找到数字，则返回转换后的整数；否则返回None  
    if numbers:  
        return int(numbers[0])  
    else:  
        return -1
  
print(str_to_int('12.3af45.6'))
print(str_to_int('12'))
print(str_to_int(''))
print(str_to_int('ff'))
print(str_to_int('ff12.3'))