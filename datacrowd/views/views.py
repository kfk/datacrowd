from datacrowd.app import app
from flask import render_template, request
from wtforms import Form, BooleanField, TextField, validators

@app.route('/tests')
def tests():
	return render_template('frame.html')

def clean_string(string):
	for item in ['\n']:
		string = string.replace(item,'')
	return string
@app.route('/financials/csvLoad', methods=['GET','POST'])
def fin_csvLoad():
	if request.method=='POST':
		fl = request.files['file']
		fl_l=fl.readlines()
		dataset = open(app.config['finDataLoc'],'r').readlines()
		entityLoad = fl_l[0].split(',')[0]
		out=''
		for row in dataset:
			print row
			if row.split(',')[0]!=entityLoad:
				out+=row
		for row in fl_l:
			out+=clean_string(row)+'\n'
		open(app.config['finDataLoc'],'w').write(out)
	return render_template('tcsvLoad.html')

#From here products view and lib (to move when done)
from pandas import read_csv, merge
import numpy as np
from flask import jsonify

@app.route('/productsAoP')
def productsAoP():
	return render_template('productsAoP.html')

@app.route('/productsAoP/json')
def productsAoP_df():
	df = read_csv('/home/alessio/projects/07_datacrowd/sample_data/pndata.dat')
	total_shp = df['shp'].sum()
	grouped = df.groupby('cus', as_index=False)
	cus_grouped = grouped.sum()
	df = merge(df,cus_grouped,on='cus')
	df['prodRankByCus']= df['shp.x']/df['shp.y']
	df['cusRank'] = df['shp.y']/total_shp
	
	print df

	#DF by product so to calculate the product importance indicator
	prod_df = df.groupby('prod', as_index=False)
	prod_df = prod_df.agg({'cusRank':np.mean, 'prodRankByCus':np.mean, 'shp.x':np.sum,'cost.x':np.sum})
	prod_df['prodInd'] = prod_df['cusRank']*prod_df['prodRankByCus']
	prod_df['smi'] = 1-prod_df['cost.x']/prod_df['shp.x']	
		
	d = {}
	selectCols = ['prod','cus','shp.x']
	grouped = df[selectCols].groupby('prod')
	for name, group in grouped:
		d[name] = {item:list(group[item]) for item in selectCols}
	dataOut = {}
	dataOut['data'] = []
	dataOut['metadata'] = {}	
	dataOut['customers'] = d
	print d
	for tup in prod_df[['smi','prodInd','prod']].to_records(index=False):
		l = list(tup)
		l[0] = round(l[0],5)
		l[1] = round(l[1],5)
		dataOut['data'].append(l[0:2])
		xyKey = '['+str(l[0])[0:7]+','+str(l[1])[0:7]+']'
		dataOut['metadata'][xyKey] = str(l[2])
	return jsonify(dataOut)
