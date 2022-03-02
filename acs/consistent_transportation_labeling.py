import pandas as pd

for year in ["2011","2014","2016"]:
    df = pd.read_csv("nyc-transportation-data-"+year+".csv")
    labels = df.iloc[0]
    print(year)
    new_labels = ['"id"', '"Geographic Area Name"']
    for label in labels:
        if label in ["id", "Geographic Area Name"]:
            continue
        if label.find("Estimate") != -1:
            new_labels.append('"Estimate!!'+label[:label.find("Estimate")]+label[label.find("Estimate")+10:]+'"')
        elif label.find("Margin") != -1:
            new_labels.append('"Margin of Error!!'+label[:label.find("Margin of Error")]+label[label.find("Margin of Error")+17:]+'"')
        else:
            print(label)
            raise Exception("WHAT??")
    with open("new_labels"+year+".txt", "w") as f:
        f.write(",".join(new_labels))


