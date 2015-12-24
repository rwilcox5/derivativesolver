def productrule(inputexpression,allparts,dvar):
	openpar = 0
	isbreak = 0
	cancelnext = 0
	#add exceptions for trig functions, etc
	for idx,i in enumerate(inputexpression):
		if i == '(':
			if openpar == 0:
				if idx > 0:
					if inputexpression[idx-1]!='*':
						if inputexpression[idx-1]!='/':
							if inputexpression[idx-1]!='^':
								if inputexpression[idx-1]!='+':
									if inputexpression[idx-1]!='-':
										inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
										print inputexpression
										allparts = productrule(inputexpression,allparts,dvar)
										cancelnext = 1
										break
	if cancelnext != 1:
		for idx,i in enumerate(inputexpression):
			if i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
				if openpar == 0:
					if idx > 0:
						if inputexpression[idx-1]!='*':
							if inputexpression[idx-1]!='^':
								if inputexpression[idx-1]!='(':
									if inputexpression[idx-1]!='/':
										if inputexpression[idx-1]!='+':
											if inputexpression[idx-1]!='-':
												inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
												print inputexpression
												allparts = productrule(inputexpression,allparts,dvar)
												cancelnext = 1
												break
	if cancelnext != 1:
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
	return allparts

print productrule('3abc*x^2*abc/(1+2)/x*4(1+x)(x+1-3)*(x)/(1+1)*x',[],'x')