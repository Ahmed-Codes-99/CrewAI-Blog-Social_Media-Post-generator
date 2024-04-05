""" import requests
#Your Access Keys
page_id_1 = 123456789
facebook_access_token_1 = 'paste-your-page-access-token-here'
msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
payload = {
'message': msg,
'access_token': facebook_access_token_1
}
r = requests.post(post_url, data=payload)
print(r.text) """