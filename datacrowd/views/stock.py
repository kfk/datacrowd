from datacrowd.app import app
from datacrowd.lib import yahoo_stocks as ysk
from flask import render_template, request, jsonify
from wtforms import Form, BooleanField, TextField, validators

import json 

class Stock_id(Form):
    stock_id = TextField('stock_id', [validators.Length(min=4, max=10)])

dh = {'url':'http://ichart.yahoo.com/table.csv?s={stock_id}&a={from_m}&b={from_d}&c={from_y}&d={to_m}&e={to_d}&f={to_y}&g={interval}&ignore=.csv','url_params':{'stock_id':'GOOG', 'from_m':'1', 'from_d':'1', 'from_y':'2007', 'to_m':'2', 'to_d':'28', 'to_y':'2012', 'interval':'w'}}

dc = {'name':'values','url':'http://download.finance.yahoo.com/d/quotes.csv?s={stock_id}&f=nsop&e=.csv','url_params':{'stock_id':'GOOG'},'header':['name','id','open','close']}

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/stock')
def stock():
	return render_template('stock.html')

#From here Apis
import calendar
@app.route('/js_plot/<stock_id>')
def js_plot_t(stock_id):
	interval = request.args['interval']
	mvs = request.args['mvs']
	from_y = request.args['from_y']
	mvs = mvs.split('-')
	dh['url_params']['stock_id']=stock_id
	dh['url_params']['interval']=interval
	dh['url_params']['from_y']=from_y
	rd = ysk.yh_stock_api_get(dh)
	l = []
	j = {}
	for item in rd['values']:
		tl = []
		item_s = item[0].split('-')
		tm = calendar.timegm((int(item_s[0]),int(item_s[1]),int(item_s[2]),0,0,0,0,0))*1000
		tl.append(tm)
		tl.append(float(item[4]))
		l.append(tl)
		tl = []
	j['stock'] = {'label':stock_id,'data':l}
	del l
	n = 0
	acc = 0
	sort_order = ['stock']
	if int(mvs[0]) != 0:
		for m in mvs:
			m = int(m)
			l = []
			for item in rd['values']:
				tl = []
				n+=1
				if n<=m:
					acc+=float(item[4])
				if n == m:
					item_s = item[0].split('-')
					tm = calendar.timegm((int(item_s[0]),int(item_s[1]),int(item_s[2]),0,0,0,0,0))*1000
					tl.append(tm)
					tl.append(acc/m)
					l.append(tl)
					n=0
					acc=0
			m_nm = 'lm'+str(m)
			sort_order.append(m_nm)
			j['lm'+str(m)] = {'label':m_nm, 'data':l}
	j['sort_order'] = sort_order
	return jsonify(j)

@app.route('/get_last_quote/<stock_id>')
def get_last_quote(stock_id):
	dc['url_params']['stock_id'] = stock_id
	last_quote = ysk.yh_stock_api_get(dc)
	t = {}
	t['aaData'] = last_quote['values']
	t['aoColumns'] = last_quote['header']
	#t['aaData'] = [["q","b","c"]]
	return jsonify(t)

@app.route('/get_hist_quotes/<stock_id>')
def get_hist_quotes(stock_id):
	dc['url_params']['stock_id'] = stock_id
	last_quote = ysk.yh_stock_api_get(dh)
	t = {}
	t['aaData'] = last_quote['values']
	t['aoColumns'] = last_quote['header']
	#t['aaData'] = [["q","b","c"]]
	return jsonify(t)



