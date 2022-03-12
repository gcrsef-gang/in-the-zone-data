import pandas as pd

with open("mergedPLUTO-2002.txt", "r") as f:
    data = pd.read_table(f, sep=",", dtype=str)


data["BBL"] = data.iloc[:, 55] + data.iloc[:, 56].str.strip().str.pad(9, fillchar='0')
print(data["BBL"])
print(len(data.iloc[0]))
print(len(data.columns))

# with open("newmergedPLUTO-2002.csv", "r") as f:
data.to_csv("newmergedPLUTO-2002.csv")