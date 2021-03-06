
import time
#print time.time()
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
from other import othertricks
import sympy
import os
import sys
#print time.time()


def myslatex(input_string):
	input_string = sympy.latex(input_string).replace('holdfordydx','\\frac{dy}{dx}')
	return input_string
def slatex(f):
	return myslatex(sympy.sympify(post_clean(f)))
def inversetrigrule(inputexpression,dvar):
	#This is unncessary if also remove the uneccsary calls
	return [False,inputexpression]
def needspar(input_string):
	needsapar = False
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
			if i=='+':
				needsapar=True
			if i=='-':
				needsapar=True
			cancel_it = 1
			isbreak = idx
			break
	for idx,i in enumerate(input_string):
		if i == '(':
			openpar = openpar+1
		elif i == ')':
			openpar = openpar-1
		if openpar == 0:
			if i=='+':
				needsapar=True
			if i=='-':
				needsapar=True
	return needsapar
	if isbreak == len(input_string)-1:
		#don't need parentheses
		return True
	else:
		return False
def derivative(inputexpression,dvar,ycount,allsteps,idvar):
	ofunction = cleanpar(inputexpression,dvar)
	##print ofunction
	allsteps.append([ycount, '\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(ofunction))+']=',ofunction])
	f = cleanpar(inputexpression,dvar)
	###print slatex(f)
	h = pulloutconstant(f,dvar,idvar)
	if h[0]!=1:
		ycount=ycount+1
		d_arr = derivative(h[1],dvar,ycount,allsteps,idvar)
		allsteps = d_arr[1]
		f = h[0]+'*('+d_arr[0]+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			for idx, i in enumerate(h):
				if idx %2==0:
					##print f, i, h
					d_arr = derivative(i,dvar,ycount,allsteps,idvar)
					allsteps=d_arr[1]
					f=f+d_arr[0]
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
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
								
								
								
								
								if h[1]=='1'+'sss':
									d_arr = derivative(h[2],dvar,ycount,allsteps,idvar)
									f='(-('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr[1]
								elif h[1]==dvar+'sss':
									d_arr = derivative(h[2],dvar,ycount,allsteps,idvar)
									f='(('+h[2]+')-('+h[1]+')*('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr[1]
								elif h[2]==dvar+'sss':
									d_arr1 = derivative(h[1],dvar,ycount,allsteps,idvar)
									f='(('+h[2]+')*('+d_arr1[0]+')-('+h[1]+'))/('+h[2]+')^2'
									allsteps=d_arr1[1]
								else:
									d_arr1 = derivative(h[1],dvar,ycount,allsteps,idvar)
									d_arr = derivative(h[2],dvar,ycount,allsteps,idvar)
									f='(('+h[2]+')*('+d_arr1[0]+')-('+h[1]+')*('+d_arr[0]+'))/('+h[2]+')^2'
									allsteps=d_arr1[1]
									allsteps=d_arr[1]
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if product Rule
									ycount =ycount+1
									d_arr = derivative(h[1],dvar,ycount,allsteps,idvar)
									allsteps=d_arr[1]
									d_arr0 = derivative(h[0],dvar,ycount,allsteps,idvar)
									allsteps=d_arr0[1]
									f='('+h[0]+')*('+d_arr[0]+')+('+h[1]+')*('+d_arr0[0]+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										d_arr = derivative(h[2],dvar,ycount,allsteps,idvar)
										
										inside_derivative = d_arr[0]
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												allsteps=d_arr[1]
												if inside_derivative==int(inside_derivative):
													f='('+h[1]+')*'+str(int(inside_derivative))
												else:
													f='('+h[1]+')*'+str(float(inside_derivative))
										except:
											allsteps=d_arr[1]
											if inside_derivative.find('+',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											else:
												f = '('+h[1]+')*'+inside_derivative
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											d_arr = derivative(h[1],dvar,ycount,allsteps,idvar)
											allsteps=d_arr[1]
											f = d_arr[0]
										else:
											f = 'IDK'
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	return [f,allsteps]

def fullderivative(inputexpression,dvar,ycount,idvar):
	f = cleanpar(inputexpression,dvar)
	nopart = inputexpression
	badword = 0
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		nopart=nopart.replace(sstr,'')
		if dvar.find(sstr)>-1:
			badword = 1
	if nopart.find(dvar)==-1 and nopart.find(idvar)==-1:
		if badword==0:
			return '0'
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar)

	if h[0]!=1:
		ycount=ycount+1
		f = h[0]+'*('+fullderivative(h[1],dvar,ycount,idvar)+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			for idx, i in enumerate(h):
				if idx %2==0:
					##print f, i, h
					f=f+fullderivative(i,dvar,ycount,idvar)
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
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
									f='(-('+fullderivative(h[2],dvar,ycount,idvar)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount,idvar)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount,idvar)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+fullderivative(h[1],dvar,ycount,idvar)+')-('+h[1]+')*('+fullderivative(h[2],dvar,ycount,idvar)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f='('+h[0]+')*('+fullderivative(h[1],dvar,ycount,idvar)+')+('+h[1]+')*('+fullderivative(h[0],dvar,ycount,idvar)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										inside_derivative = fullderivative(h[2],dvar,ycount,idvar)
										try:
											if float(inside_derivative)==1:
												f=h[1]
											elif float(inside_derivative)==0:
												f='0'
											else:
												inside_derivative=float(inside_derivative)
												if inside_derivative==int(inside_derivative):
													f='('+h[1]+')*'+str(int(inside_derivative))
												else:
													f='('+h[1]+')*'+str(float(inside_derivative))
										except:
											if inside_derivative.find('+',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											elif inside_derivative.find('-',0)>-1:
												f = '('+h[1]+')*('+inside_derivative+')'
											else:
												f = '('+h[1]+')*'+inside_derivative
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											d_arr = fullderivative(h[1],dvar,ycount,idvar)
											f = d_arr
										else:
											f = 'IDK'
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	#print f
	#print myslatex(sympy.sympify(cleanpar(f,dvar)))
	return cleanpar(f,dvar)
def laststepderivative(inputexpression,dvar,ycount,idvar):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar)
	if h[0]!=1:
		f = myslatex(sympy.sympify(h[0]))+'*(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[1],dvar,0,idvar)))+'})'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			colors = ['red','blue','magenta','red','blue','magenta','black']
			n_c = -1
			for idx, i in enumerate(h):
				if idx %2==0:
					n_c=n_c+1
					if n_c >= len(colors):
						n_c=len(colors)-1
					##print f, i, h
					f=f+'\mathcolor{'+colors[n_c]+'}{'+myslatex(sympy.sympify(fullderivative(i,dvar,0,idvar)))+'}'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
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
								if h[1]=='1'+'sss':
									f='\\frac{-(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[2],dvar,0,idvar)))+'})}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								elif h[1]==dvar+'sss':
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')-('+myslatex(sympy.sympify(h[1]))+')*(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[2],dvar,0,idvar)))+'})}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								elif h[2]==dvar+'sss':
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')*(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[1],dvar,0,idvar)))+'})-('+myslatex(sympy.sympify(h[1]))+')}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								else:
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')*(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[1],dvar,0,idvar)))+'})-('+myslatex(sympy.sympify(h[1]))+')*(\mathcolor{blue}{'+myslatex(sympy.sympify(fullderivative(h[2],dvar,0,idvar)))+'})}{('+myslatex(sympy.sympify(h[2]))+')^2}'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if porduct Rule
									ycount =ycount+1
									f0 = myslatex(sympy.sympify(h[0]))
									f1 = '\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[1],dvar,0,idvar)))+'}'
									f2 = myslatex(sympy.sympify(h[1]))
									f3 = '\mathcolor{blue}{'+myslatex(sympy.sympify(fullderivative(h[0],dvar,0,idvar)))+'}'
									if needspar(f0):
										f0 = '('+f0+')'
									if needspar(f1):
										f1 = '('+f1+')'
									if needspar(f2):
										f2 = '('+f2+')'
									if needspar(f3):
										f3 = '('+f3+')'

										
									f=f0+'*'+f1+'+'+f2+'*'+f3
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										
										f='\\left('+myslatex(sympy.sympify(h[1]))+'\\right)'+'*(\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[2],dvar,0,idvar)))+'})'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											f = '\mathcolor{red}{'+myslatex(sympy.sympify(fullderivative(h[1],dvar,0,idvar)))+'}'
										else:
											f = h[1]
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return f

