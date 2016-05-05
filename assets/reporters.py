#!/usr/bin/env python

""" Provide different types of report generator """


from __future__ import unicode_literals
from __future__ import print_function


def html_report(report, filename=None):

	if filename is None:
		filename = "output.html"

	def make_row(item):
		""" Make one table row from one report item """

		return """
			<tr>
				<td>{source1_name}</td>
				<td>{source2_name}</td>
				<td style=\"background-color:{color}\">{similarity}</td>
				<td>Not Implement</td>
			</tr>
			""".format(
				source1_name=item["source1"]["name"],
				source2_name=item["source2"]["name"],
				similarity=item["similarity"],
				color="hsl({0}, 84%, 83%)".format(100 - int(float(item["similarity"]) * 100))
			)

	HTML_HEADER = """
	<html><body>
	"""
	HTML_FOOTER = """
	</body></html>
	"""
	TABLE_HEADER = """
	<table>
	<tr><th>Name #1</th><th>Name #2</th><th>Similarity</th><th>diff</th></tr>
	"""
	TABLE_FOOTER = """
	</table>
	"""
	with open(filename, mode="w") as html_file:
		html_file.write(HTML_HEADER)
		html_file.write(TABLE_HEADER)
		for item in report:
			html_file.write(make_row(item))
		html_file.write(TABLE_FOOTER)
		html_file.write(HTML_FOOTER)


def print_json_report(report, filename="output.json"):
	raise NotImplementedError()
