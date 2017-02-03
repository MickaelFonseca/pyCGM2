# -*- coding: utf-8 -*-

import numpy as np
import pdb
import logging

def setFrameData(a1,a2,sequence):
    """
        set Frame of a ccordinate system accoring two vector and a sequence
        
        :Parameters:
           - `a1` (numy.array(1,3)) - first vector        
           - `a2` (str) - second vector  
           - `sequence` (str) - construction sequence (XYZ, XYiZ)
        
        :Return:
            - `axisX` (numy.array(1,3)) - x-axis of the coordinate system
            - `axisY` (numy.array(1,3)) - y-axis of the coordinate system
            - `axisZ` (numy.array(1,3)) - z-axis of the coordinate system
            - `rot` (numy.array(3,3)) - rotation matrix of the coordinate system

        .. note:: if sequence includes a *i* ( ex: XYiZ), opposite of vector a2 is considered  
                     
    """

    if sequence == "XYZ" or sequence == "XYiZ" :
        if sequence == "XYiZ":
            a2=a2*-1.0
        axisX=a1
        axisY=a2
        axisZ=np.cross(a1,a2)
        rot=np.array([axisX,axisY,axisZ]).T         

    if sequence == "XZY" or sequence == "XZiY" :
        if sequence == "XZiY":
            a2=a2*-1.0
        axisX=a1
        axisZ=a2
        axisY=np.cross(a2,a1)
        rot=np.array([axisX,axisY,axisZ]).T 

    if sequence == "YZX" or sequence == "YZiX" :
        if sequence == "YZiX":
            a2=a2*-1.0
        axisY=a1
        axisZ=a2
        axisX=np.cross(a1,a2)
        rot=np.array([axisX,axisY,axisZ]).T 

    if sequence == "YXZ" or sequence == "YXiZ" :
        if sequence == "YXiZ":
            a2=a2*-1.0
        axisY=a1
        axisX=a2
        axisZ=np.cross(a2,a1)
        rot=np.array([axisX,axisY,axisZ]).T 


    if sequence == "YXZ" or sequence == "YXiZ" :
        if sequence == "YXiZ":
            a2=a2*-1.0
        axisY=a1
        axisX=a2
        axisZ=np.cross(a2,a1)
        rot=np.array([axisX,axisY,axisZ]).T 


    if sequence == "ZXY" or sequence == "ZXiY" :
        if sequence == "ZXiY":
            a2=a2*-1.0
        axisZ=a1
        axisX=a2
        axisY=np.cross(a1,a2)
        rot=np.array([axisX,axisY,axisZ]).T 

    if sequence == "ZYX" or sequence == "ZYiX" :
        if sequence == "ZYiX":
            a2=a2*-1.0
        axisZ=a1
        axisY=a2
        axisX=np.cross(a2,a1)
        rot=np.array([axisX,axisY,axisZ]).T 
        
    return axisX, axisY, axisZ, rot

class Node(object):
    """
        A node is a local position of a point in a Frame 
    """        
 
    def __init__(self,label):
        """  
            :Parameters:
               - `label` (str) - desired label of the node  
       
            .. note:: automatically, the suffix "_node" ends the node label
        """

        self.m_name = label+"_node"
        self.m_global = np.zeros((1,3))
        self.m_local = np.zeros((1,3))
        
    def computeLocal(self,rot,t):
        """
            Compute local position from global position
        
            :Parameters:
                - `rot` (np.array(3,3)) - a rotation matrix 
                - `t` (np.array((1,3))) - a translation vector 
           
        """
        self.m_local=np.dot(rot.T,(self.m_global-t))

    def computeGlobal(self,rot,t):
        """
            Compute global position from local
        
            :Parameters:
                - `rot` (np.array((3,3))) - a rotation matrix 
                - `t` (np.array((1,3))) - a translation vector 
       
        """

        self.m_global=np.dot(rot,self.m_local) +t


