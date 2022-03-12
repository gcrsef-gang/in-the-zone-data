import pandas as pd

# for year in ["2011", "2014", "2016", "2019"]:
for year in ["2010", "2018"]:
    for type in ["demographic","economic","housing","social", "transportation"]:
        file = pd.read_csv("nyc-"+type+"-data-"+year+".csv", nrows=2)
        code_to_column_dict = {}
        for i, column in enumerate(file.columns):
            if column == "S0802_C01_001E": 
                print("FOUND!")
                print(file.iloc[0,i], year, type, column)
            if column == "S0802_C01_042E": 
                print("FOUND!")
                print(file.iloc[0,i], year, type, column)
            if file.iloc[0,i] in code_to_column_dict.keys():
                continue
            code_to_column_dict[file.iloc[0,i]] = column
        with open("code-to-column-"+type+"-data-"+year+".txt", "w") as f:
            f.writelines(str(code_to_column_dict))