#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#----------------------------------------------------------------------------
# Name:         ldmWidApp.py
# Purpose:      ldmWidApp.py
#               GUI for ldmWidApp
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import os
import logging
import traceback

import wx
import wx.aui
import wx.html
import wx.grid

#import wx.lib.agw.aui as aui
#from wx.lib.agw.aui import aui_switcherdialog as ASD

from lindworm import __version__
from lindworm.ldmArg import ldmArg
from lindworm.ldmWidFrmAui import ldmWidFrmAui

class ldmWidApp(wx.App):
    def __init__(self,
                redirect=False,
                filename=None,
                useBestVisual=False,
                clearSigInt=True,
                title="lindworm center",
                oArg=None,
                clsFrm=None,
                kwargs=None):
        """constructor
        ### parameter
            redirect        ... see wx.App.__init__ help
            filename        ... see wx.App.__init__ help
            useBestVisual   ... see wx.App.__init__ help
            clearSigInt     ... see wx.App.__init__ help
            title           ... title of main frame
            oArg            ... command line argument object
            clsFrm          ... main frame class 
            kwargs          ... keyword arguments for main frame object constructor
        """
        self.sTitle=title
        self.oArg=oArg
        self.clsFrm=clsFrm
        if kwargs is None:
            self.kwargs={}
        else:
            self.kwargs=kwargs
        wx.App.__init__(self,redirect=redirect,
                    filename=filename,
                    useBestVisual=useBestVisual,
                    clearSigInt=clearSigInt)
    def getCfgFN(self,oArg=None):
        """get configuration file name
        ### parameter
            oArg    ... object assumed to hold arguments
        ### return
            filename .. okay
            None    ... error
        """
        try:
            if oArg is not None:
                sCfgFN=oArg.sCfgFN
                return sCfgFN
        except:
            pass
        return None
    def OnInit(self):
        """
        ### parameter
        ### return
            True  ... okay processing done
            False ... okay nop
        """
        # +++++ beg:
        sCfgFN=self.getCfgFN(oArg=self.oArg)
        # ----- end:
        # +++++ beg:
        if self.clsFrm is None:
            self.frmAui = ldmWidFrmAui(iLv=0,
                        sLogger='frmAui',
                        title=self.sTitle,
                        oArg=self.oArg,
                        sCfgFN=sCfgFN,
                        ldmCfg=None)
        else:
            self.frmAui = self.clsFrm(iLv=0,
                        sLogger='frmAui',
                        title=self.sTitle,
                        oArg=self.oArg,
                        sCfgFN=sCfgFN,
                        ldmCfg=None,
                        **self.kwargs)
        # ----- end:
        # +++++ beg:
        self.SetTopWindow(self.frmAui.GetWid())
        self.frmAui.GetWid().Show()
        # ----- end:
        return True

# end of class ldmWidApp

def main(args=None,clsFrm=None,**kwargs):
    # +++++ beg:
    # ----- end:
    
    # +++++ beg:init
    iRet=0
    iVerbose=5                                          # 20190624 wro:set default verbose level
    # ----- end:init
    # +++++ beg:define CLI arguments
    usage = "usage: %prog [options]"
    oArg=ldmArg(sUsage=usage,sVer=__version__,iVerbose=0)
    oArg.addOpt('sCfgFN',
            sDft='ldmStorageFolderCfg.json',
            sHlp='configuration file',
            sVerbose='config FN',
            sMeta='pyGatherMDCfg.json')
    oArg.addOpt('sSrcDN',
            sDft='./',
            sHlp='source folder',
            sVerbose='source DN',
            sMeta='path/to/folder/to/read')
    oArg.addOpt('sBldDN',
            sDft='./',
            sHlp='build directory',
            sVerbose='build DN',
            sMeta='path/to/output/folder')
    oArg.addOpt('sBldFN',
            sDft='./',
            sHlp='build directory',
            sVerbose='build FN',
            sMeta='path/to/output/folder')
    oArg.addOpt('sSource',
            sDft='',
            sHlp='source filter',
            sVerbose='source',
            sMeta='ldm*.md')
    oArg.addOpt('sSizeInt',
            sDft='5',
            sHlp='size boundary;-1 <= x <= 16',
            sVerbose='limit',
            sMeta='full')
    oArg.addOpt('sSelLmtChc',
            sDft='half',
            sHlp='select limit;off|half|full|deep',
            sVerbose='limit',
            sMeta='full')
    oArg.addOpt('sLogFN',
            sDft='./log/ldmStorageFolder.log',
            sHlp='log filename',
            sVerbose='log FN',
            sMeta='./log/ldmStorageFolder.log')
    # ----- end:define CLI arguments
    # +++++ beg:parse command line
    iRet=oArg.prcParse(args)
    # ----- end:parse command line
    # +++++ beg:prepare logging
    if oArg.sLogFN is not None:
        import lindworm.logUtil as logUtil
        logUtil.logInit(oArg.sLogFN,iLevel=logging.DEBUG)
    # ----- end:prepare logging
    # +++++ beg:
    app = ldmWidApp(0,oArg=oArg,clsFrm=clsFrm,kwargs=kwargs)
    app.MainLoop()
    iRet+=1
    # ----- end:
    return iRet

if __name__ == "__main__":
    # +++++ beg:call entry point
    main(args=None)
    # ----- end:call entry point
