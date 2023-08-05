import json
import pandas as pd
import requests
import time

def timecop_univariate(URL,name,data, train=False, restart=False):
    # api-endpoint    
    send_data = {}
    send_data['data'] = data
    send_data['name']=name
    send_data['num_future'] = 5
    send_data['desv_metric'] =2
    send_data['restart'] = restart
    
    send_data['train'] = train
    salida = json.dumps(send_data)
    print (salida)

    # sending get request and saving the response as response object
    post_URL = URL + 'back_univariate'
    r = requests.post(url = post_URL, json =  send_data)
    print (r)

    # extracting data in json format

    data = r.json()

    print(data['task_id'])
    
    status_URL =  URL + 'back_univariate_status/' + data['task_id']
    #print (status_URL)
    datos={}
    state =''
    while state != 'SUCCESS':
        time.sleep(10)
        datos = requests.get(url = status_URL)
        print ('#', end='')
        #print(datos.text)
        
        datos_json = datos.json()
        state = datos_json['state']
        
        
        #print (datos_json)
    
    return (datos_json)


def timecop_multivariate(URL,name, main, timeseries, train=False, restart=False):
    # api-endpoint
    
    send_data = {}
    send_data['main'] = main
    send_data['timeseries'] = timeseries

    #send_data['name']=name
    send_data['num_future'] = 5
    send_data['desv_metric'] =2
    #send_data['restart'] = False
    
    send_data['train'] = train
    salida = json.dumps(send_data)
    print (salida)

    # sending get request and saving the response as response object
    post_URL = URL + 'back_multivariate'
    r = requests.post(url = post_URL, json =  send_data)
    print (r)


    # extracting data in json format

    data = r.json()

    print(data['task_id'])
    
    status_URL =  URL + 'back_multivariate_status/' + data['task_id']
    #print (status_URL)
    datos={}
    state =''
    while state != 'SUCCESS':
        time.sleep(10)
        datos = requests.get(url = status_URL)
        print ('#', end='')
        #print(datos.text)
        
        datos_json = datos.json()
        state = datos_json['state']
        
        
        print (datos_json)
    
    return (datos_json)