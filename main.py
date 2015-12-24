import sumrule
import clean
from sumrule import sumrule
from clean import cleanpar



inputexpression = '(3-(1+x-(a+b))-11)'
algarray = sumrule(cleanpar(inputexpression),[])
for i in range(0,len(algarray)):
	if i%2==0:
		print algarray[i]
	if i%2==1:
		if algarray[i]==0:
			print '+',
		else:
			print '-',