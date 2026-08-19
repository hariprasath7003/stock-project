import requests
import pandas as pd
pd.set_option('display.max_columns',None)
# print(requests.__version__)

a="https://api.github.com/repos/squareshift/stock_analysis/contents/"
response = requests.get(a)
# print(response.status_code)
# a=(response.json())
# print(type(a))
# b=(response.text)
# print(b)
# print(type(b))
files = response.json()
csv_files = [file['download_url'] for file in files if file['name'].endswith('.csv')]
# print(csv_files)
a=csv_files[0]
# print(a)
# print(len(csv_files))
csv_file = csv_files.pop()
# print(csv_file)
d = pd.read_csv(csv_file)
# print(d.columns)
dataframes=[]
file_names=[]
for url in csv_files:
    file_name = url.split("/")[-1].replace(".csv","")
    df = pd.read_csv(url)
    df['Symbol'] = file_name
    dataframes.append(df)
    file_names.append(file_name)
# print(file_names)
# print(dataframes)
# print(len(dataframes))
combined_df = pd.concat(dataframes,ignore_index=True)
# print(combined_df)
o_df = pd.merge(combined_df,d,on='Symbol',how='left')
# print(o_df)
# print(type(o_df))
# print(o_df.head(100))
result = o_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
# print(o_df.info())
# print(result)
o_df["timestamp"] = pd.to_datetime(o_df["timestamp"])
# print(o_df.head())
print(o_df.info())
filtered_df = o_df[(o_df['timestamp'] >= "2021-01-01") & (o_df['timestamp'] <= "2021-05-26")]
# print(filtered_df)
result_time = filtered_df.groupby("Sector").agg({'open':'mean','close':'mean','high':'max','low':'min','volume':'mean'}).reset_index()
list_sector = ["TECHNOLOGY","FINANCE"]
result_time = result_time[result_time["Sector"].isin(list_sector)].reset_index(drop=True)
# print(result_time)
# path=r"C:\Users\Admin\Documents\stock_analysis\output.csv"
# result_time.to_csv(path,header=True)
# print("done")



