#----------------------------------------------------------------------------
# Name:         ldmWidCore.py
# Purpose:      ldmWidCore.py
#               core widget
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import types
import six
import json
import os

import wx

from lindworm.logUtil import ldmUtilLog
from lindworm.ldmWidCoreEvt import ldmWidCoreEvt

gdCtrlId={}

def ldmWidCoreCtrlId(sKey,sSub=None):
    try:
        global gdCtrlId
        if sKey in gdCtrlId:
            d=gdCtrlId[sKey]
        else:
            d={}
            gdCtrlId[sKey]=d
        if sSub in d:
            iId=d[sSub]
        else:
            iId=wx.NewIdRef()
            d[sSub]=iId
        return iId
    except:
        vpc.logTB(__name__)
        return wx.NewIdRef()

def ldmWidCoreGetIcon(bmp):
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(bmp)
    return icon

class ldmWidCore(ldmUtilLog,ldmWidCoreEvt):
    def __init__(self,sLogger='',iLv=1,iVerbose=0,sCfgFN=None,**kwargs):
        """constructor
        several sub constructor methods are called
        
        + __initCls__: initialize class
        + __initCfg__: initialize object configuration
        + __initDat__: initialize internal data
        + __initObj__: initialize object data
        + __initWid__: initialize widget
        + __initEvt__: initialize widget event
        + __initPrp__: initialize properties, widget data
        
        ### parameter
            sLogger ... log origin
            iLv         ... trivial logging level
                0       ... debug
                1       ... info
                2       ... warning
                3       ... error
                4       ... critical
                x       ... debug
            iVerbose    ... higher values add more logs
            sCfgFN  ... json configuration file
            kwargs  ... keyword arguments passed to all init methods
        """
        ldmUtilLog.__init__(self,sLogger,iLv=iLv,
                    iVerbose=iVerbose)
        try:
            if sCfgFN is not None:
                self.loadCfgWid(sCfgFN=sCfgFN)
        except:
            self.logTB()
        try:
            self.__initCls__(**kwargs)
            self.__initCfg__(**kwargs)
            self.__initDat__(**kwargs)
            self.__initObj__(**kwargs)
            self.__initWid__(**kwargs)
            self.__initEvt__(**kwargs)
            self.__initPrp__(**kwargs)
        except:
            self.logTB()
        try:
            self.__initLayout__(**kwargs)
        except:
            self.logTB()
    def __initCls__(self,**kwargs):
        """initialize class
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        self.clsWid=None
    def __initCfg__(self,**kwargs):
        """initialize configuration
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initCfg__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            if hasattr(self,'dCfgWid'):
                pass
            else:
                self.dCfgWid=None
            # ----- end:
            # +++++ beg:
            self.dCfgWidDft={
                'common':{
                    'bmpWidth':32,
                    },
                }
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initDat__(self,**kwargs):
        """initialize internal data, intended to application
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initDat__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initObj__(self,**kwargs):
        """initialize object properties, widgets aren't present yet.
        data is supposed to be related to widgets or support their
        function.
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initObj__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initWid__(self,**kwargs):
        """initialize widgets
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        wid=None
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initWid__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
        return wid
    def __initEvt__(self,**kwargs):
        """initialize event handling, widgets are already created
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initEvt__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initLayout__(self,**kwargs):
        """initialize layout
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initLayout__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
    def __initPrp__(self,**kwargs):
        """initialize properties, supposed to be related to widgets.
        ### parameter
            kwargs  ... keyword arguments passed to all init methods
        """
        wid=None
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::__initPrp__'
            self.logDbg('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:
            # ----- end:
            # +++++ beg:finalize
            self.logDbg('end:%s'%(sOrg))
            # ----- end:finalize
        except:
            self.logTB()
        return wid
    def __str__(self):
        """get object string
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        return self.sOrg
    def __repr__(self):
        """get object representation
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        return self.sOrg
    def GetWid(self):
        """get main widget.
        panel some times.
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        return self.wid
    def GetWidMod(self):
        """ get widget to indicate modification.
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        return self.wid
    def GetWidChild(self):
        """future extension
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        return None
    def GetCacheDict(self,sAttr,bChk=False):
        """get dictionary for caching data,
        create empty dictionary if attribute isn't present yet.
        ### parameter
            sAttr   ... dictionary name, object attribute
            bChk    ... check only
        ### return
            if bChk==False
                dictionary
            if bChk==True
                boolean check
                True    ... attribute present
                False   ... or not
            None    ... exception
        """
        try:
            bDbg=self.GetVerboseDbg(0)
            if bDbg:
                self.logDbg('')
            if bChk==True:
                if hasattr(self,sAttr):
                    return True
                else:
                    return False
            if hasattr(self,sAttr):
                dTmp=getattr(self,sAttr)
            else:
                dTmp={}
                setattr(self,sAttr,dTmp)
            return dTmp
        except:
            self.logTB()
        return None
    def GetCtrlId(self,sKey,sSub=None):
        """get widget (control) id, used in GUI framework
        reuse id for similar controls, which are cached
        in global dictionary, build by use of ldmWidCoreCtrlId.
        ### parameter
            sKey    ... primary key
                        None uses class name instead
            sSub    ... secondary key
        ### return
            widget id
        """
        if sKey is None:
            return ldmWidCoreCtrlId(self.__class__.__name__,sSub)
        else:
            return ldmWidCoreCtrlId(sKey,sSub)
    def GetKw(self,kwargs,lKey,dDft=None,kag=None):
        """get keyword arguments lightweight copy with
        defaults mixed in.
        ### parameter
            kwargs  ... original keyword arguments at constructor
            lKey    ... list of required keyword arguments returned
            dDft    ... default values
            kag     ... dictionary preset, None create a new dictionary
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        if kag is None:
            kag={}
        for s in lKey:
            if s in kwargs:
                kag[s]=kwargs[s]
        if dDft is not None:
            for k,it in six.iteritems(dDft):
                if k not in kag:
                    kag[k]=it
                else:
                    if kag[k] is None:
                        kag[k]=it
        return kag
    def GetWidArgs(self,kwargs,lKey,dDft,kag=None,sSub=None,
                bValidate=True,par=None,lArg=None):
        """get widget arguments to be passed at constructor
        
        gui frameworks are restrict when it comes to arguments 
        accepted. depending on widget class a specific set
        of arguments and keyword arguments are needed.
        this method provide a way to construct arguments and
        keyword arguments by mixing in defaults to lightweight 
        copy of original kwargs.
        
        method GetCtrlId is used to get widget id determined by
        parent name and sSub. similar ids shall be used through
        entire application.
        ### parameter
            kwargs  ... original keyword arguments at constructor
            lKey    ... list of required keyword arguments returned
            dDft    ... default values
            kag     ... dictionary preset, None create a new dictionary
            sSub .. 
            bValidate . enforce elementary arguments to be present,
                        pos ... widget position (wx.DefaultPosition)
                        size .. widget size (wx.DefaultSize)
            par     ... parent object/widget, determine parent name
                        GetWid is used to retrieve widget of object
            lArg    ... list of arguments removed from keyword 
                        and 
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        lArgs=[]
        kag=self.GetKw(kwargs,lKey,dDft,kag=kag)
        if 'pos' not in kag:
            kag['pos']=wx.DefaultPosition
        if 'size' not in kag:
            kag['size']=wx.DefaultSize
        if bValidate==True:
            if kag['pos'] is None:
                kag['pos']=wx.DefaultPosition
            if kag['size'] is None:
                kag['size']=wx.DefaultSize
        #else:
        #    sz=kag['size']
        if sSub is None:
            if 'sSub' in kwargs:
                sSub=kwargs['sSub']
                #print self.__class__.__name__,sSub
            else:
                # 20150112 wro: is this really a good idea?
                if 'name' in kwargs:
                    #sSub=kwargs['name']
                    #print self.__class__.__name__,sSub,'name'
                    pass
        if par is None:
            sNamePar=self.__class__.__name__
        else:
            sNamePar=par.GetName()
        if 'id' not in kag:
            iId=self.GetCtrlId(sNamePar,sSub)
            kag['id']=iId
        else:
            if kag['id'] is None:
                iId=self.GetCtrlId(self.__class__.__name__,sSub)
                kag['id']=iId
            else:
                iId=kag['id']
        if 'parent' in kag:
            parent=kag['parent']
            if hasattr(parent,'GetWid'):
                par=parent.GetWid()
                kag['parent']=par
        #if 'style' not in kag:
        #    kag['style']=wx.TAB_TRAVERSAL
        #else:
        #    if kag['style'] is None:
        #        kag['style']=wx.TAB_TRAVERSAL
        #self.logDbg({'kag':kag,'name':self.__class__.__name__,
        #        'kwargs':kwargs,'lKey':lKey,'dDft':dDft})
        if lArg is not None:
            for sK in lArg:
                if sK in kag:
                    lArgs.append(kag[sK])
                    del kag[sK]
                else:
                    lArgs.append(None)
        arg=tuple(lArgs)
        return arg,kag
    def CB(self,func,*args,**kwargs):
        """callback func/method in main thread
        widget manipulation inside a thread may cause
        stability issues.
        ### parameter
            func    ... callable
            args    ... arguments to pass
            kwargs  ... keyword arguments to pass
        """
        try:
            wx.CallAfter(func,*args,**kwargs)
        except:
            self.logTB()
    def CallBackDelayed(self,zSleep,func,*args,**kwargs):
        """delayed callback func/method in main thread
        widget manipulation inside a thread may cause
        stability issues.
        ### parameter
            zSleep  ... delay time in seconds
            func    ... callable
            args    ... arguments to pass
            kwargs  ... keyword arguments to pass
        """
        try:
            wx.CallAfter(wx.FutureCall,int(zSleep*1000),func,*args,**kwargs)
        except:
            self.logTB()
    def setCfgWid(self,sGrp,sKey,sVal,iMode=1):
        """get configuration value
        ### parameter
            sGrp    ... configuration group
            sKey    ... configuration key
            sVal    ... value
            iMode   ... configuration dictionary to change
                1   ... default dictionary
                2   ... active dictionary
                3   ... both
                <=0 ... default dictionary
        ### return
            return code
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:adapt faulty iMode
            if iMode<=0:
                iMode=1
            # ----- end:adapt faulty iMode
            # +++++ beg:set value in default dictionary
            if (iMode & 1)==1:
                if self.dCfgWidDft is None:
                    self.dCfgWidDft={}
                if sGrp in self.dCfgWidDft:
                    dGrp=self.dCfgWidDft[sGrp]
                else:
                    dGrp={}
                    self.dCfgWidDft[sGrp]=dGrp
                dGrp[sKey]=sVal
                iRet+=1
            # ----- end:set value in default dictionary
            # +++++ beg:set value in active dictionary
            if (iMode & 2)==2:
                if self.dCfgWid is not None:
                    if sGrp in self.dCfgWid:
                        dGrp=self.dCfgWid[sGrp]
                    else:
                        dGrp={}
                        self.dCfgWid[sGrp]=dGrp
                        dGrp[sKey]=sVal
                iRet+=2
            # ----- end:set value in active dictionary
            return iRet
        except:
            self.logTB()
            return -1
    def getCfgWidTup(self,sGrp,sKey,sType=None,oDft=None):
        """get configuration value and return code
        ### parameter
            sGrp    ... configuration group
            sKey    ... configuration key
            sType   ... type enforcement
            oDft    ... default value
        ### return
            return code
                1   ... value taken from defaults dictionary
                2   ... value taken from active dictionary
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
            value
        """
        try:
            # +++++ beg:initialize
            iRet=0
            oVal=oDft
            # ----- end:initialize
            # +++++ beg:find value
            if self.dCfgWid is not None:
                if sGrp in self.dCfgWid:
                    dGrp=self.dCfgWid[sGrp]
                    if sKey in dGrp:
                        iRet=2
                        oVal=dGrp[sKey]
            # ----- end:find value
            # +++++ beg:find default value
            if iRet==0:
                if self.dCfgWidDft is not None:
                    if sGrp in self.dCfgWidDft:
                        dGrp=self.dCfgWidDft[sGrp]
                        if sKey in dGrp:
                            iRet=1
                            oVal=dGrp[sKey]
            # ----- end:find default value
            # +++++ beg:type enforcement
            if iRet>0:
                if sType=='int':
                    try:
                        iVal=int(oVal)
                        return iRet,iVal
                    except:
                        iVal=oDft
                        return iRet,iVal
            # ----- end:type enforcement
            return iRet,oVal
        except:
            self.logTB()
            return -1,None
    def getCfgWid(self,sGrp,sKey,sType=None,oDft=None):
        """get configuration value
        ### parameter
            sGrp    ... configuration group
            sKey    ... configuration key
            sType   ... type enforcement
            oDft    ... default value
        ### return
            value   ... value
        """
        try:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:get value
            iRet,oVal=self.getCfgWidTup(sGrp,sKey,sType=sType,oDft=oDft)
            # ----- end:get value
            return oVal
        except:
            self.logTB()
            return oDft
    def loadCfgWid(self,sCfgFN='cfg.json'):
        """read configuration file, given in json format
        ### parameter
            sCfgFN  ... configuration file name
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmWidCore::loadCfgWid'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:read cfg file
            self.sCfgWidFN=sCfgFN
            self.dCfgWid=None
            if os.path.exists(self.sCfgWidFN):
                with open(self.sCfgWidFN,'r') as oFile:
                    self.dCfgWid=json.loads(oFile.read())
                iRet=1
            # ----- end:read cfg file
            # +++++ beg:verbose cfg dict
            if self.iVerbose>=30:
                self.oLog.debug('%r %r',self.sCfgWidFN,self.dCfgWid)
            # ----- end:verbose cfg dict
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def IsMainThread(self,bMain=True,bSilent=False):
        return True
        if wx.Thread_IsMain()!=bMain:
            if bSilent==False:
                if bMain:
                    self.logCri('called by thread'%())
                else:
                    self.logCri('called by main thread'%())
            return False
        return True