def onestepderivative(inputexpression,dvar,ycount,idvar):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar)
	if h[0]!=1:
		f = myslatex(sympy.sympify(h[0]))+'*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[1]))+']}'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			colors = ['red','blue','magenta','red','blue','magenta','black']
			n_c = -1
			for idx, i in enumerate(h):
				if idx %2==0:
					n_c =n_c+1
					if n_c >= len(colors):
						n_c=len(colors)-1
					##print f, i, h
					f=f+'\\mathcolor{'+colors[n_c]+'}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(i))+']}'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
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
								if h[1]=='1'+'sss':
									f='\\frac{-'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[2]))+']}}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								elif h[1]==dvar+'sss':
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')-('+myslatex(sympy.sympify(h[1]))+')*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[2]))+']}}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								elif h[2]==dvar+'sss':
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[1]))+']}-('+myslatex(sympy.sympify(h[1]))+')}{('+myslatex(sympy.sympify(h[2]))+')^2}'
								else:
									f='\\frac{('+myslatex(sympy.sympify(h[2]))+')*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[1]))+']}-('+myslatex(sympy.sympify(h[1]))+')*'+'\\mathcolor{blue}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[2]))+']}}{('+myslatex(sympy.sympify(h[2]))+')^2}'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									#Here if product Rule
									ycount =ycount+1
									f='\\left('+myslatex(sympy.sympify(h[0]))+'\\right)'+'*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[1]))+']}+\\left('+myslatex(sympy.sympify(h[1]))+'\\right)*'+'\\mathcolor{blue}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[0]))+']}'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										#Here if chain rule works
										ycount =ycount+1
										
										f='\\left('+myslatex(sympy.sympify(h[1]))+'\\right)'+'*'+'\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[2]))+']}'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											ycount =ycount+1
											f = '\\mathcolor{red}{\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(h[1]))+']}'
										else:
											f = h[1]
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return f

