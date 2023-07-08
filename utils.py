import os

import glob


def copy2dir(srcFileNam, destFileNam, folder):
    with open(srcFileNam, "r") as f1:
        data = f1.read()
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    dest_path = os.path.join(folder, destFileNam)

    with open(dest_path, "w") as f2:
        f2.write(data)


def copy2dir2(srcFileNam, destFileNam):
    with open(srcFileNam, "r") as f1:
        data = f1.read()  
    

    with open(destFileNam, "w") as f2:
        f2.write(data)

    

if __name__=="__main__":

    srcFileNam = "frame_00000-seg.txt"
    destFileNam = "frame_00000.txt"

    folder = "out"

    copy2dir(srcFileNam, destFileNam, folder)

    copy2dir2(srcFileNam, destFileNam)

    db = [srcFileNam, destFileNam]

    import pickle

    dbfile = open('data', 'ab')


    pickle.dump(db, dbfile)    

    dbfile = open('data', 'rb')     
 

    db = pickle.load(dbfile)

    print(db)
                

    
