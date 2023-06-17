import cv2
import glob
import os
import shutil


from tqdm import tqdm

SRC_IMG_FORMAT = "jpg"
DEST_IMG_FORMAT = "PNG"

src_dir = "mixed_dataset"
dest_dir = src_dir + f"_{DEST_IMG_FORMAT}"

img_files = glob.glob(os.path.join(src_dir, f'*.{SRC_IMG_FORMAT}'))

# print(img_files[0].split(f".{SRC_IMG_FORMAT}")[0] + f".{DEST_IMG_FORMAT}")

# dd = ""+img_files[0].split(f".{SRC_IMG_FORMAT}")[0] + f".{DEST_IMG_FORMAT}"

# img = cv2.imread(img_files[0])

# print()

# print(img_files[0].split("/")[-1])

# os.mkdir(dest_dir)

# cv2.imwrite("mixed_dataset_PNG/2023-06-17T13\:02\:27\.975332_out_168.PNG", img)

for file1 in tqdm(img_files):
    file = f"{file1}"
    img = cv2.imread(file)

    # print(file)
    f1 = file.split("/")[-1]
    fg = f1.split(f".{SRC_IMG_FORMAT}")[0] + f".{DEST_IMG_FORMAT}"
    d = os.path.join(dest_dir, fg).replace(":", "_")
    # print(img.shape)
    # print(d)
    cv2.imwrite(d, img)



xml_files = glob.glob(os.path.join(src_dir, f'*.xml'))

for xml_file in xml_files:

    

    # xml_file = file.replace(f".{SRC_IMG_FORMAT}", ".xml")
    f1 = xml_file.split("/")[-1]
    d = os.path.join(dest_dir, f1).replace(":", "_")


    # print(".{SRC_IMG_FORMAT}}")
    # print("xml:",d)
    # if not os.path.exists(xml_file):
    #     print(file)
    #     print(xml_file)
    #     print("xml is not here")
    #     break
    shutil.copy(xml_file, d)