def audioonestep(inputexpression,dvar,ycount,idvar):
	f = cleanpar(inputexpression,dvar)
	##print slatex(f)
	h = pulloutconstant(f,dvar,idvar)
	if h[0]!=1:
		audio = h[len(h)-1]
		f = h[0]+'*('+'\\frac{d}{d'+dvar+'}('+h[1]+'))'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			audio = 'Use the sum rule and find the derivative of each term separately.'
			#Here if can use sum rule
			ycount =ycount+1
			f = ''
			##print h
			for idx, i in enumerate(h):
				if idx %2==0:
					##print f, i, h
					f=f+'\\frac{d}{d'+dvar+'}('+i+')'
				else:
					if i==0:
						f=f+'+'
					else:
						f=f+'-'
		else:
			#Here if cannot use sum rule
			h = powerrule(f,dvar,idvar)
			if h[0]:
				audio = h[len(h)-1]
				#Here if can use power rule
				f= h[1]
			else:
				#Here if cannot use power rule
				f = h[1]
				h = expologrule(f,dvar)
				if h[0]:
					audio = h[len(h)-1]
					f=h[1]
				else:
					f = h[1]
					h = trigrule(f,dvar)
					if h[0]:
						audio = h[len(h)-1]
						f=h[1]
					else:
						f = h[1]
						h = inversetrigrule(f,dvar)
						if h[0]:
							audio = h[len(h)-1]
							f=h[1]
						else:
							f = h[1]
							h = quorule(f,dvar)
							
							if h[0]:
								audio = h[len(h)-1]
								#Here if quotient rule applied
								ycount=ycount+1
								if h[1]=='1':
									f='(-('+'\\frac{d}{d'+dvar+'}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+'\\frac{d}{d'+dvar+'}('+h[2]+')'+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+'\\frac{d}{d'+dvar+'}('+h[1]+')'+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+'\\frac{d}{d'+dvar+'}('+h[1]+')'+')-('+h[1]+')*('+'\\frac{d}{d'+dvar+'}('+h[2]+')'+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									audio = h[len(h)-1]
									#Here if porduct Rule
									ycount =ycount+1
									f=h[0]+'*('+'\\frac{d}{d'+dvar+'}('+h[1]+')'+')+'+h[1]+'*('+'\\frac{d}{d'+dvar+'}('+h[0]+')'+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar,idvar)
									if h[0]:
										audio = h[len(h)-1]
										#Here if chain rule works
										ycount =ycount+1
										
										f=h[1]+'*'+'\\frac{d}{d'+dvar+'}('+h[2]+')'
									else:
										#Here if chain rule fails
										#print "no Derivative", h[1]
										f = h[1]
										h = othertricks(f,dvar)
										if h[0]:
											audio = "Apply the special rule!"
											ycount =ycount+1
											f = '\\frac{d}{d'+dvar+'}('+myslatex(sympy.sympify(h[1]))+')'
										else:
											audio = "I don't know what to do"
											f = h[1]
	##print f
	##print myslatex(sympy.sympify(post_clean(f)))
	#tret = myslatex(sympy.sympify(post_clean(f)))
	##print ycount, cleanpar(f,dvar)
	return audio




