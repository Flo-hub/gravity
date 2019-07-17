import math
import xml.etree.ElementTree as ET
import pprint
#import numpy as np
#from numpy.linalg import inv, norm

## Fürs Code-Schreiben: limitiere Länge der Datensätze zu:
p = 1000 # Anzahl Trainpoints
q = 1000 # Anzahl Testpoints

## Einlesen
tree = np.genfromtxt("bananas-1-2d.train.csv", delimiter=',')
    # data ist Matrix mit data[i][j] ist Eintrag in i+1 Zeile, j+1 Spalte
KSET = [1,3,5,10] # Anzahlen der Nachbarn aus denen k* gesucht wird

## Erstmal weniger verwenden als Test (später diese Zeilen löschen)
dataTest = tree[0:p]
tree = dataTest

CIRCLE_TAG_NAME = '{http://www.w3.org/2000/svg}circle'
GROUP_TAG_NAME = '{http://www.w3.org/2000/svg}g'

pp = pprint.PrettyPrinter(indent=4)

def get_all_points(tree):
    return [circle_to_point(circle)
            for circle in tree.iter(CIRCLE_TAG_NAME)]


def get_point_by_id(tree, point_id):
    return [circle_to_point(circle)
            for circle in tree.iter(CIRCLE_TAG_NAME)
            if 'id' in circle.attrib
            if circle.attrib['id'] == point_id]


def get_group_by_id(tree, group_id):
    return [circle
            for group in tree.iter(GROUP_TAG_NAME)
            if 'id' in group.attrib:
                if group.attrib['id'] == group_id:
                    for circle in get_all_points(group)]:

[pivot] = get_point_by_id(tree, 'pivot')
[closest] = get_point_by_id(tree, 'closest')
points = get_group_by_id(tree, 'points')

def distance_squared(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    dx = x1 - x2
    dy = y1 - y2

    return dx * dx + dy * dy


def closest_point(all_points, new_point):
    best_point = None
    best_distance = None

    for current_point in all_points:
        current_distance = distance_squared(new_point, current_point)

        if best_distance is None or current_distance < best_distance:
            best_distance = current_distance
            best_point = current_point

    return best_point


k = 2


def build_kdtree(points, depth=0):
    n = len(points)

    if n <= 0:
        return None

    axis = depth % k

    sorted_points = sorted(points, key=lambda point: point[axis])

    return {
        'point': sorted_points[n / 2],
        'left': build_kdtree(sorted_points[:n / 2], depth + 1),
        'right': build_kdtree(sorted_points[n/2 + 1:], depth + 1)
    }


kdtree = build_kdtree(points)


def kdtree_naive_closest_point(root, point, depth=0, best=None):
    if root is None:
        return best

    axis = depth % k

    next_best = None
    next_branch = None

    if best is None or distance_squared(point, best) > distance_squared(point, root['point']):
        next_best = root['point']
    else:
        next_best = best

    if point[axis] < root['point'][axis]:
        next_branch = root['left']
    else:
        next_branch = root['right']

    return kdtree_naive_closest_point(next_branch, point, depth + 1, next_best)


def closer_distance(pivot, p1, p2):
    if p1 is None:
        return p2

    if p2 is None:
        return p1

    d1 = distance_squared(pivot, p1)
    d2 = distance_squared(pivot, p2)

    if d1 < d2:
        return p1
    else:
        return p2


def kdtree_closest_point(root, point, depth=0):
    if root is None:
        return None

    axis = depth % k

    next_branch = None
    opposite_branch = None

    if point[axis] < root['point'][axis]:
        next_branch = root['left']
        opposite_branch = root['right']
    else:
        next_branch = root['right']
        opposite_branch = root['left']

    best = closer_distance(point,
                           kdtree_closest_point(next_branch,
                                                point,
                                                depth + 1),
                           root['point'])

    if distance_squared(point, best) > (point[axis] - root['point'][axis]) ** 2:
        best = closer_distance(point,
                               kdtree_closest_point(opposite_branch,
                                                    point,
                                                    depth + 1),
                               best)

    return best

class Point:
    
    def __init_(value, position, heith = 0):
        self.val = value  # in {-1,1}
        self.pos = position  # im d-dimensionalen Raum
        self.h = heith  # Hôhe im Baum nachdem Einbauen
        
        self.path = []  # Liste von 1er und 2er, repräsentiert den Weg
        
        self.left = None  # habe ich einen linken
        self.right = None  # bzw. rechten Zweig?
    
    def starts_climbing(p):
        
        d = len(self.pos)  # praktischer
        self.h += 1  # auf jeden Fall bin ich im Baum um 1 Stockwerk höher
        
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
          
        
            
        
        
class Tree:
    
    def __init_(dimension):
        self.d = dimension
        self.out = False
        self.points = []
        
    def grows(point):
        
        assert len(point.pos) == d
        
        if self.out:
            point.starts_climbing(points[0])
        else: 
            self.out = true
            
        self.points.append(point)
        
        #print str(point.path)
        
        
      import numpy as np

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
        r = self.pos - p.pos
        return np.sqrt(np.sum())
        
            
           
                
            
            
            
        
        
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
                  
        
    def closest_of(self,point):
        
        self.grows(point)
        print('')
        for p in self.points:
            print(str(p.path))
        
        print('')
        
        dist = sorted(self.node_distances(point,point,[]))  # step 1
        print('')
        print(str(dist))
       
        champ = dist[0]
        
        
        
        self.points.remove(point)
        print('')
        for p in self.points:
            print(str(p.path))
        
        
        return dist[0]
        
      
        
    






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

  
    
