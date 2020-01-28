from tkinter import *
from PIL import Image, ImageTk
import os
import fnmatch
from tkinter.filedialog import askdirectory # python3.5
import shutil



input_path = "./"
files = []
files = fnmatch.filter(os.listdir(input_path), "*.jpg")
index = 0
size = len(files)

root = Tk()
root.title("Aupera Labeler")
f = Frame(root, width=700, height=600, bg="gray")

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def display():
    print ("Processing image " + str(index+1) + " out of " + str(size))
    image2 = Image.open(input_path + files[index])
    image1 = Image.open(input_path + files[index+1])
    image = get_concat_h_blank(image1, image2, color=(0, 0, 0))
    photo = ImageTk.PhotoImage(image)

    label.configure(image=photo)
    label.image = photo # keep a reference!
    label.pack()

def file():
    global input_path
    global files
    global size
    global index
    global parent_dir
    index = 0
    input_path = askdirectory()

    # last_slash = input_path.rfind("/")
    # parent_dir = input_path[:last_slash]
    parent_dir = input_path
    input_path = input_path + "/"
    print (input_path)

    if not os.path.exists(parent_dir + "/correct"):
        os.makedirs(parent_dir + "/correct")
    if not os.path.exists(parent_dir + "/wrong"):
        os.makedirs(parent_dir + "/wrong")
    if not os.path.exists(parent_dir + "/not_sure"):
        os.makedirs(parent_dir + "/not_sure")
    if not os.path.exists(parent_dir + "/none"):
        os.makedirs(parent_dir + "/none")
    files = fnmatch.filter(os.listdir(input_path), "*.jpg")
    files.sort() # added by ness
    size = len(files)
    display()



def Click_on(event=None):
    global index
    name_temp = files[index+1]
    name_str = os.path.splitext(name_temp)[0]
    extension = os.path.splitext(name_temp)[1]
    name_splt = name_str.split("_")
    print(name_splt)
    q_id = name_splt[0]
    g_id = name_splt[1]
    hotel_id = name_splt[2]
    save_path = parent_dir + "/correct/" + g_id + "/"
    print(save_path)
    print(input_path + files[index])
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    shutil.copy(input_path + files[index],save_path+q_id+extension)

    index += 2
    if index <= size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()

def Click_off(event=None):
    global index
    name_temp = files[index]
    shutil.copy(input_path + files[index], parent_dir + "/wrong/" + name_temp.replace(".jpg", "_wrong.jpg"))
    index += 2
    if index <= size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


def Click_questionable(event=None):
    global index
    name_temp = files[index]
    shutil.copy(input_path + files[index], parent_dir + "/not_sure/" + name_temp.replace(".jpg", "_not_sure.jpg"))
    index += 2
    if index <= size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


def Click_none(event=None):
    global index
    name_temp = files[index]
    shutil.copy(input_path + files[index], parent_dir + "/none/" + name_temp.replace(".jpg", "_none.jpg"))
    index += 2
    if index <= size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


image = Image.open('./aupera.png')
photo = ImageTk.PhotoImage(image)
label = Label(f,image=photo, width=700, height=570,)

label.image = photo # keep a reference!
label.pack()

button_on = Button(f, padx = 25, pady = 25, text="correct (y)",command = Click_on)
button_on.pack(side = LEFT)


button_q = Button(f, padx = 25, pady = 25, text="not sure (h)",command = Click_questionable)
button_q.pack(side = LEFT)

button_off=Button(f, padx = 25, pady = 40, text="wrong (n)",command = Click_off)
button_off.pack(side = LEFT)

button_off=Button(f, padx = 25, pady = 40, text="missing human (m)",command = Click_off)
button_off.pack(side = LEFT)



errmsg = 'Error!'
button_folder = Button(f, text='File Open', command=file)
button_folder.pack(side = TOP)





f.pack(fill=X, expand=True)
f.pack_propagate(0)
root.bind('y', Click_on)
root.bind('n', Click_off)
root.bind('h', Click_questionable)
root.bind('m', Click_none)

root.mainloop()
