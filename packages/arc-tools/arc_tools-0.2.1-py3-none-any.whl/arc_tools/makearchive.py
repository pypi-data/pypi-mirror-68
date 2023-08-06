import tarfile
import zipfile
import os
import sys
import time
from threading import Thread
from .utils import Color
import logging

if sys.platform == 'win32' or sys.platform == 'win64':
	splitter = '\\'
else:
	splitter = '/'

def join_thread(fn):
    def wrapper(*args, **kwargs):
        print(fn)
        th = Thread(target=fn, args=(args, kwargs),)
        th.start()
        th.join()
    return wrapper


class Compress:
    # @join_thread 

    def make_zip(name, compression, root_dir=os.getcwd()):
        if os.path.exists(name):
            logging.info(f"remove old archive {name}")
            os.remove(name)
        with zipfile.ZipFile(file=name, mode='w', compression=compression) as zip:
            files = os.listdir()
            for file in files:
                if check_white_list(file):
                    continue
                else:
                    logging.info(f"Archivate - {file}")
                    path = os.path.join(root_dir, file)
                    zip.write(path, arcname=file)
                    
            # logging.debug(__file__)     
    # @join_thread
    def make_tar(mode, name, root_dir=os.getcwd()):
        files = os.listdir(root_dir)
        if os.path.exists(name):
            logging.info(f"remove old archive {name}")
            os.remove(name)
        with tarfile.open(name=os.path.join(root_dir, name), mode=f"x:{mode}") as tar:
            for file in files:
                if check_white_list(file) or file == name:
                        continue
                else:
                    logging.info(file)
                    tarinfo = tarfile.TarInfo(file)
                    with open(os.path.join(root_dir, file), 'rb') as f:
                        fileobj = f.read()
                    tar.addfile(tarinfo, fileobj)
                

def check_white_list(file):
    if (os.path.isdir(file) or file.startswith('.')
        or file.endswith('.zip')
        or file.startswith('__')
        or file.endswith('.tar.gz')
        or file.endswith('.tar.bz2')
        or file.endswith('.tar.xz')
        or file.endswith('.tar')
        or file.split(splitter)[-1] == __file__):
        return True
    else:
        return False  

