# 图文精灵

## 软件功能
  1. 截图或打开图片识别图像上的文字
  2. 显示识别文字，翻译成其他语言
  3. 访问识别历史记录


## 百度云开放接口文档
如果想发布同款软件，请自行申请百度云开放接口，替换 `ImgTranText.py` 及 `TextTransAPI.py` 中的秘钥内容（不要使用源码中的密钥信息）

[百度识图 OCR Python SDK](https://cloud.baidu.com/doc/OCR/s/wkibizyjk)
* ImgTranText.py
```python
"""
User AppID AK SK
AK = API_KEY
SK = Secret_KEY
"""
APP_ID = '16289977'
AK = '1UUME9IqLLRwlbrQFcjePBwe'
SK = '0wNmCRtXgNGpvwGVNxFewiqqzrgKvwUv'

client = AipOcr(APP_ID, AK, SK)
```

[百度翻译 Api](https://api.fanyi.baidu.com/doc/21)
* TextTransAPI.py

```python

# Set your own appid/appkey.
appid = '20210422000794630'
appkey = 'Cp7G1L9U12aRsx3_tk2c'
```


## 软件架构
  gui.py-----------------------thinker框架的gui主界面

  History.py------------------用于toplevel的历史记录浮窗显示和历史记录存取实现

ImgTranText.py-----------基于百度Api，实现图文转换

minIcon.py----------------  用于实现串口最小化到托盘


## pip 导入库
```
pip3.8 install baidu-aip
pip3.8 install pillow
pip3.8 install pywin32
pip3.8 install requests
```
记得换源，否则速度很慢

## 主要类及其函数一览

### gui.py
```python
class MyCapture:
      """实现屏幕截图类"""

class _Main:  #Mian window class
      def main(s):
        """初始化窗口"""
      def buttonCaptureClick(s):
        """桌面截图函数"""
      def display(s):
        """显示布局"""
      def Catch_chipboard(s):
        """将截图得到的图片，转为文字"""
      def Hidden_window(s, icon = './res/image/icon.ico', hover_text = "图文精灵"):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''
      def exit(s, _sysTrayIcon=None):
        """从托盘区退出的重要函数"""
      def UpdateConnect(s):
        """更新网络状态"""
      def center_window(s,width=300, height=200):
        """将窗口屏幕居中"""
```

### History.py
```python
class history:
  def __init__(self,fileObj,tk_window = None):
      '''
      fileObj      历史文件存储结构体 RecordHty类
      tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
      '''
  def CreatHistory(self):
      """创建顶层窗口"""
  def WheelCtrl(self,event):
      """滚轮事件，绑定画布'"""
  def updateCanvas(self,event):
      """动态更新画布 少了这个就滚动不了"""
  def AddHistory(self,time,text):
      """在fm1中动态创建Label组件,time 当前时间,text Label中填充文本"""
  def DelAllData(self):
      """清除所有历史记录(文件)"""
  def SelectHistroy(self,widget = None):
      """鼠标左键点击历史元素返回内容"""

```
### TextTransAPI.py
```python
def TextTranslate(to_lang,srcText,from_lang = 'auto'):
    r"""Translate src text to dst text.
    :param from_lang: auto,en,zh.....
    :param to_lang: en.zh.....
    :param srcText: need to translate texts
    :return dstTest: translated texts to aim langurge 
    """
```

### ImgTranText.py
```python
def Transform_GT(accuracy_option, image=None):
    r"""OCR image.
    :param accuracy_option: 1：high definition 2：Normal definition
    :param image: If equals None means Open PicFile，or Transfer input 
    :return dstTest: translated texts form image
    """
```

### minIcon.py 
> 最小化托盘例程，原文连接https://blog.csdn.net/dyx1024/article/details/7430638

### ColorOfTk.py 
> 一个小例程可以帮助你了解Tkinter支持的所有颜色


通过本软件例程，基本可以学到到大部分的Python Tkinter 组件用法，推荐用于简单软件的制作，想要开发大型软件，推荐使用pySider2

Have fun！
