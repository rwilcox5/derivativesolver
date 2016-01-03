
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
inputexpression = 'xx^4(x+1)'
dvar = 'x'
ycount = 0
stopnow = 0
def slatex(f):
	return sympy.latex(sympy.sympify(post_clean(f)))
def inversetrigrule(inputexpression,dvar):
	return [False,inputexpression]

def derivative(inputexpression,dvar):
	global ycount, stopnow
	f = cleanpar(inputexpression,dvar)
	#print slatex(f)
	h = pulloutconstant(f,dvar)
	if h[0]!=1:
		f = h[0]+'*('+derivative(h[1],dvar)+')'
	else:
		#Here if cannot pull out a constant
		f=h[1]
		h = sumrule(f,[],dvar)
		if len(h)>1:
			#Here if can use sum rule
			f = ''
			for idx, i in enumerate(h):
				if idx %2==0:
					if derivative(i,dvar)==i:
						f=f+i
					else:
						#print f, derivative(i,dvar), i
						f=f+derivative(i,dvar)
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
								if h[1]=='1':
									f='(-('+derivative(h[2],dvar)+'))/('+h[2]+')^2'
								elif h[1]==dvar:
									f='(('+h[2]+')-('+h[1]+')*('+derivative(h[2],dvar)+'))/('+h[2]+')^2'
								elif h[2]==dvar:
									f='(('+h[2]+')*('+derivative(h[1],dvar)+')-('+h[1]+'))/('+h[2]+')^2'
								else:
									f='(('+h[2]+')*('+derivative(h[1],dvar)+')-('+h[1]+')*('+derivative(h[2],dvar)+'))/('+h[2]+')^2'
							else:
								#Here if no quotient rule applied
								f=h[1]
								h = productrule(f,[],dvar)
								if len(h)>1:
									f=h[0]+'*('+derivative(h[1],dvar)+')+'+h[1]+'*('+derivative(h[0],dvar)+')'
								else:
									#Here if product rule fails
									f = h[0]
									h = chainrule(f,dvar)
									if h[0]:
										inside_derivative = derivative(h[2],dvar)
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
										f = h[1]
	#print f
	#print sympy.latex(sympy.sympify(post_clean(f)))
	#tret = sympy.latex(sympy.sympify(post_clean(f)))
	return cleanpar(f,dvar)

the_derivative = derivative(inputexpression,dvar)
print sympy.latex(sympy.sympify(the_derivative))


print asdfsdf
def cleanconstant(inputexpression,dvar):
	cleaned = cleanpar(inputexpression,dvar)
	constanted = pulloutconstant(cleaned[0],cleaned[1])
	#print cleaned[0]
	#print pulloutconstant(cleaned[0],cleaned[1])
	return constanted

constanted = cleanconstant(inputexpression,dvar)
if constanted[0]:
	print constanted[1]
	constanted = cleanconstant(constanted[2],dvar)
	all_terms = sumrule(constanted[1],[],dvar)
else:
	all_terms = sumrule(constanted[1],[],dvar)
print all_terms
constanted = cleanconstant(all_terms[0],dvar)
if constanted[0]:
	print constanted[1]
	constanted = cleanconstant(constanted[2],dvar)
	all_terms = productrule(constanted[1],[],dvar)
else:
	all_terms = productrule(constanted[1],[],dvar)
print all_terms

print skdlf
algarray = sumrule(cleanpar(inputexpression),[],'x')
for i in range(0,len(algarray)):
	if i%2==0:
		print algarray[i]
	if i%2==1:
		if algarray[i]==0:
			print '+',
		else:
			print '-',