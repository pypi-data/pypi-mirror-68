#----------------------------------------------------------------------------
# Name:         lmdGuiNty.py
# Purpose:      gui notify class
#
# Author:       Walter Obweger
#
# Created:      20200404
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import time
import wx

from six.moves import _thread as sixThd

from lindworm.logUtil import ldmUtilLog

class ldmGuiNty:
    def __init__(self,iVal=0,iMin=0,iMax=100):
        self.sPhase=''
        self.sStatus=''
        self.iVal=iVal
        self.iMin=iMin
        self.iMax=iMax
        self.iSchedule=0
        self.iStatus=0
        self.iChg=1
    def clrSchedule(self):
        """
        ### parameter
        ### return
            actions scheduled
        """
        self.iSchedule=0
        self.iChg=1
    def finStatus(self):
        """finalize status, property iStatus set to -2,
        to ensure final notification to be posted.
        IsActive set iStatus to -1.
        """
        self.iStatus=-2
        self.iChg=1
    def clrStatus(self):
        """clear status, notification turned off.
        """
        self.iStatus=-1
        self.iChg=1
    def IsChg(self):
        if self.iChg>0:
            self.iChg=0
            return 1
        return 0
    def IsActive(self,iHndFin=1):
        """check notification still active.
        event handler is supposed to use methode to prevent
        unnecessary notifications.
        """
        if self.iStatus>=0:
            return 1
        else:
            if self.iStatus==-2:
                if iHndFin>0:
                    self.clrStatus()
                return 1
            return 0
    def IncSchedule(self):
        """increment schedule counter.
        """
        self.iSchedule+=1
        self.iStatus=0
        self.iChg=1
    def IncStatus(self):
        """increment status counter.
        """
        self.iStatus+=1
        self.iChg=1
    def GetNtyDat(self):
        """get notify data.
        """
        if self.IsChg():
            oNtyDat=ldmGuiNtyDat(oNty=self)
            return oNtyDat
        return None
    def GetStatusOfs(self):
        """get string with schedule and status counter formated.
        schedule 2 digits,
        status 6 digits, or 'fin   ' in case iStatus==-2
        counter overflow is handled here.
        """
        if self.iSchedule>99:
            self.iSchedule=0
        if self.iStatus>999990:
            self.iStatus=0
        elif self.iStatus==-1:
            return '%02d.done   '%(self.iSchedule)
        elif self.iStatus==-2:
            return '%02d.fin    '%(self.iSchedule)
        return '%02d.%06d'%(self.iSchedule,self.iStatus)
    def SetPhase(self,sPhase):
        """set phase
        ### parameter
            sPhase      ... phase : string
        """
        if sPhase!=self.sPhase:
            self.iChg=1
        self.sPhase=sPhase
    def GetPhase(self):
        """get phase
        ### return
            sPhase      ... phase : string
        """
        return self.sPhase
    def SetStatus(self,sStatus):
        """set sStatus
        ### parameter
            sStatus     ... status : string
        """
        if self.sStatus!=sStatus:
            self.iChg=1
        self.sStatus=sStatus
    def GetStatus(self):
        """get sStatus
        ### return
            sStatus     ... status : string
        """
        return self.sStatus
    def SetVal(self,iVal,iMin=None,iMax=None):
        """set value
        ### parameter
            iVal    ... value : int
            iMin    ... minimum : int
            iMax    ... maximum : int
        """
        if iMin is not None:
            self.iMin=iMin
        if iMax is not None:
            self.iMax=iMax
        if iVal>self.iMax:
            iVal=self.iMax
        if iVal<self.iMin:
            iVal=self.iMin
        if self.iVal!=iVal:
            iChg=1
        self.iVal=iVal
    def SetMin(self,iMin):
        """set minimum
        ### parameter
            iMin    ... minimum : int
        """
        if self.iMin!=Min:
            self.iChg=1
        self.iMin=iMin
    def SetMax(self,iMax):
        """set maximum
        ### parameter
            iMax    ... maximum : int
        """
        if self.iMax!=iMax:
            self.iChg=1
        self.iMax=iMax
    def GetNormalized(self,rScale=1000):
        """get normalized value scaled between 0 to rScale.
        ### parameter
            rScale  ... scale limit
        ### return
            rVal    ... normalized value (min/max),
                        0 <= rVal <= rScale
        """
        try:
            if self.iVal<self.iMin:
                self.iVal=self.iMin
            if self.iVal>self.iMax:
                self.iVal=self.iMax
            rVal=(self.iVal-self.iMin)/(self.iMax-self.iMin)
            return rVal*rScale
        except:
            return 12

class ldmGuiNtyDat:
    def __init__(self,oNty=None):
        if oNty is None:
            self.sPhase=''
            self.sStatus=''
            self.sStatusOfs=''
            self.iValNormalized=0
        else:
            self.sPhase=oNty.GetPhase()[:]
            self.sStatus=oNty.GetStatus()[:]
            self.sStatusOfs=oNty.GetStatusOfs()[:]
            self.iValNormalized=oNty.GetNormalized()
    def GetPhase(self):
        """get phase
        ### return
            sPhase      ... phase : string
        """
        return self.sPhase
    def GetStatus(self):
        """get sStatus
        ### return
            sStatus     ... status : string
        """
        return self.sStatus
    def GetStatusOfs(self):
        """get string with schedule and status counter formated.
        schedule 2 digits,
        status 6 digits, or 'fin   ' in case iStatus==-2
        counter overflow is handled here.
        """
        return self.sStatusOfs
    def GetNormalized(self):
        """get normalized value scaled between 0 to 1000.
        ### return
            rVal    ... normalized value (min/max),
                        0 <= rVal <= 1000
        """
        return self.iValNormalized
