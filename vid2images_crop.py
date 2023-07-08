
TEST_VIDEO = "video_20230617_183243.mp4"
import cv2 
import time
cap = cv2.VideoCapture(TEST_VIDEO)
img_out = "./out"

IMG_SIZE = 1280

width, height = IMG_SIZE, IMG_SIZE
dim = (width, height)

xmin, ymin, xmax, ymax = [1, 518, 1010, 1238]

i = 0
# while i < 120:
while(cap.isOpened()):
  now = time.time()
  frameLimit = 20.0
  ret, frame = cap.read()
  if ret: 
    # resize image
    # resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    # frame = frame[ ymin:ymax, xmin:xmax ]
    cv2.imwrite(img_out+ f"/frame_0000{i}.PNG", frame)
    cap.set(cv2.CAP_PROP_POS_MSEC,(i*500))
    i = i +1

    timeDiff = time.time() - now
    if (timeDiff < 1.0/(frameLimit)): time.sleep( 1.0/(frameLimit) - timeDiff )
  else:
    break