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

## Getting Started on Windows

1. Download [Python](https://www.python.org/downloads/) and run the installer
1. When the installer launches, select the checkbox **Add Python 3.8 to PATH** on the bottom and hit **Install Now**
1. After the installation completes, there may be an option to **Disable path length limit**. Enable this option if it appears
1. In the Windows start menu, search for `Powershell` and run it
1. Type in the command `pip install Pillow` and press enter. This will install the image library that the application requires
1. Once Pillow is installed, open the folder containing the labeling scripts. Double-click [labeler_result_analysis.py](./labeler_result_analysis.py) and open the file with Python. The application should now appear
