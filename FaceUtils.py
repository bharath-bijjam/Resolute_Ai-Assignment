from deepface import DeepFace

import os

db_path = os.path.join('static', 'uploads')

module_name = "Facenet"

def verifyTwo(img1,img2):    
    res = DeepFace.verify(img1,img2,model_name=module_name)
    return res

def checkForSimilarImage(img):
    images = os.listdir(db_path)

    for image in images:
        image_path = db_path + "\\" + image
        res = verifyTwo(img,image_path)
        if res['verified'] == True:
            return True
    
    return False

def findFace(img):
    dfs = DeepFace.find(img,db_path=db_path,model_name=module_name)

    shape = dfs[0].shape

    if shape[0] > 0:
        print(dfs[0])
        return True
    else:
        return False

    

