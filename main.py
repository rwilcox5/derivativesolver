
from sumrule import sumrule
from clean import cleanpar
from constantmultiple import pulloutconstant
from productrule import productrule
from powerrule import powerrule
from chainrule import chainrule
from expolog import expologrule
from clean import post_clean
from trigrule import trigrule
from quorule import quorule
import sympy
inputexpression = '2(2x+2)^5+log(x)'
dvar = 'x'
ycount = 0
stopnow = 0
allsteps = []
def slatex(f):
	return sympy.latex(sympy.sympify(post_clean(f)))
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]

def derivative(inputexpression,dvar,ycount):
	global allsteps
	ofunction = cleanpar(inputexpression,dvar)
	allsteps.append([ycount, 'd['+ofunction+']=',ofunction])
	f = cleanpar(inputexpression,dvar)
	#print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		ycount=ycount+1
		f = h[0]+'*('+derivative(h[1],dvar,ycount)+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			#print h
			for idx, i in enumerate(h):
				if idx %2==0:
					#print f, i, h
					f=f+derivative(i,dvar,ycount)
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
			if h[0]:
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+derivative(h[2],dvar)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+derivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+derivative(h[1],dvar,ycount)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+derivative(h[1],dvar,ycount)+')-('+h[1]+')*('+derivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+derivative(h[1],dvar,ycount)+')+'+h[1]+'*('+derivative(h[0],dvar,ycount)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = derivative(h[2],dvar,ycount)
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												if inside_derivative==int(inside_derivative):
													f=h[1]+'*'+str(int(inside_derivative))
												else:
													f=h[1]+'*'+str(float(inside_derivative))
										except:
											if inside_derivative.find('+',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											else:
												f = h[1]+'*'+inside_derivative
									else:
										#Here if chain rule fails
										print "no Derivative", h[1]
										f = h[1]
	#print f
	#print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	#print ycount, cleanpar(f,dvar)
	return cleanpar(f,dvar)

def fullderivative(inputexpression,dvar,ycount):
	allsteps=[]
	f = cleanpar(inputexpression,dvar)
	#print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		ycount=ycount+1
		f = h[0]+'*('+fullderivative(h[1],dvar,ycount)+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			#print h
			for idx, i in enumerate(h):
				if idx %2==0:
					#print f, i, h
					f=f+fullderivative(i,dvar,ycount)
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
			if h[0]:
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+fullderivative(h[2],dvar)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount)+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+fullderivative(h[1],dvar,ycount)+')+'+h[1]+'*('+fullderivative(h[0],dvar,ycount)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = fullderivative(h[2],dvar,ycount)
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												if inside_derivative==int(inside_derivative):
													f=h[1]+'*'+str(int(inside_derivative))
												else:
													f=h[1]+'*'+str(float(inside_derivative))
										except:
											if inside_derivative.find('+',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = h[1]+'*('+inside_derivative+')'
											else:
												f = h[1]+'*'+inside_derivative
									else:
										#Here if chain rule fails
										print "no Derivative", h[1]
										f = h[1]
	#print f
	#print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	#print ycount, cleanpar(f,dvar)
	return cleanpar(f,dvar)

def onestepderivative(inputexpression,dvar,ycount):
	f = cleanpar(inputexpression,dvar)
	#print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		f = h[0]+'*('+'\\frac{d}{dx}('+h[1]+'))'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			#print h
			for idx, i in enumerate(h):
				if idx %2==0:
					#print f, i, h
					f=f+'\\frac{d}{dx}('+i+')'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar)
			if h[0]:
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrule(f,dvar)
						if h[0]:
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+'\\frac{d}{dx}('+h[1]+')'+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+'\\frac{d}{dx}('+h[1]+')'+')-('+h[1]+')*('+'\\frac{d}{dx}('+h[2]+')'+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+'\\frac{d}{dx}('+h[1]+')'+')+'+h[1]+'*('+'\\frac{d}{dx}('+h[0]+')'+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										
										f=h[1]+'*'+'\\frac{d}{dx}('+h[2]+')'
									else:
										#Here if chain rule fails
										print "no Derivative", h[1]
										f = h[1]
	#print f
	#print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	#print ycount, cleanpar(f,dvar)
	return f

the_derivative = derivative(inputexpression,dvar,0)
print sympy.latex(sympy.sympify(the_derivative))

for i in allsteps:
	#print i
	my_str = ''
	for ii in range(0,i[0]):
		my_str=my_str+'   '
	#print my_str+i[1]+onestepderivative(i[2],dvar,0)

for idx,i in enumerate(allsteps):
	if onestepderivative(i[2],dvar,0).find('\\frac{d}{dx}',0)==-1:
		i.append('solved')
	else:
		i.append("not")
	i.append("")
	i.append([])
	i.append("")
	i.append("")
	for iidx,ii in enumerate(allsteps[idx+1:]):
		if ii[0]==i[0]+1:
			i[5].append(idx+iidx+1)
		if ii[0]==i[0]:
			i[6]=idx+iidx+1
			i[4]=idx+iidx+1
			break
		if ii[0]<i[0]:
			i[4]=idx+iidx+1
			break
	for iidx,ii in enumerate(allsteps[:idx]):
		if ii[0]<i[0]:
			i[7]=iidx


numruns = 0
#print "let's see"
previous_stuff = '$'+allsteps[0][1]+'$\\newline $'
print '$'+allsteps[0][1]+'$\\newpage '
def solve_steps(allsteps,solveid,show_children,dvar):
	global previous_stuff
	#print solveid

	level = allsteps[solveid][0]
	rangemin= solveid+1
	if allsteps[solveid][4] !="":
		rangemax = allsteps[solveid][4]
	else:
		rangemax=len(allsteps)
	run_this = 0
	for i in allsteps[rangemin:rangemax]:
		if i[3]=="not":
			run_this=1
	if run_this ==1:
		has_d = 0
		dvis=[]
		#print 'h'
		for idx,i in enumerate(allsteps[rangemin:rangemax]):
			if i[0]==level+1:
				if i[3]=="solved":
					print previous_stuff+i[1]+sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0)))+'\\newpage'
					previous_stuff = previous_stuff+i[1]+sympy.latex(sympy.sympify(fullderivative(i[2],dvar,0)))+'$\\newline $'
				else:
					print previous_stuff+i[1]+'$\\newpage '
					previous_stuff = previous_stuff+i[1]+'$\\newline $'
				
		solve_steps(allsteps,allsteps[solveid][5][0],1,dvar)


	else:
		#print 'j'
		if allsteps[solveid][3]!="solved":
			if show_children==1:
				for idx,i in enumerate(allsteps[rangemin:rangemax]):
					if i[0]==level+1:
						print previous_stuff+i[1]+onestepderivative(i[2],dvar,0)+'$\\newpage '
						previous_stuff = previous_stuff+i[1]+onestepderivative(i[2],dvar,0)+'$\\newline $'
			allsteps[solveid][3]="solved"
			print previous_stuff+allsteps[solveid][1]+sympy.latex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0)))+'$\\newpage '
			previous_stuff = previous_stuff+allsteps[solveid][1]+sympy.latex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0)))+'$\\newline $'
		if allsteps[solveid][6]!='':
			solve_steps(allsteps,allsteps[solveid][6],1,dvar)
		else:
			if allsteps[solveid][7]!=0:
				solve_steps(allsteps,allsteps[solveid][7],0,dvar)
			else:
				return "done"


solve_steps(allsteps,0,1,dvar)
#print previous_stuff
