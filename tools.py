class Init_App():
    """This class is the place where the several functions will be """
    def __init__(self, new_url):
        self.url = new_url
        self.filename = ""

    def download_dataset(self):
        import wget
        output_dir = 'images'
        self.filename = wget.download(self.url, out=output_dir)
        if self.filename:
            print("Descarga Exitosa.")
        else:
            print("Error al descargar.")
            return NULL

    def unzip_file(self):
        """Function to extract the files of the downloaded file"""
        import zipfile as zf
        zip_ref = zf.ZipFile(self.filename)
        zip_ref.extractall('images/')
        zip_ref.close()

    def remove_det_data(self):
        """Function to remove the images that belong to any object detection task"""
        import os, shlex, subprocess
        """Way to run a Linux command into python"""
        ls = os.listdir('images/FullIJCNN2013/')
        for i in ls:
            if ".ppm" in i:
                command_line = "rm images/FullIJCNN2013/"+i
                args = shlex.split(command_line)
                subprocess.call(args)

    def split_data(self):
        """This function split the data into 2 directorys, the train directory and the test directory,
         and removes the empty directory"""
        import os, shlex, subprocess
        import numpy as np
        #list each element of the directory, the result will be more directorys
        ls1 = os.listdir('images/')
        subprocess.call(shlex.split("rm images/FullIJCNN2013/gt.txt"))
        subprocess.call(shlex.split("mv images/FullIJCNN2013/ReadMe.txt ."))
        for i in ls1:
            if i == "train" or i == "test" or i == "user" or i == "FullIJCNN2013.zip":
                pass
            else:
                #list each inner-directory of the directory
                lstmp = os.listdir('images/'+i)
                for l in lstmp:
                    dirlist = os.listdir('images/'+i+'/'+l)
                    #Get the number of images that we will have for train and test
                    c_train = int(np.floor(len(dirlist)*0.8))
                    c_test = len(dirlist)-c_train
                    #print("train files:", c_train)
                    #print("test files:", c_test)
                    for j in dirlist[:c_train]:
                        command_line1 = "mv images/FullIJCNN2013/"+l+"/"+j+" images/train/"+l+j
                        args1 = shlex.split(command_line1)
                        subprocess.call(args1)
                    for k in dirlist[c_train:]:
                        command_line2 = "mv images/FullIJCNN2013/"+l+"/"+k+" images/test/"+l+k
                        args2 = shlex.split(command_line2)
                        subprocess.call(args2)
        subprocess.call(shlex.split("rm -rf images/FullIJCNN2013/"))

class ML_models(object):
    """class where the predictor will be created, trained, saved and tested."""
    def __init__(self, model, directory):
        self.new_model = model
        self.new_directory = directory

    def select_train_model(self):
        if self.new_model == "LRSKL":
            self.LogisticRegression_SKL_train()
        else:
            print("Please choose a valid model.")

    def LogisticRegression_SKL_train(self):
        """This function will create a Logistic Regression model, then trains it and saves it"""

        from PIL import Image
        import numpy as np
        import os
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import LabelEncoder
        from sklearn.externals import joblib

        lstrain = os.listdir(self.new_directory)
        lstrain.sort()
        print("Processing the images...")
        train_imgs = np.zeros((len(lstrain), 4096)) #a matrix to store the processed images

        #in this loop, the images are imported, then are resized to an equal size for all the images, then
        #this new images are converted to an array, and the average is calculated accross the 3 dimensions (RGB)
        #and a last step is flatten every image to store in the matrix created above
        for i in range(len(lstrain)):
            train_imgs[i] = np.mean(np.asarray(Image.open(self.new_directory+lstrain[i]).resize((64,64))), axis=2).flatten()

        y_train = []
        for i in lstrain:
            y_train.append(i[:2])

        print("Processing the labels...")
        new_ytrain = LabelEncoder()
        new_ytrain.fit(y_train)
        new_ytrain.transform(y_train);

        LR = LogisticRegression()
        print("Training...")
        LR.fit(train_imgs, new_ytrain.transform(y_train))
        print("Saving...")
        joblib.dump(LR, 'models/model1/saved/LogisticRegression-SKL.pkl')
        print("Finished.")

    def select_test_model(self):
        if self.new_model == "LRSKL":
            self.LogisticRegression_SKL_test()
        else:
            print("Please choose a valid model.")

    def LogisticRegression_SKL_test(self):
        """The next process is like the process made in the LogisticRegression_SKL_train function."""
        import os
        import numpy as np
        from PIL import Image
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import LabelEncoder
        from sklearn.externals import joblib

        test_path = "images/test/"
        lstest = os.listdir(test_path)
        lstest.sort()
        print("Processing the images...")
        test_imgs = np.zeros((len(lstest), 4096))
        for j in range(len(lstest)):
            test_imgs[j] = np.mean(np.asarray(Image.open(test_path+lstest[j]).resize((64,64))), axis=2).flatten()

        print("processing the labels...")
        y_test = []
        for i in lstest:
            y_test.append(i[:2])

        new_ytest = LabelEncoder()
        new_ytest.fit(y_test)
        new_ytest.transform(y_test);

        LR = joblib.load('models/model1/saved/LogisticRegression-SKL.pkl')
        print("Testing the model...")
        score = LR.score(test_imgs, new_ytest.transform(y_test))
        print("The score obtained is:", score)

    def run_infer(self):
        """This is the function to test the created models with the data stored in the user directory."""
        if self.new_model == "LRSKL":
            self.infer_SKL_Model()
        else:
            print("Please choose a valid model.")

    def infer_SKL_Model(self):
        """This Function show the image passed and the prediction given by the model"""
        import os
        import numpy as np
        from skimage import io
        from PIL import Image
        import matplotlib.pyplot as plt
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import LabelEncoder
        from sklearn.externals import joblib

        user_path = "images/user/"
        lsuser = os.listdir(user_path)
        lsuser.sort()

        print("Processing the images...")
        user_imgs = np.zeros((len(lsuser), 4096))
        for j in range(len(lsuser)):
            user_imgs[j] = np.mean(np.asarray(Image.open(user_path+lsuser[j]).resize((64,64))), axis=2).flatten()

        LR = joblib.load('models/model1/saved/LogisticRegression-SKL.pkl')
        print("Initializing testing...")
        plt.ion()
        plt.figure('ActualImage')
        for i in range(len(user_imgs)):
            result = LR.predict(user_imgs[i].reshape(1,-1))
            print(result)
            title = 'Pertenece a la clase: '+ str(result)
            plt.suptitle(title)
            im = 'images/user/'+lsuser[i]
            img = io.imread(im)
            plt.imshow(img)
            x = input()
