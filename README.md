# Correlation Power Analysis Challenge
You’ve intercepted a tamper-resistant IoT device used in a "secure" field deployment. You know that this device is used to encrypt and transmit important data, but you don't know the encryption key. The firmware is locked down, debug is fused off, and the crypto implementation is constant-time code.
Thus, your team has decided to try a side-channel attack: While the device is running, you measure the electromagnetic (EM) emissions coming from the chip. Every time the device encrypts a block, its power draw leaks tiny hints about what it’s doing internally. Your job is to turn these hints into information about the key.
The team has already managed to determine the encryption algorithm and capture quite a few recordings of the EM emissions ("traces") while the device ran encryptions on known plaintexts.

Your job is now to perform a Correlation Power Analysis (CPA) on these traces. You’re given a set of plaintext inputs and the corresponding power traces captured during an operation of the [PRESENT](https://www.iacr.org/archive/ches2007/47270450/47270450.pdf) cipher. Somewhere in those traces, the first-round computation leaks just enough information about half of one key byte to betray it. By guessing the data-dependent power consumption for each possible key and correlating it with the measured traces, you’ll pinpoint the key value that best fits the leakage.

Below you can see the operation you are targeting. This is the processing of the first four bits of the first round of the cipher.
The `in` variable is 4 bits of known plaintext, $k$ are the four key bits you need to figure out and $y$ is the value you are attacking.
![[resources/PRESENT_operation.jpg]]
Note: For these traces, the cipher was implemented on an ARM Cortex-M processor and the trace acquisition was performed with an electromagnetic probe placed on top of the chip. This often increases the amount of noise in the signal, so correlation peaks might not be very clear!

## Steps to perform the attack
1. Load the known plaintext values (`in.csv`)
2. Using these values and the structure of the PRESENT cipher, construct a matrix of value predictions for the variable $y$. Essentially, the matrix should, for every known plaintext, contain all possible values $y$ can take based on the unknown 4-bit value $k$.
   For $n$ known plaintext and $k$ possible key candidates, the matrix should have dimensions $n \times k$.
3. Convert the created matrix into a matrix of power consumption predictions by replacing every entry in the matrix with its hamming weight.
4. Load the file `traces.csv`. It contains 14900 aligned power traces, each one with 6990 time samples.
5. Using the Pearson correlation coefficient, for all possible key candidates, compute the column-wise correlation between the traces matrix and the power-prediction matrix.
6. Rank the key candidates from best to worst, based on the highest absolute value of the correlations. **The binary representation of the top key candidate based on absolute correlation is the solution to the challenge.**
