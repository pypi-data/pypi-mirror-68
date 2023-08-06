#----------------------------------------------------------------------------
# Name:         ldmWidThd.py
# Purpose:      ldmWidThd.py
#               GUI widget respond control thread
# Author:       Walter Obweger
#
# Created:      20200414
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx

from lindworm.ldmGuiThd import ldmGuiThd
from lindworm.ldmWidPanel import ldmWidPanel
from lindworm.ldmWidPanel import ldmWidPanelFlxGrd
import lindworm.ldmWidImgMed as ldmWidImgMed

#ldmWidPanelFlxGrd
class ldmWidThd(ldmWidPanelFlxGrd):
    def __init__(self,**kwargs):
        try:
            # +++++ beg:
            _kwargs=self.GetKw(kwargs,[
                        'sLogger','iLv',
                        'id','name','parent',
                        'pos','size','style',
                        'iCol',
                        'lWid'])
            tSz = (16,16)
            bmpSta=bmp=ldmWidImgMed.BtnSmlGn01.GetBitmap()
            bmpStp=bmp=ldmWidImgMed.BtnSmlRd00.GetBitmap()
            lWid=[
                ['lbl'  ,'lblPhase',    'phase'],
                ['txtRd','txtPhase',    ''],
                ['cbBmp','cbStop',    bmpStp,   'stop'],
                ['lbl'  ,'lblStatus',   'status'],
                ['txtRd','txtStatus',   ''],
                ['cbBmp','cbStart',   bmpSta,   'start'],
                
                [None],
                ['gag'  ,'gagDetail',1000],
                [None],
                
                [None],
                ['lst'  ,'lcrThd',      ''],
                [None],
                ]
            lWidArg=_kwargs.get('lWid',None)
            if lWidArg is None:
                _kwargs['lWid']=lWid
            else:
                _kwargs['lWid']=lWid+lWidArg
            _kwargs['iCol']=3
            _kwargs['lCol']=[1]
            _kwargs['lRow']=[3]
            ldmWidPanelFlxGrd.__init__(self,**_kwargs)
            # ----- end:
        except:
            self.logTB()
    def __initObj__(self,**kwargs):
        """initialize object properties, widgets aren't present yet.
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initObj__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            self.dFunc={
                'start':('dummy',self.prcDmy,(),{})
                }
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initWid__(self,**kwargs):
        try:
            self.logDbg('__initWid__')
            ldmWidPanelFlxGrd.__initWid__(self,**kwargs)
            self.lcrThd.AppendColumn("No", format=wx.LIST_FORMAT_LEFT,
                    width=self.getCfgWid('ldmWidThd','iColNo',sType='int',oDft=80))
            self.lcrThd.AppendColumn("Info", format=wx.LIST_FORMAT_LEFT, 
                    width=self.getCfgWid('ldmWidThd','iColInfo',sType='int',oDft=320))
            self.lcrThd.AppendColumn("Stat", format=wx.LIST_FORMAT_LEFT, 
                    width=self.getCfgWid('ldmWidThd','iColStat',sType='int',oDft=30))

            self.oThd=ldmGuiThd(self.GetWid(),rDly=0.2,sLogger='thdGui',iVerbose=0)
            self.oThd.BindEvtNty(self.OnThdNty)
        except:
            self.logTB()
            return -1
    def SetFunc(self,sCmd,sPhase,func,*args,**kwargs):
        try:
            # +++++ beg:
            self.logDbg('ldmWidThd::SetFunc sCmd:%r sPhase:%r',
                        sCmd,sPhase)
            self.dFunc[sCmd]=(sPhase,func,args,kwargs)
            self.logDbg('dFunc:%r',self.dFunc)
        except:
            self.logTB()
            return -1
    def DoCmd(self,sCmd,oThd,oNty):
        try:
            # +++++ beg:
            self.logDbg('ldmWidThd::DoCmd sCmd:%r',sCmd)
            self.logDbg('dFunc:%r',self.dFunc)
            sPhase,func,args,kwargs=self.dFunc.get(sCmd,
                                ('dummy',self.prcDmy,(),{}))
            self.logDbg('%s, func:%r a:%r k:%r',sPhase,func,args,kwargs)
            if sCmd=='start':
                #oNty=self.oThd.GetNty()
                func(*args,oThd=oThd,**kwargs)
                #oThd.Do(sPhase,func,*args,oThd=oThd,**kwargs)
                #self.oThd.Do('dummy',
                #            self.prcDmy,*(),
                #            oNty=oNty)
            elif sCmd=='stop':
                oThd.Stop()
            # ----- end:
            return 0
        except:
            self.logTB()
            return -1
    def prcCmd(self,sCmd):
        try:
            # +++++ beg:
            self.logDbg('ldmWidThd::prcCmd sCmd:%r',sCmd)
            if sCmd=='start':
                oNty=self.oThd.GetNty()
                self.DoCmd(sCmd,self.oThd,oNty)
                #self.oThd.Do('dummy',
                #            self.prcDmy,*(),
                #            oNty=oNty)
            elif sCmd=='stop':
                self.oThd.Stop()
            # ----- end:
            return 0
        except:
            self.logTB()
            return -1
    def GetThd(self):
        return self.oThd
    def OnThdNty(self,evt):
        evt.Skip()
        try:
            # +++++ beg:
            sStatOfs=evt.oNty.GetStatusOfs()
            iVal=evt.oNty.GetNormalized()
            sPhase=evt.oNty.GetPhase()
            sStatus=evt.oNty.GetStatus()
            self.gagDetail.SetValue(int(iVal))
            self.txtPhase.SetValue(sPhase)
            self.txtStatus.SetValue(sStatus)
            iIdx=self.lcrThd.InsertItem(0,sStatOfs)
            self.lcrThd.SetItem(iIdx,1,sStatus)
            # ----- end:
        except:
            self.logTB()
    def prcDmy(self,oNty=None):
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmWidThd::prcDmy'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:action
            if oNty is not None:
                oNty.SetPhase('process dummy')
                oNty.SetStatus('loop')
                oNty.IncStatus()
                oNty.SetMax(10)
            for iOfs in range(10):
                self.oThd.delay()
                if oNty is not None:
                    oNty.SetVal(iOfs)
            # ----- end:action
            # +++++ beg:finalize
            if oNty is not None:
                oNty.SetPhase('finished.')
                oNty.SetStatus('all good')
            # ----- end:finalize
            # +++++ beg:
            if oNty is not None:
                oNty.finStatus()
                self.oThd.delay(iCnt=5)
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
            # ----- end:
            return iRet
        except:
            self.oFdr.logTB()
            return -1
