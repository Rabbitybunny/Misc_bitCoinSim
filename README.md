# Bit Coin Simulation

This bit coin simulation showcases how blockchain, mining, and memory pool requirements prevent serveral different malicious attempts that tries to modify the transaction record. The simulation does not include encrytion nor smart contract, just the basic blockchain concept.

https://github.com/SphericalCowww/zMisc_bitCoinSim/blob/main/demo.mov

The code runs on python3 with additional packages:

    pip3 install tkinter
    python3 bitCoinSim.py

There are only 5 users (A, B, C, D, and E) in this simulation, and the control is for user E. The wallet is the currency each user has according to the globally shared blockchain. Blue arrows indicate the transaction, while the green arrows indicate sharing the blockchain. Their rate can be modified in the code. The red number indicate the local blockchains that have been affected by user E's malicious attempts.
