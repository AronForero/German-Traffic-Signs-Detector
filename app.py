import click
from tools import Application_obj

@click.command()
@click.argument('download')

def download_data(download):
    App_Obj = Application_obj('https://www.yifysubtitles.com/subtitle/thorragnarok2017web-dlx264-fgt-english-120026.zip')
    """A simple file to Download de DataSet, Extract, and split it automatically"""
    if download == "download":
        App_Obj.download_dataset()
        App_Obj.unzip_file()
        App_Obj.split_data()
    else:
        click.echo("Opcion incorrecta... Consulte la opcion --help para mas informacion")

if __name__ == '__main__':
    download_data()
