from powerrule import powerrule
try:
	from main import derivative
except:
	pass
def fullparen(input_string):
	openpar = 0
	isbreak = 0
	cancel_it = 0
	really_cancel = 0
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			cancel_it = 1
			isbreak = idx
			break
	if isbreak == len(input_string)-1:
		return True
	else:
		return False
def checkpower(inputexpression,dvar):
	power_spots = []
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		#print power_spots, inputexpression
		openpar = 0
		isbreak = 0
		cancel_it = 0
		really_cancel = 0
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			if openpar == 0:
				cancel_it = 1
				stopper = idx
				index1 = inputexpression[:stopper].find(dvar,0)
				index2 = inputexpression[stopper+1:].find(dvar,0)
				if index1 <0:
					really_cancel = 1
				if index2 >-1:
					really_cancel = 1
				break
		if really_cancel !=1:
			if cancel_it == 1:
				if stopper in power_spots:
					#print stopper
					openpar = 0
					isbreak = 0
					cancel_it = 0
					for idx,i in enumerate(inputexpression[stopper+2:]):
						if i == '(':
							openpar = openpar+1
						elif i == ')':
							openpar = openpar-1
						if openpar == 0:
							cancel_it = 1
							stopper2 = idx
							break
					if stopper2 == len(inputexpression[stopper+2:])-1:
						return [True,powerrule(inputexpression,inputexpression[:stopper+1])[1],inputexpression[:stopper+1]]
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]

def checkexpo(inputexpression,dvar):
	if inputexpression[:3]=='e^(':
		if fullparen(inputexpression[2:]):
			the_exponent = inputexpression[3:len(inputexpression)-1]
			if the_exponent.find(dvar,0)>-1:
				return [True,inputexpression,the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def checklog(inputexpression,dvar):
	if inputexpression[:4]=='log(':
		if fullparen(inputexpression[3:]):
			the_exponent = inputexpression[4:len(inputexpression)-1]
			if the_exponent.find(dvar,0)>-1:
				return [True,'1/('+the_exponent+')',the_exponent]
			else:
				return [False, inputexpression]
		else:
			return [False, inputexpression]
	else:
		return [False,inputexpression]
def chainrule(inputexpression,dvar):
	expo_chain = checkexpo(inputexpression,dvar)
	log_chain = checklog(inputexpression,dvar)
	power_chain = checkpower(inputexpression,dvar)
	if expo_chain[0]:
		return expo_chain
	elif log_chain[0]:
		return log_chain
	elif power_chain[0]:
		return power_chain
	else:
		return [False, inputexpression]