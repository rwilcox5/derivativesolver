def constantmultiple(inputexpression,dvar):
	openpar = 0
	isbreak = 0
	cancelnext = 0
	allparts = []
	nonconstant_parts = []
	inputexpression = inputexpression.replace('/','*1.00000/')
	breakprior = 0
	dvaris = []
	print inputexpression
	for idx,i in enumerate(inputexpression):
		if i == dvar:
			dvaris.append(idx)
	#print dvaris
	for idx,i in enumerate(inputexpression):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		elif i == '*':
			#print idx
			if openpar == 0:
				xinside = 0
				#print dvaris, breakprior, idx
				for dvari in dvaris:
					if dvari >= breakprior:
						if dvari < idx:
							xinside = 1
				if xinside == 0:
					allparts.append(inputexpression[breakprior:idx])
					isbreak = 1
				else:
					nonconstant_parts.append(inputexpression[breakprior:idx])
				breakprior = idx
	#print breakprior
	xinside = 0
	for dvari in dvaris:
		if dvari >= breakprior:
			xinside = 1
	if xinside == 0:
		#print "hello"
		allparts.append(inputexpression[breakprior:])
	else:
		nonconstant_parts.append(inputexpression[breakprior:])
	if isbreak == 1:
		leftpart = allparts
		#rightpart = inputexpression[breakhere+1:]
		#allparts.append(leftpart)
		#allparts.append(rightpart)
	the_not_constant = ''
	for i in nonconstant_parts:
		the_not_constant = the_not_constant+i
	the_not_constant = the_not_constant.replace('*1.00000/','/')
	if the_not_constant[0]=='*':
		the_not_constant = the_not_constant[1:]
	return [allparts, the_not_constant]

def pulloutconstant(inputexpression,dvar):
	returnedarr = constantmultiple(inputexpression,dvar)
	returned = returnedarr[0]
	nonconstant = returnedarr[1]
	the_constant_num = []
	the_constant_denom = []
	con_let = []
	con_num = []
	con_let_d = []
	con_num_d = []
	the_constant = ''
	print returned, "returned"
	for factor in returned:
		index = factor.find('/',0)
		if index > -1:
			the_constant_num.append(factor[0:index])
			denom_part = factor[index+1:]
			index2 = denom_part.find('/',0)
			if index2 ==-1:
				the_constant_denom.append(denom_part)
			index2old = -1
			while index2 > -1:
				the_constant_denom.append(denom_part[index2old+1:index2])
				index2old = index2
				index2 = denom_part.find('/',index2+1)
				if index2 == -1:
					the_constant_denom.append(denom_part[index2old+1:])
		else:
			the_constant_num.append(factor)
	print the_constant_num, the_constant_denom
	for factor in the_constant_num:
		factor = factor.replace('*','')
		haslet = 0
		for i in ['a','b','c','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
			if factor.find(i,0)>-1:
				haslet = 1
				break
		if haslet == 1:
			con_let.append(factor)
		else:
			con_num.append(factor)
	for factor in the_constant_denom:
		factor = factor.replace('*','')
		haslet = 0
		for i in ['a','b','c','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
			if factor.find(i,0)>-1:
				haslet = 1
				break
		if haslet == 1:
			con_let_d.append(factor)
		else:
			con_num_d.append(factor)
	con_number = 1
	con_number_d = 1
	for i in con_num:
		con_number=con_number*float(i)
	try:
		con_number=int(con_number)
	except:
		pass
	for i in con_num_d:
		con_number_d = con_number_d*float(i)
	try:
		con_number_d=int(con_number_d)
	except:
		pass
	con_number=str(con_number)
	con_number_d=str(con_number_d)
	if con_number != '1':
		for i in con_let:
			con_number=str(con_number)+i
	else:
		if len(con_let)>0:
			con_number = ''
			for i in con_let:
				con_number=str(con_number)+i
	if con_number_d != '1':
		for i in con_let_d:
			con_number_d=str(con_number_d)+i
	else:
		if len(con_let_d)>0:
			con_number_d = ''
			for i in con_let_d:
				con_number_d=str(con_number_d)+i
	if con_number_d == '1':
		the_constant = con_number
	else:
		the_constant = con_number+'/('+con_number_d+')'
	print con_number
	print con_let
	print con_number_d
	print con_let_d
	#the_constant=the_constant+factor
	print the_constant
	print nonconstant
	if str(the_constant) != '1':
		return [True, the_constant, nonconstant, dvar]
	else:
		return [False, inputexpression,dvar]



#print pulloutconstant()