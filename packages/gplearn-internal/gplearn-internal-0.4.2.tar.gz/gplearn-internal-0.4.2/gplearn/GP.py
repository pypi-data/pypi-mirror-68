#coding: utf-8
import numpy as np
from gplearn.genetic import SymbolicRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils.random import check_random_state

from statistics import mean

import pickle #for savel/load to/from file

import os, mmap
import csv

"""
	GENETIC PROGRAMMING
	By R.S. 2018/03

	+20 april, add latex generator

"""
__version__ = "1.7.08b"


from translateFn import translateFunctions
def toGoodRepresentationFunc(XnMax,program):
	varia={}
	for i in range(0,XnMax+1):
		varia["X"+str(i)] = "X"+str(i)
	tsf = translateFunctions(program,varia)
	return tsf.getter()


def traduct(X,program = "y=sub(mul(add(div(div(X0, X0), sub(0.112, 0.165)), -0.785), div(mul(X0, div(X0, -0.507)), mul(X0, X0))), mul(mul(add(-0.491, 0.352), div(sub(-0.410, X0), div(0.165, div(0.501, X0)))), sub(sub(sub(X0, X0), div(-0.108, -0.261)), add(div(-0.013, sub(sub(X0, X0), 0.417)), div(X0, X0)))))"):
	y=reinitrel(X,program)
	#exec(program)
	print("y=",y)
	exec("result="+y)
	return result

import random
from pytexit import py2tex
def to_latex(XnMax=1,program="y=sub(mul(add(div(div(X0, X0), sub(0.112, 0.165)), -0.785), div(mul(X0, div(X0, -0.507)), mul(X0, X0))), mul(mul(add(-0.491, 0.352), div(sub(-0.410, X0), div(0.165, div(0.501, X0)))), sub(sub(sub(X0, X0), div(-0.108, -0.261)), add(div(-0.013, sub(sub(X0, X0), 0.417)), div(X0, X0)))))"):
	for i in range(0,XnMax+1):
		exec("X"+str(i)+"="+"'X"+str(i)+"'")
	exec(program)
	print(program+"  <--- exec")
	RESULT = py2tex(program)
	return RESULT

import os, requests 
def to_texpng(file="tmp.png" ,nX=1 ,program="y=sub(mul(add(div(div(X0, X0), sub(0.112, 0.165)), -0.785), div(mul(X0, div(X0, -0.507)), mul(X0, X0))), mul(mul(add(-0.491, 0.352), div(sub(-0.410, X0), div(0.165, div(0.501, X0)))), sub(sub(sub(X0, X0), div(-0.108, -0.261)), add(div(-0.013, sub(sub(X0, X0), 0.417)), div(X0, X0)))))"):
	formula = to_latex(nX,program)
	formula = formula.replace('\n', ' ')
	r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{780}} {formula}'.format(formula=formula))
	#print('http://latex.codecogs.com/gif.latex?%5Cdpi%7B300%7D%20%5Cbegin%7Bbmatrix%7D%202%20%26%200%20%5C%5C%200%20%26%202%20%5C%5C%20%5Cend%7Bbmatrix%7D')
	#print(r.url)
	f = open(file, 'w+b')
	f.write(r.content)
	f.close()

def force_totex(filepath,program):
	program = toGoodRepresentationFunc(program.count("X"),program)
	formula = py2tex(program)
	formula = formula.replace('\n', ' ')
	r = requests.get( 'http://latex.codecogs.com/png.latex?\dpi{{780}} {formula}'.format(formula=formula))
	f = open(filepath, 'w+b')
	f.write(r.content)
	f.close()
	
from math import *
from operator import inv, neg
def reinitrel(X,program):

	for i in range(0,len(X)):
		exec("X"+str(i)+"="+str(X[i]*1.0))	
	y = str(program)
	return y

def cbrt(a):
	return "cbrt("+str(a)+")"

def hypot(a,b):
	return "hypot("+str(a)+", "+str(b)+")"

def sigmoid(a):
	return "sigmoid("+str(a)+")"

def ceil(a):
	return "ceil("+str(a)+")"

def fabs(a):
	return "fabs("+str(a)+")"

def floor(a):
	return "floor("+str(a)+")"

def trunc(a):
	return "trunc("+str(a)+")"


def sub(a,b):
	return "("+str(a)+"-"+str(b)+")"

def add(a,b):
	return "("+str(a)+"+"+str(b)+")"

def mul(a,b):
	return "("+str(a)+"*"+str(b)+")"

def div(a,b):
	return "("+str(a)+"/"+str(b)+")"
