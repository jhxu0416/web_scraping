# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 05:17:54 2016

@author: XU_Jiahao
"""
import requests
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
#Need to change city, file_number and API manually for every csv file in step_3
#Because of limited number of call of a single API per day, and the old API expired after recieving new API from google  

city='Washington, DC'
file_number='1'
myFileName=city+'_'+file_number+'.csv'
#for NYC use myFileName='NYC_'+file_number+'.csv'
API="####" #get API from https://developers.google.com/maps/documentation/directions/

df=pd.read_csv(myFileName,sep=',',encoding='latin1')
restaurant_address=df["address"]
restaurant_address=restaurant_address.dropna(axis=0,how='any') #drop missing value

#construct data frame
google_map_df = DataFrame(columns=('Starting_Address', 'Final_Address', 'Mode_of_Transport','Total_Time_to_Destination','Distance','latitude','longitude'))

index=0

for end_point_i in range(len(df)):
    end_point_address=restaurant_address[end_point_i]    
    end_point_city=city
    ending_address=end_point_address
    end_point_address=end_point_address.replace(' ','+').replace(",",'').replace("'",'').replace("[",'').replace("]",'')
    
    end_point_city=end_point_city.replace(' ','+').replace(",",'').replace("'","").replace("[",'').replace("]",'')

    start_address=city   
    start_point=city.replace(' ','+').replace(",",'')
    for mode in{'driving','walking','transit'}: 
        x=1
        if mode =='transit':
            x=-1
        url="https://maps.googleapis.com/maps/api/directions/xml?origin="+start_point+"&destination="+end_point_address+'+'+end_point_city+"&mode="+mode+"&key="+API    
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"lxml")
        All_durations_distance=soup.findAll("text")
        try:
            #find distance
            total_distance=All_durations_distance[-x].contents #to calculate total distance
            #find time
            total_time=All_durations_distance[-x-1].contents  #to calculate total time
        
            latitude=soup.findAll("lat")[-1].contents
            longitude=soup.findAll("lng")[-1].contents
            google_map_df.loc[index] =[start_address, ending_address, mode,total_time,total_distance,latitude,longitude] 
        except:
            pass
        index=index+1

google_map_df.to_csv(myFileName)

print(len(google_map_df))
    
