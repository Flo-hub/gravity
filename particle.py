import math
import numpy as np
#import xml.etree.ElementTree as ET
#import pprint
#import numpy as np
#from numpy.linalg import inv, norm

## Fürs Code-Schreiben: limitiere Länge der Datensätze zu:

def sign(zahl):
    ''' Gibt das Vorzeichen der Eingabezahl aus. '''
    if zahl >= 0:
        return 1
    else:
        return -1

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
            self.path.append(0)  # fûge ich meinem Weg einen links turn hinzu            
            if p.left != None:   # und entweder mache ich beim nâchsten Knoten weiter...
                self.starts_climbing(p.left)  #...indem ich rekursiv das selbe tue
            else:   # oder es gibt keinen nächsten Knoten 
                p.left = self  # und ich bleibe stehen
                
        else:  # falls die i-te Komponente grösser ist agiere ich analog, diesmal für 
            self.path.append(1)  # rechts
            if p.right != None: 
                self.starts_climbing(p.right)
            else: 
                p.right = self

    def distance_to(self, p):
        r = self.pos - p.pos
        return np.sqrt(np.sum(r ** 2))

    def distance_to_proj(self, p):
        d = len(self.pos)
        r = self.pos[p.h  % d] - p.pos[p.h  % d]
        return np.absolute([r])

    def ancestors(self, list):
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
        
        #print(str(point.path))
        
    def node_distances(self,point,p,distances):
        
        if p.node != None:
            distances.append(point.distance_to(p.node))
            self.node_distances(point,p.node,distances)
        
        return distances
                  
        
    def neighbors_of(self,point,k):

        self.grows(point)
        #print('')
        #print('')
        neighbors = sorted( point.ancestors([]), key = point.distance_to )
        for p in neighbors:
            print( str(p.pos) + ': ' + str(point.distance_to(p)) )
        #print('')

        #print(str(neighbors))
        #print('')

        if len(neighbors) > k:
            for i in range(len(neighbors) - k):
                neighbors.remove(neighbors[len(neighbors)-1])
            
        print('gekürzt')
        for p in neighbors:
            print( str(p.pos) + ': ' + str(point.distance_to(p)) )    
            

        for p in neighbors:
            if point.distance_to_proj(p) < point.distance_to(neighbors[k - 1]):
                print('Es gibt vielleicht Kandidaten beim anderen Zweig des Knoten nr ' + str(p.h))
                for q in self.points:
                    if q.h > p.h and (q.path[:p.h-1] == point.path[:p.h-1]  and q.path[p.h] == (point.path[p.h] + 1) % 2):
                        if len(neighbors) == k:
                            if point.distance_to(q) < point.distance_to(neighbors[k - 1]):
                                neighbors.append(q)
                                neighbors = sorted(neighbors, key = point.distance_to)
                                neighbors.remove(neighbors[k])
                        elif len(neighbors) < k:
                            neighbors.append(q)
            for p in neighbors:
                print( str(p.pos) + ': ' + str(point.distance_to(p)) )
           # print('')

        self.points.remove(point)
        #print('Die ' + str(k) + ' nächsten Nachbarn sind:')
        
        return neighbors
        
      
        
    


    




#tree = Tree(2)

#tree.grows(Point([3,3]))
#tree.grows(Point([4,2]))
#tree.grows(Point([5,3]))
#tree.grows(Point([5,1]))
#tree.grows(Point([3,1]))
#tree.grows(Point([1,2]))
#tree.grows(Point([1,1]))
#tree.grows(Point([2,3]))
#tree.grows(Point([5,3/2]))

#k = 3

#for p in tree.neighbors_of(Point([4,3/2]),k):
#    print(str(p.pos))



#def data_points(list):
 #   for 
    

  
def classify(name, l = 5):
    
    t1 = process_time()
    
    data_set = np.genfromtxt("{}.train.csv".format(name) , delimiter=',')
    
    d = len(data_set[0])-1                                                                    
    n = len(data_set)
    if n % l == 0:  # Falls n durch l teilbar ist, erhalten wir exakt gleich große Teildatensätze.
        l1 = int(n / l)
        l2 = l1
    else:           # Falls n nicht durch l teilbar ist, kürzen wir den letzten Teildatensatz
        l1 = math.ceil(n/l) - 1         # Anzahl der Datenpunkte in den ersten (l-1) Blocks
        l2 = math.ceil(n/l) - 1 + n % l   
                                                                 
    trees = []
    
    for r in range(l-1):
        trees.append(Tree(d))                                                                        
        for v in data_set[:r*l1]:
            trees[r].grows(Point(v[1:],v[0]))                                                              
        for v in data_set[(r+1)*l1:]:
            trees[r].grows(Point(v[1:],v[0]))
    trees.append(Tree(d))                                                                        
    for v in data_set[:(l-1)*l1]:
        trees[l-1].grows(Point(v[1:],v[0]))  
    
    
    #values = []     
    best = 1                                                                        
    K = None

    for k in range(1,201):
        Error = 0                                                                       
        for r in range(l-1):
            R = 0                                                                  
            for w in data_set[r*l1:(r+1)*l1]:
                value = 0
                for p in trees[r].closest_of(Point(w[1:],w[0]),k):
                    value += p.value
                if sign(value) != w[0]:
                    R += 1                                                                
                #values.append(sign(value))   
            R /= l1  
            Error += R                                                                    
        R = 0                                                                        
        for w in data_set[(l-1)*l1:]:
            value = 0
            for p in trees[l-1].closest_of(Point(w[1:],w[0]),k):
                value += p.value
                if sign(value) != w[0]:
                    R += 1                                                               
            #values.append(sign(value))                                                                                                                                          
        R /= l2                                                                       
        Error += R                                                                                                                                               
        Error /= l                                                                  
        if Error < best:
            K = k                                                                    
                                                                                                                                                
                                                                        
    test_set =  np.genfromtxt("{}.test.csv".format(name) , delimiter=',')     
                                                                
    R = 0                                                                    
    for v in test_set:                                                                    
        classification = 0                                                                    
        for r in range(l):
            value = 0                                                                
            for p in trees[r].closest_of(Point(v[1:],v[0]),K):                                                                
                value += p.value   
                value = sign(value)  
            classification += value 
        classification = sign(classification)
        if classification != v[0]:
            R += 1
        v[0] = classification
    R /= len(test_set) 
    
    np.savetxt('{}.result.csv'.format(name), test_set, delimiter=',', fmt='%1.4f')
    
    t2 = process_time()
    print('Best number of neighbors: {}'.format(K))
    print('Ratio of failure: {} %'.format(100*R))
    print('Performance: {} s'.format(t2-t1))
                                                           
                                                                        
                                                                        
   #Just_do_it.py
#from Classify import classify

classify('bananas1-2d‘)
classify('bananas1-4d‘)
classify('bananas2-2d‘)
classify('bananas2-4d‘)
classify('bananas5-2d‘)
classify('bananas5-4d‘)
classify('crosses-2d‘)
classify('toy-2d‘)
classify('toy-3d‘)
classify('toy-4d‘)
classify('toy-10d‘)
                                                                   
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
                                                                        
