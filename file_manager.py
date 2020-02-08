from tkinter import *
import tkinter.ttk as ttk
import os
import shutil


dir = os.getcwd()

#Creating window
root = Tk()
root.title("File manager")
root.configure(background = "white")
root.geometry("950x500")
root.resizable(0,0)

#Folder and File images
folder_icon_png = PhotoImage(file =r"/Users/enriavil1/Desktop/project/Python/intermidiate projects/file_manager/photos/iconfinder_folder_299060.png")

file_icon_png = PhotoImage(file =r"/Users/enriavil1/Desktop/project/Python/intermidiate projects/file_manager/photos/iconfinder_File_104851.png")
python_icon_png= PhotoImage(file= r"/Users/enriavil1/Desktop/project/Python/intermidiate projects/file_manager/photos/python_file.png")

#file and folder frame images
folder_icon_for_display= folder_icon_png.subsample(5,5)
file_icon_for_display= file_icon_png.subsample(5,5)
python_icon_for_display= python_icon_png.subsample(5,5)

#actions in the dropdown menu
actions= [
    "go in",
    "pick file to move",
    "copy",
    "delete"
    ]

global action
action= StringVar()
action.set(actions[0])
 
#variable for file to move
file_to_move= None

#adding files
def add_files_to_frame(scrollable_frame,current_dir,button_action):
    global files
    files = os.listdir(current_dir)


    column= 0
    row= 1


    btn= []
    for i in range(len(files)):
        if ".DS_Store" in files:
            files.pop(files.index(".DS_Store"))
        if ".vscode" in files:
            files.pop(files.index(".vscode"))

    #backward button
    backward_button = Button(scrollable_frame, text= "<", padx= 10, command= lambda: go_back(current_dir))
    backward_button.grid(column= 0, row= 0)

    #menu to decide action
    drop= OptionMenu(scrollable_frame, action, *actions)
    drop.grid_propagate(0)
    drop.grid(column= 1, row= 0, columnspan= 3, padx=80)

    #here button to move file to that directory/folder
    global here_button
    here_button= Button(
    scrollable_frame, 
    text= "move file here",
    state= DISABLED,
    command= move_file
    )

    #paste button
    global paste
    paste= Button(
        scrollable_frame,
        text= "paste here",
        state= DISABLED,
        command= paste
    )

    #adds files to frame 
    for i in range(len(files)):
        fullname = os.path.join(current_dir, files[i])

        #checks if the file is a folder
        if os.path.isdir(fullname) == True:
            button= Button(
                scrollable_frame,
                text= str(files[i]),
                image= folder_icon_for_display,
                pady=10,
                padx= 10,
                compound = TOP,
                command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
            )
            btn.append(button)
            button.grid(column= column, row =row)
            column += 1
            if column >= 5:
                column= 0
                row+= 1
        #check if the file is not a folder
        else:
            if str(files[i]).endswith(".py"):
                button= Button(
                    scrollable_frame,
                    text= str(files[i]),
                    image= python_icon_for_display,
                    padx= 10,
                    pady= 10,
                    compound = TOP,
                    command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
                )
                button.grid(column= column, row= row)
                btn.append(button)
                column+=1
                if column >= 5:
                    column= 0
                    row += 1
            else:
                button= Button(
                    scrollable_frame,
                    text= str(files[i]),
                    image= file_icon_for_display,
                    padx= 10,
                    pady= 10,
                    compound = TOP,
                    command= lambda c=i: button_action(current_dir, btn[c].cget("text"))
                )
                btn.append(button)
                button.grid(column= column, row= row)
                column +=1 
                if column >= 5:
                    column= 0
                    row += 1


#changing directories
def button_action(current_dir, name):
    global state
    global old_dir
    global new_dir_path
    global file_to_move

    state = action.get()

    if state == "go in":
        #writes the new directory and changes the current working directory
        new_dir_path= os.path.join(current_dir, name)
        os.chdir(new_dir_path)
        new_dir = os.getcwd()

        #destroys all the frames and packs them with new files
        container.destroy()
        tree_frame.destroy()
        creating_frame(new_dir)
        create_tree_frame()
        add_files_to_tree("", new_dir)

        if file_to_move is not None:
            #enabling here button
            here_button.configure(state= NORMAL)
            here_button.grid(row= 0, column= 4)

    if state == "pick file to move":
        #file to move
        file_to_move= os.path.join(current_dir, name)

        action.set(actions[0])

        #enabling here button
        here_button.configure(state= NORMAL)
        here_button.grid(row= 0, column= 4)
    
    if state == "copy":
        #copied file
        file_to_copy= os.path(current_dir, name)
        



