def powerrule(inputexpression,dvar):
	#print inputexpression, dvar
	if len(inputexpression)>len(dvar)+1:
		if inputexpression[:len(dvar)]==dvar:
			if inputexpression[len(dvar)]=='^':
				#print "heree"
				the_exponent = inputexpression[len(dvar)+1:]
				#print the_exponent
				try:
					the_exponent = float(the_exponent)
					if int(the_exponent)==float(the_exponent):
						the_exponent=int(the_exponent)
						return str(the_exponent)+'*'+dvar+'^('+str(the_exponent-1)+')'
					else:
						return str(the_exponent)+'*'+dvar+'^('+str(the_exponent-1)+')'
					#print 'hereee'
				except:
					try:
						if the_exponent[0]=='(':
							if the_exponent[len(the_exponent)-1]==')':
								the_exponent = the_exponent[1:len(the_exponent)-1]
								the_exponent = float(the_exponent)
								if int(the_exponent)==float(the_exponent):
									the_exponent=int(the_exponent)
									return str(the_exponent)+'*'+dvar+'^('+str(the_exponent-1)+')'
								else:
									return str(the_exponent)+'*'+dvar+'^('+str(the_exponent-1)+')'
							else:
								return inputexpression
						else:
							return inputexpression
					except:
						return inputexpression
			else:
				return inputexpression
		else:
			return inputexpression
	elif inputexpression == dvar:
		return '1'
	elif inputexpression.find(dvar,0)<0:
		return '0'
	else:
		return inputexpression



