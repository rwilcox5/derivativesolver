def cleanpar(inputexpression):
	inputexpression = inputexpression.replace(' ','')
	if inputexpression[0]=='(':
		if inputexpression[len(inputexpression)-1]==')':
			inputexpression = inputexpression[1:len(inputexpression)-1]
	return inputexpression

