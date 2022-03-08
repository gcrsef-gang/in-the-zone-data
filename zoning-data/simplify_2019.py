"""Temp script which cuts the last couple columns of 2019 data, reducing it to a size which is pushable by 
Github. 

mergedPLUTO-2019.7z uses the merged-PLUTO-2019.csv file rather than the full-merged-PLUTO-2019.csv file. 
"""

with open("merged-PLUTO-2019.csv", "r") as f:
    lines = f.readlines()
newlines = []
print("done!")
for line in lines:
    pos = line.find("07/06/2019")-1
    newlines.append("\n"+line[:pos])
print(len(newlines))
print("done1!")
with open("full-merged-PLUTO-2019.csv", "w") as f:
    f.writelines(newlines)