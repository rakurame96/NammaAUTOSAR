#
# Created on Sun Aug 21 2022 7:14:37 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import tkinter as tk
from tkinter import ttk

import json
import os


class AppInfo:
    git = None
    arxml = None


AppView = None
N_AppsStr = None
N_Apps = 0
HeaderObjs = 3   # Objects / widgets that are part of the header and shouldn't be destroyed
HeaderSize = 2   # Number of rows in Header Area of view
MaxApps = 1024

AppRepoStr_List = []
AppInfo_List = []

Parent_Frame = None
Canvas_Frame = None
Child_Frame = None
Canvas = None

AppJsonFile = os.getcwd()+"/submodules/AL/applications.json"


def update_or_clone_app(app_id):
    print("clone git repo ("+str(app_id)+") is under construction!")
    
def select_arxml_file(app_id):
    print("clone git repo ("+str(app_id)+") is under construction!")


def contains_any(str, set):
    return True in [c in str for c in set]

def validate_git_path(path):
    if ".git" not in path:
        return None
    if contains_any(path, '<>'):
        return None
    return path


def backup_data():
    data = []
    for i in range(N_Apps):
        AppInfo_List[i].git = validate_git_path(AppRepoStr_List[i].get())
        appinfo = {}
        appinfo["git"] = AppInfo_List[i].git
        appinfo["arxml"] = AppInfo_List[i].arxml
        data.append(appinfo)
    
    with open(AppJsonFile, "w") as jfile:
        json.dump(data, jfile)


def restore_data_from_disk():
    global N_Apps, AppJsonFile, AppInfo_List
    
    data = None
    with open(AppJsonFile) as jfile:
        data = json.load(jfile)
        
    N_Apps = len(data)
    
    AppInfo_List.clear()
    for item in data:
        appinfo = AppInfo()
        appinfo.git = item["git"]
        appinfo.arxml = item["arxml"]
        AppInfo_List.append(appinfo)



def app_draw(view, xsize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, HeaderObjs, MaxApps
    global Canvas
    
    print("xsize = ", xsize)
    
    view.grid_rowconfigure(0, weight=1)
    view.columnconfigure(0, weight=1)
    Parent_Frame = tk.Frame(view)
    Parent_Frame.grid(sticky="news")

    # Create a frame for the Canvas with non-zero row&column weights
    Canvas_Frame = tk.Frame(Parent_Frame)
    Canvas_Frame.grid(row=2, column=0, pady=(5, 0), sticky='nw')
    Canvas_Frame.grid_rowconfigure(0, weight=1)
    Canvas_Frame.grid_columnconfigure(0, weight=1)

    # Set grid_propagate to False to allow Canvas frame resizing later
    Canvas_Frame.grid_propagate(False)

    # Add a Canvas in that frame
    Canvas = tk.Canvas(Canvas_Frame)
    Canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the Canvas
    scrollbar = tk.Scrollbar(Canvas_Frame, orient="vertical", command=Canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    Canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to draw message table
    Child_Frame = tk.Frame(Canvas)
    Canvas.create_window((0, 0), window=Child_Frame, anchor='nw')

    #Number of modes - Label + Spinbox
    label = tk.Label(Child_Frame, text="No. of Application SWCs:")
    label.grid(row=0, column=0, sticky="w")
    N_AppsStr = tk.StringVar()
    spinb = tk.Spinbox(Child_Frame, width=10, textvariable=N_AppsStr, command=lambda: update_apps(N_AppsStr, xsize),
                values=tuple(range(0,MaxApps)))
    N_AppsStr.set(N_Apps)
    spinb.grid(row=0, column=1, sticky="w")
    
    label_spc = tk.Label(Child_Frame, text="---")
    label_spc.grid(row=1, column=0, sticky="w")

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    Child_Frame.update_idletasks()
    # Resize the main frame to show contents for FULL SCREEN (Todo: scroll bars won't work in reduced size window)
    canvas_w = view.winfo_screenwidth()-scrollbar.winfo_width()
    canvas_h = view.winfo_screenheight()-(spinb.winfo_height()*6)
    Canvas_Frame.config(width=canvas_w, height=canvas_h)

    app_update(xsize)



def update_apps(mstr, xsize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, HeaderObjs, MaxApps
    
    N_Apps = int(mstr.get())
    # print("No of Apps: "+ str(N_Apps))        
    for i, item in enumerate(Child_Frame.winfo_children()):
        if i >= HeaderObjs:
            item.destroy()
    app_update(xsize)



def app_update(xsize):
    global Parent_Frame, Canvas_Frame, Child_Frame, N_Apps, N_AppsStr, HeaderObjs, MaxApps
    global AppInfo_List, Canvas

    # Tune memory allocations based on number of rows or boxes
    n_apps_str = len(AppRepoStr_List)
    if N_Apps > n_apps_str:
        for i in range(N_Apps - n_apps_str):
            AppRepoStr_List.insert(len(AppRepoStr_List), tk.StringVar())
            appinfo = AppInfo()
            appinfo.git = "<Enter the git clone path here>"
            appinfo.arxml = None
            AppInfo_List.insert(len(AppInfo_List), appinfo)
    elif n_apps_str > N_Apps:
        for i in range(n_apps_str - N_Apps):
            del AppRepoStr_List[-1]
            del AppInfo_List[-1]

    #print("n_apps_str = "+ str(n_apps_str) + ", n_apps = " + str(N_Apps))
    # Draw new objects
    for i in range(0, N_Apps):
        # Label
        label = tk.Label(Child_Frame, text="App "+str(i)+": ")
        label.grid(row=HeaderSize+i, column=0, sticky="e")

        # Edit box
        entry = tk.Entry(Child_Frame, width=int(xsize/(2*5)), textvariable=AppRepoStr_List[i])
        AppRepoStr_List[i].set(AppInfo_List[i].git)
        entry.grid(row=HeaderSize+i, column=1)

        # Button - Update / Clone
        select = tk.Button(Child_Frame, width=10, text="Update", command=lambda id = i : update_or_clone_app(id))
        select.grid(row=HeaderSize+i, column=2)

        # Button - Update / Clone
        select = tk.Button(Child_Frame, width=20, text="Select ARXML File", command=lambda id = i : select_arxml_file(id))
        select.grid(row=HeaderSize+i, column=3)

    # Set the Canvas scrolling region
    Canvas.config(scrollregion=Canvas.bbox("all"))


def on_app_view_close():
    global AppView

    AppView.destroy()
    AppView = None
    backup_data()
    

###############################################################################
# Main Entry Points
def app_block_constructor(gui, app_blk):
    restore_data_from_disk()



def app_block_click_handler(gui):
    global AppView
    
    # If previous view is active return
    if AppView != None:
        return

    # Create a child window
    width = gui.main_view.xsize * 70 / 100
    height = gui.main_view.ysize * 70 / 100
    AppView = tk.Toplevel()
    AppView.geometry("%dx%d+%d+%d" % (width, height, 10, 50))
    AppView.title("Applications Configs")
    AppView.protocol("WM_DELETE_WINDOW", on_app_view_close)

    app_draw(AppView, width)
    print("App block click handler -- under construction")
