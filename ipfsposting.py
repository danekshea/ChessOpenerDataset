import requests, urllib

NODE = "http://localhost:5001"
FILE_PATH = "./metadata/8" # path to file you're trying to add
MFS_PATH = "/metadata"   # mfs path you're trying to write to

response = requests.post(NODE+"/api/v0/files/write?arg=%s&create=true" % urllib.parse.quote(MFS_PATH), files={FILE_PATH:open(FILE_PATH, 'rb')})