import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# contains count, median price for each quarter as cols, LGA in 2nd entry of 
# each row.

def preprocess_house(fname):
    # reorganises the house price csv files into a more standard format
    # columns: Quarter, LGA, Count, Median

    h = pd.read_csv(fname)



    # creates a sorted list of LGAs 
    LGAs = h["Unnamed: 1"].to_list()
    LGAs = sorted(LGAs[2:-6])
    LGAs = LGAs[0:28] + LGAs[35:] # removing "group total" rows

    # creates a sorted list of quarters
    quarters = h.values.tolist()[0]
    quarters = quarters[2::2]

    # duplicates list values to store 1 row per quarter per LGA
    quarters_new = [""] * (len(quarters)*len(LGAs))
    for i in range(len(quarters)):
        for j in range(len(LGAs)):
            quarters_new[i * len(LGAs) + j] = quarters[i]

    LGAs_new = [""] * (len(quarters)*len(LGAs))
    for i in range(len(quarters)):
        for j in range(len(LGAs)):
            LGAs_new[i * len(LGAs) + j] = LGAs[j]



    dict = {} # stores counts and median house prices as list of tuples for each LGA
    row_count = len(h.index)
    for r in [i + 2 for i in range(row_count - 7)]:
        row = h.values.tolist()[r]
        if row[1] != "Group Total":
            dict[row[1]] = []
            for j in range(len(quarters)):
                dict[row[1]].append((row[2*j+2], row[2*j+3]))
    
    # uses dict to create columns for counts and median house prices
    counts = [""] * len(quarters_new)
    prices = [""] * len(quarters_new)
    for i in range(len(quarters)):
        j = 0
        for LGA in sorted(dict.keys()):
            if "-" not in dict[LGA][i][0]:
                counts[i * len(LGAs) + j] = int(dict[LGA][i][0].replace(",", ""))
                prices[i * len(LGAs) + j] = int(dict[LGA][i][1][1:].replace(",", ""))
            else:
                counts[i * len(LGAs) + j] = 0
                prices[i * len(LGAs) + j] = 0
            j += 1

    df = pd.DataFrame.from_dict({"Quarter": quarters_new, "LGA": LGAs_new, "Count": counts, "Median House Price": prices})



    # aggregating data per year
    years = df["Quarter"].to_list()
    for i in range(len(years)):
        years[i] = years[i][4:]
    df.insert(1, "Year", years, True)
    df.drop("Quarter", inplace=True, axis=1)
    df = df.reset_index()
    df = df.groupby(['Year', 'LGA']).sum()
    df = df[-790::]

    return df




def preprocess_crime1(fname):
    # reorganises and cleans crime1 csv
    # columns: year, lga, incidents, rate per 100k

    df = pd.read_csv(fname, usecols=["Year", "Local Government Area", "Incidents Recorded", 'Rate per 100,000 population']) # contains incidents and rate/100k

    # sorting years in ascending order
    df = df.sort_values(by=["Year", "Local Government Area"])

    # removing misc rows
    df = df[df["Local Government Area"] != "Total"]
    df = df[df["Local Government Area"] != " Unincorporated Vic"]
    df = df[df["Local Government Area"] != " Justice Institutions and Immigration Facilities"]
    df = df.reset_index()
    df.drop("index", inplace=True, axis=1)


    # converting rate and incidents to int/float
    rates = df["Rate per 100,000 population"].to_list()
    incidents = df["Incidents Recorded"].to_list()
    for i in range(len(rates)):
        rates[i] = float(rates[i].replace(",", ""))
        incidents[i] = int(incidents[i].replace(",", ""))
    df["Rate per 100,000 population"] = rates
    df["Incidents Recorded"] = incidents


    return df