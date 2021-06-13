#/opt/local/bin/python3
import sys, math, re, time, os
import numpy as np
import numpy.random as rand
import random
import hashlib
from copy import deepcopy

#helpful resources: https://www.youtube.com/c/learnmeabitcoin/videos
#Txn for transaction
#BlkChn for blockchain
##################################################################################
class blockEntry:
    _thisHash     = None;
    _preHash      = None;
    _timeTime     = None;
    _transactions = None;
    def __init__(self, preHash, transactions):
        self._transactions = deepcopy(transactions);
        self._preHash = deepcopy(preHash);
        self._timeTime = str(int(time.time()));
        strToHash="".join(self._transactions) + self._preHash + self._timeTime;
        self._thisHash = hashlib.sha1(strToHash.encode()).hexdigest();
    def content(self):
        return deepcopy({"transactions": self._transactions,\
                         "timeTime":     self._timeTime,\
                         "thisHash":     self._thisHash,\
                         "preHash":      self._preHash});
    def secretContentAccess(self):
        return {"transactions": self._transactions,\
                "timeTime":     self._timeTime,\
                "thisHash":     self._thisHash,\
                "preHash":      self._preHash};

class userEntry:
    __name = None;
    __wallet = None;
    __mineRate = None;
    __txnRate = None;
    __mempool = None;
    __blockchain = None;
    __updateIter = None;
    __isMalicious = False;
    def __init__(self, name, mineRate, txnRate, blockchain):
        self.__name = deepcopy(name);
        self.__blockchain = deepcopy(blockchain);
        self.__wallet = 10;
        self.__mineRate = mineRate;
        self.__txnRate = txnRate;
        self.__updateIter = 0;
        self.__mempool = [];
        self.updateTxnFromBlkChn();
    def updateMempool(self, mempool, userList, selfPosted=False,\
                      clearSelfMempool=False, ignoreDoubleSpending=False):
        if clearSelfMempool == True:
            self.__mempool = [];
        memNew = self.__mempool + mempool;
        memNew = list(set(memNew));
        blockNtoCheck = 3;
        warnings = [];
        for block in self.__blockchain[-blockNtoCheck:]:
            transactions = block.content()["transactions"];
            memNew = [m for m in memNew if m not in transactions];
        #check wallet amount
        walletNums = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0};
        txnNums    = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0};
        for user in userList:
            uName    = user.content()["name"];
            uWallet  = user.content()["wallet"];
            walletNums[uName] += uWallet;
        #sort in time
        memNewSort = [];
        for transaction in memNew:
            memNewSort.append([transaction.split(":")[-1], transaction]);
        memNewSort = np.array(memNewSort);
        memNewSort.sort(axis=0);
        memNewTemp = [];
        for item in memNewSort:
            memNewTemp.append(item[1]);
        memNew = memNewTemp; 
        #remove unsolicited
        txnWanted = "";
        RmIdxs = 0;
        for i, transaction in enumerate(memNew):
            if "Rm_" in transaction:
                txnWanted = transaction[1:].replace("Rm_", "");
                if int(transaction[0]) > RmIdxs:
                    RmIdxs = int(transaction[0]);
        RmIdxs += 1;
        self.__mempool = [t for t in self.__mempool\
                          if (t != txnWanted) and ("Rm_" not in t)];
        memNew = [t for t in memNew\
                  if (t != txnWanted) and ("Rm_" not in t)];
        if txnWanted != "":
            memNew.append(str(RmIdxs) + "Rm_" + txnWanted);
        ###
        for transaction in self.__mempool:
            if "Rm_" not in transaction:
                sender = transaction.split("=>")[0];
                txnNums[sender] += 1; 
        for transaction in memNew:
            if transaction not in self.__mempool:
                txn = transaction.split("=>");
                sender = txn[0];
                receiver = txn[1].split(":")[0];
                coin = int(txn[1].split(":")[1]);
                if "Rm_" in transaction:
                    if "9Rm_" not in transaction:
                        self.__mempool.append(transaction);
                elif (selfPosted == False) and (sender == self.__name):
                    warnings.append(
                        self.genWarning(self.__name, receiver, transaction,
                                        "unsolicited transaction"));
                    self.__mempool.append("0Rm_"+transaction);
                elif coin > walletNums[sender]:
                    warnings.append(
                        self.genWarning(self.__name, sender, transaction,
                                        "not enough coin in wallet"));
                else:
                    txnNums[sender] += 1; 
                    if txnNums[sender] > 1:
                        warnings.append(
                            self.genWarning(self.__name, sender, transaction,\
                                            "only one transaction allowed "+\
                                            "in memory pool"));
                        if ignoreDoubleSpending == True:
                            self.__mempool.append(transaction);
                    else:
                        self.__mempool.append(transaction);
        return warnings;
    def checkTxnValidityFromBlkChn(self, name, blockchain):
        validity = True;
        warnings = [];
        txnWanted = "";
        for transaction in self.__mempool:
            if "Rm_" in transaction:
                txnWanted = transaction[1:].replace("Rm_", "");
        for block in blockchain[max(0, len(self.__blockchain)-3):]:
            transactions = block.content()["transactions"];
            for transaction in transactions:
                txn = transaction.split("=>");
                if "genesis" not in transaction:
                    formatBool = (len(txn) == 2) and\
                                 (len(txn[1].split(":")) == 3) and\
                                 (int(txn[1].split(":")[1]) >= 0);
                    if (formatBool == False) or\
                       ("Rm_" in transaction):
                        validity = False;
                        warnings.append(self.genWarning(self.__name, name,\
                            transaction, "invalid transaction in block"));
                    elif transaction in warnings:
                        validity = False;
                        warnings.append(self.genWarning(self.__name, name,\
                            transaction, "unsolicited transaction in block"));
        return validity, warnings;
    def checkTxnDuplicateFromBlkChn(self, name, blockchain):
        blockNtoCheck = 10;
        validity = True;
        txns = [];
        warnings = [];

        for block in blockchain[-blockNtoCheck:]:
            transactions = block.content()["transactions"];
            for transaction in transactions:
                if transaction in txns:
                    validity = False;
                    warnings.append(self.genWarning(self.__name, name,\
                        transaction, "repeated transaction"));
            txns = txns + transactions;
        return validity, warnings;
    def genWarning(self, nameFind, nameCulprit, transaction, reason):
        warning =  "WARNING: "+nameFind+" reject transaction from ";
        warning += nameCulprit+" (";
        warning += transaction.split(":")[0]+":"+transaction.split(":")[1]+"): ";
        warning += reason+".";
        return warning;
    def checkBlkChnValidity(self, blockchain):
        validity = True;
        warnings = [];
        for i, block in enumerate(blockchain):
            if i != 0:
                transactions = block.content()["transactions"];
                preHash      = block.content()["preHash"];
                timeTime     = block.content()["timeTime"];
                strToHash = "".join(transactions) + preHash + timeTime;
                thisHash = hashlib.sha1(strToHash.encode()).hexdigest();
                if (block.content()["thisHash"] != thisHash) and\
                   (self.__isMalicious == False):
                    validity = False;
                    blockName = "block" + str(i);
                    firstTxn = block.content()["transactions"][0];
                    warnings.append(self.genWarning(self.__name,blockName,firstTxn,
                                                    "block hash mismatching")); 
        return validity, warnings;
    def checkBlkChnLength(self, blockchain):
        if len(blockchain) > len(self.__blockchain):
            return True;
        return False;
    def updateBlkChn(self, blockchain):
        self.__updateIter = len(self.__blockchain) - 1;
        while self.__blockchain[self.__updateIter].content()["thisHash"] != \
                     blockchain[self.__updateIter].content()["thisHash"]:
            self.__reverseWallet(self.__blockchain[self.__updateIter]);
            self.__updateIter -= 1;
            if self.__updateIter < 0:
                break;
        self.__updateIter += 1;
        self.__blockchain = deepcopy(blockchain);
    def __reverseWallet(self, block):
        transactions = block.content()["transactions"];
        if "genesis" in transactions:
            pass;
        else:
            for transaction in transactions:
                txn = transaction.split("=>");
                sender = txn[0];
                receiver = txn[1].split(":")[0];
                coin = int(txn[1].split(":")[1]);
                if sender == self.__name:
                    self.__wallet += coin;
                if receiver == self.__name:
                    self.__wallet -= coin;
    def updateTxnFromBlkChn(self):
        for block in self.__blockchain[self.__updateIter:]:
            transactions = block.content()["transactions"];
            if "genesis" in transactions:
                pass;
            else:
                for transaction in transactions:
                    txn = transaction.split("=>");
                    sender = txn[0];
                    receiver = txn[1].split(":")[0];
                    coin = int(txn[1].split(":")[1]);
                    if sender == self.__name:
                        self.__wallet -= coin;
                    if receiver == self.__name:
                        self.__wallet += coin;
            self.__mempool = [t for t in self.__mempool if t not in transactions];
        self.__updateIter = len(self.__blockchain);
        return 0;
    def getTxnRate(self):
        return deepcopy(self.__txnRate);
    def getMineRate(self):
        return deepcopy(self.__mineRate);
    def mine(self):
        blockNtoCheck = 3;
        for block in self.__blockchain[-blockNtoCheck:]:
            transactions = block.content()["transactions"];
            self.__mempool = [m for m in self.__mempool if m not in transactions];
        txnStr = "SYS=>" + self.__name + ":1";   #earning 1 coin for mining
        txnStr += ":" + str(int(np.ceil(time.time()*pow(10, 3))));
        self.__mempool.append(txnStr); 
        blockPre = self.__blockchain[-1];
        block = blockEntry(blockPre.content()["thisHash"], self.__mempool);
        self.__blockchain.append(block);
        self.__mempool = [];
    def content(self):
        return deepcopy({"name":       self.__name,\
                         "wallet":     self.__wallet,\
                         "mempool":    self.__mempool,\
                         "blockchain": self.__blockchain});
    def setMalicious(self, isMalicious):
        self.__isMalicious = isMalicious;
    def secretContentAccess(self):
        return {"name":       self.__name,\
                "wallet":     self.__wallet,\
                "mempool":    self.__mempool,\
                "blockchain": self.__blockchain};



