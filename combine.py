import requests
import csv
import os
import xlrd
import openpyxl
import pandas as pd  
from text_operations import *
from spell_check import *


def sheet_operations():
    sheet = pd.read_excel('D:\Data Cleanising Project\CompanyData.xlsx')

    sheet['dispatch date'] = pd.to_datetime(sheet['dispatch date'], format='%Y%m%d')
    sheet['dispatch date'] = sheet['dispatch date'].astype(str)

    sheet['due date'] = pd.to_datetime(sheet['due date'], format='%Y%m%d')
    sheet['due date'] = sheet['due date'].astype(str)


    sheet2 = text_split(sheet, 'delivery adress')
    sheet3 = text_split2(sheet2, 'gift message')

    sheet3['posting date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
    # sheet.head()

    sheet3.to_excel('Company_Data_updated.xlsx')

def quantity():
    df = pd.read_excel('Company_Data_updated.xlsx' , engine="openpyxl")
    df['Contact Telephone'] = df['Contact Telephone'].str.replace(" ","")
    df['Contact Telephone'] = df['Contact Telephone'].str[-10:]
    new_rows = []
    for index, row in df.iterrows():
        if row['Quantity'] > 1:
            for i in range(row['Quantity']):
                new_row = row.copy()
                new_row['Quantity'] = 1
                new_rows.append(new_row)
        else:
            new_rows.append(row)
            
    new_df = pd.DataFrame(new_rows)
    new_df.to_excel('ModifiedData.xlsx', index=False)
    

def postal_code(zip_code , countryCode):
    zipcode = zip_code
    if countryCode.lower() == 'ireland' or countryCode == "IRL":
        zipcode = zipcode[:3]

    country_code = None
    headers = {
        "apikey": "773bbea0-e1e0-11ed-9323-d50dbf271faf"
    }

    params = {
        "codes": f"{zipcode}",
    }

    if country_code:
        params["country"] = f"{country_code}"

    response = requests.get('https://app.zipcodebase.com/api/v1/search', headers=headers, params=params)

    fields = ['postal_code', 'country_code', 'latitude', 'longitude', 'city', 'state', 'city_en', 'state_en', 'state_code',
            'province', 'province_code']

    data = response.json()
    results =[]
    if(type(data['results']) is not list):
        if len(data['results']) != []:
            results = data['results'][f'{zipcode}']

    for result in results:
        file_exists = os.path.isfile('locations.csv')
        if not os.path.isfile('locations.csv'):
            # create file if it doesn't exist
            with open('locations.csv', mode='w', newline='' , encoding='utf=8') as file:
                writer = csv.writer(file)
                # writer.writerow(fields)
                print("locations.csv file created.")
        # write the data to a CSV file
        with open('locations.csv', mode='a', newline='' , encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            if not file_exists:
                writer.writeheader()
            writer.writerow(result)
        print("Location data saved to locations.csv")
        break

def combine_function():
    sheet_operations()
    quantity()
    new_df = pd.read_excel('ModifiedData.xlsx' , engine="openpyxl")
    
    for ind in new_df.index:
        zipCode = str(new_df["Postcode"][ind]).strip()
        Country_code = str(new_df["Country Code"][ind]).strip()
        
        postal_code(zipCode , Country_code)

    df1 = pd.read_excel('ModifiedData.xlsx')
    df2 = pd.read_csv("locations.csv")

    # merge_df = pd.merge(df ,df1 , left_on='index' , right_on ='index', how = 'outer')
    df = df1.merge(df2, left_index=True, right_index=True, how='outer')

    print(df)
    df.to_excel('Final_Demo.xlsx', index=False)

combine_function()
    