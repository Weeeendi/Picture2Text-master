import datetime
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import BOTH, E, END, INSERT, LEFT, N, TOP, W, X, YES
import json
from turtle import color
from typing import List

from requests import delete
import pyperclip

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
HistoryList = []
HistoryRemind_List = []
MAX_HISTORY = 50
PATH = ['res','history']
File = '/history.json'

WinWidth = 220
WinHeight = 400


selectEditCont = ''

class RecordHty():    
    def __init__(self,file) -> None:
        """历史数据初始化"""
        self.file = file
        self.dict = {}
        self.LoadRec()

    def SaveRec(self):
        """存储历史记录"""
        if(self.file == None):
            logging.debug("Have not this file")
            return
        tf = open(self.file,"w")
        json.dump(self.dict,tf)
        tf.close()

    def LoadRec(self):
        """载入历史记录"""
        try:
            tf = open(self.file, "r")
        except Exception as e:
            logging.debug(e)
            #如不存在则创建该文件
            tf = open(self.file, "w")
            tf.close()
            return
        try:
            self.dict = json.load(tf)
            keys = list(self.dict.keys())
            print(keys)
        except Exception as e:
            logging.debug(e)
            pass
        tf.close()


class ToolTip(object):

    def __init__(self,root,rootwidget,widget):
        self.widget = widget
        self.rootwidget = rootwidget
        self.root = root

    def hovershow(self,color):    
        self.widget.config(background = color,cursor = "heart")

    def hoverhide(self,color):
        self.widget.config(background = color,cursor = "arrow") 
        

    def Leftclick(self):
        text = self.widget['text']
        #text = self.widget.get(2.0,END)
        pyperclip.copy(text)
        self.rootwidget.destroy()     

    def AddTop(self):  
        self.widget.config(background = "#D3D3D3",cursor = "arrow")
        self.widget.unbind('<Enter>')
        self.widget.unbind('<Leave>')
        
        HistoryRemind_List.append(HistoryList.index(self.widget))

    def RemoveTop(self):
        self.widget.config(background = "#FFFFFF",cursor = "arrow")
        HistoryRemind_List.remove(HistoryList.index(self.widget))
        def enter(event):
            self.hovershow("#FFFFDA")
        def leave(event):
            self.hoverhide("#FFFFFF")
        self.widget.bind('<Enter>',enter)
        self.widget.bind('<Leave>',leave)
    
    def Rightclick(self,x,y):
        def popup(s,event):
            s.menu.post(event.x_root, event.y_root)   # post在指定的位置显示弹出菜单
        self.rootwidget.menu = tk.Menu(self.rootwidget,
            tearoff=False,
            #bg="grey",
            )
        text = self.widget['text']
        if(HistoryList.index(self.widget) in HistoryRemind_List):
            self.rootwidget.menu.add_command(label="取消保留", command=self.RemoveTop)
        else:
            self.rootwidget.menu.add_command(label="保留", command=self.AddTop)
        self.rootwidget.menu.add_command(label="清除", command=lambda: self.root.DeleteHistory(text,HistoryList.index(self.widget)))
        self.rootwidget.menu.add_separator()
        self.rootwidget.menu.add_command(label="全部清除", command=lambda: self.root.DeleteAll())

        self.rootwidget.menu.post(x,y)   # post在指定的位置显示弹出菜单


def CreateToolTip(root,rootwidget,widget):
        toolTip = ToolTip(root,rootwidget,widget)
        def enter(event):
            toolTip.hovershow("#C0C0C0")
        def leave(event):
            toolTip.hoverhide("#FFFFFF")
        def click(event):
            toolTip.Leftclick()
        #def click2(event):
            #toolTip.Rightclick(event.x_root, event.y_root)
       
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        widget.bind('<Button-1>',click)
        #widget.bind('<Button-3>',click2)



