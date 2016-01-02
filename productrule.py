def productrule(inputexpression,allparts,dvar):
	#print inputexpression
	openpar = 0
	isbreak = 0
	cancelnext = 0
	for idx,i in enumerate(inputexpression):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		elif i == '+':
			if openpar == 0:
				breakhere = idx
				isbreak = 1
				isneg = 0
				break
		elif i == '-':
			if idx > 0:
				if openpar == 0:
					breakhere = idx
					isbreak = 1
					isneg = 1
					break
	if isbreak != 1:
		for idx,i in enumerate(inputexpression):
			if i == dvar:
				firstdvar = idx
				break
		for idx,i in enumerate(inputexpression):
			if i == dvar:
				lastdvar = idx
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			elif i == '*':
				if openpar == 0:
					#print inputexpression, dvar
					if idx > firstdvar:
						if idx < lastdvar:
							breakhere = idx
							isbreak = 1
							isneg = 0
							break

		if isbreak == 1:
			leftpart = inputexpression[0:breakhere]
			rightpart = inputexpression[breakhere+1:]
			allparts.append(leftpart)
			allparts.append(rightpart)
		else:
			allparts.append(inputexpression)
	else:
		allparts.append(inputexpression)
	return allparts

#print productrule('3abc*x^2*abc/(1+2)/x*4(1+x)(x+1-3)*(x)/(1+1)*x',[],'x')