#'sqrt','log','abs','neg','inv','max','min','sin','cos','tan'
def sqrt(a):
	return "sqrt("+str(a)+")"

def log(a):
	return "log("+str(a)+")"

def abs(a):
	return "abs("+str(a)+")"

def neg(a):
	return "neg("+str(a)+")"

def inv(a):
	return "inv("+str(a)+")"

def max(*args):
	return "max("+",".join(map(str,args))+")"

def min(*args):
	return "min("+",".join(map(str,args))+")"

def sin(a):
	return "sin("+str(a)+")"

def cos(a):
	return "cos("+str(a)+")"

def tan(a):
	return "tan("+str(a)+")"

def modulox(a,b):
	return "modulox("+str(a)+","+str(b)+")"
def xor(a,b):
	return "xor("+str(a)+","+str(b)+")"


def string_to_float(x):
    z = ""
    for i in x:
        if i in "0123456789.":
            if i == ".":
                if z.count(i)==0:
                    z=z+i
            else:
                z=z+i
    if z=="": z="0.00"
    return float(z)

def string_to_int(x):
    z = ""
    for i in x:
        if i in "0123456789":
            z=z+i
    if z=="": z="0"
    return int(z)

class dataset(object):
	def __init__(self):
		self.x,self.y = [],[]
	def add(self,x,y):
		self.x.append(x)
		self.y.append(y)
	def get(self):
		return self.x,self.y
	def new(self):
		self.x,self.y = [],[]



