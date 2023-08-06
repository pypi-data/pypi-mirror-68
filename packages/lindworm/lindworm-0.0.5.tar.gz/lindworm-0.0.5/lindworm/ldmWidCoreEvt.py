#----------------------------------------------------------------------------
# Name:         ldmWidCoreEvt.py
# Purpose:      ldmWidCoreEvt.py
#               core widget event
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx

gdSysEvtName={}
gTypeString=type('')

def ldmWidCoreKeyCode(evt):
    if wx.VERSION >= (2,8):
        return evt.GetKeyCode()
    else:
        return evt.KeyCode()

ldmEVT_WID_CORE_CMD=wx.NewEventType()
def EVT_WID_CORE_CMD(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_CMD,func)
def EVT_WID_CORE_CMD_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_CMD,func)
class ldmWidCoreCmd(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_CMD(<widget_name>, xxx)
    """
    def __init__(self,obj,cmd,data=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_CMD)
        self.cmd=cmd
        self.data=data
    def GetCmd(self):
        return self.cmd
    def GetData(self):
        return self.data
    GetDat=GetData

ldmEVT_WID_CORE_OK=wx.NewEventType()
def EVT_WID_CORE_OK(win,func):
    if hasattr(win,'GetWid'):
        win.__logDebug__(func)
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_OK,func)
def EVT_WID_CORE_OK_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_OK,func)
class ldmWidCoreOk(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_OK(<widget_name>, xxx)
    """
    def __init__(self,obj,res,data=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_OK)
        self.res=res
        self.data=data
    def GetResult(self):
        return self.res
    GetRlt=GetResult
    def GetData(self):
        return self.data
    GetDat=GetData

ldmEVT_WID_CORE_CANCEL=wx.NewEventType()
def EVT_WID_CORE_CANCEL(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_CANCEL,func)
def EVT_WID_CORE_CANCEL_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_CANCEL,func)
class ldmWidCoreCancel(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_CANCEL(<widget_name>, xxx)
    """
    def __init__(self,obj,res,data=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_CANCEL)
        self.res=res
        self.data=data
    def GetResult(self):
        return self.res
    GetRlt=GetResult
    def GetData(self):
        return self.data
    GetDat=GetData

ldmEVT_WID_CORE_FB=wx.NewEventType()
def EVT_WID_CORE_FB(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_FB,func)
def EVT_WID_CORE_FB_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_FB,func)
class ldmWidCoreFB(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_FB(<widget_name>, xxx)
    """
    def __init__(self,obj,fb,data=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_FB)
        self.fb=fb
        self.data=data
    def GetFB(self):
        return self.fb
    def GetData(self):
        return self.data
    GetDat=GetData

ldmEVT_WID_CORE_MOD=wx.NewEventType()
def EVT_WID_CORE_MOD(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_MOD,func)
def EVT_WID_CORE_MOD_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_MOD,func)
class ldmWidCoreMOD(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_MOD(<widget_name>, xxx)
    """
    def __init__(self,obj,res,data=None,gui=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_MOD)
        self.res=res
        self.data=data
        self.gui=gui
    def GetResult(self):
        return self.res
    GetRlt=GetResult
    def GetData(self):
        return self.data
    GetDat=GetData
    def GetGUI(self):
        return self.gui

ldmEVT_WID_CORE_NFY=wx.NewEventType()
def EVT_WID_CORE_NFY(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_NFY,func)
def EVT_WID_CORE_NFY_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_NFY,func)
class ldmWidCoreNFY(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_NFY(<widget_name>, xxx)
    """
    def __init__(self,obj,res,data=None,gui=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_NFY)
        self.res=res
        self.data=data
        self.gui=gui
    def GetResult(self):
        return self.res
    GetRlt=GetResult
    def GetData(self):
        return self.data
    GetDat=GetData
    def GetGUI(self):
        return self.gui

ldmEVT_WID_CORE_ADT=wx.NewEventType()
def EVT_WID_CORE_ADT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Connect(-1,-1,ldmEVT_WID_CORE_ADT,func)
def EVT_WID_CORE_ADT_DISCONNECT(win,func):
    if hasattr(win,'GetWid'):
        win=win.GetWid()
    win.Disconnect(-1,-1,ldmEVT_WID_CORE_ADT,func)
class ldmWidCoreADT(wx.PyEvent):
    """
    Posted Events:
        Tree Item selected event
            EVT_WID_CORE_ADT(<widget_name>, xxx)
    """
    def __init__(self,obj,res,old=None,new=None,gui=None):
        wx.PyEvent.__init__(self)
        self.SetEventObject(obj)
        self.SetId(obj.GetId())
        self.SetEventType(ldmEVT_WID_CORE_ADT)
        self.res=res
        self.old=old
        self.new=new
        self.gui=gui
    def GetResult(self):
        return self.res
    GetRlt=GetResult
    def GetOld(self):
        return self.old
    def GetNew(self):
        return self.new
    def GetGUI(self):
        return self.gui

class ldmWidCoreEvt:
    _MAP_EVENT={}
    _MAP_EVENT_UNBIND={}
    def BindEvent(self,name,func,par=None):
        try:
            bDbg=self.GetVerboseDbg(100)
            if bDbg:
                self.logDbg('BindEvent name:%s',name)
            # ++++++++++
            # 20141125 wro: event mapping added
            evt=None
            if name in self._MAP_EVENT:
                evt=self._MAP_EVENT[name]
                if type(evt)==gTypeString:
                    name=evt
                    if name in self._MAP_EVENT:
                        evt=self._MAP_EVENT[name]
            else:
                #self.BindEventWid(par,name,func)
                #return
                evt=self.__get_widget_event__(name)
                if type(evt)==gTypeString:
                    name=evt
                    evt=self.__get_widget_event__(name)
                else:
                    wid=self.GetWid()
                    if par is None:
                        wid.Bind(evt,func)
                    else:
                        wid.Bind(evt,func,par)
                    return 1
                if evt is None:
                    return -2
            # ----------
            if evt is not None:
                if par is None:
                    evt(self,func)
                else:
                    evt(par,func)
                return 0
            else:
                self.logErr('evt name:%s not resolved',name)
        except:
            self.logTB()
        return -1
    def UnBindEvent(self,name,func,par=None):
        try:
            # ++++++++++
            # 20141125 wro: event mapping added
            evt=None
            if name in self._MAP_EVENT_UNBIND:
                evt=self._MAP_EVENT_UNBIND[name]
                if type(evt)==gTypeString:
                    name=evt
                    if name in self._MAP_EVENT_UNBIND:
                        evt=self._MAP_EVENT_UNBIND[name]
            # ----------
            if evt is not None:
                if par is None:
                    evt(self,func)
                else:
                    evt(par,func)
                return 0
            else:
                self.logErr('evt name:%s not resolved',name)
        except:
            self.logTB()
        return -1
    def __get_widget_event__(self,sK):
        try:
            bDbg=self.GetVerboseDbg(100)
            if bDbg:
                self.logDbg('__get_widget_event__ sK:%s',sK)
            if sK=='txt':
                return wx.EVT_TEXT
            elif sK=='ent':
                return wx.EVT_TEXT_ENTER
            elif sK=='btn':
                return wx.EVT_BUTTON
            elif sK=='mn':
                return wx.EVT_MENU
            elif sK=='tg':
                return wx.EVT_TOGGLEBUTTON
            elif sK=='choice':
                return wx.EVT_CHOICE
            elif sK=='check':
                return wx.EVT_CHECKBOX
            elif sK=='checkBox':
                return wx.EVT_CHECKLISTBOX
            elif sK=='lstSel':
                return wx.EVT_LISTBOX
            elif sK=='lstDblclk':
                return wx.EVT_LISTBOX_DCLICK
            elif sK=='lstCtrlSel':
                return wx.EVT_LIST_ITEM_SELECTED
            elif sK=='lstCtrlDesel':
                return wx.EVT_LIST_ITEM_DESELECTED
            elif sK=='lstCtrlDblClk':
                return wx.EVT_LIST_ITEM_ACTIVATED
            elif sK=='lstCtrlAct':
                return wx.EVT_LIST_ITEM_ACTIVATED
            elif sK=='lstCtrlActivate':
                return wx.EVT_LIST_ITEM_ACTIVATED
            elif sK=='lstCtrlColClk':
                return wx.EVT_LIST_COL_CLICK
            elif sK=='lstCtrlColClkLf':
                return wx.EVT_LIST_COL_CLICK
            elif sK=='lstCtrlColClkRg':
                return wx.EVT_LIST_COL_RIGHT_CLICK
            elif sK=='lstCtrlKey':
                return wx.EVT_LIST_KEY_DOWN
            elif sK=='trCtrlSel':
                return wx.EVT_TREE_ITEM_SELECTED
            elif sK=='trCtrlDesel':
                return wx.EVT_TREE_ITEM_DESELECTED
            elif sK=='trCtrlDbClk':
                return wx.EVT_TREE_ITEM_ACTIVATED
            elif sK=='trCtrlAct':
                return wx.EVT_TREE_ITEM_ACTIVATED
            elif sK=='trCtrlActivate':
                return wx.EVT_TREE_ITEM_ACTIVATED
            elif sK=='trCtrlDel':
                return wx.EVT_TREE_DELETE_ITEM
            elif sK=='trCtrlCollapsing':
                return wx.EVT_TREE_ITEM_COLLAPSING
            elif sK=='trCtrlCollapsed':
                return wx.EVT_TREE_ITEM_COLLAPSED
            elif sK=='trCtrlExpanding':
                return wx.EVT_TREE_ITEM_EXPANDING
            elif sK=='trCtrlExpanded':
                return wx.EVT_TREE_ITEM_EXPANDED
            elif sK=='trCtrlSelChg':
                return wx.EVT_TREE_SEL_CHANGING
            elif sK=='trCtrlSel':
                return wx.EVT_TREE_SEL_CHANGED
            elif sK=='trCtrlLclk':
                return wx.EVT_TREE_ITEM_LEFT_CLICK
            elif sK=='trCtrlMclk':
                return wx.EVT_TREE_ITEM_MIDDLE_CLICK
            elif sK=='trCtrlRclk':
                return wx.EVT_TREE_ITEM_RIGHT_CLICK
            elif sK=='trCtrlMenu':
                return wx.EVT_TREE_ITEM_MENU
            elif sK=='trCtrlDragBeg':
                return wx.EVT_TREE_BEGIN_DRAG
            elif sK=='trCtrlDragBegRg':
                return wx.EVT_TREE_BEGIN_RDRAG
            elif sK=='trCtrlDragEnd':
                return wx.EVT_TREE_END_DRAG
            elif sK=='trCtrlKey':
                return wx.EVT_TREE_KEY_DOWN
            elif sK=='char':
                return wx.EVT_CHAR
            elif sK=='char_hook':
                return wx.EVT_CHAR_HOOK
            elif sK=='keyDn':
                return wx.EVT_KEY_DOWN
            elif sK=='keyUp':
                return wx.EVT_KEY_UP
            elif sK=='mouse':
                return wx.EVT_MOUSE_EVENTS
            elif sK=='wheel':
                return wx.EVT_MOUSEWHEEL
            elif sK=='rgDbl':
                return wx.EVT_RIGHT_DCLICK
            elif sK=='mdDbl':
                return wx.EVT_MIDDLE_DCLICK
            elif sK=='lfDbl':
                return wx.EVT_LEFT_DCLICK
            elif sK=='motion':
                return wx.EVT_MOTION
            elif sK=='rgDn':
                return wx.EVT_RIGHT_DOWN
            elif sK=='rgUp':
                return wx.EVT_RIGHT_UP
            elif sK=='mdUp':
                return wx.EVT_MIDDLE_UP
            elif sK=='mdDn':
                return wx.EVT_MIDDLE_DOWN
            elif sK=='lfUp':
                return wx.EVT_LEFT_UP
            elif sK=='lfDn':
                return wx.EVT_LEFT_DOWN
            elif sK=='enter':
                return wx.EVT_ENTER_WINDOW
            elif sK=='leave':
                return wx.EVT_LEAVE_WINDOW
            elif sK=='move':
                return wx.EVT_MOVE
            elif sK=='size':
                return wx.EVT_SIZE
            elif sK=='erase':
                return wx.EVT_ERASE_BACKGROUND
            elif sK=='paint':
                return wx.EVT_PAINT
            elif sK=='focusKill':
                return wx.EVT_KILL_FOCUS
            elif sK=='focusSet':
                return wx.EVT_SET_FOCUS
            elif sK=='help':
                return wx.EVT_HELP
            elif sK=='colorChanged':
                return wx.EVT_SYS_COLOUR_CHANGED
            # dialog events
            elif sK=='idle':
                return wx.EVT_IDLE
            elif sK=='navKey':
                return wx.EVT_NAVIGATION_KEY
            elif sK=='iconize':
                return wx.EVT_ICONIZE
            elif sK=='maximize':
                return wx.EVT_MAXIMIZE
            elif sK=='dropFiles':
                return wx.EVT_DROP_FILES
            elif sK=='close':
                return wx.EVT_CLOSE
            elif sK=='activate':
                return wx.EVT_ACTIVATE
            elif sK=='init':
                return wx.EVT_INIT_DIALOG
            elif sK=='ctxmn':
                return wx.EVT_CONTEXT_MENU
            elif sK=='cxtmn':
                return wx.EVT_CONTEXT_MENU
            return None
        except:
            self.logTB()
        return None
    def GetSysEvtNameByEvt(self,evt):
        try:
            global gdSysEvtName
            bDbg=self.GetVerboseDbg(100)
            if bDbg:
                self.LogDbg('GetSysEvtNameByEvt')
            iEvtId=evt.GetEventType()
            if iEvtId in gdSysEvtName:
                return gdSysEvtName[iEvtId]
            for s in dir(wx):
                if s.startswith('EVT'):
                    #print s
                    e=getattr(wx,s)
                    if hasattr(e,'evtType'):
                        lEvtId=e.evtType
                        #print iEvtId,lEvtId
                        if iEvtId in lEvtId:
                            gdSysEvtName[iEvtId]=s[:]
                            return s
        except:
            self.logTB()
    def BindEventDict(self,wid,dEvt):
        try:
            bDbg=self.GetVerboseDbg(100)
            if bDbg:
                self.logDbg('BindEventDict wid:%r dEvt:%r',wid,dEvt)
            for sK,fct in dEvt.iteritems():
                if wid is None:
                    self.BindEvent(sK,fct)
                else:
                    self.BindEventWid(wid,sK,fct)
        except:
            self.logTB()
    def BindEventWid(self,wid,sEvt,fct):
        try:
            bDbg=self.GetVerboseDbg(100)
            if bDbg:
                self.logDbg('BindEventWid sEvt:%s fct:%r wid:%r',sEvt,fct,wid)
            evt=self.__get_widget_event__(sEvt)
            if type(evt)==gTypeString:
                sEvt=evt
                evt=self.__get_widget_event__(sEvt)
            if evt is not None:
                t=type(wid)
                if t==gTypeString:
                    w=self.__dict__.get(wid,None)
                elif t==types.UnicodeType:
                    w=self.__dict__.get(wid,None)
                else:
                    w=wid
                if w is None:
                    return 
                w.Bind(evt,fct)
        except:
            self.logTB()

