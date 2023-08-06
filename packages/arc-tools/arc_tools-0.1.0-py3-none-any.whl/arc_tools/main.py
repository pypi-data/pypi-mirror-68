import tarfile
import os
import sys
import logging
import argparse
from .utils import Color
from .utils import splitter
from .utils import rand_pwd
from .utils import StartGetConfig
from .modules.makearchive import Compress
from .utils import ScreenConfig
from .modules.unarchivate import UnCompress

parser = argparse.ArgumentParser(description='Easy arhivate your data with this script')
parser.add_argument("-unzip", action='store', type=str, help="Unarchivate")
parser.add_argument("-contribute", action='store_true', help="Contribute https://gihub.com/Reglament989/Compressor")
parser.add_argument("-tree", action='store_true', help="Archivate all tree")
parser.add_argument("-make", action='store_true', help="Archive current dir")
parser.add_argument("-name", action='store', help="Named for archive, only with -make")
parser.add_argument("-debug", action='store_true', help="More info on shell")
parser.add_argument("-config", action='store_true', help="Get more options and save as default")

config = StartGetConfig()

ParentDir = os.getcwd()
try:
	GitDirs = [x[0] for x in os.walk(os.path.join(ParentDir, '.git'))]
except:
	GitDirs = []

MOD = 'TAR'
OVER_SIZE = 1048576000 # 1 GB


def get_dirs():
	logging.info(f"{Color.Red}ParentDir: {ParentDir}{Color.Clear}")
	dirs = [x[0] for x in os.walk(ParentDir)]
	for directory in dirs:
		if directory == ParentDir or directory in GitDirs:
			continue
		logging.info(f"{Color.Yellow}Start selecting for directory - {directory}{Color.Clear}")
		tarCompress(directory)
		logging.info(f"{Color.Blue}Successffull compress, {directory}{Color.Clear}")

def tarCompress(directory: str):
	name_archive = os.path.join(os.getcwd(), directory.split(splitter)[-1] + '.tar.xz') 
	files = os.listdir(directory)
	tar = tarfile.open(name_archive, 'x:xz')
	archives = [tar]
	memory = 0
	count = 0
	try:
		for file in files:
			if os.path.isdir(file):
				continue
			else:
				absolute_path_file = os.path.join(directory, file)
				file_size = os.path.getsize(absolute_path_file)
				memory + file_size
				if memory > OVER_SIZE:
					count += 1
					name_archive = os.path.join(os.getcwd(), directory.split(splitter)[-1] + f'_{count}' + '.tar.xz') 
					archives[-1].close()
					archives.append(tarfile.open(name_archive))
				with open(absolute_path_file, 'rb') as f:
					fileobj = f.read()
				tarinfo = tarfile.TarInfo(file)
				logging.debug(f"{Color.Green}Append {file} to {archives[-1].name}, Size - will be soon {Color.Clear}")
				archives[-1].addfile(tarinfo, fileobj)
	except Exception as e:
		raise e
	finally:
		try:
			for archive in archives:
				archive.close()
		except:
			pass
		
def started_cli():
	if sys.platform == 'win64' or sys.platform == 'win32':
		os.system('cls')
	else:
		os.system('clear')
	print(f"""
{Color.Yellow}Hello this app arhivate all directory for parrent dir of script.{Color.Clear}
{Color.Green}Run script with options -h for more help{Color.Clear}
{Color.Blue}Author - Reglament989{Color.Clear}\n\n""")
	

def main():
	args = parser.parse_args()
	started_cli()
	if args.contribute:
		print(Color.Blue, 'My github: https://github.com/Reglament989', Color.Clear)
		sys.exit(0)
	if args.debug:
		level = logging.DEBUG
	else:
		level = logging.INFO
	logging.basicConfig(
		format=Color.Yellow + "\t[Arc] >> %(message)s" + Color.Clear,
		level=level,
	)
	if args.tree:
		get_dirs()
	if args.config:
		screen = ScreenConfig()
		screen.render()
	if args.unzip:
		UnCompress(os.getcwd(),args.unzip)
	if args.make:
		if config['global']['default_arc'] == 'ZIP':
			if not args.name:
				name = os.getcwd().split(splitter)[-1] + ".zip"
			else:
				if args.name.endswith('.zip'):
					pass
				else:
					name = args.name + ".zip"
			Compress.make_zip(name=name, compression=config['ZIP']['compression'])
		elif config['global']['default_arc'] == 'TAR':
			if not args.name:
				name = os.getcwd().split(splitter)[-1] + ".tar." + config['TAR']['compression']
			else:
				name = args.name
			logging.info(name)
			Compress.make_tar(name=name, mode=config['TAR']['compression'])
		sys.exit(0)
	

if __name__ == '__main__':
	main()
