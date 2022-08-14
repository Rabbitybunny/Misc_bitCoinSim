import sys, math, re, time, os
import numpy as np
import numpy.random as rand
import random
import hashlib
from copy import deepcopy
import pickle
try:
    import tkinter as Tk
except:
    import Tkinter as Tk

from bitCoinFuncs import *
#Txn for transaction
#BlkChn for blockchain


VERBOSITY   = 2;
COMMUTERATE = 0.5;
MINERATE    = {"A": 0.1, "B": 0.04, "C": 0.02, "D": 0.01, "E": 0.04}
TXNRATE     = {"A": 0.3, "B": 0.6,  "C": 0.6,  "D": 0.6,  "E": 0.0}
#COMMUTERATE = 1.0;
#MINERATE    = {"A": 0.2, "B": 0.08, "C": 0.04, "D": 0.02, "E": 0.1}
#TXNRATE     = {"A": 0.5, "B": 0.9,  "C": 0.9,  "D": 0.9,  "E": 0.0}
TRACKLENGTH=10;
SAVEFILENAME="SavedBlockchain.pickle";
rand.seed(2);#rand.seed(int(time.time()));

TXNARROWCOORD = {"AB": [40-5,  65,  150-5, 120], "BA": [150+5, 120, 40+5,  65],
                 "AC": [40-5,  65,  200-5, 210], "CA": [200+5, 210, 40+5,  65],
                 "AD": [40-5,  65,  165-5, 302], "DA": [165+5, 302, 40+5,  65],
                 "AE": [40-5,  65,  40-5,  375], "EA": [40+5,  375, 40+5,  65],
                 "BC": [165-5, 140, 200-5, 210], "CB": [200+5, 210, 165+5, 140],
                 "BD": [165-5, 140, 165-5, 302], "DB": [165+5, 302, 165+5, 140],
                 "BE": [165-5, 140, 40-5,  375], "EB": [40+5,  375, 165+5, 140],
                 "CD": [200-5, 240, 165-5, 302], "DC": [160+5, 302, 200+5, 240],
                 "CE": [200-5, 240, 40-5,  375], "EC": [40+5,  375, 200+5, 240],
                 "DE": [150-5, 325, 40-5,  375], "ED": [40+5,  375, 150+5, 325]}; 
COMMARROWCOORD = {"AB": [40,  65,   120, 70,   160, 95],  "BA": [150, 120,  50, 120,   40,  65],
                  "AC": [40,  65,   120, 80,   200, 210], "CA": [200, 210,  50, 180,   40,  65],
                  "AD": [40,  65,   140, 100,  165, 300], "DA": [165, 305,  10, 200,   40,  65],
                  "AE": [40,  65,   80,  250,  40,  375], "EA": [40,  375,  10,  250,  40,  65],
                  "BC": [165, 140,  200, 150,  220, 200], "CB": [200, 210,  110, 180,  165, 140],
                  "BD": [165, 140,  200, 200,  165, 310], "DB": [165, 305,  100, 200,  165, 140],
                  "BE": [165, 140,  200, 250,  40,  375], "EB": [40,  375,  30,  230,  165, 140],
                  "CD": [200, 230,  120, 250,  150, 315], "DC": [160, 305,  140, 250,  200, 235],
                  "CE": [200, 240,  170, 320,  40,  375], "EC": [40,  375,  60,  300,  200, 240],
                  "DE": [150, 330,  125, 370,  40,  375], "ED": [40,  375,  50,  320,  150, 325]};
