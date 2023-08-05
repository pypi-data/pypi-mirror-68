#coding: utf-8
import numpy as np
from gplearn.genetic import SymbolicClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.utils.random import check_random_state

from statistics import mean

import pickle #for savel/load to/from file

import os, mmap
import csv


__version__ = "1.0.00proto"


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
	exec(program)
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



class GP_Classifier(object):
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

	def __init__(self,
					population_size=1000, 
					generations=20, 
					tournament_size=20, 
					stopping_criteria=0.0, 
					const_range=(-1.0, 1.0), 
					init_depth=(2, 6), 
					init_method='half and half', 
					function_set=('add', 'sub', 'mul', 'div'), 
					transformer='sigmoid', 
					metric='log loss', 
					parsimony_coefficient=0.001, 
					p_crossover=0.9, 
					p_subtree_mutation=0.01, 
					p_hoist_mutation=0.01, 
					p_point_mutation=0.01, 
					p_point_replace=0.05, 
					max_samples=1.0, 
					feature_names=None, 
					warm_start=False, 
					low_memory=False, 
					n_jobs=1, 
					verbose=0, 
					random_state=None):
		#self.BESTOF = 0
		self.y_ = None
		#('add', 'sub', 'mul', 'div','sqrt','log','abs','neg','sin','cos','tan')
		if function_set == "logic":
			function_set = ("and","or","xor")
		if function_set == "all":
			function_set = ('add', 'sub', 'mul', 'div','sqrt','log','abs','neg','inv','max','min','sin','cos','tan','sigmoid','ceil','fabs','floor','trunc','cbrt','hypot',"modulox")
		self.est_gp = SymbolicClassifier(population_size=population_size, generations=generations, 
			tournament_size=tournament_size, stopping_criteria=stopping_criteria, 
			const_range=const_range, init_depth=init_depth, 
			init_method=init_method, function_set=function_set, 
			transformer=transformer, metric=metric, parsimony_coefficient=parsimony_coefficient, 
			p_crossover=p_crossover, p_subtree_mutation=p_subtree_mutation, p_hoist_mutation=p_hoist_mutation, 
			p_point_mutation=p_point_mutation, p_point_replace=p_point_replace, max_samples=max_samples, feature_names=feature_names, 
			warm_start=warm_start, low_memory=low_memory, n_jobs=n_jobs, verbose=verbose, random_state=random_state)

	def learn(self):
		print("ENTRAINEMENT...")
		rng = check_random_state(0)
		perm = rng.permutation(len(self.x_))
		self.est_gp.fit(self.x_[perm],self.y_[perm])
		print("ENTRAINEMENT TERMINE!")
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
		print(self.est_gp._program)

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
