import pandas as pd
df_defense = pd.read_csv('data/defense.csv')

color_list1 = ["green", "blue", "black", "maroon"]
color_list2 = ["red", "purple", "orange", "white"]

table_attribute_list = df_defense.columns.tolist()
table_unwanted = [0, 4, 6]
for ele in sorted(table_unwanted, reverse=True):
    del table_attribute_list[ele]

attribute_list = df_defense.columns.tolist()
del attribute_list[0:7]

attribute_list_2= df_defense.columns.tolist()
unwanted = [0, 1, 2, 3, 6]
for ele in sorted(unwanted, reverse = True):
    del attribute_list_2[ele]
