#----------------------------------------------------------------------------
# Name:         logUtil.py
# Purpose:      logging utilities
#
# Author:       Walter Obweger
#
# Created:      20191223
# CVS-ID:       $Id$
# Copyright:    (c) 2019 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import logging
import logging.handlers
import traceback

import lindworm.ldmOS as ldmOS

lngFileHandler=None
iVerbose=0

def logInit(sLogFN,sLogger='',iLevel=logging.DEBUG,iNameLen=6):
    """initialize logging
    sLogFN      ... filename
    sLogger     ... module log name
    iLevel      ... detail level
    iNameLen    ... module name length of formatting
    return 
    """
    # +++++ beg:info
    global lngFileHandler
    if iVerbose>0:
        print('logInit:%s'%(sLogFN))
    # ----- end:info
    # +++++ beg:build FN
    try:
        iRet,sBldFN=ldmOS.bldFN(sLogFN,sExt='log')
        if iRet>0:
            sLogFN=sBldFN
    except:
        pass
    # ----- end:build FN
    # +++++ beg:prepare logging
    lngFileHandler=logging.handlers.RotatingFileHandler(sLogFN,backupCount=9)
    lngFileHandler.setLevel(iLevel)
    sFmt='%(asctime)s|%(name)-'+'%d'%(iNameLen)+'s|%(levelname)-8s|%(message)s'
    formatter=logging.Formatter(sFmt)
    lngFileHandler.setFormatter(formatter)
    lngFileHandler.doRollover()
    if iVerbose>0:
        print('lngFileHandler:%r'%(lngFileHandler))
    # ----- end:prepare logging
    # +++++ beg:add root logger
    logging.getLogger('').setLevel(iLevel)
    logging.getLogger('').addHandler(lngFileHandler)
    # ----- end:add root logger
    # +++++ beg:add specific logger
    if sLogger is not None:
        oLog=logGet(sLogger)
        return oLog
    else:
        return None
    # ----- end:add specific logger

def logGet(sLogger,iLevel=logging.DEBUG):
    """get logger
    ### parameter
        sLogger ... logging name
        iLevel  ... logging level
    """
    global lngFileHandler
    if iVerbose>0:
        print('logGet:%s'%(sLogger))
        print('lngFileHandler:%r'%(lngFileHandler))
    oLog=logging.getLogger(sLogger)
    oLog.setLevel(iLevel)
    #if lngFileHandler is not None:
    #    oLog.addHandler(lngFileHandler)
    return oLog

class ldmUtilLog:
    def __init__(self,sLogger='',iLv=0,iLevel=None,iVerbose=0,sOrg=None):
        """constructor
        ### parameter
            sLogger     ... log origin
            iLv         ... trivial logging level
                0       ... debug
                1       ... info
                2       ... warning
                3       ... error
                4       ... critical
                x       ... debug
            iLevel      ... logging level
            iVerbose    ... higher values add more logs
        """
        self.iVerbose=iVerbose
        if iLevel is None:
            if iLv==0:
                iLevel=logging.DEBUG
            elif iLv==1:
                iLevel=logging.INFO
            elif iLv==2:
                iLevel=logging.WARNING
            elif iLv==3:
                iLevel=logging.ERROR
            elif iLv==4:
                iLevel=logging.CRITICAL
            else:
                iLevel=logging.DEBUG
        self.oLog=logGet(sLogger,iLevel)
        self.iIsDbg=0
        if iLevel==logging.DEBUG:
            self.iIsDbg=1
        if sOrg:
            self.sOrg=sOrg
        else:
            self.sOrg=sLogger
    def logDbg(self,sMsg,*args):
        """log debugging data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
        """
        if self.oLog is not None:
            if len(args)==0:
                self.oLog.debug(sMsg)
            else:
                self.oLog.debug(sMsg%args)
    def logInf(self,sMsg,*args):
        """log information data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
        """
        if self.oLog is not None:
            if len(args)==0:
                self.oLog.info(sMsg)
            else:
                self.oLog.info(sMsg%args)
    def logWrn(self,sMsg,*args):
        """log warning data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
        """
        if self.oLog is not None:
            if len(args)==0:
                self.oLog.warning(sMsg)
            else:
                self.oLog.warn(sMsg%args)
    def logErr(self,sMsg,*args):
        """log error data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
        """
        if self.oLog is not None:
            if len(args)==0:
                self.oLog.error(sMsg)
            else:
                self.oLog.error(sMsg%args)
    def logCri(self,sMsg,*args):
        """log critical data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
        """
        if self.oLog is not None:
            if len(args)==0:
                self.oLog.critical(sMsg)
            else:
                self.oLog.critical(sMsg%args)
    def log(self,sMsg,*args,iLv=0):
        """log data
        ### parameter
            sMsg    ... message
            args    ... arguments for mmessage
            iLv     ... trivial logging level
                0   ... debug
                1   ... info
                2   ... warning
                3   ... error
                4   ... critical
                x   ... debug
        """
        if iLv==0:
            self.logDbg(sMsg,*args)
        elif iLv==1:
            self.logInf(sMsg,*args)
        elif iLv==2:
            self.logWrn(sMsg,*args)
        elif iLv==3:
            self.logErr(sMsg,*args)
        elif iLv==4:
            self.logCri(sMsg,*args)
        else:
            self.logDbg(sMsg,*args)
    def logTB(self):
        self.oLog.error(traceback.format_exc())
    def GetVerbose(self,iVerbose=-1):
        """get verbose level 
        ### parameter
        ### return
            True    ... object verbose >= iVerbose
            False   ... object verbose < iVerbose
            number  ... object verbose if iVerbose < 0
        """
        if iVerbose>=0:
            if self.iVerbose>=iVerbose:
                return True
            else:
                return False
        else:
            return self.iVerbose
    def GetVerboseDbg(self,iVerbose=-1):
        """get verbose level in debugging mode
        ### parameter
        ### return
            True    ... object verbose >= iVerbose
            False   ... object verbose < iVerbose
                    ... log level not in debugging
            number  ... object verbose if iVerbose < 0
        """
        if self.iIsDbg>0:
            return self.GetVerbose(iVerbose=iVerbose)
        else:
            return False
