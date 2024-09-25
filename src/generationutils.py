import shutil
import os

def copy_files(src, dest):
	for path in os.listdir(src):
		os_path = os.path.join(src, path)
		target = os.path.join(dest, path)
		if os.path.isdir(os_path):
			print(f"Directory: {os_path} --> {target}")
			if not os.path.exists(target):
				os.mkdir(target)
			copy_files(os_path, target)
		else:
			print(f"File: {os_path} --> {target}")
			shutil.copy(os_path, target)

def delete_files(dest):
	if os.path.exists(dest) and os.path.isdir(dest):
		print(f"Deleting Folder: {dest}")
		shutil.rmtree(dest)
	print(f"Creating Folder: {dest}")
	os.mkdir(dest)