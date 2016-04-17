import sympy
from sympy import *
def checksame(guess,checkfn,dvar):
	notsame = 0
	if sympy.sympify(guess).equals(sympy.sympify(checkfn)):
		return True
	else:
		return False

#print sympy.sympify('log(x)').subs('x',0).evalf()
#print checksame('ln(sin(x))+1','ln(sin(x))+cos(x)^2+sin(x)^2','x')