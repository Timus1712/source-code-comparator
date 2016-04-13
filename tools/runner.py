#!/usr/bin/env python

""" A tool to run source code comprassion in specified folder """


from __future__ import unicode_literals
from __future__ import print_function

import argparse
import sys
import json
import itertools


def parse_args():
	parser = argparse.ArgumentParser(
		description="A tool to run source code comprassion in specified folder")

	parser.add_argument("source-list", type=dir, help="Source list file in json format")
	parser.add_argument("--tool", help="Compare tool (executable file)")
	parser.add_argument("--report-type", choices=("json", "html"), help="Report type")
	parser.add_argument("--file", help="Output file")

	parser.add_argument()

	return parser.parse_args()


def run_comparator(tool, source1_path, source2_path):
	raise NotImplementedError()


def run_compare(tool, sources_file, tool_args):
	"""
	Run compare tool for every pair of source codes in sources_file
	Sources file list in following format:
	[
		{
			"path": str,
			"name": str,
			... Any additional information
		},
	]
	Return list in following format (sorted by similarity desceding):
	[
		{
			"source1": {"path": str, "name": str, ...}
			"source2": {"path": str, "name": str, ...}
			"similarity": float
		}
	]
	"""

	with open(sources_file, "r") as fd:
		sources = json.loads(fd.read())

	result = []

	for source1, source2 in itertools.combinations(sources):
		print("Comparing '{0}' : '{1}'".format(source1["name"], source2["name"]))
		similarity = run_comparator(tool, source1["path"], source2["path"])
		result.append({
			"source1": source1,
			"source2": source2,
			"similarity": similarity
		})

	return sorted(result, key=lambda x: x["similarity"])


def print_html_report(report, file="output.html"):
	raise NotImplementedError()


def print_json_report(report, file="output.json"):
	raise NotImplementedError()


def main():
	args = parse_args()

	report = run_compare(args.tool, args.source_list)

	if args.report_type == "html":
		print_html_report(report, args.file)
	else:
		print_json_report(report, args.file)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		sys.exit("Error: {0}".format(e))
