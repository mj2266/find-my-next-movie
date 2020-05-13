import http.client
import json
import requests
imdbID = '0109830'
print(imdbID)
movie_id = 'tt{}'.format(imdbID)  # this will generate the imdb Movie ID
# -----------------------------------------------------------------------------

# ----------- HERE I WILL CONNECT WITH API AND SEND REQUEST -------------------
# ----------- I WILL GET MY FINAL CLEANED DATA IN VARIABLE 'data' -------------
conn = http.client.HTTPSConnection("api.themoviedb.org")
payload = "{}"
# req_string = "/3/find/%s?external_source=imdb_id&language=en-US&api_key=55ae4e90966677050f53e4c93ae7b804" % movie_id

req_string = 'https://api.themoviedb.org/3/find/tt0109830?api_key=55ae4e90966677050f53e4c93ae7b804&language=en-US&external_source=imdb_id'

response = requests.get(req_string)

# conn.request("GET", req_string, payload)
# res = conn.getresponse()
# data = res.read()

print(response)
data = response.json()
print("data", data)



data = data.get('movie_results')
if not data:
    data = data.get('tv_results')
print (data[0])

