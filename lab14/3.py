#!/bin/python3

from matplotlib.axes import Axes
import matplotlib.pyplot as plt  
import json
from enum import Enum

# gruvbox color palette enum
class Gruvbox(Enum):
	BG0_H	= '#1D2021'
	BG0_S	= '#32302F'
	BG0		= '#282828'
	BG1		= '#3C3836'
	BG2		= '#504945'
	BG3		= '#665C54'
	BG4		= '#7C6F64'
	BG		= BG0
	FG0		= '#FBF1C7'
	FG1		= '#EBDBB2'
	FG2		= '#D5C4A1'
	FG3		= '#BDAE93'
	FG4		= '#A89984'
	FG		= FG1

	BG_GRAY		= '#928374'
	BG_RED		= '#CC241D'
	BG_ORANGE	= '#D65D0E'
	BG_YELLOW	= '#D79921'
	BG_GREEN	= '#98971A'
	BG_AQUA		= '#689D6A'
	BG_BLUE		= '#458588'
	BG_PURPLE	= '#B16286'

	FG_GRAY		= '#A89984'
	FG_RED		= '#FB4934'
	FG_ORANGE	= '#FE8019'
	FG_YELLOW	= '#FABD2F'
	FG_GREEN	= '#B8BB26'
	FG_AQUA		= '#8EC07C'
	FG_BLUE		= '#83A598'
	FG_PURPLE	= '#D3869B'

def main():
	# load json data from lab12 (i created a soft link to it in this directory)
	try:
		data = json.load(open('students.json'))
		if not isinstance(data, dict):
			raise Exception('students.json appears to be corrupted.')
	except Exception as e:
		print(f"Exception encountered when reading students.json: {e}")
		exit(1)

	# create the figure and axes objects
	fig, ax = plt.subplots()
	if not isinstance(ax, Axes):
		print("Failed to init axes.")
		exit(1)
	# set background to something better
	fig.patch.set_facecolor(Gruvbox.BG0_H.value)

	# get student counts in each grade (in 'grade:student_count' form)
	students_per_grade = {
		g: len([d for d in data.values() if d['grade'] == g]) / len(data) for g in
		sorted({d['grade'] for d in data.values()})
	}
	# create a pie chart and
	# get labels and autotexts (the % values) to style them later
	_,labels,autotexts = ax.pie(
		[*students_per_grade.values()],
		[i/len(students_per_grade)/4 for i in range(0,len(students_per_grade))],
		labels=[*students_per_grade.keys()],
		colors=[*(str(Gruvbox[a+b].value) for a in ('FG_','BG_') for b in ('RED','YELLOW','GREEN','AQUA','PURPLE') )],
		autopct='%1.1f%%'
	)
	# set color for labels
	for l in labels:
		l.set_color(Gruvbox.FG2.value)
	# set color for autotexts
	for l in autotexts:
		l.set_color(Gruvbox.BG0_H.value)

	# add label
	ax.set_xlabel('Students in grades (% of total)', color=Gruvbox.FG1.value)

	# style axes a little better
	for spine in ax.spines.keys():
		ax.spines[spine].set_color(Gruvbox.FG3.value)
	for axis in (ax.xaxis, ax.yaxis):
		axis.label.set_color(Gruvbox.FG3.value)
	ax.set_facecolor(Gruvbox.BG0.value)
	ax.legend(facecolor=Gruvbox.BG0_S.value, labelcolor=Gruvbox.FG3.value, edgecolor=Gruvbox.BG2.value)

	fig.set_layout_engine('tight')

	# show the figure
	plt.show()

main()
