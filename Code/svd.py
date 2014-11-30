import math, numpy, random, os, sys


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
    x.append(int(line[0]))
    x.append(int(line[1]))
    x.append(int(line[2]))
    R.append(x)
    max1=max(max1,int(line[0]))
    max2=max(max2,int(line[1]))
  return R, max1,max2

class recsys_svd:
  U=[]
  V=[]
  b_i= []
  b_u= []
  mu=0
  m=0
  n=0
  k=0
  R=[]
  steps=100
  alpha=0.01
  beta=0.07
  iteration =[]

  def __init__(self, n,m, k,R):
    self.n=n
    self.m=m
    self.k=k
    self.U=numpy.random.rand(n+1,k)
    self.V=numpy.random.rand(m+1,k)
    self.b_u=numpy.zeros(n+1)
    self.b_i=numpy.zeros(m+1)
    self.R=R    
    self.mu= sum(self.R[:][2])/len(self.R[:][2])
    


  def factor(self,R):
    self.V=self.V.T;
    numrows = len(R)
    temp= range(numrows)  
    for step in range(self.steps):
      random.shuffle(temp)
      e=0
      for x in temp:
        i=R[x][0]
        j=R[x][1]
        R_ij=R[x][2]
        error_ij =  R_ij - numpy.dot(self.U[i,:],self.V[:,j]) - self.mu - self.b_u[i] -self.b_i[j]
        
        #Update Rules for U,V

        self.U[i,:]=self.U[i,:]+self.alpha*(error_ij*self.V[:,j] - self.beta*self.U[i,:])
        self.V[:,j]=self.V[:,j]+self.alpha*(error_ij*self.U[i,:] - self.beta*self.V[:,j])
        
        #Update Rules for b_i, b_u

        self.b_u = self.b_u - self.alpha*(self.beta*self.b_u-error_ij)
        self.b_i = self.b_i - self.alpha*(self.beta*self.b_i-error_ij)
        #print "Not Here"

      
        e= e+ pow(R_ij - numpy.dot(self.U[i,:],self.V[:,j]) - self.mu - self.b_u[i] -self.b_i[j], 2)
      if e<0.01:
        break
      e=e/len(R)
      e=math.sqrt(e)
      #print e, step
      self.iteration.append( [e,step])
    self.V=self.V.T
    #print "Factored"

  def final_res(self):
    return self.U, self.V

  def error(self,R):
    e=0
    for x in R:
      i=x[0]
      j=x[1]
      R_ij=x[2]
      R_hat=numpy.dot(self.U[i,:],self.V.T[:,j])+self.mu + self.b_u[i] +self.b_i[j]
      e= e+ pow(R_ij- R_hat, 2)
    e=e/len(R)
    e=math.sqrt(e)
    return e

  def save_results(self,file1):
    prefix_result = os.path.abspath('..') +"/Results/"+sys.argv[0]+"/"+sys.argv[1]+"/"
    if not os.path.exists(str(prefix_result)):
      os.makedirs(str(prefix_result))
    fd=open(prefix_result+file1+".result","w")
   
    y=instance.error(R2)
    print y, int(sys.argv[4])
    fd.write("RMSE ="+str(y))
    fd.close()
    fd=open(prefix_result+file1+".iteration","w")
    for z1 in self.iteration:
      fd.write(str(z1[0])+", "+str(z1[1])+"\n")
    fd.close()

numpy.random.seed(int(sys.argv[4]))
files = [ "ua", "ub" ]


prefix_result = os.path.abspath('..') +"\\results\\"+sys.argv[0]+"\\"+sys.argv[1]


R,n,m=read_ratings(files[int(sys.argv[3])]+".base")  
R2,n1,m1=read_ratings(files[int(sys.argv[3])]+".test")  
instance= recsys_svd(n,m,int(sys.argv[1]),R)
instance.factor(R)
Udash, Vdash=instance.final_res()
instance.save_results(files[int(sys.argv[3])])
