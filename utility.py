import requests

# onemap authentication
def get_onemap_token(username, password):
    api_query = "https://developers.onemap.sg/commonapi/search/privateapi/auth/post/getToken"
    results = requests.post(api_query, headers={'email':username, 'password':password})
    results = results.json()
    token = results['access_token']
    exp_date = results['expiry_timestamp']
    
    return token