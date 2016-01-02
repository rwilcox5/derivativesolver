
from sumrule import sumrule
from clean import cleanpar
from constantmultiple import pulloutconstant
from productrule import productrule
from powerrule import powerrule
from chainrule import chainrule
inputexpression = '3x^2+x^1*x^4+x(x^2+1)^(2)'
dvar = 'x'
ycount = 0
stopnow = 0
def derivative(inputexpression,dvar):
	global ycount, stopnow
	f = cleanpar(inputexpression,dvar)
	#print f
	h = pulloutconstant(f,dvar)
	if h[0]==1:
		f = h[1]
	else:
		f = h[0]+'*('+derivative(h[1],dvar)+')'
	#print f, h
	h = sumrule(f,[],dvar)
	if len(h)>1:
		f = ''
		for idx, i in enumerate(h):
			if idx %2==0:
				if derivative(i,dvar)==i:
					f=f+i
				else:
					print f, derivative(i,dvar), i
					f=f+derivative(i,dvar)
			else:
				if i==0:
					f=f+'+'
				else:
					f=f+'-'
	h = productrule(f,[],dvar)
	if len(h)>1:
		if stopnow == 1:
			f = h[0]
		else:
			f=h[0]+'*('+derivative(h[1],dvar)+')+'+h[1]+'*('+derivative(h[0],dvar)+')'
			#ycount = ycount+1
			#print f, "AAA", h
			#if ycount > 10:
			#	stopnow = 1
	else:
		f = h[0]
	h = powerrule(f,dvar)
	f = h
	h = chainrule(f,dvar)
	if len(h)>1:
		if h[1]=='derivative':
			f = h[0]+'*('+derivative(h[2],dvar)+')'
		else:
			f=h
	else:
		f = h
	return f

print derivative(inputexpression,dvar)
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