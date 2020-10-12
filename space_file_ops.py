#
# File and folder operations for SpACE
#
# Currently includes: selecting files in folder
# and subfolders, filtering files by filename
#
# TODO: file saving functions likely will go here

import os.path
import glob

def path_exists(folder):
	"""Just checks to see if a path is a valid path."""
	return os.path.exists(folder)

def collect_all_filenames(folder):
	"""Finds all files in a given folder and all of its
	subfolders. Returns a Python list where each entry
	is a filename with full path to the file."""
	return glob.glob(folder + '/**', recursive = True)

def filter_filenames(file_list):
	"""Iterates through a list of files and retains only
	those that have 'tir' 'nicolet' 'spectrum' and '.txt'
	in the filename. Returns a Python list."""
	return list(filter(lambda filename: 'tir' in filename
								and 'nicolet' in filename
								and 'spectrum' in filename
								and '.txt' in filename,
								file_list))

def save_files(folder, suffix, data_objects):
	"""Accepts a specified filepath, a suffix to add to it, and a list of data_objects.  Iterates
	through them all and saves them to the filepath with the suffix added on. Saves as .csv"""
	save_folder_name = os.path.join(folder, suffix)
	if not path_exists(save_folder_name):
		os.mkdir(save_folder_name)
	for dobj in data_objects:
		save_string = (save_folder_name + dobj.filename).rstrip("txt") + "csv"
		dobj.pairs.to_csv(save_string)  # other arguments can be supplied, check pandas docs
