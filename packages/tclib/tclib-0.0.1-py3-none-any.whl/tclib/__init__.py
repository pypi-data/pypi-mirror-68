VERSION='0.0.1'
def download(url,path,checksum=None):
	import urllib.request
	import hashlib
	try:
		if checksum is not None and hashlib.sha256(open(path,'rb').read()).hexdigest()==checksum:
			return
	except:
		pass
	urllib.request.urlretrieve(url, path)
	if checksum is not None:
		if hashlib.sha256(open(path,'rb').read()).hexdigest()!=checksum:
			raise Exception('Checksum failed')
