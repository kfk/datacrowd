from datacrowd.app import app
from datacrowd.lib.lfinancials import financials_grid 
from flask import jsonify, render_template

@app.route('/financials')
def financials():
	return render_template('tfinancials.html')

@app.route('/financials_json')
def financials_json():
	finDataLoc=app.config['finDataLoc']
	formuDataLoc=app.config['formuDataLoc']
	d = financials_grid(finDataLoc,formuDataLoc)
	return jsonify(d)
