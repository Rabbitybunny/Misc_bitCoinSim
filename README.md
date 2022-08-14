# Bit Coin Simulation

This bit coin simulation showcases how blockchain, mining, and memory pool requirements prevent serveral different malicious attempts that tries to modify the transaction record. The simulation does not include encrytion nor smart contract, just the basic blockchain concept.

https://user-images.githubusercontent.com/55116073/183714345-f96b9a20-d949-4714-94ea-3deff3992568.mp4


The code runs on python3 with additional packages:

    pip3 install tkinter
    python3 bitCoinSim.py
There are only 5 users (A, B, C, D, and E) in this simulation, and the control is for user E. The wallet is the currency each user has according to the globally shared blockchain. Blue arrows indicate the transaction, while the green arrows indicate sharing the blockchain. Their rate can be modified in the code. The red number indicate the local blockchains that have been affected by user E's malicious attempts.

References:
- learnmeabitcoin's Youtube Channel (2017) (<a href="https://www.youtube.com/c/learnmeabitcoin/videos">arxiv</a>)
