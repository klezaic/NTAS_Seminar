"""
    AVL Implementation of Binary Tree.
    
    
    Subclasses can override key methods for customizing methods in 
    BinaryTree (newNode) and BinaryNode (newNode, compareTo). For now,
    these support standard <= and >= semantics 
    
"""
import rotationCount

class BinaryNode:

    def __init__ (self, value = None, obj = None):
        """Create binary node."""
        self.value  = value
        self.obj    = obj
        self.left   = None
        self.right  = None
        self.height = 0
        
        
    def computeHeight (self):
        """Compute height of node in BST."""
        height = -1
        if self.left:
            height = max(height, self.left.height)
        if self.right:
            height = max(height, self.right.height)
            
        self.height = height + 1

    def dynamicHeight (self):
        """Compute height of node in BST."""
        height = -1
        if self.left:
            height = max(height, self.left.dynamicHeight())
        if self.right:
            height = max(height, self.right.dynamicHeight())
            
        return height + 1

    def dynamicHeightDifference (self):
        """Compute height difference of node's children in BST."""
        leftTarget = 0
        rightTarget = 0
        if self.left:
            leftTarget = 1 + self.left.dynamicHeight()
        if self.right:
            rightTarget = 1 + self.right.dynamicHeight()
            
        return leftTarget - rightTarget

    def heightDifference (self):
        """Compute height difference of node's children in BST."""
        leftTarget = 0
        rightTarget = 0
        if self.left:
            leftTarget = 1 + self.left.height
        if self.right:
             rightTarget = 1 + self.right.height
                   
        return leftTarget - rightTarget

    def assertAVLProperty (self):
        """Validate AVL property for BST node."""
        if abs(self.dynamicHeightDifference()) > 1:
            return False
        if self.left:
            if not self.left.assertAVLProperty():
                return False
        if self.right:
            if not self.right.assertAVLProperty():
                return False

        return True

    def rotateRight (self):
        """Perform right rotation around given node."""
        newRoot = self.left
        grandson = newRoot.right
        self.left = grandson
        newRoot.right = self

        self.computeHeight()

        rotationCount.right += 1
        
        return newRoot

    def rotateLeft (self):
        """Perform left rotation around given node."""
        newRoot = self.right
        grandson = newRoot.left
        self.right = grandson
        newRoot.left = self
    
        self.computeHeight()

        rotationCount.left += 1
        
        return newRoot

    def rotateLeftRight (self):
        """Perform left, then right rotation around given node."""
        child = self.left
        newRoot = child.right
        grand1  = newRoot.left
        grand2  = newRoot.right
        child.right = grand1
        self.left = grand2
    
        newRoot.left = child
        newRoot.right = self
    
        child.computeHeight()
        self.computeHeight()

        #rotationCount.left += 1
        #rotationCount.right += 1
        
        return newRoot

    def rotateRightLeft (self):
        """Perform right, then left rotation around given node."""
        child = self.right
        newRoot = child.left
        grand1  = newRoot.left
        grand2  = newRoot.right
        child.left = grand2
        self.right = grand1
    
        newRoot.left = self
        newRoot.right = child
    
        child.computeHeight()
        self.computeHeight()

        #rotationCount.right += 1
        #rotationCount.left += 1
      
        return newRoot

    def compareTo (self, value):
        """
        Returns 0 if equal, negative if smaller and positive if greater.
        Suitable for overriding.
        """
        if self.value == value:
            return 0
        if self.value < value:
            return -1
        return +1
        
    def add (self, val, obj):
        """Adds a new node to BST with value and rebalance as needed."""
        newRoot = self

        # if val <= self.value        
        if self.compareTo(val) >= 0:
            self.left = self.addToSubTree (self.left, val, obj)
            if self.heightDifference() == 2:
                #if val <= self.left.value:
                
                if self.left.compareTo(val) >= 0:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateLeftRight()
        else:
            self.right = self.addToSubTree (self.right, val, obj)
            if self.heightDifference() == -2:
                #if val > self.right.value:
                if self.right.compareTo(val) < 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()

        newRoot.computeHeight()
        return newRoot

    def newNode (self, val, obj):
        """Return new Binary Node, amenable to subclassing."""
        return BinaryNode(val, obj)

    def addToSubTree (self, parent, val, obj):
        """Add val to parent subtree (if exists) and return root in case it has changed because of rotation."""
        if parent is None:
            return self.newNode(val, obj)

        parent = parent.add(val, obj)
        return parent
           
    def removeFromParent (self, parent, val):
        """Helper method for remove. Ensures proper behavior when removing node that 
        has children."""
        if parent:
            return parent.remove(val)
        return None

    def remove (self, val):
        """
         Remove val from BinaryTree. Works in conjunction with remove
         method in BinaryTree.
        """
        newRoot = self
        rc = self.compareTo(val)
        if rc == 0:
            if self.left is None:
                return self.right

            child = self.left
            while child.right:
                child = child.right
            
            childKey = child.value;
            self.left = self.removeFromParent(self.left, childKey)
            self.value = childKey;

            if self.heightDifference() == -2:
                if self.right.heightDifference() <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()
        elif rc > 0:
            self.left = self.removeFromParent(self.left, val)
            if self.heightDifference() == -2:
                if self.right.heightDifference() <= 0:
                    newRoot = self.rotateLeft()
                else:
                    newRoot = self.rotateRightLeft()
        else:
            self.right = self.removeFromParent(self.right, val)
            if self.heightDifference() == 2:
                if self.left.heightDifference() >= 0:
                    newRoot = self.rotateRight()
                else:
                    newRoot = self.rotateLeftRight()

        newRoot.computeHeight()
        return newRoot

    def __repr__ (self):
        """Useful debugging function to produce linear tree representation."""
        leftS = ''
        rightS = ''
        if self.left:
            leftS = str(self.left)
        if self.right:
            rightS = str(self.right)
        return "(L:" + leftS + " " + str(self.value) + " R:" + rightS + ")"

    def inorder (self):
        """In order traversal generator of tree rooted at given node."""
        if self.left:
            for n in self.left.inorder():
                yield n

        yield self.value

        if self.right:
            for n in self.right.inorder():
                yield n

    def findMin(self):
        if self.left is None:
            print ("Minimal value of tree: " + self.value)
            print ("ID at minValue location:" + str(self.obj.ID))
            print ("ShortName at minValue location:" + self.obj.shortName)
            print ("LongName at minValue location:" + self.obj.longName)
        else:
            self.left.findMin();

    def findMax(self):
        if self.right is None:
            print ("Maximum value of tree: " + self.value)
            print ("ID at maxValue location:" + str(self.obj.ID))
            print ("ShortName at maxValue location:" + self.obj.shortName)
            print ("LongName at maxValue location:" + self.obj.longName)
        else:
            self.right.findMax();
                
