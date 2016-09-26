import geoip
import sys
import signal

node={}
reply={}
def parse_trace_caida():
	geoip_helper = geoip.geoip_helper()
	try:
		while True:
			line = raw_input()
			if line.split('\t')[1] == "R":
				r = line.split('\t')[2]
				if not reply.has_key(r):
					reply[r] = (geoip_helper.query(r)["bgp"])["country"]
			for n in (line.split('\t')[3:]):
				n = n.split(',')[0]
				if (n == "q"):
					continue
				if not node.has_key(n):
					node[n] = (geoip_helper.query(n)["bgp"])["country"]
	except:
		return

def get_country_ip():
	country_ip = {"ip":{},"reply":{}}
	for n in node.keys():
		if not country_ip["ip"].has_key(node[n]):
			country_ip["ip"][node[n]] = 1
		else:
			country_ip["ip"][node[n]] = country_ip["ip"][node[n]] + 1
	
	for n in reply.keys():
		if not country_ip["reply"].has_key(reply[n]):
			country_ip["reply"][reply[n]] = 1
		else:
			country_ip["reply"][reply[n]] = country_ip["reply"][reply[n]] + 1

	return country_ip

def sig_handler(sig, frame):
	country_ip = get_country_ip()
	for c in country_ip.keys():
		print c+"\t"+str(country_ip[c])
	exit()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sig_handler)
	parse_trace_caida()
	country_ip = get_country_ip()
	for c in country_ip["ip"].keys():
		print c+"\t"+str(country_ip["ip"][c]),
		if country_ip["reply"].has_key(c):
			print str(country_ip["reply"][c])
		else:
			print "*"
