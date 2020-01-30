import os
from collections import defaultdict
import numpy as np
import shutil
import fnmatch
import re
import argparse



def sorted_nicely(l):
    """ Sorts the given iterable in the way that is expected.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def save_higher_scores(results,input_folder,start,stop):
    """ saving results with scores between score and score+10
    """
    matched_folder = input_folder+"matched-"+str(start)+"-"+str(stop)+"/"
    if not os.path.exists(matched_folder):
        os.makedirs(matched_folder)

    for key in results.keys():
        data = results[key]
        q_id = key
        g_id = data[0]
        hotel_id = data[1]
        sim_score = float(data[2])
        if  (sim_score >=start and sim_score <stop):
            query_name = q_id + ".jpg"
            query_path = input_folder +  query_name
            newqueryname = matched_folder + q_id + ".jpg"
            shutil.copyfile(query_path, newqueryname)
            gallery_name =  q_id.split("_")[0] + "_" + g_id + "_"+ hotel_id + "_" + data[2] + ".jpg"
            gallery_path = input_folder + gallery_name
            newgalleryname = matched_folder + gallery_name
            print("saving {}".format(newgalleryname))
            shutil.copyfile(gallery_path, newgalleryname)


def save_gallery_query(results,input_folder, gallery_folder, query_folder):
    """ separating query and gallery from senstime results
    """
    for key in results.keys():
        queryname = input_folder + key + ".jpg"
        newpathandname = query_folder + key + ".jpg"
        shutil.copyfile(queryname, newpathandname)
        data = results[key]
        q_id = key
        g_id = data[0]
        hotel_id = data[1]
        sim_score = float(data[2])
        if sim_score>0:
            gallery_name =  q_id.split("_")[0] + "_" + g_id + "_"+ hotel_id + "_" + data[2] + ".jpg"
            gallery_path = input_folder + gallery_name
            newgalleryname = gallery_folder + g_id + ".jpg"
            print("saving {}".format(newgalleryname))
            shutil.copyfile(gallery_path, newgalleryname)

parser = argparse.ArgumentParser()
parser.add_argument("--input_folder", type=str, required=True,
                    help="path to the input folder with saved results from sensetime")
args = parser.parse_args()


if __name__ == "__main__":

    if args.input_folder is None:
        raise RuntimeError("Need --input_folder")
    input_folder = args.input_folder
    if input_folder[-1] != '/':
        args.input_folder = args.input_folder + '/'
    input_folder = args.input_folder

    gallery_folder = input_folder +"gallery/"
    query_folder = input_folder +"query/"

    if not os.path.exists(gallery_folder):
        os.makedirs(gallery_folder)
    if not os.path.exists(query_folder):
        os.makedirs(query_folder)


    # reading senstime results into dictionary
    results = defaultdict(list)
    filenames = fnmatch.filter(os.listdir(input_folder), "*.jpg")
    filenames = sorted_nicely(filenames)
    for filename in filenames:
        name_str = os.path.splitext(filename)[0]
        name_splt = name_str.split("_")
        if (len(name_splt) == 2):
            key = name_str
            results[key] = [['','','-1']]
    for filename in filenames:
        name_str = os.path.splitext(filename)[0]
        name_splt = name_str.split("_")
        if (len(name_splt) == 4):
            q_id = name_splt[0]
            for key in results.keys():
                if key.startswith(q_id):
                    g_id = name_splt[1]
                    score = name_splt[3]
                    results[key].append(name_splt[1:])
    for key in results.keys():
        results[key] = sorted(results[key], key=lambda i: float(i[2]), reverse=True)[0] # replace it with top one

    save_gallery_query(results, input_folder, gallery_folder, query_folder)
    for start, stop in zip([80,70,60,50,45,40,43,45,47],[90,80,70,60,50,43,45,47,50]):
        save_higher_scores(results,input_folder,start,stop)
