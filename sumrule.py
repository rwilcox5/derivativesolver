def sumrule(inputexpression,allparts,dvar):
	openpar = 0
	isbreak = 0
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
	if isbreak == 1:
		leftpart = inputexpression[0:breakhere]
		rightpart = inputexpression[breakhere+1:]
		allparts.append(leftpart)
		allparts.append(isneg)
		nextparts = sumrule(rightpart,allparts,dvar)
		if len(nextparts) == 1:
			allparts.append(rightpart)
	else:
		allparts.append(inputexpression)
	return allparts
