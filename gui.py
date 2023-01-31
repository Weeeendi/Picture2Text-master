#!/usr/bin/python
# -*- coding: UTF-8 -*-

import win32api, win32print, win32gui
from logging import root
from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES

from PIL import ImageGrab
from time import sleep
from minIcon import SysTrayIcon
from History  import *
import pyperclip
import os
import tkinter as tk          # 导入 Tkinter 库
from tkinter import Y,ttk
from tkinter import * 
import tkinter.messagebox
import traceback
import ImgTranText as Itt
import TextTransAPI as TextT
import ctypes

About = "图文精灵 \t版本号 v2.0 \n该软件遵守 MIT 开源协议\nhttps://github.com/Weeeendi/Picture2Text" 
Shareble = 1
NeedExit = 0

#默认配置项
default_srclang = 'auto'
default_lang = 'en'
current_lang = default_lang

default_theme = "light"
current_theme = default_theme

main_windowHeight = 300
main_windowWidth = 500

disconnect = 0 

def message_askyesno(root):
    '''
    # Gets the requested values of the height and width.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    '''
    root.withdraw()  # ****实现主窗口隐藏
    return (tk.messagebox.askyesno("提示","要执行此操作？"))

def clearEdit(Editx):
    Editx.delete('1.0',END)
    # Editx.configure(fg='black')  # 修改字体颜色，修改其它参数只需要传入对应的参数即可


#图片识别的结果显示在Edit1
def OcrDisplayCallback(root,Edit1,Edit2):
    clearEdit(Edit1)
    clearEdit(Edit2)
    Temptext = pyperclip.paste()
    Edit1.insert(INSERT,Temptext)
    root.UpdateBg("请打开图片或截图","./res/image/background1.png")   
    #保存到历史记录

def TransCallback(Edit1,Edit2,fm):
    clearEdit(Edit2)
    var = TextT.TextTranslate(current_lang,Edit1.get('1.0',END))
    Edit2.insert(INSERT,var)
    fm.pack(side=LEFT, fill=BOTH, expand=YES)
 
#语言菜单
src_languages = {"自动":"auto","英语":"en", "简中":"zh",  "日语":"jp", "西班牙语": "spa",
              "韩语":"kor",  "繁中":"cht",  "意大利语":"it", "捷克语":"cs","法语":"fra"}

dec_languages = {"英语":"en", "简中":"zh",  "日语":"jp", "西班牙语": "spa",
              "韩语":"kor",  "繁中":"cht",  "意大利语":"it", "捷克语":"cs","法语":"fra"}

def get_real_resolution():
	"""获取真实的分辨率"""
	#hDC = win32gui.GetDC(0)
	# 横向分辨率
	w =win32api.GetSystemMetrics(0)
	# 纵向分辨率
	h =win32api.GetSystemMetrics(1)
	return w,h


class MyCapture:
    def __init__(self, png, root):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        #屏幕尺寸
        #screenWidth = root.winfo_screenwidth()
        #screenHeight = root.winfo_screenheight()
        #解决windows缩放问题
        
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware(2)
        [screenWidth, screenHeight] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        
        #screenWidth,screenHeight = get_real_resolution()
        #创建顶级组件容器
        self.top = tkinter.Toplevel(
            root, width=screenWidth, height=screenHeight)

        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(
            self.top, bg='blue', width=screenWidth, height=screenHeight)
        
        #显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(
            screenWidth//2, screenHeight//2, image=self.image)

        def onRightButtonDown(event):
            self.top.destroy()
            os.remove(filename)
            root.state('normal')
        self.canvas.bind('<Button-3>', onRightButtonDown)

        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(
                self.X.get(), self.Y.get(), event.x, event.y, outline='blue')

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            '''try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
                '''
            sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            #弹出保存截图对话框
            file_path = './res/image/somefile.png'
            pic.save(file_path, 'PNG')
            sleep(0.1)
            '''
            fileName = tkinter.filedialog.asksaveasfilename(
                title='保存截图', filetypes=[('image', '*.jpg *.png')])
            
            if fileName:
                pic.save(fileName)
            '''
            #关闭当前窗口
            self.top.destroy()
            return pic
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
#让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

 #开始截图

#判断是否有网络连接
def isConnected():
    import requests
    try:
        html = requests.get("http://www.baidu.com",timeout=2)
    except:
        return False
    return True

application_path = "./res/image/"
iconFile = "icon.ico"
        
