def constantmultiple(inputexpression,dvar):
	openpar = 0
	isbreak = 0
	cancelnext = 0
	allparts = []
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
										allparts = constantmultiple(inputexpression,dvar)
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
												allparts = constantmultiple(inputexpression,dvar)
												cancelnext = 1
												break
	if cancelnext != 1:
		breakprior = 0
		dvaris = []
		for idx,i in enumerate(inputexpression):
			if i == dvar:
				dvaris.append(idx)
		print dvaris
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			elif i == '*':
				if openpar == 0:
					xinside = 0
					for dvari in dvaris:
						if dvari > breakprior:
							if dvari < idx:
								xinside = 1
						#print dvari, xinside, breakprior, idx
					if xinside == 0:
						allparts.append(inputexpression[breakprior:idx])
						isbreak = 1
					breakprior = idx
		if isbreak == 1:
			leftpart = allparts
			#rightpart = inputexpression[breakhere+1:]
			#allparts.append(leftpart)
			#allparts.append(rightpart)
		else:
			allparts.append(inputexpression)
	return allparts

def pulloutconstant():
	returned = constantmultiple('1/3*x^2*abc/(1+2)/x*4(1+x)(x+1-3)*(x)/(1+1)*x','x')
	try:
		if int(float(returned[0]))==float(returned[0]):
			returned[0]=int(float(returned[0]))
			return [True,returned]
		else:
			returned[0]=float(returned[0])
			return [True,returned]
	except:
		return [False,returned]

print pulloutconstant()