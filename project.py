"""
Resources: https://data.cityofnewyork.us/Environment/Recycling-Diversion-and-Capture-Rates/gaq9-z3hz
https://www.nj.gov/dep/dshw/recycling/stat_links/2018finalreport.pdf
https://www.tceq.texas.gov/downloads/permitting/waste-permits/waste-planning/docs/187-21.pdf
https://stackoverflow.com/questions/36684013/extract-column-value-based-on-another-column-pandas-dataframe - helped with specifying Trenton and Austin sums
https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/ - basic plot formatting
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html - renaming NYC Dataset name
URL: https://kalyanamogh7.wixsite.com/mysite
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reading all CSV Files 
nyc_inp = input("Enter NYC Dataset: ")
nj_inp = input("Enter NJ Dataset: ")
tx_inp = input("Enter TX Dataset: ")

############### NEW YORK ###############
# Arrays for getting boroughs and total of boroughs for plotting
borough_arr = []
nyc_totals = []

# Reading CSV file for NYC Recycling Rates
nyc_inp = input("Enter NYC Dataset: ")
nyc_data = pd.read_csv(nyc_inp)

# Renaming column for ease of use
nyc_data.rename(columns= {'Capture Rate-Total ((Total Recycling - Leaves (Recycling)) / (Max Paper + Max MGP))x100': 'Capture Rate Total'}, inplace=True)

# Used for graphing
# Finding total sum of NYC Dataset
NYC_totalWaste = nyc_data['Capture Rate Total'].sum()

# Finding each individual Zone within nyc_data['Zone'], adding to borough_arr
for i in nyc_data['Zone']:
    if i not in borough_arr:
        borough_arr.append(i)

# Finding totals for each borough, adding to totals array
for i in borough_arr:
    temp = nyc_data.groupby('Zone')['Capture Rate Total'].sum()[i]
    nyc_totals.append([temp, i])

# Sorting totals array by total descending
sorted_totals = sorted(nyc_totals, key=lambda x:x[0], reverse=True)

# Reset arrays and add new values
borough_arr = []
nyc_totals = []
for i in sorted_totals:
    nyc_totals.append(i[0])
    borough_arr.append(i[1])

# first diagram code
'''
x, y = borough_arr, totals          # original code had nyc_totals as just "totals"
plt.figure(figsize=(11, 5))
plt.bar(x, y)
plt.title('NYC Visualization')
plt.xlabel('NYC Boroughs')
plt.ylabel('Capture Rate Total (in Tons)')
plt.legend()
plt.show()
'''

############### TRENTON ###############
nj_data = pd.read_csv(nj_inp)

# Added total sum of all values in 'MUNI TOTAL (tons)' relating to Mercer
nj_totalWaste = nj_data['MUNI TOTAL (tons)'].sum()
trenton_data = nj_data.loc[nj_data['MUN'] == 'Trenton', 'MUNI TOTAL (tons)'].iloc[0]


############### AUSTIN ###############
tx_data = pd.read_csv(tx_inp)

# Added total sum of all values in '2020 Tons' relating to Travis
tx_totalWaste = tx_data['2020 Tons'].sum()
austin_data = tx_data.loc[tx_data['County'] == 'Travis', '2020 Tons'].sum()


############### PLOTTING ###############
# x-axis values
x = [borough_arr[0] + '/ NYC', 'Trenton / Mercer', 'Austin / Travis']

# plotting values
city_waste = [nyc_totals[0], trenton_data, austin_data]
totals = [NYC_totalWaste, nj_totalWaste, tx_totalWaste]

# separation of plotting values and figure formatting
xes = np.arange(len(x))
plt.figure(figsize=(11, 5))

# plotting both bar graphs, labeling, color distinction, and using the xes array as separation
plt.bar(xes + 0.2, totals, label = 'Total Amount Recycled By County')
plt.bar(xes - 0.2, city_waste, color='red', label = 'Total Amount Recycled By City')
plt.xticks(xes, x)

# formatting the window, giving it a title and x/y labels along with a legend
plt.title('Capital City VS County Recycling Rates')
plt.xlabel('City / Municipality')
plt.ylabel('Total Recylcled Materials (in tons)')
plt.legend()
plt.show()