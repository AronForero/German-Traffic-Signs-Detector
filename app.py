import click
from tools import Application_obj

@click.command()
@click.argument('download')

def download_data(download):
    App_Obj = Application_obj('http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip')
    """A simple file to Download de DataSet, Extract, and split it automatically"""
    if download == "download":
        #App_Obj.download_dataset()
        #App_Obj.unzip_file()
        #App_Obj.remove_det_data()
        #App_Obj.split_data()
        print("Hola")
    else:
        click.echo("Opcion incorrecta... Consulte la opcion --help para mas informacion")

if __name__ == '__main__':
    download_data()
