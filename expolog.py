def logrule(inputexpression,dvar):
	if inputexpression[:4]=='log(':
		if inputexpression[4:4+len(dvar)]==dvar:
			if inputexpression[4+len(dvar):]==')':
				return [True,'1/('+dvar+')']
			else:
				return [False,inputexpression]
		elif inputexpression[4:2+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if inputexpression[2+len(dvar):]==')':
						return [True,'1/'+dvar]
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[4:6+len(dvar)]=='('+dvar+')':
			if inputexpression[6+len(dvar):]==')':
				return [True,'1/('+dvar+')']
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]

def exporule(inputexpression,dvar):
	if inputexpression[:3]=='e^(':
		if inputexpression[3:3+len(dvar)]==dvar:
			if inputexpression[3+len(dvar):]==')':
				return [True,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[3:1+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if inputexpression[1+len(dvar):]==')':
						return [True,inputexpression]
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[3:5+len(dvar)]=='('+dvar+')':
			if inputexpression[5+len(dvar):]==')':
				return [True,inputexpression]
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	elif inputexpression[:2]=='e^':
		if inputexpression[2:2+len(dvar)]==dvar:
			if len(inputexpression)==len(dvar)+2:
				return [True,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[2:0+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if len(inputexpression)==len(dvar):
						return [True,inputexpression]
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

def expologrule(inputexpression,dvar):
	log_it = logrule(inputexpression,dvar)
	if log_it[0]:
		return [True,log_it[1]]
	else:
		exp_it = exporule(inputexpression,dvar)
		if exp_it[0]:
			return [True,exp_it[1]]
		else:
			return [False,inputexpression]
