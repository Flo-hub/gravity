import math
import xml.etree.ElementTree as ET
import pprint
#import numpy as np
#from numpy.linalg import inv, norm

## Fürs Code-Schreiben: limitiere Länge der Datensätze zu:

class Point:
    
    def __init__(self, position, value = 0, heith = 0):
        self.val = value  # in {-1,1}
        self.pos = np.array(position, dtype=np.double)  # im d-dimensionalen Raum
        self.h = heith  # Hôhe im Baum nachdem Einbauen
        
        self.path = []  # Liste von 1er und 2er, repräsentiert den Weg
        
        self.left = None  # habe ich einen linken
        self.right = None  # bzw. rechten Zweig?
        self.node = None # oder die letzte Kreuzung
    
    def starts_climbing(self,p):
        
        d = len(self.pos)  # praktischer
        self.h += 1  # auf jeden Fall bin ich im Baum um 1 Stockwerk höher
        self.node = p
        if self.pos[p.h % d] < p.pos[p.h % d]:  # falls die i-te Komponente kleiner ist als die von p:
            self.path.append(1)  # fûge ich meinem Weg einen links turn hinzu            
            if p.left != None:   # und entweder mache ich beim nâchsten Knoten weiter...
                self.starts_climbing(p.left)  #...indem ich rekursiv das selbe tue
            else:   # oder es gibt keinen nächsten Knoten 
                p.left = self  # und ich bleibe stehen
                
        else:  # falls die i-te Komponente grösser ist agiere ich analog, diesmal für 
            self.path.append(2)  # rechts
            if p.right != None: 
                self.starts_climbing(p.right)
            else: 
                p.right = self
          
    def distance_to(self,p):
        r = self.pos - p.pos
        print(str(p.pos))
        return np.sqrt(np.sum(r ** 2 ))
    
    def distance_to_proj(self,p):
        d = len(self.pos)
        r = self.pos[p.h/ % d]-p.pos[p.h/ % d]
        return np.absolute([r])
        
    def ancestors(self,list):
        if self.node != None:
            list.append(self.node)
            self.node.ancestors(list)
        return list
    
    
            
           
                
            
            
            
        
        
class Tree:
    
    def __init__(self,dimension):
        self.d = dimension
        self.out = False
        self.points = []
        
    def grows(self,point):
        
        #assert len(point.pos) == self.d
        
        if self.out:
            point.starts_climbing(self.points[0])
        else: 
            self.out = True
            
        self.points.append(point)
        
        print(str(point.path))
        
    def node_distances(self,point,p,distances):
        
        if p.node != None:
            distances.append(point.distance_to(p.node))
            self.node_distances(point,p.node,distances)
        
        return distances
                  
        
    def closest_of(self,point,k):
        
        
        self.grows(point)
        
        neighbours = sorted(point.ancestors([]), key = point.distance_to())
        
        if len(neighbours) > k:
            for i in range(len(neighbours)-k):
                neighbours.remove(neighbours[k-1+i])
         
        for p in neighbours:
            if point.distance_to_proj(p) < point.distance_to(neighbours[k-1]):
                for q in self.points:
                    if len(q.path) > p.h + 1 and q.path[p.h + 1] = (point.path[p.h + 1] + 1) % 2 :
                            if point.distance_to(q) < point.distance_to(neighbours[k-1] and len(neighbours) = k:
                                neighbours = sorted(neighbours.append(q))
                                neighbours.remove(neighbours[k])
                            elif  len(neighbours) < k:
                                neighbours.append(q)
                        
        self.points.remove(point)                             
        return neighbours
        
    

        print('')
        for p in self.points:
            print(str(p.path))
        
        print('')
        
        dist = sorted(self.node_distances(point,point,[]))  # step 1
        #print(str(dist))
       
        
            
        
        else:
            return dist
        
        
        print('')
        for p in self.points:
            print(str(p.path))        
    






tree = Tree(2)

tree.grows(Point([3,3]))
tree.grows(Point([4,2]))
tree.grows(Point([5,3]))
tree.grows(Point([5,1]))
tree.grows(Point([3,1]))
tree.grows(Point([1,2]))
tree.grows(Point([1,1]))
tree.grows(Point([2,3]))

print(tree.closest_of(Point([4,3/2])))

print('')
print()

  
 #Wir brauchen:
d
l                                                                       
l1 = 
l2 =                                                                     
train_set = 
trees = []
values = []     
sign()  
best = 1                                                                        
K =     

for k in KSET:
    Error = 0                                                                       
    for r in range(l-1):
        R = 0                                                                  
        trees.append(Tree(d))                                                                        
        for v in data_set[:r*l1]:
            trees[r].grows(Point(v[1:],v[0]))                                                              
        for v in data_set[(r+1)*l1:]:
            trees[r].grows(Point(v[1:],v[0]))
        for w in data_set[r*l1:(r+1)*l1]:
            value = 0
            for p in trees[r].closest_of(Point(w[1:],w[0]),k):
                value += p.value
            if sign(value) != w[0]:
                R += 1                                                                
            values.append(sign(value))   
        R /= l1  
        Error += R                                                                    
    R = 0                                                                        
    trees.append(Tree(d))                                                                        
        for v in data_set[:(l-1)*l1]:
            trees[r].grows(Point(v[1:],v[0]))                                                            
        for w in data_set[(l-1)*l1:]:
            value = 0
            for p in trees[r].closest_of(Point(w[1:],w[0]),k):
                value += p.value
             if sign(value) != w[0]:
                R += 1                                                               
            values.append(sign(value))                                                                                                                                          
    R /= l2                                                                       
    Error =+ R                                                                                                                                               
    Error /= l                                                                  
    if Error < best:
        K = k                                                                    
                                                                                                                                                
                                                                        
test_set =                                                                         
classifications = []
                                                                        
for v in test_set:                                                                    
    classification = 0                                                                    
    for r in range(l):
        value = 0                                                                
        for p in trees[r].closest_of(Point(v[1:],v[0])):                                                                
            value += p.value   
        value = sign(value)  
        classification += value                                                                
    classifications.append(sign(classification))                                                               
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
