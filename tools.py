class Application_obj():
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
        import zipfile as zf
        zip_ref = zf.ZipFile(self.filename)
        zip_ref.extractall('images/')
        zip_ref.close()

    def split_data(self):
        import shlex, subprocess
        """Way to run a Linux command into python"""
        #subprocess.call(shlex.split('pwd'))
        command_line = "rm"+self.filename
        args = shlex.split(command_line)
        subprocess.call(args)
