from powerrule import powerrule
try:
	from main import derivative
except:
	pass
def checkpower(inputexpression,dvar):
	power_spots = []
	for idx,i in enumerate(inputexpression):
		if i == '^':
			power_spots.append(idx-1)
	if len(power_spots)>0:
		#print power_spots, inputexpression
		openpar = 0
		isbreak = 0
		cancel_it = 0
		for idx,i in enumerate(inputexpression):
			if i == '(':
				openpar = openpar+1
			elif i == ')':
				openpar = openpar-1
			if openpar == 0:
				cancel_it = 1
				stopper = idx
				break
		if cancel_it == 1:
			if stopper in power_spots:
				#print stopper
				openpar = 0
				isbreak = 0
				cancel_it = 0
				for idx,i in enumerate(inputexpression[stopper+2:]):
					if i == '(':
						openpar = openpar+1
					elif i == ')':
						openpar = openpar-1
					if openpar == 0:
						cancel_it = 1
						stopper2 = idx
						break
				if stopper2 == len(inputexpression[stopper+2:])-1:
					return [powerrule(inputexpression,inputexpression[:stopper+1]),"derivative",inputexpression[:stopper+1]]
				else:
					return inputexpression
			else:
				return inputexpression
		else:
			return inputexpression
	else:
		return inputexpression

def chainrule(inputexpression,dvar):
	
	return checkpower(inputexpression,dvar)
	#except:
	#	return inputexpression