class BinaryTree:

    def __init__ (self):
        """Create empty binary tree."""
        self.root = None
        rotationCount.left = 0
        rotationCount.right = 0

    def __repr__ (self):
        if self.root is None:
            return "avl:()"
        return "avl:" + str(self.root)
                
    def newNode (self, value, obj):
        """Return new BinaryNode object. Suitable for overriding."""
        return BinaryNode(value, obj)
    
    def add (self, value, obj):
        """Insert value into proper location in Binary Tree."""
        if self.root is None:
            self.root = self.newNode(value, obj)
        else:
            self.root = self.root.add(value, obj)

    def __contains__ (self, target):
        """Check whether BST contains target value."""
        node = self.root
        while node:
            rc = node.compareTo(target)
            if rc > 0:
                node = node.left
            elif rc < 0:
                node = node.right
            else:
                return True     
        return False

    def findByShortName (self, target):
        node = self.root
        while node:
            rc = node.compareTo(target)
            if rc > 0:
                node = node.left
            elif rc < 0:
                node = node.right
            else:
                return node.obj        
        return False
    
    def remove (self, val):
        """Remove value from tree."""
        if self.root:
            self.root = self.root.remove(val)

    def __iter__ (self):
        """In order traversal of elements in the tree."""
        if self.root:
            return self.root.inorder()
                        
    def assertAVLProperty (self):
        """Validate AVL property for BST Tree."""
        if self.root:
            return self.root.assertAVLProperty()
        else:
            return True

"""
Change Log
----------
2014.05.23     removeFromParent
               defect:    elif value < parent.val:
               fix:       elif value < parent.value

2014.06.16     added inorder iterator capability to allow 'for x in bt'
2015.05.18     updated to python 3.0 with timeit
2015.05.19     added ability to override core methods.
"""
