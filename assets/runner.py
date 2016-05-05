#!/usr/bin/env python

""" A tool to run source code comprassion """


from __future__ import unicode_literals
from __future__ import print_function

import argparse
import sys
import subprocess
import json
import itertools

import threading
import Queue

import reporters


def _multi_run(fn, data, threads=5):
	results = []

	def worker(q):
		while True:
			try:
				item = q.get(False)
			except Queue.Empty:
				break

			similarity = fn(item[0], item[1])
			results.append({
				"source1": item[0],
				"source2": item[1],
				"similarity": similarity
			})

	q = Queue.Queue()
	for item in data:
		q.put(item)

	thread_pool = []
	try:
		for i in range(threads):
			thread = threading.Thread(target=worker, args=(q,))
			thread_pool.append(thread)
			thread.start()
	finally:
		for t in thread_pool:
			if t and t.isAlive():
				t.join()

	return results


def parse_args():
	parser = argparse.ArgumentParser(
		description="A tool to run source code comprassion")

	parser.add_argument("sourcelist", type=str, help="Source list file in json format")
	parser.add_argument("--tool", help="Compare tool (executable file)")
	parser.add_argument("--report-type", choices=("json", "html"), help="Report type")
	parser.add_argument("--file", help="Output file")

	return parser.parse_args()


def run_comparator(tool, source1, source2):
	print("Comparing '{0}' : '{1}'".format(source1["name"], source2["name"]))
	s = subprocess.Popen([tool, source1["path"], source2["path"]], shell=False,
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result = s.stdout.read()
	return float(result)


def run_compare(tool, sources_file, tool_args=None):
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

	result = _multi_run(lambda x, y: run_comparator(tool, x, y),
		itertools.combinations(sources, r=2))

	# for source1, source2 in itertools.combinations(sources, r=2):
	# 	similarity = run_comparator(tool, source1["path"], source2["path"])
	# 	result.append({
	# 		"source1": source1,
	# 		"source2": source2,
	# 		"similarity": similarity
	# 	})

	return sorted(result, key=lambda x: x["similarity"])


def main():
	args = parse_args()

	report = run_compare(args.tool, args.sourcelist)

	if args.report_type == "html":
		reporters.html_report(report, args.file)
	elif args.report_type == "json":
		reporters.json_report(report, args.file)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		raise
		sys.exit("Error: {0}".format(e))
