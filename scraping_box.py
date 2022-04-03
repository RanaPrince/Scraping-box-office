#importing the relevant libraries

from cgitb import html
from tkinter import W
from urllib import request
from matplotlib.pyplot import table
import requests
import datetime
from requests_html import HTML
import pandas as pd
import lxml.html
import os


# now = datetime.datetime.now()
# year = now.year

# if res.status_code == 200:
#     html_text = res.text
#     with open(f"worldwide-{year}.html","w",encoding="utf-8") as f:
#         f.write(html_text)






# A function Box_office_data defined to get the data from 

def Box_office_data(year):
    if len(f"{year}") == 4 and year >= 1977:
        
#       url  = "https://www.boxofficemojo.com/year/world/"
        
        #to get the response form the box-officce url
        res = requests.get(f"https://www.boxofficemojo.com/year/world/{year}") 
         
        #check if the url is active,working
        if res.status_code in range(200,299):
            
            r_html = HTML(html=res.text)
            
            #now we start building our table parser
            
            #find the table by the class value
            table_class =".imdb-scroll-table" 
            r_table = r_html.find(table_class)
            parsed_table = r_table[0]
            
            #value of the year as per the website
            year_w = ((r_html.find(".mojo-gutter")[0].find("h1"))[0].text).split("Worldwide")[0]
           
            #find the header & row values in the table
            rows = parsed_table.find("tr")
            
            #header values find by element, storing them to a list
            header = rows[0]
            header_names = [h.text for h in header.find("th")]

            #row values find by element,storing them to a list
            row_values = []
            for row in rows[1:]:
                row_val = [r.text for r in row.find("td")]
                row_values.append(row_val)
            
            #Creating a dataframe for the table scraped
            boxoffice_data= pd.DataFrame(row_values,columns = header_names)
            
            #storing the table as a csv file based on year for which data extracted
            boxoffice_data.to_csv(os.path.join(r'C:\Users\ranap\OneDrive\Desktop\Crawling & API\Scraping Box Office',
                            f'Box-Office {year} Data.csv'),index=False)
            
            print(f"Box office Data extracted for the year,{year} - Saved as a csv")
            
        #reroutes & directions for failed cases
        
        else:
            print("Url has some issue or redirection detected")
            
    else:
        print("Please check the year entered - as per the website data available for year 1977 & after")
        
        
    #Function to extract the data for past n years

def Extract_past_data(past_years):
    current_year = datetime.datetime.now().year
    start_year = current_year - past_years
    
    #to extract the data in range
    for i in range(start_year+1,current_year+1):
        Box_office_data(i)

        if i == current_year: #Display the complte extraction message 
            print("-"*20)
            print(f"\nExtraction done for past {past_years} years,files saves as csv")