class Frame(object):
    """
        A Frame defined a segment pose
 
    """    
    
    
    
    
    def __init__(self):

        self.m_axisX=np.zeros((1,3))                    
        self.m_axisY=np.zeros((1,3))
        self.m_axisZ=np.zeros((1,3))
        
        self._translation=np.zeros((1,3))
        self._matrixRot=np.zeros((3,3))


        self._nodes=[]

    def getRotation(self):
        """ 
            Get rotation matrix
            
            :Return:
                - `na` (np.array((3,3))) - a rotation matrix 
            
        """
        return self._matrixRot

    def getTranslation(self):
        """ 
            Get translation vector

            :Return:
                - `na` (np.array((3,))) - a translation vector 
                    
        """
        return self._translation

    def setRotation(self, R):
        """ 
            Set rotation matrix
        
            :Parameters:
               - `R` (np.array(3,3) - a rotation matrix 
        """

        self._matrixRot=R

    def setTranslation(self,t):
        """ 
            Set translation vector
        
            :Parameters:
               - `t` (np.array(3,)) - a translation vector 
        """
        self._translation=t

    def updateAxisFromRotation(self,R):
        """ 
            Update a rotation matrix
        
            :Parameters:
               - `R` (np.array(3,3) - a rotation matrix 
        """
        self.m_axisX = R[:,0]
        self.m_axisY = R[:,1]
        self.m_axisZ = R[:,2]

        self._matrixRot = R

    def update(self,R,t):
        """ 
            Update both rotation matrix and translation vector
        
            :Parameters:
               - `R` (np.array(3,3) - a rotation matrix
               - `t` (np.array(3,)) - a translation vector 
        """        
        
        self.m_axisX = R[:,0]
        self.m_axisY = R[:,1]
        self.m_axisZ = R[:,2]
        self._translation = t
        self._matrixRot = R

    def addNode(self,nodeLabel,position, positionType="Global"):
        """ 
            Append a `Node` to a Frame
        
            :Parameters:
                - `nodeLabel` (str) - node label 
                - `position` (np.array(3,)) - a translation vector 
                - `positionType` (str) - two choice Global or Local 

        """
        #TODO : use an Enum for the argment positionType
        
        logging.debug("new node (%s) added " % nodeLabel)
        
        isFind=False
        i=0
        for nodeIt in self._nodes:
            if str(nodeLabel+"_node") == nodeIt.m_name:
                isFind=True
                index = i
            i+=1
        
        if isFind:
            if positionType == "Global":
                self._nodes[index].m_global = position
                self._nodes[index].computeLocal(self._matrixRot,self._translation)
            elif positionType == "Local":
                self._nodes[index].m_local=position
                self._nodes[index].computeGlobal(self._matrixRot,self._translation)
            else :
                raise Exception("positionType not Known (Global or Local")                
            
        else:
            node=Node(nodeLabel)
            if positionType == "Global":
                node.m_global=position
                node.computeLocal(self._matrixRot,self._translation)
            elif positionType == "Local":
                node.m_local=position
                node.computeGlobal(self._matrixRot,self._translation)
            else :
                raise Exception("positionType not Known (Global or Local")
            self._nodes.append(node)
    
    def getNode_byIndex(self,index):
        """ 
            Return a node within the list from its index
        
            :Parameters:
                - `index` (int) - index of the node within the list
            :Return:
                - `na` (pyCGM2.pyCGM2.Model.CGM2.Frame.Node) - a node instance
        """
        return self._nodes[index]           
    
    def getNode_byLabel(self,label):
        """ 
            Return a node in the list from its label
        
         :Parameters:
            - `label` (str) - label of the node you want to find
         :Return:
            - `na` (pyCGM2.pyCGM2.Model.CGM2.Frame.Node) - a node instance
        """
        
        for nodeIt in self._nodes:
            if str(label+"_node") == nodeIt.m_name:
                logging.debug( " target label ( %s) - label find (%s) " %(label,nodeIt.m_name) )       
                return nodeIt
        
        return False        




    def printAllNodes(self):
        """ 
            Display all node labels
    
        """
        for nodeIt in self._nodes:
            print nodeIt.m_name

    def eraseNodes(self):    
        """
            erase all nodes
        """
        self._nodes=[]
