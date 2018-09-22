#libs
from tkinter import *
from tkinter import filedialog
import os
from bs4 import BeautifulSoup
import requests as rq
import urllib.request
import random
 
#important variables
baseAdresses = []
fileUrls = []

#create root window and set properties
root = Tk()
root.title("4chan File Downloader")
root.configure(bg="white")
root.geometry("300x400")

#functions
def update_listbox():
    #clear the listbox
    clear_listbox()
    #populate listbox
    for baseAdresse in baseAdresses:
        lb_tasks.insert("end", baseAdresse)

def clear_listbox():
    lb_tasks.delete(0, "end")

def add_url():
    task = txt_input.get()
    if task != "":
        baseAdresses.append(task)
        
    elif task[4:] != "http":
        lbl_disp["text"] = "Please Enter a valid 4chan Url!"     

    else:
        lbl_disp["text"] = "Please Enter a valid 4chan Url!"
    
    txt_input.delete(0,"end")
    update_listbox()


def del_one():
    #get the text of curr seleced task
    task = lb_tasks.get("active")
    if task in tasks:
        tasks.remove(task)

    update_listbox()

def del_all():
    #globalizing tasks list
    global baseAdresses
    baseAdresses = []
    update_listbox()

def del_one():
    #get the text of curr seleced task
    baseAdresse = lb_tasks.get("active")
    if baseAdresse in baseAdresses:
        baseAdresses.remove(baseAdresse)

    update_listbox()

def dir_path():
   root.directory = filedialog.askdirectory()
   dir_path = root.directory + "/"
   return dir_path
   
def exit():
    quit()

#download functions
def download():
    path = dir_path()
    global baseAdresses
    for baseAdresse in baseAdresses:
        #get full html code
        page =  rq.get(baseAdresse)
        soup = BeautifulSoup(page.content, "html.parser")
        
        #find divs with the right image resolution                  
        divs = soup.find_all("div",{"class":"fileText"})
        for div in divs:
            #extract href from 'a' tag and make a proper http link
            text = div.find("a")
            text = text["href"]
            url ="http:" + text
            fileUrls.append(url)

        lb_tasks.delete(0, "end")
        for fileUrl in fileUrls:
            download_files(fileUrl,path)


def download_files(url,path):
    
    #random file name with the right format
    imgName = random.randint(1,100000) 
    if url[-3:] == "jpg":
        fullFileName = str(imgName) + ".jpg"
    elif url[-3:] == "gif":
        fullFileName = str(imgName) + ".gif"
    elif url[-3:] == "png":
        fullFileName = str(imgName) + ".png"
    elif url[-4:] == "webm":
        fullFileName = str(imgName) + ".webm"
     
    fullFileName = os.path.join(path, fullFileName)
    #download actual file if possible
    try: 
        urllib.request.urlretrieve(url,fullFileName)
        lb_tasks.insert("end","downloaded " + fullImgName)
    except:
        lb_tasks.insert("end", "error")

#create widgets
lbl_text = Label(root, text="4chan Meme Downloader", bg="white")
lbl_text.pack()

lbl_disp = Label(root, text="", bg="white")
lbl_disp.pack()

txt_input = Entry(root, width=225)
txt_input.pack()

btn_add_task = Button(root,text = "Add 4chan Thread Url", fg="green", bg="white", command = add_url)
btn_add_task.pack()

btn_del_one = Button(root,text = "Delete One", fg="green", bg="white", command = del_one)
btn_del_one.pack()

btn_del_all = Button(root,text = "Delete All", fg="green", bg="white", command = del_all)
btn_del_all.pack()

btn_download = Button(root,text = "Download", fg="green", bg="white", command = download)
btn_download.pack()

btn_exit = Button(root,text="Exit", bg="white", fg="green", command=exit)
btn_exit.pack()

lb_tasks = Listbox(root,width=300)
lb_tasks.pack()

#main event loop
root.mainloop()