def allof(show_all):
	mystr = ''
	for i in show_all:
		mystr=mystr+i
	return mystr

def solve_steps(allsteps,solveid,show_children,dvar,show_all,audio_file,all_ordered,previous_stuff,idvar):
	##print solveid, 'xxxxx'
	#print solveid
	#print allsteps
	colors = ['red','blue','magenta','red','blue','magenta','black']
	#print time.time()
	for idx,i in enumerate(show_all):
		for ii in colors:
			i=i.replace('athcolor{'+ii+'}','athcolor{black}')
		show_all[idx]=i
	if allsteps[0][3]=='solved':
		show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+myslatex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0,idvar)))+'$'
		audio_file.append(audioonestep(allsteps[0][2],dvar,0,idvar))
		#print allof(show_all)+'\\newpage '
		all_ordered.append(allof(show_all)+'\\newpage ')
	if allsteps[solveid][3]!='solved':
		tstring = '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0,idvar)+'$'
		if show_all[solveid]!= tstring:
			for ii in colors:
				tstring=tstring.replace('athcolor{'+ii+'}','athcolor{black}')
			if show_all[solveid]!= tstring:
				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0,idvar)+'$'
				audio_file.append(audioonestep(allsteps[solveid][2],dvar,0,idvar))
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
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
		##print 'h'
		n_c=-1
		
		for idx,i in enumerate(allsteps[rangemin:rangemax]):
			if i[0]==level+1:
				n_c=n_c+1
				if n_c < len(colors):
					the_color = colors[n_c]
				else:
					the_color = 'black'
				if i[3]=="solved":
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
					audio_file.append('We need to find the derivative of this part.')
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+myslatex(sympy.sympify(fullderivative(i[2],dvar,0,idvar),evaluate=False))+'$'
					audio_file.append(audioonestep(i[2],dvar,0,idvar))
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					if myslatex(sympy.sympify(fullderivative(i[2],dvar,0,idvar),evaluate=False)).replace(' ','') != myslatex(sympy.sympify(fullderivative(i[2],dvar,0,idvar),evaluate=True)).replace(' ',''):
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+myslatex(sympy.sympify(fullderivative(i[2],dvar,0,idvar),evaluate=True))+'$'
						audio_file.append('Simplify.')
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
				else:
					show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
					audio_file.append('We need to find the derivative of this part.')
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')
					
				
		solve_steps(allsteps,allsteps[solveid][5][0],1,dvar,show_all,audio_file,all_ordered,previous_stuff,idvar)


	else:
		##print 'j'
		if allsteps[solveid][3]!="solved":
			if show_children==1:
				n_c = -1
				for idx,i in enumerate(allsteps[rangemin:rangemax]):
					if i[0]==level+1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}$'
						audio_file.append('We need to find the derivative of this part.')
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
						show_all[idx+rangemin]= '\\newline $\hspace*{'+str(i[0])+'em} \mathcolor{'+the_color+'}{'+i[1]+'}'+myslatex(sympy.sympify(fullderivative(i[2],dvar,0,idvar),evaluate=True))+'$'
						audio_file.append(audioonestep(i[2],dvar,0,idvar))
						#print allof(show_all)+'\\newpage '
						all_ordered.append(allof(show_all)+'\\newpage ')
			allsteps[solveid][3]="solved"
			n_c=-1
			needtorecolor=False
			for idx,i in enumerate(allsteps[rangemin:rangemax]):
				if i[0]==level+1:
					n_c=n_c+1
					if n_c < len(colors):
						the_color = colors[n_c]
					else:
						the_color = 'black'
					if show_all[idx+rangemin].find('athcolor{'+the_color+'}',0)== -1:
						needtorecolor=True
			if needtorecolor:
				n_c=-1
				for idx,i in enumerate(allsteps[rangemin:rangemax]):
					if i[0]==level+1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{black}','athcolor{'+the_color+'}')

						for ii in colors:
							show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
						show_all[idx+rangemin]='\mathcolor{'+the_color+'}{'+show_all[idx+rangemin]+'}'
						#print "here",solveid, show_all[idx+rangemin]

				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+onestepderivative(allsteps[solveid][2],dvar,0,idvar)+'$'
				audio_file.append("We're going to substitute this in.")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
			
			show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+laststepderivative(allsteps[solveid][2],dvar,0,idvar)+'$'
			audio_file.append("Combine those steps to get this.")
			#print allof(show_all)+'\\newpage '
			all_ordered.append(allof(show_all)+'\\newpage ')

			for idx,i in enumerate(show_all):
				for ii in colors:
					i=i.replace('athcolor{'+ii+'}','athcolor{black}')
				show_all[idx]=i
			#n_c=-1
			#for idx,i in enumerate(allsteps[rangemin:rangemax]):
			#	if i[0]==level+1:
			#		n_c=n_c+1
			#		if n_c < len(colors):
			#			the_color = colors[n_c]
			#		else:
			#			the_color = 'black'
			#		show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{black}','athcolor{'+the_color+'}')

			#		for ii in colors:
			#			show_all[idx+rangemin]=show_all[idx+rangemin].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
			#		show_all[idx+rangemin]='\mathcolor{'+the_color+'}{'+show_all[idx+rangemin]+'}'

			if laststepderivative(allsteps[solveid][2],dvar,0,idvar).replace(' ','') != myslatex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0,idvar),evaluate=True)).replace(' ',''):
				show_all[solveid]= '\\newline $\hspace*{'+str(allsteps[solveid][0])+'em} '+allsteps[solveid][1]+myslatex(sympy.sympify(fullderivative(allsteps[solveid][2],dvar,0,idvar),evaluate=True))+'$'
				audio_file.append("Simplify.")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')

		if allsteps[solveid][6]!='':
			solve_steps(allsteps,allsteps[solveid][6],1,dvar,show_all,audio_file,all_ordered,previous_stuff,idvar)
		else:
			if allsteps[solveid][7]!=0:
				if solveid !=0:
					solve_steps(allsteps,allsteps[solveid][7],0,dvar,show_all,audio_file,all_ordered,previous_stuff,idvar)
			else:
				n_c=-1
				for idx,i in enumerate(allsteps):
					if i[0]==1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx]=show_all[idx].replace('athcolor{black}','athcolor{'+the_color+'}')

						for ii in colors:
							show_all[idx]=show_all[idx].replace('athcolor{'+ii+'}','athcolor{'+the_color+'}')
						show_all[idx]='\mathcolor{'+the_color+'}{'+show_all[idx]+'}'
						#print "here",solveid, show_all[idx+rangemin]

				show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+onestepderivative(allsteps[0][2],dvar,0,idvar)+'$'
				audio_file.append("We're going to substitute this in.")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')

				show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+laststepderivative(allsteps[0][2],dvar,0,idvar)+'$'
				audio_file.append("And finally we arrive at our derivative!")
				#print allof(show_all)+'\\newpage '
				all_ordered.append(allof(show_all)+'\\newpage ')
				n_c=-1
				for idx,i in enumerate(allsteps):
					if i[0]==1:
						n_c=n_c+1
						if n_c < len(colors):
							the_color = colors[n_c]
						else:
							the_color = 'black'
						show_all[idx]=show_all[idx].replace('athcolor{black}','athcolor{black}')

						for ii in colors:
							show_all[idx]=show_all[idx].replace('athcolor{'+ii+'}','athcolor{black}')
						show_all[idx]='\mathcolor{black}{'+show_all[idx]+'}'
				if laststepderivative(allsteps[0][2],dvar,0,idvar).replace(' ','') != myslatex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0,idvar),evaluate=True)).replace(' ',''):
					show_all[0]= '\\newline $\hspace*{'+str(allsteps[0][0])+'em} '+allsteps[0][1]+myslatex(sympy.sympify(fullderivative(allsteps[0][2],dvar,0,idvar),evaluate=True))+'$'
					audio_file.append("Simplify.")
					#print allof(show_all)+'\\newpage '
					all_ordered.append(allof(show_all)+'\\newpage ')



