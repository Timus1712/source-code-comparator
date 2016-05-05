#!/usr/bin/env python
"""Prepare JSON for all files in current directory."""

import argparse
import os
import json


def main():
	parser = argparse.ArgumentParser("Prepare JSON for all files in specified directory")
	parser.add_argument("directory", help="directory with sources")
	parser.add_argument("output", help="output file")
	args = parser.parse_args()
	path = args.directory
	files = [path + f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	source_files = []
	for f in files:
		source_files.append({
			"path": os.path.abspath(f),
			"name": os.path.basename(f)
		})

	s = json.dumps(source_files)
	with open(args.output, "w") as f:
		f.write(s)


if __name__ == "__main__":
	main()
