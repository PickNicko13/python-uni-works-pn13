#!/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
from calendar import month_name

def main():
	try:
		df = pd.read_csv(
			'comptagevelo2011.csv',
			parse_dates=['Date'], dayfirst=True,
			index_col='Date'
		)
	except Exception as e:
		print(f"Error while reading origin csv file: {e}")
		exit(1)

	print(f"\nLoaded data:\n{df}")

	# drop time, since it's always 00:00 anyway
	df.pop('Time')
	# fill blanks with 0s
	df.fillna(0, inplace=True)

	print(f"\nAfter cleanup:\n{df}")

	# mean_daily_per_month_per_location seemed too long
	monthly = df.groupby(df.index.month).mean(numeric_only=True)
	# create a new column named "Total"
	# containing sums of all locations' mean daily cyclists each month
	monthly['Total'] = monthly.sum(axis=1)

	# convert index to month name string
	monthly.index = monthly.index.map(lambda x: month_name[x])


	print(f"\nMean cyclists per day each month:\n{monthly}")
	mpm = monthly.idxmax()['Total'] # Most Popular Month
	print(f"Most popular month: {mpm} with {monthly.loc[mpm]['Total']:.0f} cyclists per day on average.")

	df.plot(title='Daily cyclists at each location in 2011')
	plt.show()


if __name__ == "__main__":
	main()


# possible future improvement could be to account for the day of week, since some month will have more
# of the less mopular DAYS OF THE WEEK
