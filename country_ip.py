import geoip
import sys
import signal
import re
import ip_bst

ip_bst = ip_bst.ip_bst()
ip_dict = {}
country_ip = {"country":{}, "city":{}}

def parse_trace():
	geoip_helper = geoip.geoip_helper()
	
	cnt = 0
	try:
		while True:
			line = raw_input()
			ip = line.strip('\n')
			ip_dict[ip] = ""
			if not ip_bst.has_key_ip(ip):
				try:
					geo = (geoip_helper.query(ip)["mmdb"])
				except:
					print ip
					continue
				insert_geoip(geo)
				ip_bst.insert_key_ip(ip,"")
	except Exception, ex:
		print ex
		print "total dict: "+str(len(ip_dict.keys()))
		return

def insert_geoip(geo):
	country = geo["country"]
	city = geo["city"]
	if not country_ip["country"].has_key(country):
		country_ip["country"][country] = 1
	else:
		country_ip["country"][country] = country_ip["country"][country] + 1
	if not country_ip["city"].has_key(country):
		country_ip["city"][country] = {city:1}
	elif not country_ip["city"][country].has_key(city):
		country_ip["city"][country][city] = 1
	else:
		country_ip["city"][country][city] = country_ip["city"][country][city] + 1

def print_result(country_ip):
	country = country_ip["country"]
	city = country_ip["city"]
	for k in country.keys():
		print k + " " + str(country[k])
		for c in city[k].keys():
			print "\t" + c.encode('utf-8') + " " + str(city[k][c])
	
	print "total ip: "+str(ip_bst.ip_cnt)

def sig_handler(sig, frame):
	print_result(country_ip)
	exit()

def main(argv):
	signal.signal(signal.SIGINT, sig_handler)
	parse_trace()
	print_result(country_ip)
	
if __name__ == "__main__":
	main(sys.argv)
