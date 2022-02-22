with open("merged-PLUTO-2019.csv", "r") as f:
    lines = f.readlines()
newlines = []
print("done!")
for line in lines:
    pos = line.find("07/06/2019")-1
    newlines.append("\n"+line[:pos])
print(len(newlines))
print("done1!")
with open("modified-2019.csv", "w") as f:
    f.writelines(newlines)