def run_it(inputexpression,hashprefix,dvar,idvar):
	allsteps=[]
	show_all = []
	audio_file = ["We want to find the derivative of this function"]
	all_ordered = []
	previous_stuff = ''
	ycount = 0
	stopnow = 0
	nopart = inputexpression
	for sstr in ['sin','cos','log','tan','cot','sec','csc','cot','sqrt','arc','ln']:
		nopart=nopart.replace(sstr,'')
	if nopart.find(dvar) ==-1 and nopart.find(idvar)==-1:
		os.system('./testlm2p.py -f "\$\\frac{d}{d'+dvar+'}['+myslatex(sympy.sympify(cleanpar(inputexpression,dvar)))+']=0\$" -o "images/new/'+hashprefix+'ex0.png"')
		return [1,myslatex(sympy.sympify('0')),myslatex(sympy.sympify(cleanpar(inputexpression,dvar)))]
	else:
		#print time.time(), "A"
		the_derivative_arr = derivative(inputexpression,dvar,0,allsteps,idvar)
		#print time.time(), 'B'
		the_derivative = the_derivative_arr[0]
		allsteps=the_derivative_arr[1]
		#print myslatex(sympy.sympify(the_derivative))
		for i in allsteps:
			##print i
			my_str = ''
			for ii in range(0,i[0]):
				my_str=my_str+'   '

		for idx,i in enumerate(allsteps):
			if onestepderivative(i[2],dvar,0,idvar).find('\\frac{d}{d'+dvar+'}')==-1:
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



		#print time.time(), 'C'
		numruns = 0
		##print "let's see"
		for i in allsteps:
			show_all.append(' \\newline ')

		previous_stuff = '$'+allsteps[0][1]+'$\\newline $'
		show_all[0]='$'+allsteps[0][1]+'$'
		#print allof(show_all)+'\\newpage '
		#print time.time(), 'D'
		all_ordered.append(allof(show_all)+'\\newpage ')
		#print time.time(), 'E'
		##print '$'+allsteps[0][1]+'$\\newpage '
		

		solve_steps(allsteps,0,1,dvar,show_all,audio_file,all_ordered,previous_stuff,idvar)
		#print time.time(), 'F'

		#print audio_file
		##print all_ordered
		##print './testlm2p.py -f "'+all_ordered[0]+'" -o "ex1"'
		#myteststr = '$\\hspace*{0em} d[2 \\left(2 x + 2\\right)^{5} + \\log{\\left (x \\right )}]=x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x+x$'
		#os.system('./testlm2p.py -f "'+myteststr+'" -o "ex'+str(111)+'"')
		#return_str = ''
		#print "working"
		#print allsteps
		#print asdfsdh
		for i in range(0,len(all_ordered)):
			#print time.time()
			#print './testlm2p.py -f "'+all_ordered[i]+'" -o "images/ex'+str(i)+'"\n'
			if all_ordered[i][0:9]=='\\newline ':
				all_ordered[i]=all_ordered[i][9:]
			os.system('./testlm2p.py -f "'+all_ordered[i]+'" -o "images/new/'+hashprefix+'ex'+str(i)+'.png"')
			#print all_ordered[i]
			#os.system('espeak "'+audio_file[i]+'" --stdout > images/audio/'+hashprefix+'ex'+str(i)+'.mp3')
			#print audio_file[i]
		##print previous_stuff
		#print time.time(), 'G'
		return [len(all_ordered),myslatex(sympy.sympify(fullderivative(inputexpression,dvar,0,idvar))),myslatex(sympy.sympify(cleanpar(inputexpression,dvar))),audio_file]
def index_fn(inputexpression,dvar,idvar):
	return [myslatex(sympy.sympify(fullderivative(inputexpression,dvar,0,idvar))),myslatex(sympy.sympify(cleanpar(inputexpression,dvar)))]


#print myslatex(sympy.sympify(cleanpar('x^(-2)','x')))
#print index_fn('x^(-2)','x')[1]
#import uuid
#print run_it('x*y','asdfsdf','x','y')[1]

#print sympy.sympify('x^2+1').subs('x',2)
#from sympy import Symbol
#x=Symbol('x',commutative=False)
#inputstr = 'x*1/x+log(x)*1'

#from sympy.core.sympify import kernS
#print myslatex(sympy.sympify(inputstr,evaluate=True))
#print myslatex(sympy.sympify(inputstr,evaluate=False))
#print myslatex(inputstr)
#print 
#if myslatex(sympy.sympify(inputstr,evaluate=True))==myslatex(sympy.sympify(inputstr,evaluate=False)):
#	print "True"
#else:
#	print "False"

