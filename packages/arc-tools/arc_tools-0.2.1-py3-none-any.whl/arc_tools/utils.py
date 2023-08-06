import sys
import random
import zipfile
import os
import secrets
import string
import time
import json
import logging
import ctypes

def on_create_dump(f):
	json.dump({
		"global":{
			"default_arc":"ZIP",
		},
		"ZIP":{
			"compression": zipfile.ZIP_LZMA,
		},
		"TAR":{
			"compression": 'xz',
		}
	},f, sort_keys=True, indent=4)

class Color:
	Red="\033[31m"
	Blue="\033[34m"
	Green = "\033[32m"
	Yellow = "\033[33m"
	Clear="\033[0m"

	def setup_windows(self=None):
		import ctypes
		kernel32 = ctypes.windll.kernel32
		kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

logging.basicConfig(
	format=Color.Yellow + "\t[Arc] >> %(message)s" + Color.Clear,
	level=logging.INFO,
)

if sys.platform == 'win32' or sys.platform == 'win64':
	splitter = '\\'
	cmd = 'cls'
	config_path = 'C:\\Python\\.py_compressor_config.json'
	if not os.path.exists(config_path):
		os.mkdir('C:\\Python\\')
		with open(config_path, 'w') as f:
			on_create_dump(f)
		win_api = ctypes.windll.kernel32.SetFileAttributesW("C:\\Python\\", 2)
		logging.debug(f'Windows hide (1 = successffull) - {win_api}')
	Color.setup_windows()
else:
	splitter = '/'
	config_path = '~/.py_compressor_config.json'
	if not os.path.exists(config_path):
		with open(config_path, 'w') as f:
			on_create_dump(f)
	cmd = 'clear'

def StartGetConfig():
	with open(config_path) as f:
		data = json.load(f)
	return data

class ScreenConfig():
	def __init__(self):
		self.screen = 0
		self.screen_comprs = 0
	
	def render(self):
		os.system(cmd)
		if self.screen == 0:
			print(f"""
	{Color.Red}Please entry number configuration{Color.Clear}:
		{Color.Blue}1.Type compression
		2.Type arhivator to default
		0.Exit{Color.Clear}
""")
		elif self.screen == 1:
			print(f"""
	{Color.Red}Arhivator{Color.Clear}:
		{Color.Blue}1.Zip
		2.Tar
		0.Exit{Color.Clear}
""")
		elif self.screen == 2:
			if self.screen_comprs == 1:
				print(f"""
	{Color.Red}Zip compressions{Color.Clear}:
		{Color.Blue}1.BZIP2
		2.ZIP_DEFLATED
		3.ZIP_LZMA
		4.ZIP_STORED
		0.Exit{Color.Clear}
""")
			elif self.screen_comprs == 2:
				print(f"""
	{Color.Red}Tar compressions{Color.Clear}:
		{Color.Blue}1.Gzip compressions
		2.bzip2 compressions
		3.lzma compressions
		4.Without compression
		0.Exit{Color.Blue}
""")
		elif self.screen == 5:
			print(f"""
	{Color.Red}Default arhivator{Color.Clear}:
		{Color.Blue}1.Zip
		2.Tar
		0.Exit{Color.Clear}
""")
		while True:
			logging.debug(f"State: {self.screen}")
			self.new_screen = input(f"\n{Color.Yellow}>>{Color.Clear} ")
			try:
				self.new_screen = int(self.new_screen)
			except:
				print("Try integer.")
				time.sleep(0.5)
				self.render()
			if self.new_screen == 0:
				if self.screen == 0:
					sys.exit(0)
				else:
					if self.screen == 5:
						self.screen = 0
					else:
						self.screen -= 1
					break

			if self.screen == 0:
				if self.checkScreen(1,2):
					if self.new_screen == 2:
						self.screen = 5
					else:
						self.screen = self.new_screen
					# self.render()
					break
				else:
					continue
			elif self.screen == 1:
				if self.checkScreen(1,2):
					self.screen_comprs = self.new_screen
					self.screen = 2
					break
				else:
					continue
			elif self.screen == 5:
				if self.checkScreen(1,2):
					if self.new_screen == 1:
						arc = 'ZIP'
					elif self.new_screen == 2:
						arc = 'TAR'
					self.dump_config(var='default_arc',value=arc,t_arc='global')
					self.screen = 0
					break
				else:
					continue
			elif self.screen == 2:
				if self.checkScreen(1,4):
					if self.screen_comprs == 1: # ZIP
						arhivator = 'ZIP'
						if self.new_screen == 1:
							cs = zipfile.ZIP_BZIP2
						elif self.new_screen == 2:
							cs = zipfile.ZIP_DEFLATED
						elif self.new_screen == 3:
							cs = zipfile.ZIP_LZMA
						elif self.new_screen == 4:
							cs = zipfile.ZIP_STORED
					elif self.screen_comprs == 2: # TAR
						arhivator = 'TAR'
						if self.new_screen == 1:
							cs = 'gz'
						elif self.new_screen == 2:
							cs = 'bz2'
						elif self.new_screen == 3:
							cs = 'xz'
						elif self.new_screen == 4:
							cs = 'None'
					self.dump_config(var="compression", value=cs, t_arc=arhivator)
					self.screen = 0
					break
				else:
					continue
		self.render()

	def dump_config(self, var, value, t_arc):
		with open(config_path, 'r') as j_file:
			current_config = json.load(j_file)
		current_config[t_arc][var] = value
		with open(config_path, 'w') as j_file:
			json.dump(current_config, j_file, sort_keys=True, indent=4)
		logging.info(f'Successffull update {var}')
		time.sleep(0.5)

	def checkScreen(self, min_screen, max_screen):
		if self.new_screen > max_screen or self.new_screen < min_screen:
			print(f"{min_screen}:{max_screen}")
			return False
		else:
			return True
	
	def clear(self):
		self.screen = 0
		self.screen_comprs = 0


def rand_pwd():
	name = string.ascii_letters + string.digits

	password = "".join([secrets.SystemRandom().choice(name) for i in range(secrets.SystemRandom().randrange(8, 10))])
	return password

