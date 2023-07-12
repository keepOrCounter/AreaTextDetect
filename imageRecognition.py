import numpy as np
from PIL import Image
import os,cv2
# import torch

def resizer(path,flag=False):
    if not flag:
        files=os.listdir(path)

        for x in files:
            image = cv2.imread(path+"\\"+x)

            imageNew = cv2.resize(image, (100,100))

            cv2.imwrite(path+"\\"+x, imageNew)
            
    # else:
    #     image = cv2.imread(path+"\\"+x)
    #
    #     imageNew = cv2.resize(image, (100,100))
    #
    #     return imageNew

def ind(x):
    return np.where(x==np.max(x))[0][0]

def l2ModelTrainer(data, labels,lmbd=0):
    
    X, y = data, labels
    X=np.atleast_2d(X)
    y=np.atleast_1d(y)
    
    X_tilde = np.insert(X, 0, 1,axis=1)


    
    if lmbd!=0:
        #(X_tilde^T * X_tilde +  λI)^-1
        inversedFormula=np.linalg.inv(np.dot(X_tilde.swapaxes(0, 1),X_tilde)+np.dot(lmbd,np.identity(X_tilde.shape[1])))
        print(inversedFormula)
        subFormula2=np.dot(inversedFormula,X_tilde.swapaxes(0, 1))
        print(subFormula2)
    else:
        subFormula2=np.linalg.pinv(X_tilde)


    # Compute the coefficient vector.
    w = np.dot(subFormula2,y)

    
    # Return model parameters.
    return w


def l2ModelPredicter(w, data):
    """
    A summary of your function goes here.

    data: type and description of "data"
    w: type and description of "w"

    Returns: type and description of the returned variable(s).
    """
    X_tilde = np.insert(data, 0, 1,axis=1)
    # Compute the prediction.  
    predicted_y = np.dot(X_tilde,w)
        
    return predicted_y


class ImageProcess():
    def __init__(self) -> None:
        self.location=os.getcwd()+"\\"
        self.labels=[]
    
    def imageLoad(self,path)->np.array:
        image = Image.open(path)
        imageArray = np.array(image)
        
        return imageArray
    
    def imagesLoad(self,path,labelRecord=False)->list:
        imageArray=[]
        files=os.listdir(path)
        for x in files:
            if x[-4:]==".jpg":
                image = Image.open(path+"\\"+x)
                imageArray.append(np.array(image))
                if labelRecord:
                    self.labels.append(int(x[0:2]))
        
        return imageArray
    
    def imageSave(self,fileName,imageArray):
        for x in range(len(imageArray)):
            image = Image.fromarray(imageArray[x])

            image.save(self.location+"new\\"+fileName[0:-4]+str(x)+fileName[-4:])
        
    def imageCut(self,imageArray,xyList,width,height,insertValue=255)->list:
        imageArrayCutted=[]
        xFlag=0
        counter=0

        for x in range(len(xyList)):
            if xyList[x][0]==-1:
                xFlag=1
                counter=xyList[x][1]
                xPosition=xyList[x-1][0]+xyList[x][2]
                yPosition=xyList[x-1][1]+xyList[x][3]
                xOffset=xyList[x][4]
                yOffset=xyList[x][5]
            elif xyList[x][1]==-1:
                xFlag=2
                counter=xyList[x][0]
                xPosition=xyList[x-1][0]+xyList[x][2]
                yPosition=xyList[x-1][1]+xyList[x][3]
                xOffset=xyList[x][4]
                yOffset=xyList[x][5]
            else:
                xFlag=0
                counter=1
                xPosition=xyList[x][0]
                yPosition=xyList[x][1]
                
            for y in range(counter):
                if xFlag==0:
                    imageArrayCutted.append(imageArray[yPosition*(y+1)+height*y:(yPosition*(y+1)+height*(y+1)),\
                        xPosition*(y+1)+width*y:(xPosition*(y+1)+width*(y+1)),:])
                elif xFlag==1:
                    imageArrayCutted.append(imageArray[yPosition*(y+2)+height*(y+1)+yOffset:(yPosition*(y+2)+height*(y+2)+yOffset),\
                        xPosition+xOffset:(xPosition+width+xOffset),:])
                elif xFlag==2:
                    imageArrayCutted.append(imageArray[yPosition+yOffset:(yPosition+height)+yOffset,\
                        xPosition*(y+2)+width*(y+1)+xOffset:(xPosition*(y+2)+width*(y+2))+xOffset,:])
                    
                if imageArrayCutted[-1].shape[0]<height or imageArrayCutted[-1].shape[1]<width:
                    if imageArrayCutted[-1].shape[0]<height:
                        count=imageArrayCutted[-1].shape[0]
                        axis=0
                        tem=height
                    if imageArrayCutted[-1].shape[1]<width:
                        count=imageArrayCutted[-1].shape[1]
                        axis=1
                        tem=width

                    print(">>>>>>>>>>>>>>",imageArrayCutted[-1].shape)
                    while count<tem:
                        
                        imageArrayCutted[-1] = np.insert(imageArrayCutted[-1], count, insertValue,axis=axis)
                        count+=1
                        
        return imageArrayCutted
    
if __name__=="__main__":
    tem=ImageProcess()
    # image=tem.imageLoad("a2ee0bb8526a7d35c606c5bdc2bfc5b3.jpg")
    # print(image)
    # print(image.shape)
    # imageNew=tem.imageCut(image,[(0,50),(12,-1,6,0,-5,0),(0,255),(12,-1,6,0,-5,0),(0,460),(4,-1,6,0,-5,0)],140,140,254)
    # # print(imageNew)
    # # print(imageNew.shape)
    # tem.imageSave("new.jpg",imageNew)
    # resizer(os.getcwd()+"\\new")
    # resizer(os.getcwd()+"\\test")
    images=tem.imagesLoad(tem.location+"new",True)
    test=ImageProcess()
    imagesTest=test.imagesLoad(tem.location+"test",True)
    
    # imageNew=[]
    # label=np.repeat(np.arange(8, 15), 5)
    print(tem.labels)
    label=np.eye(16)[np.array(tem.labels)]
    
    
    labelTest=np.eye(16)[np.array(test.labels)]
    
    print(label)
    print(tem.labels)
    print(test.labels)
    # for x in range(len(images)):
    #     if x<=10:
    #         for y in range(5):
    #             imageNew.append(images[x])
    #     else:
    #         imageNew.append(images[x])
    print(len(images))
    # print(len(images))
    
    images=np.array(images)
    reshaped_array = images.reshape(images.shape[0], images.shape[1]*images.shape[2]*images.shape[3])

    imagesTest=np.array(imagesTest)
    imagesTest=imagesTest.reshape(imagesTest.shape[0], imagesTest.shape[1]*imagesTest.shape[2]*imagesTest.shape[3])
    reshaped_array=np.divide(reshaped_array,255)
    imagesTest=np.divide(imagesTest,255)

    print(reshaped_array.shape)
    print(reshaped_array)
    print("-------------------")
    w=l2ModelTrainer(reshaped_array,label,1)
    print(w.shape)
    print(w)
    np.save("w.npy",w,fix_imports=True)
    
    result=l2ModelPredicter(w,imagesTest)
    # print(result)
    yPredict = np.apply_along_axis(ind,1,result)
    
    
    trueResult=np.where(labelTest==np.max(labelTest))[1]
    print(labelTest)
    
    correctNum=np.count_nonzero(yPredict==trueResult)
    print(correctNum)
    print(yPredict)
    print(trueResult)
    print(correctNum/trueResult.shape[0])