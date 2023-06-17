import xml.etree.ElementTree as ET
import glob
import os
import json
from tqdm import tqdm
import sys

classes = ["MetalPart", "Pliers", "PlasticPart", "Bolt", "Washer", "Screwdriver", "Nut", "BoltWasher", "Nail", 
           "AdjustableClamp", "Hammer", "Cutter", "Pen", "FuelCap", "BoltNutSet", "Wire", "Wrench", "Battery",
           "LuggageTag", "MetalSheet", "Label", "Rock", "SodaCan", "ClampPart", "PaintChip", "AdjustableWrench",
           "LuggagePart", "Hose", "Screw", "Tape", "Wood", "Spring", "Spanner", "Cloth"]
# print([name for name in os.listdir(".") if os.path.isdir(name)])


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


# create the labels folder (output directory)
# os.mkdir(output_dir)

# input_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
input_dirs =  [sys.argv[1]]#["Laballed_data_spanner_flat"]

for input_dir in input_dirs:

    # input_dir = "Bolt_Large_Concrete_Even_9523"
    print(f"Update the dir:{input_dirs}")
    output_dir = input_dir
    image_dir = input_dir

    # identify all the xml files in the annotations folder (input directory)
    files = glob.glob(os.path.join(input_dir, '*.xml'))
    print(files[0])
    # loop through each 
    for fil in tqdm(files):
        basename = os.path.basename(fil)
        filename = os.path.splitext(basename)[0]
        # check if the label contains the corresponding image file
        if not os.path.exists(os.path.join(image_dir, f"{filename}.PNG")):
            s1 = os.path.join(image_dir, f"{filename}.PNG")
            print(f"{s1} image does not exist!")
            exit()
            continue

        result = []

        try:

            # parse the content of the xml file
            tree = ET.parse(fil)
            root = tree.getroot()
            width = int(root.find("size").find("width").text)
            height = int(root.find("size").find("height").text)
        except:
            print("Currupt xml", fil)

        for obj in root.findall('object'):
            label = obj.find("name").text
            # check for new classes and append to list
            if label not in classes:
                classes.append(label)
            index = classes.index(label)
            pil_bbox = [int(float(x.text)) for x in obj.find("bndbox")]
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

        if result:
            # generate a YOLO format text file for each xml file
            with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(result))

# generate the classes file as reference
with open('classes.txt', 'w') as f:
    for cls in classes:
        f.write('%s\n'%cls)
    print("classes.txt generated")
