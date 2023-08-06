import tarfile
import zipfile
import logging
import os

class UnCompress():
	def __init__(self, root_pwd, archive_name):
		if archive_name.endswith('zip'):
			self.unzip(root_pwd, archive_name)
		elif archive_name.endswith('tar.xz'):
			self.untar(root_pwd, archive_name, 'r:xz')
		elif archive_name.endswith('tar.gz'):
			self.untar(root_pwd, archive_name, 'r:gz')
		elif archive_name.endswith('tar.bz'):
			self.untar(root_pwd, archive_name, 'r:bz2')
		else:
			raise Exception('Cant unarhivate this.')
	
	def unzip(self, root_pwd, archive_name):
		with zipfile.ZipFile(os.path.join(root_pwd, archive_name), 'r') as zip:
			error = zip.testzip()
			if error:
				logging.error(error)
				return
			else:
				zip.extractall(root_pwd)
				logging.info("Successffull extrcat")


	def untar(self, root_pwd, archive_name, method_tar):
		with tarfile.open(os.path.join(root_pwd, archive_name), method_tar) as tar:
			tar.extractall(root_pwd)
			logging.info("Successffull extrcat")
	