import math, scipy, random, os,sys
from collections import defaultdict
from numpy import *

def read_ratings(filename):
  prefix = os.path.abspath('..') +"/Datasets/"+ sys.argv[2]+"/"
  x=open(prefix+filename,"r")
  max1=0
  max2=0
  R= []
  for line in x:
    x=[]
    line=line.replace("\n","")
    line=line.split(",")
    #R[int(line[0])][int(line[1])]=int(line[2])
    x.append(int(line[0]))
    x.append(int(line[1]))
    x.append(int(line[2]))
    R.append(x)
    max1=max(max1,int(line[0]))
    max2=max(max2,int(line[1]))
  return R, max1,max2

class recsys_mf:
  U=[]
  V=[]
  m=0
  n=0
  k=0
  steps=100
  alpha=0.02
  beta=0.7
  iteration_data=[]

  def __init__(self, n,m, k):
    self.n=n
    self.m=m
    self.k=k
    self.U=random.rand(n+1,k)
    self.V=random.rand(m+1,k)

  def factor(self,R,R2):
    self.V=self.V.T;
    numrows = len(R)
    
    temp= range(numrows)  
    eleast=10000
    estep=0
    epoch = 0
    for step in range(self.steps):
      random.shuffle(temp)
      e=0
      iteration =1
      for x in temp:
        i=R[x][0]
        j=R[x][1]
        R_ij=R[x][2]
        error_ij =  R_ij - dot(self.U[i,:],self.V[:,j])
        t=self.U[i,:]+self.alpha*(2*error_ij*self.V[:,j].T - self.beta*self.U[i,:])
        self.V[:,j]=self.V[:,j]+self.alpha*(2*error_ij*self.U[i,:].T - self.beta*self.V[:,j])
        self.U[i,:]=t
        
        e= e+ pow(R_ij - dot(self.U[i,:],self.V[:,j]), 2)
      
      e=e/len(R)
      e=math.sqrt(e)
      if e<0.01:
        break
      self.iteration_data.append( [e, step]) 
    self.V=self.V.T

  def final_res(self):
    return self.U, self.V

  def error(self,R):
    e=0
    for x in R:
      i=x[0]
      j=x[1]
      R_ij=x[2]
      R_hat=dot(self.U[i,:],self.V.T[:,j])
      e= e+ pow(R_ij- R_hat, 2)
    e=e/len(R)
    e=math.sqrt(e)
    return e

  def save_results(self,file1):
    prefix_result = os.path.abspath('..') +"/Results/"+sys.argv[0]+"/"+sys.argv[1]+"/"
    if not os.path.exists(str(prefix_result)):
      os.makedirs(str(prefix_result))
    fd=open(prefix_result+file1+".result","w")
   
    fd.write("RMSE ="+str(instance.error(R2)))
    print instance.error(R2), sys.argv[4]
    fd.close()
    fd=open(prefix_result+file1+".iteration","w")
    for z1 in self.iteration_data:
      fd.write(str(z1[0])+", "+str(z1[1])+"\n")
    fd.close()


random.seed(int(sys.argv[4]))
files = [ "ua", "ub" ]


prefix_result = os.path.abspath('..') +"\\results\\"+sys.argv[0]+"\\"+sys.argv[1]


R,n,m=read_ratings(files[int(sys.argv[3])]+".base")  
R2,n1,m1=read_ratings(files[int(sys.argv[3])]+".test")  
instance= recsys_mf(n,m,int(sys.argv[1]))
instance.factor(R,R2)
Udash, Vdash=instance.final_res()
instance.save_results(files[int(sys.argv[3])])




