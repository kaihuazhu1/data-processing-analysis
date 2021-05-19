import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# contains count, median price for each quarter as cols, LGA in 2nd entry of 
# each row.

def preprocess_house(fname):
    # reorganises the house price csv files into a more standard format
    # columns: Quarter, LGA, Count, Median

    h = pd.read_csv(fname)

    # # creates a sorted list of LGAs 
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
    df = df.reset_index().drop("index", axis=1)

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

# Combines two dataframes and removes rows with 0
def preprocess_combined(df1, df2):
    df1["Incidents Recorded"] = df2["Incidents Recorded"]
    df1["Rate per 100,000 population"] = df2["Rate per 100,000 population"]
    df1 = df1[df1.Count != 0]
    df1.reset_index(inplace=True)
    return df1


# reading in csv files
one_bf = preprocess_house("1bflat.csv") # contains count and median price
two_bf = preprocess_house("2bflat.csv") 
two_bh = preprocess_house("2bhouse.csv")
three_bf = preprocess_house("3bflat.csv") 
three_bh = preprocess_house("3bhouse.csv")
four_bh = preprocess_house("4bhouse.csv") 
all = preprocess_house("all.csv")
c1 = preprocess_crime1("crime1.csv") # contains incidents and rate/100k



# three_bh = three_bh[-79:]
# one_bf = one_bf[-79:]
# c1 = c1[-79:]

# print(one_bf["Count"][1])



# print(h1)
# print(h1)
# print(c1)
# h1.to_csv("h1.csv")
# c1.to_csv("c1.csv")

