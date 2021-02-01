import tkinter as tk
import os.path
from tkinter import messagebox
import tkinter.font as tkFont

#--------------------------函数和声明------------------------------
itemlist = []
#用来对任务进行暂时存储

def initialize():
    if os.path.exists('task_data.txt'):
        #文件存在，读文件
        file = open('task_data.txt', 'r')
        file.seek(0)
        line = file.readline()
        while line != "":
            itemlist.append(line)
            line = file.readline()
        file.close()
        while '\n' in itemlist:
            itemlist.remove('\n')
        #print(itemlist)
        itemlist.sort()
        for x in itemlist:
            todolist.insert(tk.END, x)
    else:
        #文件不存在，创建文件
        file = open("task_data.txt", 'w')

def add():
    file = open('task_data.txt', 'a')
    tasktext = task.get()
    deadlinetext = deadline.get()
    mergedtext = deadlinetext + " " + tasktext

    # 判断所输入的截止日期是否有效
    if len(tasktext) == 0 or len(deadlinetext) == 0:
        return
    else:
        if len(deadlinetext) != 8:
            messagebox.showwarning("Warning", "The date entered is invalid\nPlease try again in this format：YYYYMMDD\n\n eg. 20191204")
        else:
            try:
                millennium = deadlinetext[0]
                month = deadlinetext[4:6]
                day = deadlinetext[-2:]
                # print(int(millennium))
                # print(int(month))
                # print(int(day))
                if int(millennium) != 2 or int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > 31:
                    # 判断年，月，日   
                    messagebox.showwarning("Warning", "The date entered is invalid\nPlease try again in this format：YYYYMMDD\n\n eg. 20191204")
                    return 
                elif int(month)==2:
                    #二月平
                    if int(day)>29:
                        messagebox.showwarning("Warning", "The date entered is invalid\nPlease try again in this format：YYYYMMDD\n\n eg. 20191204")
                        return                    
                elif int(month)== 4 or 6 or 9 or 11:
                    #小月
                    if int(day)>30:
                        messagebox.showwarning("Warning", "The date entered is invalid\nPlease try again in this format：YYYYMMDD\n\n eg. 20191204")
                        return  
                todolist.insert(tk.END, mergedtext)      #将任务插入listbox中
                itemlist.append(mergedtext)
                file.write(str(mergedtext) + '\n')       #将任务写入txt文件中
                task.delete(0, 'end')
                deadline.delete(0, 'end')
                file.close()
            except ValueError:
                # 若输入的截止日期为其他字符
                messagebox.showwarning("Warning", "The date entered is invalid\nPlease try again in this format：YYYYMMDD\n\n eg. 20191204")
                return

def edit():
    try:
        item_num = todolist.curselection()
        todolist.delete(item_num)
    except:
        messagebox.showwarning("Warning","No task selected yet")
    else:
        file = open('task_data.txt', 'w')
        item_marker = item_num[0]
        item = itemlist[item_marker]
        temp=item.replace("\n","")        #剔除换行符
        raw=temp.replace(" ","")          #剔除空格
        #print(raw)
        deadline_segment=raw[0:8]         #提取截止日期
        #print(deadline_segment)
        task_segment=raw[8:]              #提取任务内容
        #print(task_segment)
        task.insert(0, task_segment)            #任务内容写回entry控件
        deadline.insert(0, deadline_segment)    #截止日期写回entry控件

        itemlist.remove(itemlist[item_marker])  # 下面步骤与删除操作类似
        file.truncate()
        for x in itemlist:
            file.write(x+'\n')
        file.close()

def delete():
    
    try:
        item_num = todolist.curselection()   #此时item_num为元组
        #print(item_num)
        todolist.delete(item_num)            #把所选任务从listbox中移除
    except:
        messagebox.showwarning("Warning","No task selected yet")
    else:
        file = open('task_data.txt', 'w+')
        item_num = item_num[0]               #从元组item_num中取出所选任务的序号
        #print(item_num)
        del itemlist[item_num]         #把所选任务从暂存列表中删除

        file.truncate()                #清空txt文件
        for x in itemlist:
            file.write(x + '\n')       #将暂存列表中其余未被删除的任务写回txt文件
        file.close()

def clear():
    confirm = messagebox.askyesno("Warning", "Are you sure to clear all tasks?")
    if confirm:
      file = open('task_data.txt', 'w')
      todolist.delete(0, tk.END)
      file.truncate()
      file.close()
      return

def exit_app():
    confirm = messagebox.askyesno("Exit", "Are you sure to exit?")
    if confirm:
        box.destroy()
        quit()


#-------------------------图形用户界面-------------------------------
box = tk.Tk()
box.title('Task Inbox')
box.geometry('840x460')

#-----------控件定义-----------
icon = tk.PhotoImage(file="productivity.png")
logo = tk.Label(box, image=icon)
headline_font = tkFont.Font(family='Eras Bold ITC', size=40)
headline = tk.Label(box, text="  Be productive today! ", font=headline_font)

lab1 = tk.Label(box, text="Create Event：", font=("Aria", 16, "bold"))
lab2 = tk.Label(box, text=" Todo List：\n", font=("Aria", 16, "bold"))
lab3 = tk.Label(box, text="Task:   ", font=("Aria", 14, "bold"))
lab4 = tk.Label(box, text="Deadline：  ", font=("Aria", 14, "bold"))

add_button = tk.Button(box, text="Add", command=add, font=("Times New Roman", 10), bd=3, fg="black", bg="pale green", width=5)
edit_button = tk.Button(box, text="Edit", command=edit, font=("Times New Roman", 10), bd=3, fg="black", bg="pale green", width=5)
del_button = tk.Button(box, text="Del ", command=delete, font=("Times New Roman", 10), bd=3, fg="black", bg="orangered", width=5)
clear_button = tk.Button(box, text="Clear", command=clear, font=("Times New Roman", 10), bd=3, fg="black", bg="crimson", width=5)
exit_button = tk.Button(box, text="Exit", command=exit_app, font=("Times New Roman", 10), bd=3, fg="black", bg="powder blue", width=5)

global task
global deadline
task = tk.Entry(box, width=30)
task.config(borderwidth='4px')
deadline = tk.Entry(box, width=30)
deadline.config(borderwidth='4px')

todolist = tk.Listbox(box, width=40)
todolist.config(borderwidth='4px')

#-----------控件摆放-----------
logo.grid(row=0, column=0)
headline.grid(row=0, column=1, columnspan=3)

lab1.grid(row=1, column=0, sticky=tk.W)
lab2.grid(row=1, column=3, sticky=tk.W)
lab3.grid(row=2, column=0, sticky=tk.E)
lab4.grid(row=3, column=0, sticky=tk.E)

add_button.grid(row=4, column=1, sticky=tk.W)
edit_button.grid(row=2, column=4)
del_button.grid(row=3, column=4)
clear_button.grid(row=4, column=4)
exit_button.grid(row=5, column=4)

task.grid(row=2, column=1, sticky=tk.W)
deadline.grid(row=3, column=1, sticky=tk.W)

todolist.grid(row=2, column=3, rowspan=4)


initialize()
miniicon=tk.PhotoImage(file='box.png')
box.tk.call('wm', 'iconphoto', box._w, miniicon)

box.mainloop()
