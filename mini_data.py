import os, sys


def read_ratings(filename):

  prefix = os.path.abspath('..') +"/BTP/datasets/ml-100k/"
  x=open(prefix+filename,"r")
  max1=0
  max2=0
  R= []
  for line in x:
    x=[]
    line=line.replace("\n","")
    line=line.split("\t")
    #R[int(line[0])][int(line[1])]=int(line[2])
    x.append(int(line[0]))
    x.append(int(line[1]))
    x.append(int(line[2]))
    R.append(x)
    max1=max(max1,int(line[0]))
    max2=max(max2,int(line[1]))
  return R, max1,max2

files = [ "u1", "u2", "u3", "u4", "u5", "ua", "ub" ]
ext= [".base", ".test"]

for fil in files:
	for ext1 in ext:
		prefix_result = os.path.abspath('.') +"/Datasets/ml-100k-subset/"
		if not os.path.exists(str(prefix_result)):
			os.makedirs(str(prefix_result))
		fd=open(prefix_result+fil+ext1,"w")
		R,n,m = read_ratings(fil+ext1)
		R2=[]
		for x in R:
			if x[0] <= 100 and x[1] <= 100:
				R2.append(x)
		for x in R2:
			 fd.write(str(x[0])+", "+str(x[1])+", "+str(x[2])+"\n")
		fd.close()


