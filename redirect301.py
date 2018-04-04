#!/usr/bin/env python
import CloudFlare
import pprint
import re

def main():  
	target = "" #Куда редиректить
	mask = "" #Какие доменные имена или кусочек имени

	cf = CloudFlare.CloudFlare()
	zones = cf.zones.get(params={'per_page':50})

	for zone in zones:
		zone_name = zone['name']
		zone_id = zone['id']

		print zone_id, zone_name
		rules = cf.zones.pagerules(zone_id)
		
		for rule in rules:
			print(rule['id'])
			cf.zones.pagerules.delete(zone_id, rule['id'])

		if re.search(r'%s' % mask, zone_name):
			data = {"targets":[{"target":"url","constraint":{"operator":"matches","value":zone_name}}],"actions":[{ "id": "forwarding_url", "value": { "status_code": 301, "url": target } }],"priority":1,"status":"active"}
			cf.zones.pagerules.post(zone['id'], data = data)
		

	exit(0)
if __name__ == '__main__':  
	main()
