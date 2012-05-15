import urllib2, csv 
import calendar, time

def yh_stock_api_get(d):
	'Gets a hash table with url and url params: {url_1:{param1:xyz,parm2:zvx}}'
	rd = {}
	try:
		rd['header'] = d['header']
	except KeyError:
		rd['header']=False
		
	url = d['url'].format(**d['url_params'])
	data = urllib2.urlopen(url)
	l = []
	n = -1

	for row in csv.reader(data, delimiter=',', quotechar='"'):
		n+=1	
		if rd['header'] != False:
			l.append(row)
		else:
			if n>0:
				l.append(row)
			else:
				rd['header'] = row
	rd['values'] = l
	return rd

