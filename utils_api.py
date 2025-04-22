import requests 

# server side
def api_send_alarm(aggregator_server, bank_name, bank_code, alarm_type, img_b64=''):
    print(f"ACTION: Send Alarm")
    data = {
        'bank_code': bank_code, 
        'bank_name': bank_name, 
        'alarm_type': alarm_type, 
        'filename': img_b64
    }
    api_url = "{}/api/alarm".format(aggregator_server)
    ret = True
    try:
        response = requests.post(api_url, json=data)
        result = response.json()
        if response.status_code == 200:
            ret = True
    except BaseException as exception:
        print("Error: ", exception)
        ret = False
    return ret

def api_get_init_transactions(aggregator_server, bank_name, bank_code):
    print(f"ACTION: Get Init Transactions")
    init_transactions = []
    data = {
        'bank_code': bank_code, 
        'bank_name': bank_name
    }
    api_url = "{}/api/init_transactions".format(aggregator_server)
    
    try:
        response = requests.post(api_url, json=data)    
        init_transactions = response.json()
        for r in init_transactions:
            print(r)
    except BaseException as exception:
        print("Error: ", exception)
    return init_transactions

def api_set_init_transactions(aggregator_server, bank_name, bank_code, username, transactions, running_balance):
    print(f"ACTION: Set Init Transactions")
    api_url = "{}/api/set_init_transactions".format(aggregator_server)
    
    print("send data--------------------------")    
    for d in transactions:
        print(d)
    print("--------------------------")
    data = {
        'bank_code': bank_code, 
        'bank_name': bank_name,
        'username': username,
        'data': transactions, 
        'running_balance': running_balance,
    }
    ret = False
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            ret = True
    except BaseException as exception:        
        print("Error: ", exception)

    return ret

def api_send_transactions(aggregator_server, bank_name, bank_code, username, transactions, available_balance, current_balance):
    print(f"ACTION: Save Transactions")
    api_url = "{}/api/save_transactions".format(aggregator_server)
    
    print("send data--------------------------")    
    print("available_balance", available_balance)
    print("current_balance", current_balance)
    for d in transactions:
        print(d)
    print("--------------------------")
    data = {
        'bank_code': bank_code, 
        'bank_name': bank_name,
        'username': username,
        'available_balance': available_balance,
        'current_balance': current_balance,
        'data': transactions
    }
    ret = False
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            ret = True
    except BaseException as exception:        
        print("Error: ", exception)

    return ret

##
def api_send_site_info(aggregator_server, bank_name, bank_code, username, password):
    api_url = "{}/api/save_info".format(aggregator_server)
    
    data = {
        'bank_code': bank_code, 
        'bank_name': bank_name,
        'username': username,
        'password': password
    }
    ret = False
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            ret = True
    except BaseException as exception:        
        print("Error: ", exception)

    return ret