# 1 BEDROOM FLAT
plt.scatter(preprocess_combined(one_bf, c1)["Median House Price"], preprocess_combined(one_bf, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 1 Bedroom Flat")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot1bf.png")
plt.clf()

plt.scatter(preprocess_combined(one_bf, c1)["Median House Price"], preprocess_combined(one_bf, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 1 Bedroom Flat")
plt.savefig("plot1bf100k.png")
plt.clf()

# 1 BEDROOM FLAT 2020
plt.scatter(preprocess_combined(one_bf[-79:], c1)["Median House Price"], preprocess_combined(one_bf[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 1 Bedroom Flat in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot1bf-2020.png")
plt.clf()

plt.scatter(preprocess_combined(one_bf[-79:], c1)["Median House Price"], preprocess_combined(one_bf[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 1 Bedroom Flat in 2020")
plt.savefig("plot1bf100k-2020.png")
plt.clf()

# 2 BEDROOM FLAT
plt.scatter(preprocess_combined(two_bf, c1)["Median House Price"], preprocess_combined(two_bf, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 2 Bedroom Flat")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot2bf.png")
plt.clf()

plt.scatter(preprocess_combined(two_bf, c1)["Median House Price"], preprocess_combined(two_bf, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 2 Bedroom Flat")
plt.savefig("plot2bf100k.png")
plt.clf()

# 2 BEDROOM FLAT 2020
plt.scatter(preprocess_combined(two_bf[-79:], c1)["Median House Price"], preprocess_combined(two_bf[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 2 Bedroom Flat in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot2bf-2020.png")
plt.clf()

plt.scatter(preprocess_combined(two_bf[-79:], c1)["Median House Price"], preprocess_combined(two_bf[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 2 Bedroom Flat in 2020")
plt.savefig("plot2bf100k-2020.png")
plt.clf()

# 2 BEDROOM HOUSE
plt.scatter(preprocess_combined(two_bh, c1)["Median House Price"], preprocess_combined(two_bh, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 2 Bedroom House")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot2bh.png")
plt.clf()

plt.scatter(preprocess_combined(two_bh, c1)["Median House Price"], preprocess_combined(two_bh, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 2 Bedroom House")
plt.savefig("plot2bh100k.png")
plt.clf()

# 2 BEDROOM HOUSE 2020
plt.scatter(preprocess_combined(two_bh[-79:], c1)["Median House Price"], preprocess_combined(two_bh[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 2 Bedroom House in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot2bh-2020.png")
plt.clf()

plt.scatter(preprocess_combined(two_bh[-79:], c1)["Median House Price"], preprocess_combined(two_bh[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 2 Bedroom House in 2020")
plt.savefig("plot2bh100k-2020.png")
plt.clf()

# 3 BEDROOM FLAT
plt.scatter(preprocess_combined(three_bf, c1)["Median House Price"], preprocess_combined(three_bf, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 3 Bedroom Flat")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot3bf.png")
plt.clf()

plt.scatter(preprocess_combined(three_bf, c1)["Median House Price"], preprocess_combined(three_bf, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 3 Bedroom Flat")
plt.savefig("plot3bf100k.png")
plt.clf()

# 3 BEDROOM FLAT 2020
plt.scatter(preprocess_combined(three_bf[-79:], c1)["Median House Price"], preprocess_combined(three_bf[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 3 Bedroom House in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot3bf-2020.png")
plt.clf()

plt.scatter(preprocess_combined(three_bf[-79:], c1)["Median House Price"], preprocess_combined(three_bf[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 3 Bedroom House in 2020")
plt.savefig("plot3bf100k-2020.png")
plt.clf()

# 3 BEDROOM HOUSE
plt.scatter(preprocess_combined(three_bh, c1)["Median House Price"], preprocess_combined(three_bh, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 3 Bedroom House")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot3bh.png")
plt.clf()

plt.scatter(preprocess_combined(three_bh, c1)["Median House Price"], preprocess_combined(three_bh, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 3 Bedroom House")
plt.savefig("plot3bh100k.png")
plt.clf()

# 3 BEDROOM HOUSE 2020
plt.scatter(preprocess_combined(three_bh[-79:], c1)["Median House Price"], preprocess_combined(three_bh[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 3 Bedroom House in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot3bh-2020.png")
plt.clf()

plt.scatter(preprocess_combined(three_bh[-79:], c1)["Median House Price"], preprocess_combined(three_bh[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 3 Bedroom House in 2020")
plt.savefig("plot3bh100k-2020.png")
plt.clf()

# 4 BEDROOM HOUSE
plt.scatter(preprocess_combined(four_bh, c1)["Median House Price"], preprocess_combined(four_bh, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 4 Bedroom House")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot4bh.png")
plt.clf()

plt.scatter(preprocess_combined(four_bh, c1)["Median House Price"], preprocess_combined(four_bh, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 4 Bedroom House")
plt.savefig("plot4bh100k.png")
plt.clf()

# 4 BEDROOM HOUSE 2020
plt.scatter(preprocess_combined(four_bh[-79:], c1)["Median House Price"], preprocess_combined(four_bh[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for 4 Bedroom House in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plot4bh-2020.png")
plt.clf()

plt.scatter(preprocess_combined(four_bh[-79:], c1)["Median House Price"], preprocess_combined(four_bh[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for 4 Bedroom House in 2020")
plt.savefig("plot4bh100k-2020.png")
plt.clf()

# ALL
plt.scatter(preprocess_combined(all, c1)["Median House Price"], preprocess_combined(all, c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for All Housing")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plotall.png")
plt.clf()

plt.scatter(preprocess_combined(all, c1)["Median House Price"], preprocess_combined(all, c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for All Housing")
plt.savefig("plotall100k.png")
plt.clf()

# ALL 2020
plt.scatter(preprocess_combined(all[-79:], c1)["Median House Price"], preprocess_combined(all[-79:], c1)["Incidents Recorded"])
plt.xlabel("Median Rent Price")
plt.ylabel("Incidents Recorded")
plt.title("Median Rent Price vs Incidents Recorded for All Housing in 2020")
plt.yticks(np.arange(0, 32000, 2000))
plt.savefig("plotall-2020.png")
plt.clf()

plt.scatter(preprocess_combined(all[-79:], c1)["Median House Price"], preprocess_combined(all[-79:], c1)["Rate per 100,000 population"])
plt.xlabel("Median Rent Price")
plt.ylabel("Rate per 100,000 population")
plt.title("Median Rent Price vs Rate per 100,000 population for All Housing in 2020")
plt.savefig("plotall100k-2020.png")
plt.clf()

# to add: plot more things, add calculations
