from django.http import HttpResponse
from django.shortcuts import render
import requests,json
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


# Create your views here.
@api_view()
@parser_classes([JSONParser])
def home(request):

    url = "https://gbfs.divvybikes.com/gbfs/en/station_status.json"
    url_bike = "https://gbfs.divvybikes.com/gbfs/en/free_bike_status.json"


    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_bike = requests.request("GET", url_bike, headers=headers, data=payload)

    reply=response.json()
    reply_bike=response_bike.json()
    dock_lst=[]
    ebike_lst=[]
    bike_lst=[]
    stn_lst=[]
    result=reply['data']['stations']
    result_bike=reply_bike['data']['bikes']
    print(len(result))
    for num_dock in result:
        dock_lst.append(num_dock['num_docks_available'])
    for num_ebike in result:
        ebike_lst.append(num_ebike['num_ebikes_available'])
    for num_bike in result:
        bike_lst.append(num_bike['num_bikes_available'])  

    search=list(filter(lambda x:x['station_status']=='active',result))   
    search_bike=list(filter(lambda x:x['is_reserved']==0,result_bike))   
    
    context={
        "num_docks":sum(dock_lst),
        "num_bike":sum(ebike_lst)+sum(bike_lst),
        "num_stn":len(search),
        "num_avail_bike":len(search_bike)
        
    }
    # return render(request,'home.html',context)
    return Response({'data': context})