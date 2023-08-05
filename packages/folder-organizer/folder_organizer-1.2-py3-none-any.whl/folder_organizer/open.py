import folder_organizer.organizer as fo
from pathlib import Path
import os
import sys
import re


def main():
	pattern = r'python\d\.?\d$'

	for i in sys.path:
		if re.search(pattern, i.lower()):
			path = i

	try:
		os.chdir(path)
	except UnboundLocalError:
		raise RuntimeError("Python folder is not in path")
	
	fo.main()

if __name__ == '__main__':
	main()
