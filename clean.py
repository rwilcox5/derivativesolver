def cleanpar(inputexpression, dvar):
	inputexpression = inputexpression.replace(' ','')
	if inputexpression[0]=='(':
		if inputexpression[len(inputexpression)-1]==')':
			inputexpression = inputexpression[1:len(inputexpression)-1]

	openpar = 0
	isbreak = 0
	cancelnext = 0
	allparts = []
	#add exceptions for trig functions, etc
	for idx,i in enumerate(inputexpression):
		if i == '(':
			if idx > 0:
				if inputexpression[idx-1]!='*':
					if inputexpression[idx-1]!='/':
						if inputexpression[idx-1]!='^':
							if inputexpression[idx-1]!='+':
								if inputexpression[idx-1]!='-':
									if inputexpression[idx-1]!='(':
										inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
										#print inputexpression
										inputexpression = cleanpar(inputexpression,dvar)[0]
										cancelnext = 1
										break
	if cancelnext != 1:
		for idx,i in enumerate(inputexpression):
			if i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
				if idx > 0:
					if inputexpression[idx-1]!='*':
						if inputexpression[idx-1]!='^':
							if inputexpression[idx-1]!='(':
								if inputexpression[idx-1]!='/':
									if inputexpression[idx-1]!='+':
										if inputexpression[idx-1]!='-':
											inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
											#print inputexpression
											inputexpression = cleanpar(inputexpression,dvar)[0]
											cancelnext = 1
											break

	return [inputexpression,dvar]

#print cleanpar('1/3x^2*abc/(1+2)/ x*4(1+x)(x+1-3)*(x)/(1+1)x','x')

