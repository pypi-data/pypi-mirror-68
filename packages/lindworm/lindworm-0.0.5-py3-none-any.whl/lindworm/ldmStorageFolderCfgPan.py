#----------------------------------------------------------------------------
# Name:         ldmStorageFolderCfgPan.py
# Purpose:      ldmStorageFolderCfgPan.py
#               GUI for ldmStorageFolder configuration panel
# Author:       Walter Obweger
#
# Created:      20200412
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx
import os
import logging
import traceback

from optparse import OptionParser

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

from lindworm import __version__
import lindworm.ldmGui as ldmGui
from lindworm.ldmGuiThd import ldmGuiThd
from lindworm.ldmStorageFolder import ldmStorageFolder

gOpt=None

class ldmStorageFolderCfgPan(wx.Panel):
    WILDCARD_JSON=["json file (*.json)|*.json",
            "All files (*.*)|*.*"]
    def __init__(self, *args, **kwds):
        self.__initDat__()
        # begin wxGlade: ldmStorageFolderFrm.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.SetSize((600, 400))
        self.txtSrcDN = wx.TextCtrl(self, wx.ID_ANY, self.sSrcDN)
        self.cbSrcDN = wx.Button(self, wx.ID_ANY, "...")
        self.txtBldDN = wx.TextCtrl(self, wx.ID_ANY, self.sBldDN)
        self.cbBldDN = wx.Button(self, wx.ID_ANY, "...")
        self.txtBldFN = wx.TextCtrl(self, wx.ID_ANY, self.sBldFN)
        self.cbBldFN = wx.Button(self, wx.ID_ANY, "...")
        self.txtCfgFN = wx.TextCtrl(self, wx.ID_ANY, self.sCfgFN)
        self.cbCfgFN = wx.Button(self, wx.ID_ANY, "...")
        self.spnShaMB = wx.SpinCtrl(self, wx.ID_ANY, "1", min=-1, max=64)
        self.chcShaMB = wx.Choice(self, wx.ID_ANY, choices=["disabled", "01 MB", "02 MB", "04 MB", "08 MB", "16 MB", "32 MB", "64 MB", "all data"])

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnSrcDnEnter, self.txtSrcDN)
        self.Bind(wx.EVT_BUTTON, self.OnSrcDN, self.cbSrcDN)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnBldDnEnter, self.txtBldDN)
        self.Bind(wx.EVT_BUTTON, self.OnBldDN, self.cbBldDN)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnBldFnEnter, self.txtBldFN)
        self.Bind(wx.EVT_BUTTON, self.OnBldFN, self.cbBldFN)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnCfgFnEnter, self.txtCfgFN)
        self.Bind(wx.EVT_BUTTON, self.OnCfgFN, self.cbCfgFN)
        self.Bind(wx.EVT_SPINCTRL, self.OnShaMbSpin, self.spnShaMB)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnShaMbEnter, self.spnShaMB)
        self.Bind(wx.EVT_CHOICE, self.OnShaMbChoice, self.chcShaMB)
        # end wxGlade

    def __initDat__(self):
        global gOpt
        self.sCfgFN=gOpt.sCfgFN      #"ldmStorageFolderCfg.json"
        self.sSrcDN=gOpt.sSrcDN             #'.'
        self.sBldDN=gOpt.sBldDN             #'.'
        self.sBldFN=gOpt.sBldFN             #None
        self.iShaMB=1
        self.iVerbose=10
        # +++++ beg:
        # ----- end:
    def __set_properties(self):
        # begin wxGlade: ldmStorageFolderFrm.__set_properties
        self.SetTitle("ldmStorageFolder")
        self.txtSrcDN.SetToolTip("source directory name")
        self.txtBldDN.SetToolTip("build directory name")
        self.txtBldFN.SetToolTip("build file name\nempty field uses current time in UTC\n0 uses current local time\n1 uses current time in UTC")
        self.txtCfgFN.SetToolTip("configuration file name")
        self.spnShaMB.SetMinSize((20, -1))
        self.chcShaMB.SetMinSize((20, -1))
        self.chcShaMB.SetToolTip("data size to calculate SHA fingerprint in MBytes")
        self.chcShaMB.SetSelection(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ldmStorageFolderFrm.__do_layout
        fgsMain = wx.FlexGridSizer(9, 3, 0, 0)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        szShaMB = wx.BoxSizer(wx.HORIZONTAL)
        lblSrcDN = wx.StaticText(self, wx.ID_ANY, "source DN")
        lblSrcDN.SetToolTip("source folder")
        fgsMain.Add(lblSrcDN, 0, 0, 0)
        fgsMain.Add(self.txtSrcDN, 0, wx.EXPAND, 0)
        fgsMain.Add(self.cbSrcDN, 0, 0, 0)
        lblBldDN = wx.StaticText(self, wx.ID_ANY, "build DN")
        fgsMain.Add(lblBldDN, 0, 0, 0)
        fgsMain.Add(self.txtBldDN, 0, wx.EXPAND, 0)
        fgsMain.Add(self.cbBldDN, 0, 0, 0)
        lblBldFN = wx.StaticText(self, wx.ID_ANY, "build FN")
        fgsMain.Add(lblBldFN, 0, 0, 0)
        fgsMain.Add(self.txtBldFN, 0, wx.EXPAND, 0)
        fgsMain.Add(self.cbBldFN, 0, 0, 0)
        lblCfgFN = wx.StaticText(self, wx.ID_ANY, "configuration file")
        fgsMain.Add(lblCfgFN, 0, 0, 0)
        fgsMain.Add(self.txtCfgFN, 0, wx.EXPAND, 0)
        fgsMain.Add(self.cbCfgFN, 0, 0, 0)
        lblShaMB = wx.StaticText(self, wx.ID_ANY, "data for SHA [MB]")
        fgsMain.Add(lblShaMB, 0, 0, 0)
        szShaMB.Add(self.spnShaMB, 1, wx.EXPAND, 0)
        szShaMB.Add(self.chcShaMB, 2, wx.EXPAND, 0)
        fgsMain.Add(szShaMB, 1, wx.EXPAND, 0)
        lblEmpty063 = wx.StaticText(self, wx.ID_ANY, "")
        fgsMain.Add(lblEmpty063, 0, 0, 0)
        self.SetSizer(fgsMain)
        fgsMain.AddGrowableCol(1)
        self.Layout()
        # end wxGlade

    def OnSrcDnEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sSrcDN=self.txtSrcDN.GetValue()
            if os.path.exists(sSrcDN):
                self.sSrcDN=sSrcDN
                self.oFld.log('OnSrcOnEnter sSrcDN:%s ok',sSrcDN)
            else:
                self.oFld.logErr('OnSrcOnEnter sSrcDN:%s does not exist',sSrcDN)
            # ----- end:get DN
        except:
            self.oFld.logTB()
    def OnSrcDN(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sSrcDN=self.txtSrcDN.GetValue()
            iRet,sSrcDN=ldmGui.getDN(sSrcDN,self,
                         'choose source directory')
            if iRet>0:
                self.sSrcDN=sSrcDN
                self.txtSrcDN.SetValue(self.sSrcDN)
                self.oFld.log('fin:OnSrcDN iRet:%d sSrcDN:%s',
                            iRet,sSrcDN)
            # ----- end:get DN
        except:
            self.oFld.logTB()

    def OnBldDnEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sBldDN=self.txtBldDN.GetValue()
            if os.path.exists(sBldDN):
                self.sBldDN=sBldDN
                self.oFld.log('OnBldOnEnter sBldDN:%s ok',sBldDN)
            else:
                self.oFld.logErr('OnBldOnEnter sBldDN:%s does not exist',sBldDN)
            # ----- end:get DN
        except:
            self.oFld.logTB()
    def OnBldDN(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sBldDN=self.txtBldDN.GetValue()
            iRet,sBldDN=ldmGui.getDN(sBldDN,self,
                         'choose build directory')
            if iRet>0:
                self.sBldDN=sBldDN
                self.txtBldDN.SetValue(self.sBldDN)
                self.oFld.log('fin:OnBldDN iRet:%d sBldDN:%s',
                            iRet,sBldDN)
            # ----- end:get DN
        except:
            self.oFld.logTB()

    def OnBldFnEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sBldFN=self.txtBldFN.GetValue()
            self.sBldFN=sBldFN
            self.oFld.log('OnBldFnEnter sBldFN:%s ok',sBldFN)
        except:
            self.oFld.logTB()

    def OnBldFN(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            # +++++ beg:get DN
            sBldFN=self.txtBldFN.GetValue()
            # ----- end:get DN
            iRet,sBldFN=ldmGui.getFN(sBldFN,self,
                         'choose build file name',
                         lWildCard=self.WILDCARD_JSON,
                         oLog=self.oFld)
            if iRet>0:
                sBldDN,sBldFN=ldmGui.getSplitFN(sBldFN)
                if (sBldDN is not None) and (sBldFN is not None):
                    self.sBldDN,self.sBldFN=sBldDN,sBldFN
                    self.txtBldDN.SetValue(self.sBldDN)
                    self.txtBldFN.SetValue(self.sBldFN)
                    self.oFld.log('fin:OnBldFN iRet:%d sBldFN:%s',
                                iRet,sBldFN)
        except:
            self.oFld.logTB()

    def OnLogFnEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        print("Event handler 'OnLogFnEnter' not implemented!")
        event.Skip()

    def OnLogFN(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        print("Event handler 'OnLogFN' not implemented!")
        event.Skip()

    def OnCfgFnEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        print("Event handler 'OnCfgFnEnter' not implemented!")
        event.Skip()
    def OnCfgFN(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            sCfgFN=self.txtCfgFN.GetValue()
            iRet,sCfgFN=ldmGui.getFN(sCfgFN,self,
                         'choose configuration file name',
                         lWildCard=self.WILDCARD_JSON,
                         oLog=self.oFld)
            if iRet>0:
                self.sCfgFN=sCfgFN
                self.txtCfgFN.SetValue(self.sCfgFN)
                self.oFld.log('fin:OnCfgFN iRet:%d sCfgFN:%s',
                            iRet,sCfgFN)
        except:
            self.oFld.logTB()

    def OnShaMbChoice(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            sVal=self.chcShaMB.GetString(self.chcShaMB.GetSelection())
            iIdx=self.chcShaMB.GetSelection()
            self.oFld.logDbg('OnShaMbChoice sVal:%s iIdx:%d',sVal,iIdx)
            if iIdx==0:
                self.spnShaMB.SetValue(0)
                self.iShaMB=0
            elif iIdx==8:
                self.spnShaMB.SetValue(-1)
                self.iShaMB=-1
            elif iIdx==1:
                self.spnShaMB.SetValue(1)
                self.iShaMB=1
            elif iIdx==2:
                self.spnShaMB.SetValue(2)
                self.iShaMB=2
            elif iIdx==3:
                self.spnShaMB.SetValue(4)
                self.iShaMB=4
            elif iIdx==4:
                self.spnShaMB.SetValue(8)
                self.iShaMB=8
            elif iIdx==5:
                self.spnShaMB.SetValue(16)
                self.iShaMB=16
            elif iIdx==6:
                self.spnShaMB.SetValue(32)
                self.iShaMB=32
            elif iIdx==7:
                self.spnShaMB.SetValue(64)
                self.iShaMB=64
        except:
            self.oFld.logTB()

    def OnShaMbSpin(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        event.Skip()
        try:
            iVal=self.spnShaMB.GetValue()
            self.oFld.logDbg('OnShaMbSpin iVal:%d',iVal)
            self.iShaMB=iVal
            #["disabled", "01 MB", "02 MB", "04 MB", "08 MB", "16 MB", "32 MB", "64 MB", "all data"]
            if iVal==0:
                self.chcShaMB.SetSelection(0)
            elif iVal<0:
                self.chcShaMB.SetSelection(8)
            elif iVal==1:
                self.chcShaMB.SetSelection(1)
            elif iVal==2:
                self.chcShaMB.SetSelection(2)
            elif iVal==4:
                self.chcShaMB.SetSelection(3)
            elif iVal==8:
                self.chcShaMB.SetSelection(4)
            elif iVal==16:
                self.chcShaMB.SetSelection(5)
            elif iVal==32:
                self.chcShaMB.SetSelection(6)
            elif iVal==64:
                self.chcShaMB.SetSelection(7)
            
        except:
            self.oFld.logTB()

    def OnShaMbEnter(self, event):  # wxGlade: ldmStorageFolderFrm.<event_handler>
        print("Event handler 'OnShaMbEnter' not implemented!")
        event.Skip()