MINEDCOORD = {"A": [50, 20], "B": [170, 95], "C": [230, 200], "D": [170, 305], "E": [50, 380]}
##################################################################################################################
class bitCoinSim(Tk.Tk):
    def __init__(self, inputUserList):
        super().__init__();
        self.title("Bitcoin Simulation");
        self.configure(background="white"); 

        self.epoch = 0;
        self.epoch_track = 0;
        self.userList = inputUserList;
        self.userList0   = deepcopy(inputUserList);
        self.minedBlock  = [];
        self.shareList   = [];
        self.warningList = [];
        self.auto = False;
        self.miningOnUserE         = False;
        self.falseTxnOnUserE       = False;
        self.wantedTxnUserE        = "";
        self.doubleSpendingOnUserE = False;  
        self.alterBlockOnUserE     = False;
        self.badBlockIdxE          = -1;

        self.userLists    = [];
        self.minedBlocks  = [];
        self.shareLists   = [];
        self.warningLists = [];
        self.miningOnUserEs         = [];
        self.falseTxnOnUserEs       = [];
        self.wantedTxnUserEs        = [];
        self.doubleSpendingOnUserEs = [];
        self.alterBlockOnUserEs     = [];
        self.badBlockIdxEs          = [];

        self.bReset    = Tk.Button(self);
        self.bSave     = Tk.Button(self);
        self.bBackward = Tk.Button(self);
        self.bForward  = Tk.Button(self);
        self.bAct1 = Tk.Button(self);
        self.bAct0 = Tk.Button(self);
        self.bAct2 = Tk.Button(self);
        self.bAct3 = Tk.Button(self);
        self.bAct4 = Tk.Button(self);
        self.bAct5 = Tk.Button(self);
        self.bReset   .config(          width=14, borderwidth=2);
        self.bSave    .config(          width=14, borderwidth=2);
        self.bBackward.config(                    borderwidth=2);
        self.bForward .config(                    borderwidth=2);
        self.bAct1    .config(height=1, width=21, borderwidth=2);
        self.bAct0    .config(          width=4,  borderwidth=2);
        self.bAct2    .config(height=1,           borderwidth=2);
        self.bAct3    .config(height=1,           borderwidth=2);
        self.bAct4    .config(height=1,           borderwidth=2);
        self.bAct5    .config(height=1,           borderwidth=2);
        self.bReset   .grid  (row=0, column=2,               sticky="ns");
        self.bSave    .grid  (row=0, column=3,               sticky="ns");
        self.bBackward.grid  (row=1, column=2,               sticky="nswe");
        self.bForward .grid  (row=1, column=3,               sticky="nswe");
        self.bAct1    .grid  (row=1, column=0);
        self.bAct0    .grid  (row=1, column=1,               sticky="ns");
        self.bAct2    .grid  (row=2, column=0, columnspan=2, sticky="we");
        self.bAct3    .grid  (row=3, column=0, columnspan=2, sticky="we");
        self.bAct4    .grid  (row=4, column=0, columnspan=2, sticky="we");
        self.bAct5    .grid  (row=5, column=0, columnspan=2, sticky="we");
        self.bReset   .config(command=lambda:self.playerMove("Reset"));
        self.bSave    .config(command=lambda:self.playerMove("Save"));
        self.bBackward.config(command=lambda:self.playerMove("Backward"));
        self.bForward .config(command=lambda:self.playerMove("Forward"));
        self.bAct1    .config(command=lambda:self.playerMove("Act1"));
        self.bAct0    .config(command=lambda:self.playerMove("Act0"));
        self.bAct2    .config(command=lambda:self.playerMove("Act2"));
        self.bAct3    .config(command=lambda:self.playerMove("Act3"));
        self.bAct4    .config(command=lambda:self.playerMove("Act4"));
        self.bAct5    .config(command=lambda:self.playerMove("Act5"));
        self.bReset   .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bSave    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bBackward.config(highlightbackground="black", background="white", activebackground="light grey");
        self.bForward .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct1    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct0    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct2    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct3    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct4    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bAct5    .config(highlightbackground="black", background="white", activebackground="light grey");
        self.bReset   .config(font="times 14");
        self.bSave    .config(font="times 14");
        self.bBackward.config(font="times 14");
        self.bForward .config(font="times 14");
        self.bAct1    .config(font="times 20", anchor="w");
        self.bAct0    .config(font="times 20", anchor="w");
        self.bAct2    .config(font="times 20", anchor="w");
        self.bAct3    .config(font="times 20", anchor="w");
        self.bAct4    .config(font="times 20", anchor="w");
        self.bAct5    .config(font="times 20", anchor="w");
        self.buttons = {"Reset": self.bReset, "Save": self.bSave,\
                        "Backward": self.bBackward, "Forward": self.bForward,\
                        "Act1": self.bAct1, "Act0": self.bAct0, "Act2": self.bAct2,\
                        "Act3": self.bAct3, "Act4": self.bAct4, "Act5": self.bAct5};

        self.lEpoch        = Tk.Label(self);
        self.lGlobalBlkChn = Tk.Label(self);
        self.lMinedBlk     = Tk.Label(self);
        self.lWal          = Tk.Label(self);
        self.cWal          = Tk.Canvas(self);
        self.lMem0         = Tk.Label(self);
        self.lMemA         = Tk.Label(self);
        self.lMemB         = Tk.Label(self);
        self.lMemC         = Tk.Label(self);
        self.lMemD         = Tk.Label(self);
        self.lMemE         = Tk.Label(self);
        self.lBlkChn0      = Tk.Label(self);
        self.lBlkChnA      = Tk.Label(self);
        self.lBlkChnB      = Tk.Label(self);
        self.lBlkChnC      = Tk.Label(self);
        self.lBlkChnD      = Tk.Label(self);
        self.lBlkChnE      = Tk.Label(self);
        self.lWarning      = Tk.Label(self);
        self.props = [];
        self.lEpoch       .config(height=1, bg="white");
        self.lGlobalBlkChn.config(width=58, bg="white", borderwidth=1, relief="groove");
        self.lMinedBlk    .config(          bg="white", borderwidth=1, relief="groove");
        self.lWal         .config(          bg="snow2");
        self.cWal         .config(          bg="white");
        self.lMem0        .config(height=1, bg="snow3");
        self.lMemA        .config(height=3, bg="white", borderwidth=1, relief="solid");
        self.lMemB        .config(height=3, bg="white", borderwidth=1, relief="solid");
        self.lMemC        .config(height=3, bg="white", borderwidth=1, relief="solid");
        self.lMemD        .config(height=3, bg="white", borderwidth=1, relief="solid");
        self.lMemE        .config(height=3, bg="white", borderwidth=1, relief="solid");
        self.lBlkChn0     .config(          bg="snow2");
        self.lBlkChnA     .config(          bg="white", borderwidth=1, relief="solid");
        self.lBlkChnB     .config(          bg="white", borderwidth=1, relief="solid");
        self.lBlkChnC     .config(          bg="white", borderwidth=1, relief="solid");
        self.lBlkChnD     .config(          bg="white", borderwidth=1, relief="solid");
        self.lBlkChnE     .config(          bg="white", borderwidth=1, relief="solid");
        self.lWarning     .config(          bg="white", borderwidth=1, relief="solid");
        self.lEpoch       .grid(row=0,  column=0,                          sticky="we");
        self.lGlobalBlkChn.grid(row=0,  column=4, rowspan=4,               sticky="ns");
        self.lMinedBlk    .grid(row=4,  column=4, rowspan=2,               sticky="nswe");
        self.lWal         .grid(row=6,  column=0, columnspan=2,            sticky="nswe");
        self.cWal         .grid(row=7,  column=0, columnspan=2, rowspan=5, sticky="nswe");
        self.lMem0        .grid(row=6,  column=2, columnspan=2,            sticky="we");
        self.lMemA        .grid(row=7,  column=2, columnspan=2,            sticky="we");
        self.lMemB        .grid(row=8,  column=2, columnspan=2,            sticky="we");
        self.lMemC        .grid(row=9,  column=2, columnspan=2,            sticky="we");
        self.lMemD        .grid(row=10, column=2, columnspan=2,            sticky="we");
        self.lMemE        .grid(row=11, column=2, columnspan=2,            sticky="we");
        self.lBlkChn0     .grid(row=6,  column=4,                          sticky="nswe");
        self.lBlkChnA     .grid(row=7,  column=4,                          sticky="nswe");
        self.lBlkChnB     .grid(row=8,  column=4,                          sticky="nswe");
        self.lBlkChnC     .grid(row=9,  column=4,                          sticky="nswe");
        self.lBlkChnD     .grid(row=10, column=4,                          sticky="nswe");
        self.lBlkChnE     .grid(row=11, column=4,                          sticky="nswe");
        self.lWarning     .grid(row=12, column=0, columnspan=5,            sticky="we");
        self.lEpoch       .config(font="times 20", anchor="w",  justify="left");
        self.lGlobalBlkChn.config(font="times 16", anchor="nw", justify="left");
        self.lMinedBlk    .config(font="times 16", anchor="nw", justify="left");
        self.lWal         .config(font="times 20", anchor="w",  justify="left");
        self.lMem0        .config(font="times 20", anchor="nw", justify="left");
        self.lMemA        .config(font="times 20", anchor="nw", justify="left");
        self.lMemB        .config(font="times 20", anchor="nw", justify="left");
        self.lMemC        .config(font="times 20", anchor="nw", justify="left");
        self.lMemD        .config(font="times 20", anchor="nw", justify="left");
        self.lMemE        .config(font="times 20", anchor="nw", justify="left");
        self.lBlkChn0     .config(font="times 20", anchor="nw", justify="left");
        self.lBlkChnA     .config(font="times 16", anchor="nw", justify="left");
        self.lBlkChnB     .config(font="times 16", anchor="nw", justify="left");
        self.lBlkChnC     .config(font="times 16", anchor="nw", justify="left");
        self.lBlkChnD     .config(font="times 16", anchor="nw", justify="left");
        self.lBlkChnE     .config(font="times 16", anchor="nw", justify="left");
        self.lWarning     .config(font="times 12", anchor="nw", justify="left");
        self.labels = {"Epoch": self.lEpoch, "GlobalBlkChn": self.lGlobalBlkChn, "MinedBlk": self.lMinedBlk,\
                       "lWal": self.lWal, "cWal": self.cWal, "props": self.props,\
                       "WalA": None, "WalB": None, "WalC": None, "WalD": None, "WalE": None,\
                       "Mem0": self.lMem0, "MemA": self.lMemA, "MemB": self.lMemB,\
                       "MemC": self.lMemC, "MemD": self.lMemD, "MemE": self.lMemE,\
                       "BlkChn0": self.lBlkChn0, "BlkChnA": self.lBlkChnA, "BlkChnB": self.lBlkChnB,\
                       "BlkChnC": self.lBlkChnC, "BlkChnD": self.lBlkChnD, "BlkChnE": self.lBlkChnE,\
                       "Warning": self.lWarning};
        self.reset();
    def reset(self):
        self.epoch = 0;
        self.epoch_track = 0;
        self.userList    = deepcopy(self.userList0);
        self.minedBlock  = [];
        self.shareList   = [];
        self.warningList = [];
        self.auto = False;
        self.miningOnUserE         = False;
        self.falseTxnOnUserE       = False;
        self.wantedTxnUserE        = "";
        self.doubleSpendingOnUserE = False;
        self.alterBlockOnUserE     = False;
        self.badBlockIdxE          = -1;       
 
        self.userLists    = [];
        self.minedBlocks  = [];
        self.shareLists   = [];
        self.warningLists = [];
        self.miningOnUserEs         = [];
        self.falseTxnOnUserEs       = [];
        self.wantedTxnUserEs        = [];
        self.doubleSpendingOnUserEs = [];
        self.alterBlockOnUserEs     = [];
        self.badBlockIdxEs          = [];

        self.buttons["Reset"]   .config(text="RESET");
        self.buttons["Save"]    .config(text="SAVE");
        self.buttons["Backward"].config(text="<<", state="disabled");
        self.buttons["Forward"] .config(text=">>", state="disabled");
        self.buttons["Act1"].config(text="Do Nothing",             state="normal");
        self.buttons["Act0"].config(text="Auto",                   state="normal");
        self.buttons["Act2"].config(text="Mine",                   state="normal");
        self.buttons["Act3"].config(text="False Transaction",      state="normal");
        self.buttons["Act4"].config(text="Double Spending",        state="normal");
        self.buttons["Act5"].config(text="Altering Block Content", state="normal");
        self.labels["lWal"]   .config(text="User(Wallet)");
        self.labels["Mem0"]   .config(text="User Memory Pool");
        self.labels["BlkChn0"].config(text="User Blockchain");

        self.userLists   .append(deepcopy(self.userList));
        self.minedBlocks .append(self.minedBlock);
        self.shareLists  .append(self.shareList);
        self.warningLists.append(self.warningList);
        self.miningOnUserEs        .append(self.miningOnUserE);
        self.falseTxnOnUserEs      .append(self.falseTxnOnUserE);
        self.wantedTxnUserEs       .append(self.wantedTxnUserE);
        self.doubleSpendingOnUserEs.append(self.doubleSpendingOnUserE);
        self.alterBlockOnUserEs    .append(self.alterBlockOnUserE);
        self.badBlockIdxEs         .append(self.badBlockIdxE);
        self.generalDisplay();
    def playerMove(self, bID):
        if bID == "Reset":
            self.reset();
        elif bID == "Save":
            self.saveProgress();
        elif bID == "Backward":
            self.backwardInspect();
        elif bID == "Forward":
            self.forwardInspect();
        elif bID == "Act0":
            self.advanceEpochAutoInit();
        elif "Act" in bID:
            if bID == "Act1":
                pass;
            elif bID == "Act2":
                self.miningOnUserE = True;
            elif bID == "Act3":
                self.falseTxnUserE(); 
            elif bID == "Act4":
                self.doubleSpendingUserE();
            elif bID == "Act5":
                self.alterBlockUserE();
            self.buttons["Backward"].config(state="normal");
            self.advanceEpoch();
    def advanceEpoch(self):
        verbosity = 1*VERBOSITY;
        self.epoch += 1;
        self.epoch_track = self.epoch*1;
        if verbosity >= 1:
            print("\nEpoch " + str(self.epoch_track) + " ======================================================");
        rand.shuffle(self.userList);
        #for Act4
        user = [u for u in self.userList if u.content()["name"] == "E"][0];
        if self.alterBlockOnUserE == True:
            user.setMalicious(True);
        else:
            user.setMalicious(False);
        #generate transactions
        self.shareList = [];
        self.warningList = [];
        for u, user in enumerate(self.userList):
            uName    = user.content()["name"];
            uWallet  = user.content()["wallet"];
            uMempool = user.content()["mempool"];
            uBlkChn  = user.content()["blockchain"];
            if rand.uniform() < user.getTxnRate():
                userToIdx = (u+int(np.ceil(rand.uniform()*(len(self.userList)-1))))%len(self.userList);
                userTo = self.userList[userToIdx];
                txnStr = uName + "=>" + userTo.content()["name"];
                txnStr += ":" + str(int(np.ceil(rand.uniform()*uWallet)));
                txnStr += ":" + str(int(np.ceil(time.time()*1e3)));
                if rand.uniform() < user.getTxnRate()*userTo.getTxnRate():  #note: TxnRate in product
                    uMempool.append(txnStr);
                    warnMem = user.updateMempool(uMempool, self.userList, selfPosted=True);
                    self.warningList += warnMem; 
        #sharing mempool and blockchain 
        for u, user in enumerate(self.userList):
            uMempool = user.content()["mempool"];
            uBlkChn  = user.content()["blockchain"];
            ###previous user 
            userPre    = self.userList[(u-1+len(self.userList))%len(self.userList)];
            namePre    = userPre.content()["name"];
            mempoolPre = userPre.content()["mempool"];
            blkChnPre  = userPre.content()["blockchain"];
            if rand.uniform() < COMMUTERATE:
                memToAdd = [t for t in mempoolPre if t not in uMempool];
                uMempool = uMempool + memToAdd;
                warnMem = user.updateMempool(uMempool, self.userList);
                valiVali, warnVali = user.checkTxnValidityFromBlkChn(namePre, blkChnPre);
                valiDup,  warnDup  = user.checkTxnDuplicateFromBlkChn(namePre, blkChnPre);
                valiBlkChn, warnBlkChn = user.checkBlkChnValidity(uBlkChn);
                if (valiVali == True) and (valiDup == True) and (valiBlkChn == True) and\
                   (user.checkBlkChnLength(blkChnPre) == True):
                    user.updateBlkChn(blkChnPre);
                    user.updateTxnFromBlkChn();
                self.shareList.append(namePre + user.content()["name"]);
                self.warningList += warnMem + warnVali + warnDup + warnBlkChn;
        #print out: later for encryptions
        if verbosity >= 2:
            totCoin = 0;
            for u, user in enumerate(self.userList):
                uName    = user.content()["name"];
                uWallet  = user.content()["wallet"];
                uMempool = user.content()["mempool"];
                uBlkChn  = user.content()["blockchain"];
                txns = [(t.split(":")[0]+":"+t.split(":")[1]) for t in uMempool];
                print(uName, "("+str(uWallet)+"):",txns);
                for i, block in enumerate(uBlkChn[-5:]):
                    idx = i;
                    timeTime = block.content()["timeTime"];
                    thisHash = block.content()["thisHash"];
                    preHash  = block.content()["preHash"];
                    txns = block.content()["transactions"];
                    if len(uBlkChn) > 5:
                        idx = len(uBlkChn) - 5 + i;
                    if "genesis" not in txns: 
                        txns = [(t.split(":")[0] + ":" + t.split(":")[1]) for t in txns];
                    print("  ", idx, txns);
                    print("    time:    ", timeTime);
                    print("    preHash: ", preHash);
                    print("    thisHash:", thisHash);
                totCoin += uWallet;
            print("Tot coins:", totCoin);
            print(self.warningList);
        #mining 
        self.minedBlock = [];
        for u, user in enumerate(self.userList):
            uName   = user.content()["name"];
            uBlkChn = user.content()["blockchain"];
            valiVali,   warnVali   = user.checkTxnValidityFromBlkChn(uName, uBlkChn);
            valiDup,    warnDup    = user.checkTxnDuplicateFromBlkChn(uName, uBlkChn);
            valiBlkChn, warnBlkChn = user.checkBlkChnValidity(uBlkChn);
            if ( (uName != "E") or (self.miningOnUserE == True) ) and\
               (rand.uniform() < user.getMineRate()) and\
               (valiVali == True) and (valiDup == True) and (valiBlkChn == True):
                user.mine();
                user.updateTxnFromBlkChn();
                uBlkChn = user.content()["blockchain"];
                self.minedBlock.append([len(uBlkChn)-1, uBlkChn[-1]]);
            self.warningList += warnVali + warnDup + warnBlkChn;
        #for Act3
        user = [u for u in self.userList if u.content()["name"] == "E"][0];
        uMempool = user.content()["mempool"];    
        if self.wantedTxnUserE not in uMempool:
            self.falseTxnOnUserE = False;
            self.wantedTxnUserE = "";
            if self.auto == False:
                self.buttons["Act3"].config(state="normal");
        #saving for backwardInspect
        self.userLists   .append(deepcopy(self.userList));
        self.minedBlocks .append(deepcopy(self.minedBlock));
        self.shareLists  .append(deepcopy(self.shareList));
        self.warningLists.append(deepcopy(self.warningList));
        self.miningOnUserEs        .append(deepcopy(self.miningOnUserE));
        self.falseTxnOnUserEs      .append(deepcopy(self.falseTxnOnUserE));
        self.wantedTxnUserEs       .append(deepcopy(self.wantedTxnUserE));
        self.doubleSpendingOnUserEs.append(deepcopy(self.doubleSpendingOnUserE));
        self.alterBlockOnUserEs    .append(deepcopy(self.alterBlockOnUserE));
        self.badBlockIdxEs         .append(deepcopy(self.badBlockIdxE));
        if len(self.userLists) > TRACKLENGTH:
            self.userLists   .pop(0);
            self.minedBlocks .pop(0);
            self.shareLists  .pop(0);
            self.warningLists.pop(0);
            self.miningOnUserEs        .pop(0);
            self.falseTxnOnUserEs      .pop(0);
            self.wantedTxnUserEs       .pop(0);
            self.doubleSpendingOnUserEs.pop(0);
            self.alterBlockOnUserEs    .pop(0);
            self.badBlockIdxEs         .pop(0);
        self.generalDisplay();
    def generalDisplay(self, trackID=None):
        userListDisp    = self.userList;
        minedBlockDisp  = self.minedBlock;
        shareListDisp   = self.shareList;
        warningListDisp = self.warningList;
        miningOnUserEDisp         = self.miningOnUserE;
        falseTxnOnUserEDisp       = self.falseTxnOnUserE;
        wantedTxnUserEDisp        = self.wantedTxnUserE;
        doubleSpendingOnUserEDisp = self.doubleSpendingOnUserE;
        alterBlockOnUserEDisp     = self.alterBlockOnUserE;
        badBlockIdxEDisp          = self.badBlockIdxE;
        if trackID is not None:
            userListDisp    = self.userLists[trackID];
            minedBlockDisp  = self.minedBlocks[trackID];
            shareListDisp   = self.shareLists[trackID];
            warningListDisp = self.warningLists[trackID];
            miningOnUserEDisp         = self.miningOnUserEs[trackID];
            falseTxnOnUserEDisp       = self.falseTxnOnUserEs[trackID];
            wantedTxnUserEDisp        = self.wantedTxnUserEs[trackID];
            doubleSpendingOnUserEDisp = self.doubleSpendingOnUserEs[trackID];
            alterBlockOnUserEDisp     = self.alterBlockOnUserEs[trackID];
            badBlockIdxEDisp          = self.badBlockIdxEs[trackID];
        self.labels["Epoch"].config(fg="black", text=("Epoch: " + str(self.epoch_track)));
        for prop in self.labels["props"]:
            self.labels["cWal"].delete(prop);
        self.labels["props"] = [];
        #get globalShareBlockNum
        globalShareBlockNum = pow(10, 12);
        for user in userListDisp:
            uBlkChn = user.content()["blockchain"];
            if len(uBlkChn) < globalShareBlockNum:
                globalShareBlockNum = len(uBlkChn);
        sameFinalBlock = False;
        while sameFinalBlock == False:
            sameFinalBlock = True;
            refBlock = userListDisp[0].content()["blockchain"][globalShareBlockNum-1];
            for user in userListDisp:
                block = user.content()["blockchain"][globalShareBlockNum-1];
                if refBlock.content()["thisHash"] != block.content()["thisHash"]:
                    sameFinalBlock = False;
                    globalShareBlockNum -= 1;
                    break;
        #display global blockchain
        textGBlkChn = "Globally shared blockchain:\n"; 
        for i, block in enumerate(userListDisp[0].content()["blockchain"]\
                                  [globalShareBlockNum-5:globalShareBlockNum]):
            txns = block.content()["transactions"];
            idx = max(globalShareBlockNum-5, 0) + i;
            if "genesis" not in txns:
                txns = [(t.split(":")[0] + ":" + t.split(":")[1]) for t in txns];
            textGBlkChn += "     " + str(idx) + ":" + str(txns).replace("'", "") + "\n";
        self.labels["GlobalBlkChn"].config(text=textGBlkChn);
        #display communication
        for comm in shareListDisp:
            curvedArrow = self.labels["cWal"].create_line(*COMMARROWCOORD[comm], arrow=Tk.LAST,\
                                                          smooth=1, width=2, arrowshape=(8,10,3), fill="green");
            self.labels["props"].append(curvedArrow);
        #display user wallet, mempool, and blockchain
        dictWal = {};
        for user in userListDisp:
            name    = user.content()["name"];
            wallet  = user.content()["wallet"];
            mempool = user.content()["mempool"];
            uBlkChn = user.content()["blockchain"];
            dictWal[name] = name + "(" + str(wallet) + ")";
            mempool = [(t.split(":")[0] + ":" + t.split(":")[1]) for t in mempool];
            textUMem = "";
            spaceMemIter = 0;
            for i, txn in enumerate(mempool):
                textUMem += txn;
                if spaceMemIter == 1:
                    textUMem += "\n";
                    spaceMemIter = -1;
                else:
                    textUMem += "  ";
                spaceMemIter += 1;
                if ((name+"=>") in txn) and ("Rm_" not in txn): 
                    txnDigest = txn.split("=>");
                    sender = txnDigest[0];
                    receiver = txnDigest[1].split(":")[0];
                    arrow = self.labels["cWal"].create_line(*TXNARROWCOORD[sender+receiver], arrow=Tk.LAST,\
                                                            width=4, arrowshape=(16,20,6), fill="blue");
                    self.labels["props"].append(arrow);
            self.labels["Mem" + name].config(text=textUMem);
            textUBlkChn = "";
            activateAct5 = (name == "E") and (self.badBlockIdxE > 0);
            if (len(uBlkChn) > globalShareBlockNum) or (activateAct5 == True):
                dispIdx = [len(uBlkChn)-1];
                while (len(dispIdx) < 4) and (dispIdx[0] > globalShareBlockNum):
                    dispIdx.insert(0, dispIdx[0]-1);
                if activateAct5 == True:
                    while (len(dispIdx) < 4) and (dispIdx[0] > self.badBlockIdxE):
                        dispIdx.insert(0, dispIdx[0]-1);
                for i, idx in enumerate(dispIdx):
                    block = uBlkChn[idx];
                    txns = block.content()["transactions"];
                    txns = [(t.split(":")[0] + ":" + t.split(":")[1]) for t in txns];
                    textUBlkChn += "     ";
                    textUBlkChn += str(idx) + ":" + str(txns).replace("'", "") + "\n";
                textUBlkChn = textUBlkChn[:-1];
            self.labels["BlkChn" + name].config(text=textUBlkChn);
        self.labels["cWal"].delete(self.labels["WalA"]); self.labels["WalA"] = None;
        self.labels["cWal"].delete(self.labels["WalB"]); self.labels["WalB"] = None;
        self.labels["cWal"].delete(self.labels["WalC"]); self.labels["WalC"] = None;
        self.labels["cWal"].delete(self.labels["WalD"]); self.labels["WalD"] = None;
        self.labels["cWal"].delete(self.labels["WalE"]); self.labels["WalE"] = None;
        self.labels["WalA"] = self.labels["cWal"].create_text(20,  45,  font="times 40", fill="black",\
                                                              anchor="w", justify="left", text=dictWal["A"]);
        self.labels["WalB"] = self.labels["cWal"].create_text(150, 120, font="times 40", fill="black",\
                                                              anchor="w", justify="left", text=dictWal["B"]);
        self.labels["WalC"] = self.labels["cWal"].create_text(200, 225, font="times 40", fill="black",\
                                                              anchor="w", justify="left", text=dictWal["C"]);
        self.labels["WalD"] = self.labels["cWal"].create_text(150, 330, font="times 40", fill="black",\
                                                              anchor="w", justify="left", text=dictWal["D"]);
        self.labels["WalE"] = self.labels["cWal"].create_text(20,  405, font="times 40", fill="black",\
                                                              anchor="w", justify="left", text=dictWal["E"]);
        #display mined blocks
        textMine = "Newly mined blocks:\n";
        minedName = "";
        minedNames = [];
        for [idx, block] in minedBlockDisp:
            txns = block.content()["transactions"];
            if "genesis" not in txns:
                txns = [(t.split(":")[0] + ":" + t.split(":")[1]) for t in txns];
                minedName = txns[-1].split("=>")[1][0];
                minedNames.append(minedName);
                minedText = self.labels["cWal"].create_text(*MINEDCOORD[minedName], fill="orange",\
                                                            font="times 20 italic", text="Mined");
                self.labels["props"].append(minedText);
            textMine += "    " + str(idx) + ":" + str(txns).replace("'", "") + "\n";
        textMine = textMine[:-1]; 
        if len(minedBlockDisp) == 0:
            self.labels["MinedBlk"].config(text=textMine, fg="black");
        else:
            self.labels["MinedBlk"].config(text=textMine, fg="orange");
        #display Acts:
        if ("E" not in minedNames) and (miningOnUserEDisp == True):
            failedText = self.labels["cWal"].create_text(*MINEDCOORD["E"], fill="red",\
                                                         font="times 20 italic", text="Failed");
            self.labels["props"].append(failedText);
        if (falseTxnOnUserEDisp == True) or (doubleSpendingOnUserEDisp == True):
            self.lMemE.config(fg="red");
        else:
            self.lMemE.config(fg="black");
        if self.alterBlockOnUserE == True:
            self.lBlkChnE.config(fg="red");
        else:
            self.lBlkChnE.config(fg="black");
        self.miningOnUserE     = False;
        #display warnings
        textWarn = "";
        for warning in warningListDisp:
            textWarn += warning.replace("WARNING:", "") + "\n";
        textWarn = textWarn[:-1];
        self.labels["Warning"].config(text=textWarn);
    def setBottomState(self, state):
        if state not in ["normal", "disable"]:
            print("WARNING: setBottomState: unrecognizable state");
            sys.exit();
        for bottomName in ["Reset", "Save", "Act1", "Act2", "Act3", "Act4" ,"Act5"]:
            self.buttons[bottomName].config(state=state);
    def advanceEpochAutoInit(self):
        if self.auto == False:
            self.auto = True;
            self.buttons["Act0"]    .config(text="Stop");
            self.buttons["Backward"].config(state="disable");
            self.setBottomState("disable");
            self.advanceEpochAuto();
        elif self.auto == True:
            self.auto = False;
            self.buttons["Act0"]    .config(text="Auto");
            self.buttons["Backward"].config(state="normal");
            self.setBottomState("normal");
            if self.falseTxnOnUserE == True:
                self.buttons["Act3"].config(state="disable");
    def advanceEpochAuto(self):
        if self.auto == True:
            self.advanceEpoch();
            self.generalDisplay();
            self.after(500, self.advanceEpochAuto); 
    def saveProgress(self):
        blockchainSaved = {};
        for user in self.userList:
            uName   = user.content()["name"];
            uBlkChn = user.content()["blockchain"];
            blockchainSaved[uName] = uBlkChn;    
        pickle.dump(blockchainSaved, open(SAVEFILENAME, "wb"), pickle.HIGHEST_PROTOCOL);
        self.labels["Epoch"].config(fg="blue", text=("Epoch: " + str(self.epoch_track) + " Saved!"));
    def backwardInspect(self):
        self.epoch_track -= 1;
        trackID = len(self.userLists)-1 - (self.epoch-self.epoch_track);
        if trackID == 0:
            self.buttons["Backward"].config(state="disable");
        self.buttons["Forward"].config(state="normal");
        self.buttons["Act0"].config(state="disable");
        self.setBottomState("disable");
        self.generalDisplay(trackID=trackID);
    def forwardInspect(self):
        self.epoch_track += 1;
        trackID = len(self.userLists)-1 - (self.epoch-self.epoch_track);
        self.buttons["Backward"].config(state="normal");
        if (self.epoch - self.epoch_track) == 0:
            self.buttons["Forward"].config(state="disable");
            self.buttons["Act0"].config(state="normal");
            self.setBottomState("normal");
            if self.falseTxnOnUserE == True:
                self.buttons["Act3"].config(state="disable");
        self.generalDisplay(trackID=trackID);
    def falseTxnUserE(self):
        self.falseTxnOnUserE = True;
        self.buttons["Act3"].config(state="disable");

        user = [u for u in self.userList if u.content()["name"] == "E"][0];
        uName    = user.content()["name"];
        uMempool = user.content()["mempool"];
            
        victimName = random.sample(["A", "B", "C", "D"], 1)[0];
        fromUser = [u for u in self.userList if u.content()["name"] == victimName][0];
        fromName   = fromUser.content()["name"];
        fromWallet = fromUser.content()["wallet"];
        randEarning = str(int(np.ceil(rand.uniform()*fromWallet)));
        
        self.wantedTxnUserE = fromName+"=>"+uName+":"+randEarning+":"+str(int(np.ceil(time.time()*1e3)));
        uMempool.append(self.wantedTxnUserE);
        warnMemIgnore = user.updateMempool(uMempool, self.userList, ignoreDoubleSpending=True);
    def doubleSpendingUserE(self):
        if self.doubleSpendingOnUserE == False:
            self.doubleSpendingOnUserE = True;
            self.buttons["Act4"].config(text="Clear Mempool");

            user = [u for u in self.userList if u.content()["name"] == "E"][0];
            uName    = user.content()["name"];
            uWallet  = user.content()["wallet"];
            uMempool = user.content()["mempool"];
            
            victimNameList = random.sample(["A", "B", "C", "D"], 2);
            randSpending = str(int(np.ceil(rand.uniform()*uWallet)));
            for nameTo in victimNameList:
                txnStr = uName + "=>" + nameTo + ":" + randSpending + ":";
                txnStr+= str(int(np.ceil(time.time()*1e3)));
                uMempool.append(txnStr);
                time.sleep(2e-3);
            warnMemIgnore = user.updateMempool(uMempool, self.userList,\
                                               selfPosted=True, ignoreDoubleSpending=True);
        else:
            self.doubleSpendingOnUserE = False;
            self.buttons["Act4"].config(text="Double Spending");

            user = [u for u in self.userList if u.content()["name"] == "E"][0];
            uName    = user.content()["name"];
            uMempool = user.content()["mempool"];
            uMempool = [t for t in uMempool if t.split("=>")[0] != uName];
            warnMemIgnore = user.updateMempool(uMempool, self.userList, selfPosted=True, clearSelfMempool=True);
    def alterBlockUserE(self):
        if self.alterBlockOnUserE == False:
            self.alterBlockOnUserE = True;
            self.buttons["Act5"].config(text="Pretend Nothing Happened");

            user = [u for u in self.userList if u.content()["name"] == "E"][0];
            uName    = user.content()["name"];
            uMempool = user.content()["mempool"];
            uBlkChn  = user.secretContentAccess()["blockchain"];

            victimName = random.sample(["A", "B", "C", "D"], 1)[0];
            fromUser = [u for u in self.userList if u.content()["name"] == victimName][0];
            fromName   = fromUser.content()["name"];
            fromWallet = fromUser.content()["wallet"];
            randEarning = str(int(np.ceil(rand.uniform()*fromWallet)));

            transaction = fromName+"=>"+uName+":"+randEarning+":"+str(int(np.ceil(time.time()*1e3)));
            uBlkChn[-1].secretContentAccess()["transactions"].insert(0, transaction);
            self.badBlockIdxE = len(uBlkChn)-1;
        else:
            self.alterBlockOnUserE = False;
            self.buttons["Act5"].config(text="Altering Block Content");
            self.badBlockIdxE = -1;

##################################################################################################################
if __name__ == "__main__":
#read the saved blockchain from pickle
    try:
        blockchainSaved = pickle.load(open(SAVEFILENAME, "rb"));
    except (OSError, IOError) as e:
        blockchainSaved = {"A": [blockEntry("", ["genesis"])],\
                           "B": [blockEntry("", ["genesis"])],\
                           "C": [blockEntry("", ["genesis"])],\
                           "D": [blockEntry("", ["genesis"])],\
                           "E": [blockEntry("", ["genesis"])]}
    userA = userEntry("A", MINERATE["A"], TXNRATE["A"], blockchainSaved["A"]);
    userB = userEntry("B", MINERATE["B"], TXNRATE["B"], blockchainSaved["B"]);
    userC = userEntry("C", MINERATE["C"], TXNRATE["C"], blockchainSaved["C"]);
    userD = userEntry("D", MINERATE["D"], TXNRATE["D"], blockchainSaved["D"]);
    userE = userEntry("E", MINERATE["E"], TXNRATE["E"], blockchainSaved["E"]);
    loadedUserList = [userA, userB, userC, userD, userE];
#start program
    sim = bitCoinSim(loadedUserList);
    sim.mainloop();










