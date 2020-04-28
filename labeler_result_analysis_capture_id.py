from tkinter import *
from PIL import Image, ImageTk
import os
import fnmatch
from tkinter.filedialog import askdirectory # python3.5
import shutil
import argparse
import glob
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
def path_leaf_stem(path):
    head, tail = ntpath.split(path)
    return ntpath.basename(head)+"/"+tail

root = Tk()
root.title("Aupera Result Analysis")
f = Frame(root, width=1000, height=600, bg="gray")

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def display():
    global id
    print ("Processing image " + str(index+1) + " out of " + str(results_size))
    image_result = Image.open(results[index])
    id = results[index].split("/")[-2]
    print(id)
    gal_ind = [i for i, s in enumerate(gallery) if id in s]
    gal_cap_id_ind = [i for i, s in enumerate(gallery_cap_id) if id in s]
    image1 = Image.open(gallery[gal_ind[0]])
    image2 = Image.open(gallery_cap_id[gal_cap_id_ind[0]])
    image_gall = get_concat_h_blank(image1, image2, color=(0, 0, 0))
    image = get_concat_h_blank(image_gall, image_result, color=(0, 0, 0))
    photo = ImageTk.PhotoImage(image)
    label.configure(image=photo)
    label.image = photo # keep a reference!
    label.pack()

def gallery():
    global gallery_folder
    global gallery, gallery_cap_id
    global gallery_size
    gallery_folder = askdirectory()
    gallery_folder = gallery_folder + "/"
    print(gallery_folder)
    gallery = [gallery_folder+path_leaf_stem(path) for path in glob.glob(gallery_folder+"*/*.jpg") if path_leaf(path)=="id_card.jpg"]
    gallery_cap_id = [gallery_folder+path_leaf_stem(path) for path in glob.glob(gallery_folder+"*/*.jpg") if path_leaf(path)=="capture.jpg"]
    gallery.sort()
    gallery_cap_id.sort()
    # print(gallery)
    gallery_size = len(gallery)
    # print(gallery_size)

def results():
    global results_folder
    global results
    global results_size
    global index
    global parent_dir
    index = 0
    results_folder = askdirectory()
    results_folder = results_folder + "/"
    results = [results_folder+path_leaf_stem(path) for path in glob.glob(results_folder+"*/*.jpg")]
    results.sort() # added by ness
    print(results)
    results_size = len(results)
    print(results_size)
    parent_dir = "/".join(results_folder.split("/")[:-2])+"/" + results_folder.split("/")[-2]+"_labeled"
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    print (parent_dir)
    if not os.path.exists(parent_dir + "/correct"):
        os.makedirs(parent_dir + "/correct")
    if not os.path.exists(parent_dir + "/wrong"):
        os.makedirs(parent_dir + "/wrong")
    if not os.path.exists(parent_dir + "/not_sure"):
        os.makedirs(parent_dir + "/not_sure")
    if not os.path.exists(parent_dir + "/none"):
        os.makedirs(parent_dir + "/none")
    display()


def Click_on(event=None):
    global index
    name_temp = results[index].split("/")[-1]
    save_path = parent_dir + "/correct/" + id + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print(save_path)
    print(results_folder + results[index])
    shutil.copy(results[index], save_path + name_temp.replace(".jpg", "_correct.jpg"))
    index += 1
    if index <= results_size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()

def Click_off(event=None):
    global index
    name_temp = results[index].split("/")[-1]
    save_path = parent_dir + "/wrong/" + id + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    shutil.copy(results[index], save_path + name_temp.replace(".jpg", "_wrong.jpg"))
    index += 1
    if index <= results_size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


def Click_questionable(event=None):
    global index
    save_path = parent_dir + "/not_sure/" + id + "/"
    name_temp = results[index].split("/")[-1]
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    shutil.copy(results[index], save_path+ name_temp.replace(".jpg", "_not_sure.jpg"))
    index += 1
    if index <= results_size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


def Click_none(event=None):
    global index
    name_temp = results[index].split("/")[-1]
    save_path = parent_dir + "/none/" + id + "/"
    shutil.copy(results_folder + results[index], save_path+ name_temp.replace(".jpg", "_none.jpg"))
    index += 1
    if index <= results_size - 1:
        display()
    else:
        print ("congratulations you processed all images")
        root.quit()


logo = Image.open('./aupera.png')
photo = ImageTk.PhotoImage(logo)
label = Label(f,image=photo, width=800, height=570,)

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
button_results = Button(f, text='Results Folder Open', command=results)
button_results.pack(side = LEFT)

button_folder = Button(f, text='Gallery Folder Open', command=gallery)
button_folder.pack(side = LEFT)

f.pack(fill=X, expand=True)
f.pack_propagate(0)
root.bind('y', Click_on)
root.bind('n', Click_off)
root.bind('h', Click_questionable)
root.bind('m', Click_none)
root.mainloop()
