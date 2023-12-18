#!/bin/python3

from matplotlib.axes import Axes
import matplotlib.pyplot as plt  
import csv
from enum import Enum
from sys import argv
from math import floor
from random import choice, choices

# enum with gruvbox colorscheme colors
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
	# parse arguments
	if len(argv) >= 2:
		try:
			# split by coma, trim spaces, uppercase since case doesn't matter in this context
			bar_countries = [*map(lambda x: x.strip().upper(),argv[1].split(','))]
		except Exception as e:
			print(f"Invalid country list. {e}")
			exit(1)
	else:
		bar_countries = None

	# try to read all csv data to get rid of file hande asap
	try:
		with open('data.csv', encoding='utf-8-sig') as f:
			raw_data = [*csv.DictReader(f)] # data.csv must be in the working directory
	except Exception as e:
		print(f"Exception encountered when reading data.csv: {e}")
		exit(1)

	# get sets of repeated data
	countries = {row['Country Code']:row['Country Name'] for row in raw_data}
	indicators = {row['Indicator Code']:row['Indicator Name'] for row in raw_data}
	# set the 20-year range. Yep, the data cutoff is 2016, which is like... 7 years ago...
	years = [str(y) for y in range(1996,2017)]

	# init data sub-dicts for each indicator
	data = {s:{} for s in indicators.keys()}

	# simple function to filter out the non-yearly data and return the data in appropriate 'year:value' form
	filter = lambda row: {k:float(v or 0)for (k,v) in row.items() if k in years}
	# categorize data in each row and filter it
	for row in raw_data:
		data[row['Indicator Code']][row['Country Code']] = filter(row)

	# if user specified the country list for the bar chart, validate it
	if bar_countries:
		for c in bar_countries:
			# if user entered a wrong country code, print the country code list and the corresponding country names
			if c not in countries:
				print(f"Country code {c} not found in the CSV. Default list: 'UKR,MOZ,JPN,DEU'.\nAll available countries ({len(countries)}):")
				c_keys = [*countries.keys()]
				for i in range(0,floor( (len(c_keys)-1)/10 )+1):
					r = [i*10,min( (i+1)*10, len(c_keys))]
					print(' '.join(c_keys[r[0]:r[1]]))
				print()
				# for letter in {s[0] for s in countries.keys()}:
				# 	print(f'{letter}:  ', ' '.join( c for c in countries.keys() if c[0] == letter ))
				print(*(f'{k}: {v}' for (k,v) in countries.items()), sep='\n')
				exit(2)
	# if user did not specify the country list, pick 10 countries at random
	else:
		bar_countries = [*(
			c for c in choices([*countries.keys()], k=10)
		)]
		# forcefully include Ukraine instead of the first country if it hasn't been picked at random
		if 'UKR' not in bar_countries:
			bar_countries[0] = 'UKR'
	# sort countries by the value to get a nicer view
	bar_countries = sorted(bar_countries, key=lambda x: data['IT.NET.BBND.P2'][x]['2016'])

	# create the figure and axes objects
	fig, ax = plt.subplots(1,2)
	if not isinstance(ax[0], Axes) or not isinstance(ax[1], Axes):
		print("Failed to init axes.")
		exit(1)
	# set background to something better
	fig.patch.set_facecolor(Gruvbox.BG0_H.value)
	# 'IT.NET.BBND.P2' stands for 'Fixed broadband Internet subscribers'
	# plot 4 lines... ya, I know it was supposed to be 2, but this isn't the point and I wanted to see those 4
	for n,c in enumerate(('UKR','MOZ','JPN','DEU')):
		ax[0].plot(
				years,
				data['IT.NET.BBND.P2'][c].values(),
				label=countries[c],
				linewidth=1,
				color=(Gruvbox.FG_YELLOW, Gruvbox.FG_AQUA, Gruvbox.FG_PURPLE, Gruvbox.FG_RED)[n].value,
		)
	ax[1].bar(
			[*( countries[c].replace(' ','\n') for c in bar_countries )],
			[*( data['IT.NET.BBND.P2'][c]['2016'] for c in bar_countries )],
			color=[*(Gruvbox[a+b].value for a in ('FG_','BG_') for b in ('RED','YELLOW','GREEN','AQUA','PURPLE') )]
	)
	# add labels
	ax[0].set_xlabel('Year', color=Gruvbox.FG1.value)
	ax[0].set_ylabel('Fixed broadband Internet subscribers (per 100 people)', color=Gruvbox.FG1.value)
	ax[1].set_xlabel('Country', color=Gruvbox.FG1.value)
	ax[1].set_ylabel('Fixed broadband Internet subscribers (per 100 people), 2016', color=Gruvbox.FG1.value)

	# style axes a little better
	for axes in (ax[0], ax[1]):
		for spine in axes.spines.keys():
			axes.spines[spine].set_color(Gruvbox.FG3.value)
		for axis in (axes.xaxis, axes.yaxis):
			axis.label.set_color(Gruvbox.FG3.value)
		axes.tick_params(colors=Gruvbox.FG2.value)
		axes.set_facecolor(Gruvbox.BG0.value)
		axes.tick_params('x', labelrotation=45)
	ax[0].tick_params(direction='inout')
	ax[1].tick_params(bottom=False, top=False)
	ax[0].grid(color=Gruvbox.BG3.value, linestyle='dashed')
	ax[0].legend(facecolor=Gruvbox.BG0_S.value, labelcolor=Gruvbox.FG3.value, edgecolor=Gruvbox.BG2.value)

	fig.set_layout_engine('tight')

	# show the figure
	plt.show()

main()
