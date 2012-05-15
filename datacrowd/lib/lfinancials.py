import re

regexp = r'[A-Z0-9]+\.[A-Z0-9]+\.[A-Z0-9]+|[A-Z0-9]+\.[A-Z0-9]+|[A-Z0-9]+'

def clean_string(string):
	for item in ['-','@s','@p','\n']:
		string = string.replace(item,'')
	return string

def reg_repl(entity):
	def wrapped(matchobj):
		m = matchobj.group(0)
		dict_key ='float(d["data"][("'+entity+'","'+m+'")][i])'
		return dict_key
	return wrapped

#DATA API: d[data][entity,account], d[row_len], d[entities]
#Arg: file object 
def import_financials(f):
	d = {}
	d['data'] = {}
	#TODO: change the find string in sub
	for row in f:
		row = row.split(',')
		n = len(row)
		d['data'][(row[0],row[2])]=row[3:n]
	d['row_len'] = int(n)
	entities = set()
	for k in d['data'].keys():
		entities.add(k[0])
	d['entities'] = entities
	d['fcst'] = row[1]
	return d

def mk_financials_grid(d,d_formulas):
	for entity in d['entities']:
		for k in d_formulas['ORDER']:
			formula = re.sub(regexp, reg_repl(entity),d_formulas[k])
			print entity,k
			d['data'][(entity,k)] = [eval(formula) for i in range(d['row_len']-3)]	
	return d

#TODO: check for accounts with same name
def formulas_to_d(f):
	'arg: file object'
	d = {}
	d['FORMULAS']={}
	d['FORMULAS']['ORDER'] = []
	d['ACCOUNTS'] = {}
	d['ACCOUNTS']['ORDER'] = []
	start = False
	start_sl = ['>FORMULAS','>ACCOUNTS_ORD']
	for row in f:
		if row[0]=='>':
			start = True
		if row[0]=='<':
			start = False
		if row[0:len(row)-1] in start_sl:
			conf_group=row[0:len(row)-1] 	
		if start and conf_group==start_sl[0]:
			try:
				rs = row.split('=')
				d['FORMULAS'][rs[0]]=rs[1]
				d['FORMULAS']['ORDER'].append(rs[0])
			except IndexError:
				pass
		if start and conf_group==start_sl[1] and row[0]!='>':
			row = row.split(',')	
			j = row[1:3]
			accs_attr_d = {'-':'lev2','h':'row_highlight','':'lev1','--':'lev3','l':'row_2l','g':'row_2g'}
			if row[0]=='' or row[0][0]=='@':
				key = row[1]
				attrs = row[0].split('@')
				row_class = ' '.join([accs_attr_d[attr] for attr in attrs])
				j.append(row_class)
				d['ACCOUNTS'][key] = [j]
				d['ACCOUNTS']['ORDER'].append(key)
			else:
				attrs = row[0].split('@')
				row_class = ' '.join([accs_attr_d[attr] for attr in attrs])
				j.append(row_class)
				d['ACCOUNTS'][key].append(j)
	return d

def financials_rows(entity,account,row_class,financials_d):
	n=2
	dt={}
	for i in financials_d['data'][(entity,account[0])]:
		n+=1
		dt[n]=i
		dt[0]=entity
		dt[1]=account[0]
		dt[2]=account[1]
		dt['DT_RowClass']=row_class
	return dt

def financials_grid(finDataLoc,formuDataLoc):
	f = open(finDataLoc)
	f_formulas = open(formuDataLoc)
	d_formulas = formulas_to_d(f_formulas)
	d = import_financials(f)
	financials_d = mk_financials_grid(d,d_formulas['FORMULAS'])
	d = {}
	l = []
	print d_formulas['ACCOUNTS']['ORDER']
	for entity in financials_d['entities']:
		for parent_account in d_formulas['ACCOUNTS']['ORDER']:	
			for account in d_formulas['ACCOUNTS'][parent_account]:	
				row_class = account[2]
				dt = financials_rows(entity,account,row_class,financials_d)
				l.append(dt)
	d['aaData'] = l
	d['aoColumns']=['entity','account','account_name',1,2,3,4,5,6,7,8,9,10,11,12]
	d['entities']=list(financials_d['entities'])
	return d



