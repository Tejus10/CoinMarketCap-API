import requests
from django.shortcuts import render


def string_to_float_helper(inp_str, default=0):
	if inp_str == "":
		return default
	return float(inp_str)

def index(request):
    api_key = 'c06d9b24-1222-42a0-ac0a-b2de3ad06ae9'
    api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    last24hrdata = []
    last7ddata = []
    both7d24hr = []

    percent_change_24h_min = string_to_float_helper(request.GET.get('percent_change_24h_min', 30), 30)
    percent_change_24h_max = string_to_float_helper(request.GET.get('percent_change_24h_max', 100), 100)
    percent_change_7d_min = string_to_float_helper(request.GET.get('percent_change_7d_min', 100), 100)
    percent_change_7d_max = string_to_float_helper(request.GET.get('percent_change_7d_max', 700), 700)
    volume_24h = string_to_float_helper(request.GET.get('volume_24h', 10000), 10000)
    headers = {'X-CMC_PRO_API_KEY': api_key}
    parameters = {'start': '1', 'limit': '5000', 'convert': 'USD'}

    response = requests.get(api_url, params=parameters, headers=headers)
    data = response.json()
    
    for val in data['data']:
    	is_24hr = False
    	is_7d = False
    	if (val["quote"]["USD"]["percent_change_24h"] >= percent_change_24h_min and val["quote"]["USD"]["percent_change_24h"] <= percent_change_24h_max and val["quote"]["USD"]["volume_24h"] >= volume_24h):
    		last24hrdata.append(val)
    		is_24hr = True
    	if (val["quote"]["USD"]["percent_change_7d"] >= percent_change_7d_min and val["quote"]["USD"]["percent_change_7d"] <= percent_change_7d_max and val["quote"]["USD"]["volume_24h"] >= volume_24h):
    		last7ddata.append(val)
    		is_7d = True
    	if (is_7d and is_24hr):
    		both7d24hr.append(val)

    total_24hr_data = len(last24hrdata)
    total_7d_data = len(last7ddata)
    total_both_data = len(both7d24hr)
    return render(request, 'index.html', {'last24hrdata': last24hrdata, 'last7ddata': last7ddata, 'both7d24hr': both7d24hr, 'total_24hr_data': total_24hr_data, 'total_7d_data': total_7d_data, 'total_both_data': total_both_data})
