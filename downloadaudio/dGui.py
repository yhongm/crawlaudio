import tkinter as tk
import sys
import os
import webbrowser

from middlewares import DownloadautioSpiderMiddleware
import re
from scrapy import cmdline
import settings
import multiprocessing
from tkinter.filedialog import askdirectory
from tkinter.simpledialog import messagebox
from tkinter.messagebox import askokcancel
from file_handle import FileEntry


class App:
    def __init__(self, width=500, height=180):
        self.w = width
        self.h = height
        self.title = "音频节目专辑抓取器"
        self.root = tk.Tk(className=self.title)
        self.url = tk.StringVar()
        self.path = tk.StringVar()
        self.v = tk.IntVar()
        self.tkMsgBox = messagebox
        self.v.set(1)
        self.fileEntry = FileEntry()

        self.path.set(self.fileEntry.readPath())
        frame = tk.Frame(self.root)

        menu = tk.Menu(self.root)
        self.root.configure(menu=menu)

        aboutmenu = tk.Menu(menu, tearoff=0)
        aboutmenu.add_command(label='关于作者', command=self.showAuthor)
        menu.add_cascade(label="关于", menu=aboutmenu)
        link_label = tk.Label(frame, text="please input autio link")
        link_entry = tk.Entry(frame, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=30)
        path_label = tk.Label(frame, text="please input save folder")
        path_entry = tk.Button(frame, textvariable=self.path, background='White', highlightcolor='Red',
                               highlightthickness=1, width=30, command=self.selectPath)
        b_get = tk.Button(frame, text="get", font=('楷体', 12), fg='Purple', width=10, height=1, command=self.get)
        b_save = tk.Button(frame, text='save', font=('楷体', 12), fg='Red', width=10, height=1, command=self.save)
        e_label = tk.Label(frame, width=10, height=1)

        l_link = tk.Label(frame, text='www.520tingshu.com', background='White', highlightthickness=1, width=30,
                          height=1, fg='Black')
        b_link = tk.Button(frame, text='link', width=10, height=1, fg='Black',
                           command=lambda: webbrowser.open('http://www.520tingshu.com'))
        link_label.grid(row=0, column=0)
        link_entry.grid(row=1, column=0)
        b_get.grid(row=1, column=1)
        path_label.grid(row=2, column=0)
        path_entry.grid(row=3, column=0)
        b_save.grid(row=3, column=1)
        e_label.grid(row=4, column=1)

        l_link.grid(row=5, column=0)
        b_link.grid(row=5, column=1)
        frame.pack()

    def get(self):
        print("url:" + str(self.url.get()))
        print("murl before:" + str(settings.MURL))
        currentPath = self.fileEntry.readPath()
        if (str(currentPath).strip() == ''):
            self.showInfo("未选择保存文件夹不能获取音频节目专辑")
        else:
            currentUrl = self.url.get()
            result = re.match("http://www.520tingshu.com/book/book.{1,10}.html", currentUrl)
            if (result):
                self.fileEntry.writeUrl(currentUrl)
                print("murl after:" + str(settings.MURL))
                name = multiprocessing.current_process().name
                print("pname:" + name)
                self.run()
            else:
                self.showInfo("不支持当前页面或网站,仅仅支持www.520tingshu.com站内页面  ")

    def save(self):
        currentPath = self.path.get()
        if (str(currentPath).strip() == ''):
            self.showInfo("未选择保存文件夹不能保存")
        else:
            print("save:" + currentPath)
            self.fileEntry.writePath(self.path.get())

    def selectPath(self):
        path_ = askdirectory()
        if (str(path_).strip() == ''):

            self.showInfo("未选择保存文件夹")
        else:
            print("selectPath:" + path_)
            self.path.set(path_)

    def run(self):
        p = multiprocessing.Process(target=runCmd, args=())
        p.start()
        p.join()

    def showAuthor(self):
        self.showInfo("作者:yhongm")

    def center(self):
        wx_h = self.root.winfo_screenheight()
        wx_w = self.root.winfo_screenwidth()
        x = int((wx_w / 2) - (self.w / 2))
        y = int((wx_h / 2) - (self.h / 2))

        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def loop(self):
        self.root.resizable(False, False)
        self.center()
        self.root.mainloop()

    def showInfo(self, info):
        self.tkMsgBox.showerror(title="提示", message=info)


def runCmd():
    name = multiprocessing.current_process().name
    print("runCmd_pname:" + name)
    cmdline.execute('scrapy crawl dautio'.split())


if __name__ == "__main__":
    app = App()
    app.loop()
