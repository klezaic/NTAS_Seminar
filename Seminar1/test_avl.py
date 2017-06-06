from avl import BinaryTree
from MoviesData import MoviesData
import os.path
import time
import re
import random
import fnmatch
import rotationCount

def getKeyOne(array, key):
        for data in array:
                if data[1].startswith(key[:-1]):
                        return data[1];

def getKeyTwo(array, key):
        for data in array:
                if data[1].startswith(key[:-1]):
                        return data[1];
        

def findByShortNameInRange (node, k1, k2):
        if node == None:
            return;
        if node.value > k1:
            findByShortNameInRange(node.left, k1, k2)
        if k1 <= node.value <= k2:
            print(node.obj)
        if node.value < k2:
            findByShortNameInRange(node.right, k1, k2)
            
def findWithWildCard (node, array, k1, k2):
    k_1 = getKeyOne(array, k1)
    array.reverse()
    k_2 = getKeyTwo(array, k2)
    array.reverse()

    iterator = findByShortNameInRange(node, k_1, k_2)

    return iterator
        
        
if __name__ == '__main__':
    file = "movies.txt"
    current_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(current_path, "data")
    path = os.path.join(data_path, file)
    
    array = []

    start = time.time()
    
    with open(path) as f:
        for line in f:
            row = re.split('\t', line.splitlines()[0])
            data = MoviesData(int(row[0]), row[1], row[2])
            array.append(data)
            
    end = time.time()
    print("Loaded file: " + file + " -> contains " + str(len(array)) + " rows of data")
    print("Elapsed time: " + str(end - start) + " sec\n")

    print("Inserting data into BinaryTree")
    start = time.time()

    tree = BinaryTree()
    for data in array:
        tree.add(data[1], data)

    end = time.time()  
    print("Elapsed time: " + str(end - start) + " sec\n")

    arrayOfObjectsToFind = []
    for number in range(1000):
        arrayOfObjectsToFind.append(array[random.randint(0, len(array)-1)])

    print("Find by shortName starting for 1000 random objects")
    elapsedTime = 0
    for data in arrayOfObjectsToFind:
        start = time.time()
        tree.findByShortName(data[1])
        end = time.time()
        elapsedTime += end-start
    print("Elapsed time: " + str(elapsedTime) + " sec")
    print("Average search time: " + str(elapsedTime/1000) + " sec\n")

    
    startName = "Aban*"
    endName = "Abba*"
    print("Find by shortName with wildCard starting for range " + startName + "-" + endName)
    elapsedTime = 0
    start = time.time()
    findWithWildCard(tree.root, array, startName, endName)
    end = time.time()
    elapsedTime += end-start
    print("Elapsed time: " + str(elapsedTime) + " sec")

    print("Dynamic height of tree is " + str(tree.root.dynamicHeight()))

    print("\n")
    tree.root.findMin()
    print("\n")
    tree.root.findMax()

    print("\nNumber of right rotations: " + str(rotationCount.right))
    print("Number of left rotations: " + str(rotationCount.left))  