class history:

    def __init__(self,fileObj,tk_window = None):
        '''
        fileObj      历史文件存储结构体 RecordHty类
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        '''
        self.fileObj = fileObj
        self.root = tk_window
      
        #self.CreatHistory()
    

    def CreatHistory(self):
        """创建顶层窗口"""
        if(self.root == None):
            self.window = tk.Tk() 
        else:
            self.window = tk.Toplevel(self.root, width=WinWidth, height=WinHeight)
        
        #take a name for this windows
        self.window.title("历史记录")
        #set window size for GUI
        x = max(self.root.winfo_x()-WinWidth,0)
        y = max(self.root.winfo_y(),0)
        self.window.geometry('%dx%d+%d+%d' % (WinWidth, WinHeight,x,y))
        #self.window.geometry(str(WinWidth)+"x"+str(WinHeight)+'+'+str(self.window.winfo_x)+'+'+str(self.window.winfo_y))
        self.window.resizable(False, False)
        self.window.attributes('-alpha',0.9)

        #想要实现透明标题栏，成功了！！
        self.window.overrideredirect(True)
        pad = 40 #想要实现透明标题栏，成功了！！
        #创建画布
        self.canvas= tk.Canvas(self.window,width = WinWidth,height=WinHeight, scrollregion=(0,0,WinWidth,WinHeight-pad)) #

        self.fm1 = ttk.Frame(self.canvas)
        self.fm2 = ttk.Frame(self.window,height=80)
      
        #pad = 40 #想要实现透明标题栏，成功了！！
        #竖直滚动条
        self.vbar=tk.Scrollbar(self.canvas,
                  orient=tk.VERTICAL,
                  command=self.canvas.yview,
                  width=5) 
        self.canvas.config(yscrollcommand= self.vbar.set,bg="white",selectforeground="white",highlightthickness = 1)
       
        self.canvas.place(x = 0, y = pad,width=WinWidth,height=WinHeight-pad) #放置canvas的位置  
        self.vbar.place(x = 215,y= (-pad),width=5,height=(WinHeight+pad))
        self.canvas.create_window(((0,0)), window=self.fm1,anchor='nw')  #create_window       
        """
        self.btnSet = ttk.Button(self.fm2,
                        text='增加',
                        command=self.labelSetClick)
        self.btnClear = ttk.Button(self.fm2,
                          text='清空按钮',
                          command=self.labelClearClick)
        """
        self.Tip = ttk.Label(self.fm2,text="点击历史，复制文本到剪贴板 ctrl+v 黏贴",wraplength = 150,font=("微软雅黑",8))

        #创建标题栏,想要实现透明标题栏，但是失败了
        self.Lab = ttk.Label(self.window, text='历史记录',foreground = "Gray", font=('Microsoft Yahei', 12))
        self.Lab.pack(side=TOP,anchor=W,fill=X,expand=N)
        #self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        #两按键，用于调试  实际应用可注释 fm2，并将command函数重写
        #self.btnSet.pack(side=LEFT,anchor=W,fill=X,expand=YES)
        #self.btnClear.pack(side=LEFT,anchor=W,fill=X,expand=YES) 
        self.Tip.pack(side=TOP,anchor=W,fill=X,expand=YES) 
        
        #失焦后退出
        def out(event):
            self.window.destroy()
        self.window.bind("<FocusOut>",out)

        #遍历历史记录
        for k,v in self.fileObj.dict.items():
            self.AddHistory(k,v)
        if(self.IsEmpty()):
            self.EmptyLabel = ttk.Label(self.fm1,anchor="center",text="空",wraplength = 150,font=("微软雅黑",12))
            self.EmptyLabel.place(x = 110,y=100)

        self.fm1.bind("<Configure>",self.updateCanvas)
        #self.fm1.pack(side=TOP, fill=X, expand=N)
        self.fm2.pack(side=tk.BOTTOM, fill=X, expand=N)
        #获取焦点
        self.window.focus_set()
        self.window.wait_window(self.window)
        self.window.mainloop()

    def ClickItem(event,self):
        """点击后退出历史窗口并返回元素结果"""
        global selectEditCont
        return selectEditCont

    def getTime(self):
        """更新当前时间"""
        self.time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')

    def WheelCtrl(self,event):
        """滚轮事件，绑定画布'"""
        self.fm2.forget()
        self.canvas.yview_scroll(int(-1*(event.delta/120)),"units") 
    
    def ListItem_about(self,cmd):
        """弹窗操作 置顶:'top',删除：'del'"""

    def updateCanvas(self,event):
        """铺满当前画布 少了这个就滚动不了"""
        height = self.fm1.winfo_height()
        if(height > (WinHeight-40)):
            self.canvas.bind_all("<MouseWheel>",self.WheelCtrl)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=WinWidth,height=200)
        pass
        
    def labelSetClick(self):
        """动态增加的组件"""
        self.getTime()
        self.place(self.time,"你今天真好看")
        # 根据需要禁用和启用“增加按钮”和“清空按钮”
        if(len(HistoryList)!=0):
           self.btnClear['state'] = 'normal' 

    # 删除动态创建的组件
    def labelClearClick(self):
        """删除动态创建的组件"""
        global HistoryList
        
        for history in HistoryList:
            history.destroy()
        HistoryList = []   
        #self.DeleteHistory(Index=2)
        if(self.IsEmpty()):
             self.btnClear['state'] = 'disabled'
        self.btnSet['state'] = 'normal'
   
    def AddHistory(self,time,text):
        """创建的组件"""
        #self.getTime()
        self.place(time,text)
    
    def place(self,time,text):
        """在fm1中动态创建Label组件,time当前时间,text"""
        i = len(HistoryList)
        exec('label'+str(i)+'=ttk.Label(self.fm1,text = text,background = "#FFFFFF",wraplength = 210,borderwidth= 10,width = 215,takefocus=True,padding = 2,font=("微软雅黑",8))')
        """
        exec('label'+str(i)+'=tk.Text(self.fm1,background = "#FFFFF0",highlightcolor = "#696969",highlightthickness = 1,undo = True, height=4,font=("微软雅黑",8))')
        eval('label'+str(i)).tag_config('tag',foreground='DimGray',font =("微软雅黑",7) ) #设置tag即插入文字的大小,颜色等
        eval('label'+str(i)).insert(1.0,text)
        eval('label'+str(i)).insert(0.0,time+'\n','tag')
        #记录不可编辑
        eval('label'+str(i)).unbind("<MouseWheel>")
        eval('label'+str(i))['state'] = 'disabled'
        """
        eval('label'+str(i)).pack(side=TOP,anchor="nw",fill=X,expand=N,pady = 2)
        self.SelectHistroy(eval('label'+str(i)))
        CreateToolTip(self,self.window,eval('label'+str(i)))
        HistoryList.append(eval('label'+str(i)))

    def DeleteHistory(self,text,Index = None):
        """在fm1中动态删除Text组件,Index:删除指定下标  默认删除列表尾节点"""
        global HistoryList
        if(Index == None):
            HistoryList.pop().destroy()
        else:
            HistoryList[Index].destroy()
            for k in list(self.fileObj.dict): # 使用list强制copy d.keys()，避免pop出错
	            if self.fileObj.dict[k] == text:
		            self.fileObj.dict.pop(k)# 或者 del d[k] 
            del HistoryList[Index]
            self.fileObj.SaveRec()
    
    def DeleteAll(self):
        """清除所有历史记录(面板) -- 仅用于测试历史窗口显示配合按键labelClearClick"""
        global HistoryList
        """
        for history in HistoryList:
            if(HistoryList.index(history) not in HistoryRemind_List):
                history.destroy()
                HistoryList.pop(history)
                for k in list(self.fileObj.dict): # 使用list强制copy d.keys()，避免pop出错
	                if self.fileObj.dict[k] != history:
		                self.fileObj.dict.pop(k)# 或者 del d[k] 
        """
        for history in HistoryList:
            history.destroy()
        HistoryList = []
        self.fileObj.SaveRec()

    def DelAllData(self):
        """清除所有历史记录(文件)"""
        """
        for k in list(self.fileObj.dict): # 使用list强制copy d.keys()，避免pop出错
            if HistoryList.index(self.fileObj.dict[k]) not in HistoryRemind_List:
                self.fileObj.dict.pop(k)# 或者 del d[k] 
        """
        self.fileObj.dict = {}
        self.fileObj.SaveRec()

    def IsEmpty(self):
        """判空"""
        if(len(HistoryList)):
            return False
        return True

    def SelectHistroy(self,widget = None):
        """鼠标左键点击历史元素返回内容"""
        if(widget): 
            return
        text = widget.get("0,0",END)
        self.window.destroy()
        return text

    def RightSelectHistory(self,widget):
        """鼠标右键点击历史记录 弹出两种操作 置顶、删除"""
        index = HistoryList.index(widget)
        widget.get("0,0",END)
        #label.pack(ipadx=1)

if __name__ == '__main__':
    path = os.path.join(os.extsep,*PATH)
    HistoryFile = RecordHty(path+File)
    myhistory = history(HistoryFile)
    myhistory.CreatHistory()

        