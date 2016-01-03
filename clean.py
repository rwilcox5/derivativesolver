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
def cleanpar(inputexpression, dvar):
	inputexpression = inputexpression.replace(' ','')
	if inputexpression[0]=='(':
		if inputexpression[len(inputexpression)-1]==')':
			justenough = 0
			openpar = 0
			for i in inputexpression[:len(inputexpression)-2]:
				if i =='(':
					openpar = openpar+1
				elif i == ')':
					openpar = openpar-1
				if openpar < 0:
					print "too many closing parentheses"
				elif openpar == 0:
					justenough = 1
			if justenough !=1:
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
										if inputexpression[idx-3:idx]!='log':
											inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
											#print inputexpression
											inputexpression = cleanpar(inputexpression,dvar)
											cancelnext = 1
											break
	if cancelnext != 1:
		for idx,i in enumerate(inputexpression):
			#if i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
			if i in ['x']:
				if idx > 0:
					if inputexpression[idx-1]!='*':
						if inputexpression[idx-1]!='^':
							if inputexpression[idx-1]!='(':
								if inputexpression[idx-1]!='/':
									if inputexpression[idx-1]!='+':
										if inputexpression[idx-1]!='-':
											inputexpression=inputexpression[0:idx]+'*'+inputexpression[idx:]
											#print inputexpression
											inputexpression = cleanpar(inputexpression,dvar)
											cancelnext = 1
											break

	return inputexpression

#print cleanpar('1/3x^2*abc/(1+2)/ x*4(1+x)(x+1-3)*(x)/(1+1)x','x')

def post_clean(f):
	try:
		f = str(eval(f))
	except:
		if fullparen(f):
			f = f[1:len(f)-1]
	return f



