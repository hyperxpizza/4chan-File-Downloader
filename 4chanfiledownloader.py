# In order to be able to import tkinter for
# either in python 2 or in python 3
try:                        
    from tkinter import *   
    from tkinter import filedialog 
except:
    from Tkinter import *
    from Tkinter import filedialog
import os
from bs4 import BeautifulSoup
import requests as rq
import urllib.request
import random



class Window():

    def __init__(self):
        self.baseAdresses = []
        self.fileUrls = []
        self.set_properties()
        self.set_widgets()    


    def download(self):
        self.root.directory = filedialog.askdirectory()
        self.dir_path = self.root.directory + "/"
        self.clear_listbox()
        self.lb_box.insert("end", "Downloading...")
        
        #get full html code from every url
        for self.baseAdresse in self.baseAdresses:
            self.page = rq.get(self.baseAdresse)
            self.soup = BeautifulSoup(self.page.content, "html.parser")

            #get the right divs and modify them
            self.divs = self.soup.find_all("div",{"class":"fileText"})
            for self.div in self.divs:
                self.text = self.div.find("a")
                self.text = self.text["href"]
                self.text = "http:"+ self.text
                self.fileUrls.append(self.text)

            for self.fileUrl in self.fileUrls:
                self.download_files(self.fileUrl)

            self.lb_box.insert("end", "Downloaded!")
                
    def download_files(self,url):
        
        self.fileName = random.randint(1,100000)
        if url[-3:] == "jpg":
            self.fullFileName = str(self.fileName) + ".jpg"
        elif url[-3:] == "gif":
            self.fullFileName = str(self.fileName) + ".gif"
        elif url[-3:] == "png":
            self.fullFileName = str(self.fileName) + ".png"
        elif url[-4:] == "webm":
            self.fullFileName = str(self.fileName) + ".webm"

        self.fullFileName = os.path.join(self.dir_path, self.fullFileName)
        self.msg = "saved: " + self.fullFileName
        
         #download actual file 
        urllib.request.urlretrieve(url,self.fullFileName)
        self.lb_box.insert("end", self.msg)


    def add_url(self):
        self.url = self.txt_input.get()

        self.baseAdresses.append(self.url)
        
        self.txt_input.delete(0,"end")
        self.update_listbox()

    def update_listbox(self):
        self.clear_listbox()
        for self.baseAdresse in self.baseAdresses:
            self.lb_box.insert("end", self.baseAdresse)


    def del_all(self):
        self.baseAdresses = []
        self.fileUrls = []
        self.update_listbox()

    def view_baseAdresses(self):
        for self.baseAdresse in self.baseAdresses:
            self.lb_box.insert("end", self.baseAdresse)


    def clear_listbox(self):
        self.lb_box.delete(0, "end")

    def set_properties(self):
        self.root = Tk()
        self.root.geometry("300x400")
        self.root.configure(background='white')
        self.root.resizable(True,False)
        self.root.title("4chan File Downloader")

    def set_widgets(self):
        self.lbl_text = Label(self.root, text="4chan File Downloader", bg="white")
        self.lbl_text.pack()

        self.lbl_disp = Label(self.root, text="", bg="white")
        self.lbl_disp.pack()

        self.txt_input = Entry(self.root, width=225)
        self.txt_input.pack()

        self.btn_add_task = Button(self.root,text = "Add 4chan Thread Url", fg="green", bg="white", command = self.add_url)
        self.btn_add_task.pack()

        self.view_btn = Button(self.root,text="View urls",fg="green", bg="white", command = self.view_baseAdresses)
        self.view_btn.pack()

        self.btn_del_all = Button(self.root,text = "Delete Urls", fg="green", bg="white", command = self.del_all)
        self.btn_del_all.pack()

        self.btn_download = Button(self.root,text = "Download", fg="green", bg="white", command = self.download)
        self.btn_download.pack()

        self.btn_clear_lbbox = Button(self.root, text = "Clear Listbox", fg="green", bg="white", command=self.clear_listbox)
        self.btn_clear_lbbox.pack()

        self.btn_exit = Button(self.root,text="Exit", bg="white", fg="green", command=self.exit)
        self.btn_exit.pack()

        self.lb_box = Listbox(self.root,width=300)
        self.lb_box.pack()

    def exit(self):
        quit()


def Main():
    app = Window()
    app.root.mainloop()


if __name__ == "__main__":
    Main()

