# labeling_tools Introduction

This repo is a thrid-party labeling tool that can be used for image annotations. The original repo can be found here:

https://github.com/tzutalin/labelImg

Installation and user guide can be found in this README file:

https://github.com/BingshengWei/labeling_tools/blob/master/classification_localization/labelImg/README.rst

This tool can be used to relocate, resize and create bounding boxes. Annotations can be read and saved to Pascal VOC and YOLO format. This tool was tested in the office and should work for our labelling purpose.

# If using YOLO Format

Please create two folders, one image folder and one annotation folder. The structure should look like this:

```
labeling_tools
.
├── classification_localization
│       ├── labelImg
│           ├── data
│               ├── predefined_classes.txt
│           ├── Image_folder
│               ├── ...
│           ├── Annotation_folder
│               ├── classes.txt
│               ├── ...
│           ├── ...
│           ├── labelImg.py
```

classes.txt is the classes you defined for labeling. predefined_classes.txt should be consistant with classes.txt.
