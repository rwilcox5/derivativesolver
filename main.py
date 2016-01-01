import sumrule
import clean
import constantmultiple
from sumrule import sumrule
from clean import cleanpar
from constantmultiple import pulloutconstant



inputexpression = '(1/a*x((x+1)*2) (x-1)^2/x)'
cleaned = cleanpar(inputexpression,'x')
constanted = pulloutconstant(cleaned[0],cleaned[1])
if constanted[0]:
	print sumrule(constanted[2],cleaned[1])
else:
	print sumrule(constanted[1],cleaned[1])
print cleaned[0]
print pulloutconstant(cleaned[0],cleaned[1])
print skdlf
algarray = sumrule(cleanpar(inputexpression),[])
for i in range(0,len(algarray)):
	if i%2==0:
		print algarray[i]
	if i%2==1:
		if algarray[i]==0:
			print '+',
		else:
			print '-',