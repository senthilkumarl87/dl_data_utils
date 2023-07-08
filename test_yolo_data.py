import cv2 
import time
import os
import glob
import sys
import xml.etree.ElementTree as ET
import glob
import os
import json
from tqdm import tqdm
import sys
from pascal_voc_writer import Writer
import numpy as np


input_dir = sys.argv[1]

img_frmt = "PNG"
imsz_w = 1280
imsz_h = 1280



classes = ["MetalPart", "Pliers", "PlasticPart", "Bolt", "Washer", "Screwdriver", "Nut", "BoltWasher", "Nail",
           "AdjustableClamp", "Hammer", "Cutter", "Pen", "FuelCap", "BoltNutSet", "Wire", "Wrench", "Battery",
           "LuggageTag", "MetalSheet", "Label", "Rock", "SodaCan", "ClampPart", "PaintChip", "AdjustableWrench",
           "LuggagePart", "Hose", "Screw", "Tape", "Wood", "Spring", "Spanner", "Cloth"]
# print([name for name in os.listdir(".") if os.path.isdir(name)])

def isinsideImg(x , y, w, h):
   if x < 0:
      return False
   if y < 0:
      return False

   if x > w:
      return False

   if y > h:
      return False
   return True



def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]




def get_detecction(Img_path):
  txt_file_path = Img_path.replace(".PNG", ".txt")
  frame = cv2.imread(Img_path)
  h, w = frame.shape[:2]


  if os.path.exists(txt_file_path):


    with open(txt_file_path, "r") as f:
      data = f.read()
      # print(data)
      bxyxy = []
      class_ids = []
      labels = []
      Num_obj = len(data.split("\n"))
      if Num_obj < 1:
        print(f"{txt_file_path}: No objects detected")
      for d in data.split("\n"):
        try:
          d1 = [float(d_str) for d_str in d.split(' ')]
        except Exception as e:
          print(f"{txt_file_path}: Improper format")
        class_id = int(d1[0])
        bbox = d1[1:]

        bxy = yolo_to_xml_bbox(bbox, w, h)
        # print(bxy)
        # xmin, ymin, xmax, ymax = bxy #+ [class_id, classes[class_id]]
        bxyxy.append(bxy)
        class_ids.append(class_id)
        try:
          labels.append(classes[class_id])
        except:
          print(f"Wrong label: {Img_path}")
          raise TypeError(f"Wrong label id {class_id}: {Img_path}")

      bxyxy_arr = np.array(bxyxy)
      return bxyxy_arr
  else:
    # print(f"{txt_file_path}: label file not available")
    return None





files = glob.glob(os.path.join(input_dir, f'*.{img_frmt}'))
currupted = 0
noLbl = 0
curp_files = []
for file in tqdm(files):
    try:
      frame = cv2.imread(file)
    except:
       print(f"{file}: Broken image")
       curp_files.append(file)
       currupted = currupted + 1

    h, w, c = frame.shape

    if not (h==imsz_h):
        print(f"{file}: resolution mismatch")
        curp_files.append(file)
        currupted = currupted + 1

    if not (w==imsz_w):
        print(f"{file}: resolution mismatch")
        curp_files.append(file)
        currupted = currupted + 1

    file_txt = file.replace( f".{img_frmt}" , ".txt")
    if not os.path.exists(file_txt):
        print(f"{file}:No Label file")
        noLbl += 1
        curp_files.append(file)
        currupted = currupted + 1
        continue


    else:
        det = get_detecction(file)

        if det is None:
            print(f"{file}:Improper Label")
            curp_files.append(file)
            currupted = currupted + 1
            continue
        else:
          #  print(det)
           for d in det:
            xmin, ymin, xmax, ymax = d

            if not isinsideImg(xmin, ymin, w, h):
                  print(f"{file}:Improper Label")
                  curp_files.append(file)
                  currupted = currupted + 1
                  continue
            if not isinsideImg(xmax, ymax, w, h):
                  print(f"{file}:Improper Label")
                  curp_files.append(file)
                  currupted = currupted + 1
                  continue
              


print("\n------------------------\n")

if len(curp_files) > 0:
  print("Crupted file list:")
  for fl in curp_files:
    print(fl)
  print(f"{len(curp_files)} files currupted")
  print(f"{noLbl} files has no labels")
else:
   print("All is well!")




