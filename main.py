# -*- encoding=utf8 -*-
from PIL import Image, ImageGrab
from aip import AipOcr
import pyperclip
import time
import hashlib
from airtest.core.api import *
from airtest.core.android.adb import *
import subprocess
from pykeyboard import *
from pymouse import *
import sys
import tkinter
import win32gui, win32api

#蓝叠：pixel2XL，分辨率1920x1080竖屏，240dpi


#OCR的相关参数
APP_ID = '26485327'
API_KEY = '6OiLfdhbNupkgwZXmLrRTg0T'
SECRET_KEY = '72ZhXU7U9oy7jGPhuFEIMCKwMZmDgYUG'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
fname = 'grab_clipboard.png'
md5_old = ''

order0 = 'adb connect 127.0.0.1:5555'  # 获取连接设备
os.system(order0)

print("【💗💗祝姐姐考试顺利，金榜题名💗💗】")

def readClipboardOCRAndPaste():
    # 检测到剪切板有新增图片后复制图像内文本到剪切板
    global md5_old, md5_flag
    md5_flag = 0
    #读取剪切板图片，返回图片对象
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        #print(im.size)
        im.save("grab_clipboard.png")
        print("")
        print("[✅成功读取了剪切板最后一张图片]")
    elif im:
        for filename in im:
            print("filename:%s" % filename)
            im = Image.open(filename)
    else:
        pass

    with open('grab_clipboard.png', 'rb') as fp:
        temp_img = fp.read()
        md5_new = hashlib.md5(temp_img).hexdigest()
        if md5_new != md5_old:
            results = client.basicGeneral(temp_img)["words_result"]
            textResult = ''
            for result in results:
                text = result["words"]
                textResult = textResult + text
            print("[题目内容：]")
            print("🖤"+textResult+"🖤")
            pyperclip.copy(textResult)
            print("[✅题目内容已经帮姐姐复制到剪切板了呢ヾ(≧▽≦*)o]")
            md5_old = md5_new
            textPaste()
        time.sleep(1)
        # md5_current = hashlib.md5(temp_img).hexdigest()

def textPaste():
    order1 = 'adb -s 127.0.0.1:5555 shell input tap 541 159'
    order2 = 'adb -s 127.0.0.1:5555 shell input tap 198 345'
    order3 = 'adb -s 127.0.0.1:5555 shell input tap 997 340'
    os.system(order1)
    os.system(order2)
    os.system(order3)



    print("[✅看一眼学小易吧，应该已经有答案啦(≧∀≦)ゞ]")

def threadCopy():
    while True:
        readClipboardOCRAndPaste()

class detectStdout(): # 重定向类
    def __init__(self):
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        t.insert('end', info) 
        t.update() 
        t.see(tkinter.END) 

    def restoreStd(self):
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak
        

def btn_func():
    threading.Thread(target=threadCopy).start()

mystd = detectStdout() 
window = tkinter.Tk() 
t = tkinter.Text(window) 
t.pack()
b = tkinter.Button(window, text='点我点我！', command=btn_func) 
b.pack()
window.mainloop() 
mystd.restoreStd()
