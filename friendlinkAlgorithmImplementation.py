# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:36:16 2018

@author: RAJKUMAR
"""


from collections import defaultdict
#import matplotlib.pyplot as plt
import csv
import networkx as nx
G = nx.Graph()
import time
start_time = time.time()


def read():
        
    fields = []
    u = fields[0]
    v = fields[1]
    rows = []
    filename = r"C:\Users\PSK\Documents\Priya Docs\python_pack\trust_sample.csv"
    with open(filename) as csvfile:
         #print("hii")
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader);
        for row in csvreader:
            rows.append(row)
    print('Field names are:' + ', '.join(field for field in fields))
    print(u)
    print(v)

def printsim(sim):
	
    
  s = ""
  min1 = 100
  for i in range(1,len(sim)):
    min1 = 100
    for j in range(1,len(sim)):
        if(sim[i][j] < 0.01):
            sim[i][j] = 0.0
        s = s+str(round(sim[i][j],4)) + " "
        if(sim[i][j] < min1 and sim[i][j] != 0.0) :
            min1 = round(sim[i][j],4)
    for j in range(1,len(sim)):
        if(round(sim[i][j],4) > min1):
            #G.add_nodes_from([1,10])
            G.add_edge(i,j)
            pos = nx.spring_layout(G,k=0.50,iterations=20)
  nx.draw(G,pos,with_labels = True)
  s = s+"\n"
  print(s)

class Graph:
    def __init__(self,vertices):
        self.V= vertices 
        self.graph = defaultdict(list)
        
    def addEdge(self,u,v):
        self.graph[u].append(v)

    def printAllPathsUtil(self, u, v, visited, path):
        
        global updateflag
        global lengths
        global unow,vnow
        global paths
        path.append(u)
        visited[u]= True
        if(u == v):
                lengths.append(len(path)-1)
                                #print str(unow)+","+str(vnow)+": "+"Pathlength: "+str((len(path)-1))
                                #print(path)
                if(updateflag == 1):
                                                #print "yesupdate"
                        paths[unow][vnow][len(path)-1] = paths[unow][vnow][len(path)-1] + 1
                                                #print paths[unow][vnow][len(path)-1]
        else:
                for i in self.graph[u]:
                        if visited[i] == False:
                                self.printAllPathsUtil(i, v, visited, path)
					 
		# Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False

    
    def printAllPaths(self,u,v):   
        visited = [False]*(self.V)
        path = []
        
        self.printAllPathsUtil(u,v,visited,path)
        return path
	
    def computeL(self,n):
    
        global lengths, unow, vnow
        for i in range(n):
                for j in range(n):
                        unow = i
                        vnow = j
                        self.printAllPaths(i,j)
        return max(lengths)  
   
      
    def updateMatrix (self,n):
        global updateflag, unow,vnow
        updateflag = 1
        for i in range(n):
                for j in range(n):
                        unow = i
                        vnow = j
                        self.printAllPaths(i,j)
        updateflag = 0

                
    def computeSimilarity(self,m,n,paths):
        global sim
        for i in range(n):
                for j in range(n):
                        deno = 1
                        for k in range(2,(m+1)):
                                deno = deno * (n - k)
                        sim[i][j] = sim[i][j] + (1/((m-1)*1.0)) * ((paths[i][j][m])/(deno*1.0)) 	
    
    def main(self,n,l,paths):
        
        for m in range(2,(l+1)):
           self.computeSimilarity(m,n,paths) 
           
n = int(input("Enter the no of nodes"))
g = Graph(n) 
sim = [[0] * n for i in range (n)]

lengths = []
updateflag = 0


filename = r"C:\Users\PSK\Documents\Priya Docs\python_pack\trust_sample.csv"
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    cnt = 0
    for row in csv_reader:
        if(cnt == 0):
            cnt = 1
            continue
        u = int(row[0])
        v = int(row[1])
        if(u < n and v < n):
            g.addEdge(u,v)



unow = 0
vnow = 0
l = g.computeL(n)
paths = [[[0 for m in range(l+1)] for i in range(n)] for j in range(n)]
g.updateMatrix(n)
g.main(n,l,paths)
printsim(sim)
print("--- %s seconds ---" % (time.time() - start_time))