class GP_SymReg(object):
	def load_csv(self,filepath="test.csv",name_y='y'):
		DATA = []
		with open(filepath) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				DATA.append(row)
		maxmult = 0
		for i in DATA[0].keys():
			if "x" in i:
				if string_to_int(i)>maxmult:
					maxmult = string_to_int(i)
		keyx = []
		for i in range(0,maxmult+1):
			keyx.append("x"+str(i))

		print("Nombre de X:",maxmult+1)
		X,Y = [],[]
		for i in DATA:
			Y.append(string_to_float(i[name_y]))
			for j in keyx:
				X.append(string_to_float(i[j]))

		print("X=",X)
		print("Y=",Y)
		l = maxmult+1
		if maxmult>0:
			A,B = len(X)/l,l
		else:
			A,B = len(X),-1
		try:
			self.x_ = np.array(list(map(int,X))).reshape(A,B)
		except TypeError:
			A,B = int(A),int(B)
			X = list(map(int, X))
			self.x_ = np.array(X).reshape(A,B)

		self.y_ = np.array(Y)
		print("x_=",self.x_)
		print("y_=",self.y_)
		self.nbX = maxmult

	def formula(self,formule="x0/2.0-x1/4.0"):
		rng = check_random_state(0)
		X_ = rng.uniform(-100, 100, 100).reshape(50,2)
		for i in range(0,2):
			formule = formule.replace("x"+str(i),"X_[:,"+str(i)+"]")
		print("y_ =", formule)
		exec("y_="+formule)
		self.y_ = y_
		self.x_ = X_

	def set_x_y(self,x,y,multiple=1):
		rng = check_random_state(0)
		self.x_ = rng.uniform(-len(x), len(x), len(x)).reshape(len(x)/2,multiple)
		j=0
		for i in self.x_:
			for h in range(0,multiple):
				i[h] = x[j+h]
			j+=1
		self.x_ = np.array(self.x_).reshape(len(x)/2,multiple)
		self.y_ = np.array(y)
		print(self.x_)
		print(self.y_)

	def __init__(self,population_size=5000,
					generations=20, stopping_criteria=0.01,
					function_set=('add', 'sub', 'mul', 'div'),
					warm_start=False,
					p_crossover=0.7, p_subtree_mutation=0.1,
					p_hoist_mutation=0.05, p_point_mutation=0.1,
					max_samples=0.9, verbose=1,
					parsimony_coefficient=0.01, random_state=0, n_jobs=1, warmreduce=False, pkldump=False):
		#self.BESTOF = 0
		self.warmreduce = warmreduce
		self.pkldump = pkldump
		self.warm_start = warm_start
		self.y_ = None
		#('add', 'sub', 'mul', 'div','sqrt','log','abs','neg','sin','cos','tan')
		if function_set == "logic":
			function_set = ("and","or","xor")
		if function_set == "all":
			function_set = ('add', 'sub', 'mul', 'div','sqrt','log','abs','neg','inv','max','min','sin','cos','tan','sigmoid','ceil','fabs','floor','trunc','cbrt','hypot',"modulox")
		self.est_gp = SymbolicRegressor(population_size=population_size,
						generations=generations, stopping_criteria=stopping_criteria,
						function_set=function_set,
						warm_start=warm_start,
						p_crossover=p_crossover, p_subtree_mutation=p_subtree_mutation,
						p_hoist_mutation=p_hoist_mutation, p_point_mutation=p_point_mutation,
						max_samples=max_samples, verbose=verbose,
						parsimony_coefficient=parsimony_coefficient, random_state=random_state,n_jobs=n_jobs)


	def learn(self):
		if self.pkldump:
			with open(self.filepkl, 'rb') as f:
				self.est_gp = pickle.load(f)

		print("ENTRAINEMENT...")
		self.est_gp.fit(self.x_,self.y_)
		print("ENTRAINEMENT TERMINE!")
		if self.warmreduce:
			print("Reduction de l'espace du fichier...")
			delattr(self.est_gp,'_programs')
			print("OK.")

		if self.warm_start:
			if not self.pkldump:
				with open(self.filepkl, 'wb') as f:
					pickle.dump(self.est_gp, f)


		#self.BESTOF = self.est_gp.BESTOF
		#print("BESTOF:" , self.BESTOF)


	def predict(self,X=[16,19],scale=1.):
		u = []
		for i in range(0,len(X)):
			u.append(np.arange(X[i], X[i]+1, scale))
		u = tuple(u)
		self.y_gp = self.est_gp.predict(np.c_[u]).reshape(u[0].shape)
		return mean(self.y_gp)

	def save(self,filepath="temp.bin"):
		f=open(filepath,'w+b')
		f.write(pickle.dumps(self.est_gp))
		f.close()
		print("MODEL SAVE!("+filepath+")")

	def load(self,filepath="temp.bin"):
		l = os.stat(filepath).st_size
		with open(filepath, 'rb') as f:
			mm = mmap.mmap(f.fileno(),0,prot=mmap.PROT_READ)
			self.est_gp = pickle.loads(mm.read(l))
		print("MODEL LOAD!("+filepath+")")

	def get_program(self):
		return self.est_gp._program

	def print_program(self):
		print(toGoodRepresentationFunc(self.est_gp._program.count("X"),self.est_gp._program))

	def get_png_program(self,file_,nX=1):
		to_texpng(file_,nX,str(self.est_gp._program))

	def determination(self):
		x,y=[],[]
		x=range(-100,100+1)
		for i in x:
			y.append(f(i))
		self.set_x_y(x,y)
		print("SET DETERMINATION X(-100 to 100) Y(from f(x)).")

	def approx_stat(self,x):
		a,b=self.predict(X=x,scale=1),self.predict(X=x,scale=1/1000.)
		return mean([a,b])

	def make_from_csv_for_corrector(self,filepath="newcorrect.csv"):
		f = open(filepath,"w+b")
		f.write("x0,")
		f.write("y\n")	
		j=0	
		for x in self.x_.tolist():
			xprime = [self.approx_stat(x),self.y_.tolist()[j]]
			f.write(str(xprime).replace('[','').replace(']','')+"\n")
			print("MAKE CORRECTOR CSV:",(j/(len(self.y_.tolist())*1.0)),"%")
			j+=1
		f.close()

	def define_filepkl(self,filepkl):
		self.filepkl = filepkl


def round_predict(FILEg,FILEh,x=[]):
	g = GP_SymReg()
	h = GP_SymReg()
	g.load(FILEg)
	h.load(FILEh)
	return round(h.predict([g.predict(x,1)],1/1000.))

def GP_SR_CORR(FILEg,FILEh,X=[]):
	g = GP_SymReg()
	h = GP_SymReg()
	g.load(FILEg)
	h.load(FILEh)
	c = g.approx_stat([h.approx_stat(X)])
	d = h.approx_stat(X)
	z = (c+(c-int(d)+(d-int(c))*3.0))
	return z

def txtprime_to_csv(filepath="1-2088.txt"):
	f = open(filepath,'r+b')
	BUFF = f.read()
	f.close()
	f=open(filepath.split(".")[0]+".csv",'w+b')
	f.write("x0,y\n")
	j=0
	for i in BUFF.split("\n"):
		j+=1
		print(j/(len(BUFF.split("\n"))*1.0),"%")
		f.write(str(j)+","+str(i)+"\n")
	f.close()

import math
def verify_prime(x):
	r = 2 + ( 2 * ( math.factorial(x-1) ) % x )
	if r == 2:
		return False
	if r == n:
		return True

def verify_wilson(p):
	return math.factorial(p-1)+1
