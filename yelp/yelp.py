# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:59:30 2016

@author: XU_Jiahao
"""
import pandas as pd
from pandas import DataFrame
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
auth = Oauth1Authenticator(
    consumer_key='####',
    consumer_secret='####',
    token='####',
    token_secret='####'
)
client = Client(auth)
#print(client)


neighborhood_list = pd.read_csv('neighborhood_list.csv', sep=',', encoding='latin1')
city_list_A={'Washington, DC','San Francisco, CA','Chicago, IL'}
city_list_Backup={'Boston, MA','Philadelphia, PA','Seattle, WA'}
city_list_NY={'Bronx, NY','Brooklyn, NY','Manhattan, NY','Queens, NY','Staten Island, NY'}
city_list_test={'San Francisco, CA'}

for city in city_list_test:
    for data_set_number in {'0','1'}:
        index=0
        df = DataFrame(columns=('id', ' name', 'is_claimed','is_closed','url','phone',
                                'review_count','rating','categories','snippet_text','address',
                                'city','state','country','postal_code','neighborhoods','display_address',
                                'deals','menu_provider','reservation_url'),index=[0])
        city_term=city
        if data_set_number=='1':
            city_term=city+'1'            
        neighborhood_in_city=neighborhood_list[city_term].dropna(axis=0, how='any') #drop empty data
        for neighborhood_iteration in range(0,len(neighborhood_in_city)):
            region=(neighborhood_in_city[neighborhood_iteration])+' '+city
            for term in ['food','bar']:
                for offset in [0,20]: #Everytime 20 results are given and at most 40 results are given under same search params
                    params = {
                        'term': term,
                        'sort':1,
                        'offset':offset,
                        }   
                            # use Client to get search result
                    response=client.search(region,**params)

                    for i in range(len(response.businesses)):
                        id=response.businesses[i].id #Yelp ID
                        name=response.businesses[i].name 
                        is_claimed=response.businesses[i].is_closed #Whether business has been claimed by a business owner
                        is_closed=response.businesses[i].is_closed #Whether business has been (permanently) closed
                        url=response.businesses[i].url
                        phone=response.businesses[i].phone
                        review_count=response.businesses[i].review_count
                        rating=response.businesses[i].rating
                        categories=response.businesses[i].categories
                        snippet_text=response.businesses[i].snippet_text
                        address=response.businesses[i].location.address
                        city_name=response.businesses[i].location.city
                        state=response.businesses[i].location.state_code
                        country=response.businesses[i].location.country_code
                        postal_code=response.businesses[i].location.postal_code	
                        neighborhoods=response.businesses[i].location.neighborhoods
                        display_address=response.businesses[i].location.display_address
                        deals=response.businesses[i].deals
                        menu_provider=response.businesses[i].menu_provider
                        reservation_url=response.businesses[i].reservation_url
                        df.loc[index] = [id,name,is_claimed,is_closed,url,phone,review_count,rating,
                        categories,snippet_text,address,city_name,state,country,postal_code,neighborhoods,
                        display_address,deals,menu_provider,reservation_url]
                        index=index+1
    
        myFileName="Raw_"+city+data_set_number+".csv"
        df.to_csv(myFileName)
















