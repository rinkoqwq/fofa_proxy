import requests
import json
import base64
import time
import threading

header = {'Authorization': ''}

f = open("proxy.txt","a")
f2 = open("proxy_alive.txt","a")

def test_proxy(proxy):
	sem = threading.Semaphore(128)
	with sem:
		try:
			r = requests.get("https://www.baidu.com/robots.txt",proxies={"https":"socks5://"+proxy},timeout=5)
			print(proxy+"OK")
			if 'Disallow' in r.text:
				f2.writelines(proxy+'\n')
		except Exception as e:
			pass

for ip_a in range(1,256):
	for i in range(0,6):
		for ip_b in [0,128]:
			r = requests.get(url="https://api.fofa.info/v1/search?qbase64=%s&full=false&pn=%d&ps=10"%(base64.b64encode(('protocol="socks5" && ip="%d.%d.0.0/9" && "Version:5 Method:No Authentication(0x00)"'%(ip_a,ip_b)).encode()).decode(),i),headers=header)
			data = json.loads(r.text)

			for item in data['data']['assets']:
				print(item['id'])
				f.writelines(item['id']+'\n')
				threading.Thread(target=test_proxy,args=(item['id'],)).start()
			if i >= data['data']['page']['total']//data['data']['page']['size']:
				break