#function to move a file to a new place
def move_file():
    global file_to_move
    print(file_to_move)

    working_dir = os.getcwd()

    if file_to_move == working_dir:
        #creates a warning window
        error = Toplevel()
        error.title("Same directory")
        error.geometry("150x150")
        error.propagate(0)
        error.resizable(0,0)

        #a canvas to set a red color to the window
        error_canvas = Frame(
            error, 
            width= 200, 
            height= 200, 
            bg= "red"
            )
        error_canvas.pack_propagate(0)
        error_canvas.pack()

        #warning sign
        warning_sign= Label(
            error_canvas,
            text= "WARNING",
            bg= "red"
        )
        warning_sign.pack()

        #message with the problem
        label_message= Label(
            error_canvas, 
            text= "You can\'t put the \nselected file here",
            bg= "red"
            )
        label_message.pack()
    else:
        try:
            #move file into new dir
            shutil.move(file_to_move, os.getcwd())

            file_to_move = None
            button_action(working_dir, "")
        except Exception:
            #creates a warning window
            error = Toplevel()
            error.title("Same directory")
            error.geometry("150x150")
            error.propagate(0)
            error.resizable(0,0)

            #a canvas to set a red color to the window
            error_canvas = Frame(
                error, 
                width= 200, 
                height= 200, 
                bg= "red"
                )
            error_canvas.pack_propagate(0)
            error_canvas.pack()

            #warning sign
            warning_sign= Label(
                error_canvas,
                text= "WARNING",
                bg= "red"
            )
            warning_sign.pack()

            #message with the problem
            label_message= Label(
                error_canvas, 
                text= "You can\'t put the \nselected file here",
                bg= "red"
                )
            label_message.pack()


        



#going back
def go_back(current_dir):
    #separates the current directory per word and takes the last directory off the path
    old_dir_split = current_dir.split("/")
    old_dir_split.pop()

    #Joins the dir which is the same as the directory before the current one
    new_dir= "/".join(old_dir_split)

    #changes the directory 
    os.chdir(new_dir)

    #destroys the current frames and creates new frames with the files of the new directory
    container.destroy()
    tree_frame.destroy()
    creating_frame(new_dir)
    create_tree_frame()
    add_files_to_tree("", new_dir)

    #Checks if there is a current file it can move
    if file_to_move is not None:
        #enabling here button
        here_button.configure(state= NORMAL)
        here_button.grid(row= 0, column= 4)

#creating frame
def creating_frame(current_dir):
    global row
    global column

    #Frame for files
    global container
    container=Frame(root,width=750,height=500,bd=1, bg= "white")
    container.grid(row=0, column= 2)
    container.grid_propagate(0)

    #scrollable frame for file display
    canvas=Canvas(container, width= 720, height= 500, bg= "white")
    scrollable_frame=Frame(canvas, bg= "white")
    myscrollbar=Scrollbar(container,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left", fill= "both")
    canvas.create_window((0,0),window=scrollable_frame,anchor='nw')
    canvas.pack_propagate(0)
    scrollable_frame.bind(
        "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
        )
    )

    add_files_to_frame(scrollable_frame, current_dir, button_action)

creating_frame(dir)

#tree view images
folder_icon_for_tree= folder_icon_png.subsample(30,30)
file_icon_for_tree= file_icon_png.subsample(30,30)
python_icon_for_tree= python_icon_png.subsample(25,25)

def create_tree_frame():
        #Frame for tree view
    global tree_frame
    tree_frame = Frame(root, bg = "grey", width = 200, height = 500)
    tree_frame.grid(row = 0, column =1)
    tree_frame.grid_propagate(0)

    #scrollable frame for tree files
    tree_canvas = Canvas(tree_frame, width= 187, height= 500, bg= "grey")
    scrollable_treeframe= Frame(tree_canvas, bg= "grey")
    tree_scrollbar= Scrollbar(tree_frame, orient="vertical", command= tree_canvas.yview)
    horizontal_tree_scrollbar= Scrollbar(tree_frame, orient= "horizontal", command= tree_canvas.xview)
    tree_canvas.configure(yscrollcommand= tree_scrollbar.set) #xscrollcommand= horizontal_tree_scrollbar.set

    tree_scrollbar.pack(side="right", fill= "y")
    #horizontal_tree_scrollbar.pack(side= "bottom", fill= "x")
    tree_canvas.pack(side="left", fill= "both")
    tree_canvas.create_window((0,0), window= scrollable_treeframe, anchor= "nw")
    scrollable_treeframe.bind(
        "<Configure>",
        lambda e: tree_canvas.configure(
            scrollregion=tree_canvas.bbox("all")    
        )    
    )
    global tree
    tree = ttk.Treeview(scrollable_treeframe, height= 100)

    tree.column("#0", minwidth= 190, stretch= FALSE)
    tree.heading("#0", text= "files in current folder", anchor= W)

create_tree_frame()

#adding files to the tree frame
def add_files_to_tree(parent,current_dir):
    #getting current dir
    files = os.listdir(current_dir)

    tree_item= []

    for i in range(len(files)):
        if ".DS_Store" in files:
            files.pop(files.index(".DS_Store"))
        if ".vscode" in files:
            files.pop(files.index(".vscode"))
    index = 1
    #adding the files in the view
    for i in range(len(files)):
        fullname = os.path.join(current_dir, files[i])
        if os.path.isdir(fullname) == True:
            folder = tree.insert(
                parent, 
                index, 
                text= str(files[i]), 
                image= folder_icon_for_tree
                )
            tree_item.append(folder)

            add_files_to_tree(folder, fullname)
            index += 1
        else:
            if str(files[i]).endswith(".py"):
                file = tree.insert(
                    parent, 
                    index,  
                    text= str(files[i]), 
                    image= python_icon_for_tree
                    )
                tree_item.append(file)
                index+= 1
            else:
                file = tree.insert(
                    parent, 
                    index,  
                    text= str(files[i]), 
                    image= file_icon_for_tree
                    )
                tree_item.append(file)
                index+= 1
    tree.pack(side= TOP, fill= X)


add_files_to_tree("",dir)






#runs the window
root.mainloop()

