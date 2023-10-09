import cv2
import os

def pointDrawingProcess(str):
    print(f"point drawing {str}")
    return "ok"


dd = {"点画":"pointDrawing"}
print(eval(dd["点画"]+"Process")(dd["点画"]))