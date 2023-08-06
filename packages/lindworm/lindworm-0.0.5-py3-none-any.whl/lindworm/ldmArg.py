#----------------------------------------------------------------------------
# Name:         ldmArg.py
# Purpose:      argument class
#
# Author:       Walter Obweger
#
# Created:      20200412
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import sys
import traceback

class ldmArg:
    """argument container class to simplify command line argument setup 
    and allow GUI enhancement.
    support classical command line parser package OptionParser for py version < 2.7
    and replacement ArgumentParser.
    """
    MAP_TYPE={'i':int,'r':float,'s':str}
    def __init__(self,sUsage=None,sVer='',iVerbose=0):
        """constructor of argument container

        ### parameter
            sUsage  ... help string
            sVer    ... version number
        """
        self.lArg=[]
        self.dArg={}
        self.oOptRes=None
        self.iVerbose=iVerbose
        self.iIsDbg=1
        if sys.version_info  >= (2,7,0):
            from argparse import ArgumentParser
            self.oOpt=ArgumentParser()
            self.iMode=1
        else:
            from optparse import OptionParser
            self.oOpt=OptionParser(sUsage,version="%prog "+sVer)
            self.iMode=0
        self.__initDftArg__()
    def __initDftArg__(self):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:finalize
            if self.iMode==1:
                self.oOpt.add_argument("-v", type=int, nargs='?' , 
                    default=0,
                    dest="iVerbose", 
                    )
            else:
                self.oOpt.add_option("-v", action="store_true", dest="verbose", default=True)
            # ----- end:finalize
            return iRet
        except:
            traceback.print_exc()
            return -1
    def addOpt(self,sVar,sDft='',sHlp='',sMeta='',sVerbose=None,
                funcVld=None,**kwargs):
        """add option to command line parser

        variable name define command line argument and type,
        applying rules establish standard and reduce effort.
        information made available to implement GUI later.

        For example sVar sCfgFN specify string argument --cfgFN,
        a file name browser shall be used as GUI control.

        ### parameter
            sVar    ... option name
                first letter define type
                    i   ... int
                    r   ... float
                    s   ... string
                following letters build argument
                suffix define GUI control
                    FN  ... file name browser
                    DN  ... directory name browser
                    Chc ... choice
                    Int ... integer
                    Num ... numerical
            sDft    ... default value
            sHlp    ... help string
            sMeta   ... variable example
            sVerbose .. verbose label
                if set, shown automatically if verbose activated
            funcVld ... validation function (callable)
            kwargs  ... keyword arguments passed to funcVld
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sArg=''.join(['--',sVar[1].lower(),sVar[2:]])
            cType=sVar[0]
            # ----- end:initialize
            # +++++ beg:store argument
            if self.iVerbose>0:
                print('addOpt')
                sVrbLv='   '
            if cType in self.MAP_TYPE:
                pass
            else:
                cType='s'       # known type changed to string
            self.lArg.append(sVar)
            self.dArg[sVar]={
                'sArg':sArg,
                'cType':cType,
                'sDft':sDft,
                'sHlp':sHlp,
                'sVar':sVar,
                'sVerbose':sVerbose,
                'funcVld':funcVld,
                'kwargs':kwargs,
                }
            if self.iVerbose>0:
                print(sVrbLv,'sVar',sVar)
                print(sVrbLv,'d:%r'%(self.dArg[sVar]))
            # ----- end:store argument
            # +++++ beg:add to command line parser
            if self.iMode==1:
                self.oOpt.add_argument(
                        sArg,
                        type=self.MAP_TYPE[cType],
                        default=sDft,
                        help=sHlp,metavar=sMeta,
                        dest=sVar
                        )
                return 1
            else:
                self.oOpt.add_option('',sArg,
                        dest=sVar,
                        default=sDft,
                        help=sHlp,
                        metavar=sMeta,
                        )
                return 1
            # ----- end:add to command line parser
            return 0
        except:
            traceback.print_exc()
            return -1
    def prcParse(self,args):
        """
        ### parameter
            args    ... tuple of command line arguments
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:parse
            if self.iMode==1:
                self.oOptRes=self.oOpt.parse_args(args)
                if self.oOptRes.iVerbose<=0:
                    self.iVerbose=0
                else:
                    self.iVerbose=self.oOptRes.iVerbose
            else:
                (self.oOptRes,args)=self.oOpt.parse_args(args=args)
                if self.oOptRes.verbose==False:
                    self.iVerbose=0
            # ----- end:parse
            # +++++ beg:verbose
            if self.iVerbose>0:
                print('self.oOptRes:%r'%(self.oOptRes))
                #print('  len:%d'%(len(self.oOptRes)))
            # ----- end:verbose
            # +++++ beg:finalize
            for sVar in self.lArg:
                try:
                    dDef=self.dArg[sVar]
                    oVal=getattr(self.oOptRes,sVar,dDef.get('sDft',''))
                    if oVal=='None':
                        oVal=None
                    # +++++ beg:validate
                    funcVld=dDef.get('funcVld',None)
                    if funcVld is not None:
                        kwargs=dDef.get('kwargs',{})
                        oVal=funcVld(oVal,**kwargs)
                    # ----- end:validate
                    setattr(self,sVar,oVal)
                    if self.iVerbose>0:
                        sVerbose=dDef.get('sVerbose',None)
                        if  sVerbose is not None:
                            try:
                                cType=dDef.get('cType','s')
                                if cType in ['s']:
                                    print('%20s:%r'%(sVerbose,oVal))
                                elif cType in ['i']:
                                    print('%20s:%d'%(sVerbose,oVal))
                                elif cType in ['r']:
                                    print('%20s:%f'%(sVerbose,oVal))
                                else:
                                    print('%20s:%r'%(sVerbose,oVal))
                            except:
                                traceback.print_exc()
                    iRet+=1
                except:
                    traceback.print_exc()
            # ----- end:finalize
            return iRet
        except:
            traceback.print_exc()
            return -1
    def __initPan__(self,oPar,wNb):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmArg::__initPan__'
            oPar.logDbg('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:
            lWid=[]
            iBrowser=0
            for sArg in self.lArg:
                if sArg.endswith('DN'):
                    iBrowser=1
                elif sArg.endswith('FN'):
                    iBrowser=1
            if iBrowser>0:
                iCol=3
            else:
                iCol=2
            for sArg in self.lArg:
                dDef=self.dArg[sArg]
                sArg=dDef['sArg'][2:]
                sVar=dDef['sVar'][1:]
                lWid.append(['lbl','lbl'+sVar,sArg])
                if sArg.endswith('Chc'):
                    sVal=getattr(self,dDef['sVar'])
                    sHlp=dDef['sHlp']
                    iPos=sHlp.find(';')
                    if iPos>0:
                        lChc=sHlp[iPos+1:].split('|')
                    else:
                        lChc=['???','---']
                    tVal=[sVal,lChc]
                    lWid.append(['chc','chc'+sVar[:-3],tVal])
                    lWid.append([None])
                elif sArg.endswith('Int'):
                    sVal=getattr(self,dDef['sVar'])
                    sHlp=dDef['sHlp']
                    iPos=sHlp.find(';')
                    if iPos>0:
                        lLmt=[s.strip() for s in sHlp[iPos+1:].split('<=')]
                    else:
                        lLmt=['0','x','100']
                    tVal=[sVal,lLmt]
                    lWid.append(['spn','spn'+sVar,tVal])
                    lWid.append([None])
                elif sArg.endswith('Num'):
                    lWid.append([None])
                else:
                    lWid.append(['txt','txt'+sVar,getattr(self,dDef['sVar'])])
                    if iBrowser>0:
                        if sArg.endswith('DN'):
                            lWid.append(['cbd','cb'+sVar,'txt'+sVar])
                        elif sArg.endswith('FN'):
                            sLnk=dDef['sVar'][:-2]+'DN'
                            if sLnk in self.dArg:
                                # +++++ beg:linked variable found
                                sWidLnk='txt'+sLnk[1:]
                                lWid.append(['cbf','cb'+sVar,'txt'+sVar,sWidLnk])
                                # ----- end:linked variable found
                            else:
                                lWid.append(['cbf','cb'+sVar,'txt'+sVar])
                        else:
                            lWid.append([None])
            from lindworm.ldmWidPanel import ldmWidPanelFlxGrd
            wPan=ldmWidPanelFlxGrd(sLogger='ldmArg',iLv=0,
                        parent=oPar,
                        iCol=iCol,lCol=[1],
                        lWid=lWid)
            oPar.pnCLI=wPan
            #oWid=ldmWidSizeRspWid(wNb, -1,mgr=self.mgrMain)
            wNb.AddPage(wPan.GetWid(),'CLI',True)
            # ----- end:
            # +++++ beg:finalize
            oPar.logDbg('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            oPar.logTB()
            return -1
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
