
def indtrigrule(inputexpression,dvar,tf,dtf):
	
	if inputexpression[:4]==tf+'(':
		if inputexpression[4:4+len(dvar)]==dvar:
			if inputexpression[4+len(dvar):]==')':
				if dtf not in ['-csccot','sectan']:
					return [True,dtf+'('+dvar+')']
				else:
					return [True,dtf[:len(dtf)-3]+'('+dvar+')'+dtf[len(dtf)-3:]+'('+dvar+')']
			else:
				return [False,inputexpression]
		elif inputexpression[4:2+len(dvar)]==dvar[1:len(dvar)-1]:
			if dvar[0]=='(':
				if dvar[len(dvar)-1]==')':
					if inputexpression[2+len(dvar):]==')':
						if dtf not in ['-csccot','sectan']:
							return [True,dtf+'('+dvar+')']
						else:
							return [True,dtf[:len(dtf)-3]+'('+dvar+')'+dtf[len(dtf)-3:]+'('+dvar+')']
					else:
						return [False,inputexpression]
				else:
					return [False,inputexpression]
			else:
				return [False,inputexpression]
		elif inputexpression[4:6+len(dvar)]=='('+dvar+')':
			if inputexpression[6+len(dvar):]==')':
				if dtf not in ['-csccot','sectan']:
					return [True,dtf+'('+dvar+')']
				else:
					return [True,dtf[:len(dtf)-3]+'('+dvar+')'+dtf[len(dtf)-3:]+'('+dvar+')']
			else:
				return [False,inputexpression]
		else:
			return [False,inputexpression]
	else:
		return [False,inputexpression]
	return [False,inputexpression]
def trigrule(inputexpression,dvar):
	for tf,dtf in [['sin','cos'],['cos','-sin'],['tan','sec^2'],['csc','-csccot'],['sec','sectan'],['cot','-csc^2']]:
		the_d = indtrigrule(inputexpression,dvar,tf,dtf)
		if the_d[0]:
			return the_d
	return [False,inputexpression]
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]