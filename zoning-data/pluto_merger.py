boroughs = ["bk","bx","mn","si","qn"]
years = ["02A","10v1"]

for year in years:
    rows = []
    for borough in boroughs:
        with open(borough+year+".txt", "r") as f:
            rows.extend(f.readlines())
    with open("mergedPLUTO-"+year+".txt", "w") as f:
        f.writelines(rows)