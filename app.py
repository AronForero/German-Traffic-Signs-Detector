import click
from tools import Init_App
from tools import ML_models

@click.group()
@click.option('--start', is_flag=True)
def arfa(start):
    if start:
        pass

@arfa.command()
def download():
    App_Obj = Init_App('http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip')
    """A simple file to Download de DataSet, Extract, and split it automatically"""
    App_Obj.download_dataset()
    App_Obj.unzip_file()
    App_Obj.remove_det_data()
    App_Obj.split_data()

@arfa.command()
@click.option('--model', '-m', default = False, help = "Machine Learning model to use. (LRSKL: Logistic Regression of Scikit-Learn)")
@click.option('--directory', '-d', default = False, help = "Directory where the data for train is.")
def train(model, directory):
    """Function to train the chosen model"""
    if model and directory:
        TrainModel_obj = ML_models(model, directory)
        TrainModel_obj.select_train_model()
    else:
        print("Please chose a valid model.")

@arfa.command()
@click.option('--model', '-m', default = False, help = "Machine Learning model (already trained), to test")
@click.option('--directory', '-d', default = False, help = "Directory where the data for test is.")
def test(model, directory):
    """Function to test a trained model"""
    if model and directory:
        TestModel_obj1 = ML_models(model, directory)
        TestModel_obj1.select_test_model()
    else:
        print("Please choose a trained model.")

@arfa.command()
@click.option('--model', '-m', default = False, help = "Machine Learning model (already trained), to test")
@click.option('--directory', '-d', default = False, help = "Directory where the data for test and show is.")
def infer(model, directory):
    """Function to run the infer option, this will test a model, and show the results(images and class) to the user"""
    if model and directory:
        TestModel_obj2 = ML_models(model, directory)
        TestModel_obj2.run_infer()
    else:
        print("Please choose a valid model.")


if __name__ == '__main__':
    arfa()