class _Main:  #调用SysTrayIcon的Demo窗口
    def __init__(s):
        s.SysTrayIcon  = None  # 判断是否打开系统托盘图标
        #初始化历史记录
        Recordfile = os.path.join(os.extsep,*PATH)
        s.histroyF = RecordHty(file= Recordfile+File)

    def popup(s,event):
        s.menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单

    def setlang(s,event): 
        global current_lang  
        print(s.v.get())
        current_lang = dec_languages.get(s.v.get())  

    def Edit_about(s,action,event = None):
        '''option obtain "back","callback","clear","copy"."cut","paste",'''
        #撤销、重做
        
        if(action == "back"):
            try:
                s.Edit1.edit_undo()
                s.Edit2.edit_undo()
            except Exception as e:
                traceback.print_exc()
    
        if(action == "callback"):
            try:
                s.Edit1.edit_redo()
                s.Edit2.edit_redo()
            except Exception as e:
                traceback.print_exc()

        if(action == "clear"):
            try:
                s.Edit1.delete('1.0',END)
                s.Edit2.delete('1.0',END)
            except Exception as e:
                traceback.print_exc()

        if(action == "cut"):
            global root
            s.Edit2.event_generate('<<Cut>>')
            s.Edit1.event_generate('<<Cut>>')
            
        if(action == "copy"):
            global root
            s.Edit1.event_generate('<<copy>>')
            s.Edit2.event_generate('<<copy>>')
            
        if(action == "Paste"):
            global root
            s.Edit2.event_generate('<<Paste>>')
            s.Edit1.event_generate('<<Paste>>')
    #用来显示全屏幕截图并响应二次截图的窗口类


    def buttonCaptureClick(s):
        """桌面截图函数
        """
        #当前在截图.不支持最小化判断
        global Shareble
        Shareble = 0
        isNormal = 0
        #最小化主窗口
        if(s.root.state() == "normal"):
            s.root.withdraw() #隐藏tk窗口
            isNormal = 1
        #s.root.state('icon')
        sleep(0.2)
        global filename
        filename = 'temp.png'

        #grab()方法默认对全屏幕进行截图

        im = ImageGrab.grab()
        im.save(filename)
        im.close()
        #显示全屏幕截图
        w = MyCapture(filename,s.root)
        
        s.G.wait_window(w.top)
        #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
        try:
            os.remove(filename)
        except Exception as e:
            logging.debug(e)
        s.Catch_chipboard()
        if(isNormal):
            s.root.deiconify()
        else:
            s.resume()
        Shareble = 1

    def display(s):
        """显示布局"""
        #Frame1
        s.B.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.G.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.D.pack(side=TOP,anchor=W,fill=X,expand=N)
        s.Notice.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

        #Frame2
        s.OcrRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
        s.Edit1.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)
        
        s.TransButton.pack(side=LEFT,anchor=CENTER,fill=X,expand=Y)
        s.TransChoose.pack(side=RIGHT,anchor=W,fill=BOTH,expand=Y)

        #Frame3
        s.TransRes.pack(side=TOP,anchor=W,fill=X,expand=N) 
        s.Edit2.pack(side=TOP,anchor=W,fill=BOTH,expand=Y)

        s.fm1.pack(side=LEFT, fill=BOTH, expand=YES)
        s.fm2.pack(side=LEFT, fill=BOTH, expand=YES)
        s.fm3.forget()

    def switch_icon(s, _sysTrayIcon, icon = 'D:\\2.ico'):
        #点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        #只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon.icon = icon
        _sysTrayIcon.refresh()
        
        #气泡提示的例子
        s.show_msg(title = '图标更换', msg = '图标更换成功！', time = 500)
    
    def show_msg(s, title = '标题', msg = '内容', time = 500):
        s.SysTrayIcon.refresh(title = title, msg = msg, time = time)

    def Hidden_window(s, icon = './res/image/icon.ico', hover_text = "图文精灵"):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''
        
        #托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        #24行有自动添加‘退出’，不需要的可删除
        
        menu_options=(('打开主界面', None,s.resume), 
                      ('识别图像', None, (('截图', None,s.buttonCaptureClick),('打开图像', None,s.Ocrtranslated))),
                      ('退出', None,s.beforeExit)
                      )       

        s.root.withdraw()   #隐藏tk窗口
        if not s.SysTrayIcon: s.SysTrayIcon = SysTrayIcon(
                                        icon,               #图标
                                        hover_text,         #光标停留显示文字
                                        menu_options,       #右键菜单
                                        on_quit = s.beforeExit,   #退出调用
                                        tk_window = s.root, #Tk窗口
                                        )
        s.SysTrayIcon.activation()

    def resume(s):
        s.SysTrayIcon.destroy(exit = 0)


    def exit(s):
        s.root.destroy()
        print ('exit...')
        os._exit(0) 

    def beforeExit(s):
        global NeedExit
        NeedExit = 1
        s.resume()


    def Catch_chipboard(s):
        """将截图得到的图片，转为文字"""
        file_path = './res/image/somefile.png'
        image = Itt.get_file_content(file_path)
        if Itt.Transform_GT(Itt.High_precision, image):
            s.UpdateBg('请打开图片或截图',"./res/image/background2.png")
            s.varInFm1.set('识别完成，结果已复制到粘贴板')
            Temptext = pyperclip.paste()
            time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
            s.histroyF.dict[time] = Temptext
            s.histroyF.SaveRec()
            logging.debug("已保存历史记录\n"+Temptext)
        else:        
            s.varInFm1.set('未识别到文字信息')
        
    def Ocrtranslated(s):
        if Itt.Transform_GT(Itt.High_precision):
            s.UpdateBg('请打开图片或截图',"./res/image/background2.png")
            s.varInFm1.set('识别完成，结果已复制到粘贴板')
            Temptext = pyperclip.paste()
            time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
            s.histroyF.dict[time] = Temptext
            s.histroyF.SaveRec()
            logging.debug("已保存历史记录\n"+Temptext)
        else:
            s.varInFm1.set('未识别到文字信息')
        print(s.root.state())
        if(s.root.state() == "withdrawn"):
            s.resume()
    
    def UpdateBg(s,text,imgPath):
        """变更Notice 图片文字
        @text : 显示文字
        @imgPath : 文件名带路径
        """
        s.varInFm1.set(text)
        img = tk.PhotoImage(file = imgPath)
        s.Notice.configure(image=img,textvariable=s.varInFm1,compound="top")
        s.Notice.image = img

    def changeTool_WithoutIntert(s,state):
        if(state == 1):
            s.B['state'] = 'normal'
            s.G['state'] = 'normal'
            s.D['state'] = 'normal'
            s.TransButton['state'] = 'normal'
        if(state == 0):
            s.B['state'] = 'disable'
            s.G['state'] = 'disable'
            s.D['state'] = 'disable'
            s.TransButton['state'] = 'disable'
        

    def UpdateConnect(s):
        """更新网络状态"""
        global disconnect
        if(isConnected() and disconnect):
            disconnect = 0 
            s.UpdateBg("请打开图片或截图","./res/image/background1.png")
            s.root.unbind("<Shift-Alt-A>")
            s.changeTool_WithoutIntert(True)
            
        elif isConnected() == 0:
            disconnect = 1
            s.UpdateBg("当前无网络连接，请检查后重试","./res/image/background.png") 
            s.changeTool_WithoutIntert(False)

        s.root.after(5000,s.UpdateConnect)       
            
    def center_window(s,width=300, height=200):
        """将窗口屏幕居中"""
        # get screen width and height
        screen_width = s.root.winfo_screenwidth()
        screen_height = s.root.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        s.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def showAbout(s):
        """显示关于"""
        AboutObj = tk.Toplevel(s.root)
        AboutObj.title("关于")
        AboutObj.attributes("-toolwindow", 2) # 去掉窗口最大化最小化按钮，只保留关闭
        icon = tk.PhotoImage(file = "./res/image/256x256.png")
        AboutObj.Lb = ttk.Label(AboutObj,anchor='center',image=icon,text=About,foreground='grey', font=('Microsoft Yahei',8),compound="top")
        x = max(s.root.winfo_x(),0)
        y = max(s.root.winfo_y(),0)
        AboutObj.geometry('%dx%d+%d+%d' % (250, 200,x+(main_windowWidth-250)/2,y+(main_windowHeight-200)/2))

        AboutObj.Lb.pack()
        AboutObj.focus_set()
        AboutObj.mainloop()


    def main(s):
        #tk窗口
        #解决windows缩放问题
        
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware(2)
       
        s.root = tk.Tk()
        s.root.title('图文精灵 v2.0')

        winWidth = 500
        winHeight = 300
        #s.center_window(winWidth,winHeight)
        
        #t=ttk.Style()
        #t.theme_use('classic')
        s.Fmstyle = ttk.Style()
        s.Fmstyle.configure('1.TFrame',background='DarkGray',foreground = "White")
        
        s.fm1 = ttk.Frame(s.root,style='1.TFrame')
        s.fm2 = ttk.Frame(s.root,style='1.TFrame')
        s.fm3 = ttk.Frame(s.root,style='1.TFrame')
     
        s.varInFm1= StringVar()
        try:
            starkabe = tk.PhotoImage(file = "./res/image/background1.png")
        except Exception as e:
            print(e)
            starkabe =None
        s.Notice = ttk.Label(s.fm1,anchor='center',image=starkabe,textvariable=s.varInFm1, wraplength = 130,foreground='grey', font=('Microsoft Yahei', 12),compound="top")
        s.varInFm1.set('请打开图片或截图')

        #窗口大小不可变化
        #root.resizable(True, False)  

        #在图形界面上设定输入框控件entry并放置控件
        #Edit1 = tk.Text(fm1, show='*', font=('Courier New', 12))   # 显示成密文形式
        #Edit2 = tk.Text(fm3, show=None, font=('Courier New', 12))  # 显示成明文形式

        '''Farme1 function area'''

        s.B = ttk.Button(s.fm1, text="打开图像",command =s.Ocrtranslated,width=5)
        s.G = ttk.Button(s.fm1, text="屏幕截图",command=s.buttonCaptureClick,width=5)
        s.D = ttk.Button(s.fm1,text = "显示结果",command = lambda:OcrDisplayCallback(s,s.Edit1,s.Edit2),width=5)

        s.OcrRes = ttk.Label(s.fm2, text='识别结果', font=('Microsoft Yahei', 10), width=10)
        s.Edit1 = tk.Text(s.fm2,width=10, height=5,padx=10,pady=1, undo = True,font=("Microsoft Yahei",9))
        s.TableStr = ttk.Label(s.fm2, anchor='e',text='To:', font=('Microsoft Yahei', 10))

        s.TransButton = ttk.Button(s.fm2,text = "翻译成 >",command = lambda:TransCallback(s.Edit1,s.Edit2,s.fm3),width=10)
        s.TransRes = ttk.Label(s.fm3, text='翻译结果', font=('Microsoft Yahei', 10), width=10)
        s.Edit2 = tk.Text(s.fm3,width=10, height=5,padx=10,pady=1, undo = True,font=("Microsoft Yahei",9))

        '''创建一个弹出菜单'''
        
        #右键 剪切复制黏贴
        def callback1(event=None):
            
            s.Edit1.event_generate('<<Cut>>')
            s.Edit2.event_generate('<<Cut>>')
            
        def callback2(event=None):
        
            s.Edit1.event_generate('<<copy>>')
            s.Edit2.event_generate('<<copy>>')
            
        def callback3(event=None):
            focus = s.root.focus_get()
            if(focus == s.Edit1):
                s.Edit1.event_generate('<<Paste>>')
            if(focus == s.Edit2):
                s.Edit2.event_generate('<<Paste>>')

        s.menu = tk.Menu(s.root,
            tearoff=False,
            #bg="grey",
            )
        s.menu.add_command(label="剪切", command=callback1)
        s.menu.add_command(label="复制", command=callback2)
        s.menu.add_command(label="黏贴", command=callback3)

        s.Edit1.bind("<Button-3>", s.popup)                 # 绑定鼠标右键,执行popup函数
        s.Edit2.bind("<Button-3>", s.popup)               # 绑定鼠标右键,执行popup函数

        s.v = Variable()
        s.v.set('英语')
        list_zh = list(dec_languages.keys())
        
        '''Farme2 function area'''
        s.TransChoose = ttk.OptionMenu(s.fm2, s.v , '',
                            *list_zh
                            ,command=s.setlang)

        #菜单栏
        s.menubar = tk.Menu(s.root)
        s.root.config(menu=s.menubar)

        #添加菜单选项
        s.menu1 = tk.Menu(s.menubar,borderwidth = 3,tearoff=False)
        s.menu2 = tk.Menu(s.menubar,borderwidth = 3,tearoff=False)
       
        s.menubar.add_cascade(label="选项", menu = s.menu1)

        s.menu1.add_command(label="撤销↶",command = lambda: s.Edit_about("back"))
        s.menu1.add_command(label="重做↷",command = lambda: s.Edit_about("callback"))
        s.menu1.add_command(label="清空",command = lambda: s.Edit_about("clear"))
        s.menu1.add_separator()

        s.histroy = history(s.histroyF,s.root)
        s.menu1.add_command(label="历史",command =  lambda:s.histroy.CreatHistory())
        s.menu1.add_command(label="清空历史",command = lambda: s.histroy.DelAllData())

        s.menu1.add_separator()    
        s.menu1.add_command(label="关于",command = lambda:s.showAbout())

       # s.menubar.add_cascade(label="主题", menu = s.menu2)
       # s.menu2.add_radiobutton(label = "浅色",command=lambda:set_theme(light))
       # s.menu2.add_radiobutton(label = "深色",command=lambda:set_theme(dark))

        #显示所有布局
        s.display()  
        '''快捷键'''                  
        def quicklyKey(event):
            s.buttonCaptureClick()
        s.root.bind("<Unmap>", lambda event: s.Hidden_window() if ((s.root.state() == 'iconic') and Shareble) else False) #窗口最小化判断，可以说是调用最重要的一步
        s.root.bind("<Map>",lambda event: s.exit() if(NeedExit) else False)
        s.root.bind("<Shift-Alt-A>",quicklyKey)
        s.root.protocol('WM_DELETE_WINDOW', s.exit) #点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        #定时刷新网络状态        
        s.UpdateConnect()
        s.center_window(main_windowWidth,main_windowHeight)
        s.root.iconbitmap('./res/image/icon.ico') 
        s.root.mainloop()


if __name__ == '__main__':
    Main = _Main()
    Main.main()

    