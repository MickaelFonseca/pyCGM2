# -*- coding: utf-8 -*-

import btk


class ViconInterface(object):

    def __init__(self,nexusHandle,iModel, iAcq, vskName, staticProcessing = False ):
        self.m_model = iModel
        self.m_acq = iAcq
        self.m_vskName = vskName
        self.nexusHandle = nexusHandle
        self.staticProcessing = staticProcessing

    def run(self):
        self.m_model.viconExport(self.nexusHandle,self.m_acq, self.m_vskName,self.staticProcessing)
        
        