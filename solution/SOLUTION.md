## 1. Load `in` data
Both the `in.csv` and `traces.csv` files can be loaded using the NumPy function
`genfromtxt`. For now, you only need to load the `in.csv` file. To make your life easier, you can specify the `dtype` as integer, but this is not strictly necessary. Importantly, it is not required to work with hexadecimal values like the PRESENT paper does. 
## 2. Create value-prediction matrix
Every round of the PRESENT permutation consists of the same three steps:
1. Addition of the round key
2. The S-Box
3. A bit permutation
As stated in the Challenge, we are attacking an intermediate value $y$ immediately _after_ the S-Box.
Thus, to create the value-prediction matrix we need to do the following for every value $in$ of `in.csv`:
For every possible value that $k$ can take (i.e., `[0x00, 0x01, 0x02, ...,0x0E, 0x0F]` since it is a four-bit value), compute $in \oplus k$ (in XOR k). Then, feed every single of these values into the S-Box so that you end up with the final expression $\mathtt{SBox}[in\oplus k]$.
The value-prediction matrix $V$ is the matrix where the entry $V_{i,j}$ corresponds to $\mathtt{SBox}[in_i\oplus k_j]$ for $i \in [0,14899],\ k \in [0,15]$ . Thus, your value-prediction matrix should have dimensions $14900 \times 16$.
Just make sure that if you don't work with hexadecimal values, you correctly convert the S-Box as well.
## 3. Create the power-prediction matrix
Since, abstractly, for a binary value on a computer a $1$ means power and $0$ means no power, a decent heuristic for modeling the power consumption is to count the number of ones for each value in question. This is exactly what the Hamming Weight does.
To convert the value-prediction matrix to a power-prediction matrix, all we need to do is to replace every value with the number of ones in its binary representation.
## 4. Load the power traces
Similarly to `in.csv`, load the `traces.csv` file. Note that this file contains floating point values, do not load it with `dtype='i'` as well.

## 5. Compute the column-wise correlation and find the highest
You can either implement the Pearson correlation yourself, or use the `pearsonr` function from `scipy.stats`. To get the absolute correlation, you can use `abs` from NumPy.
We now want to determine the correlation between the measured power consumption of each time point with the predicted power consumption for a single key candidate $k$ based on our power-prediction matrix. Concretely, if our power-prediction matrix is of shape $14900\times 16$ and our trace matrix is of shape $14900\times 6990$, we want to compute the __absolute__ correlation of every column of the former with every column of the latter, leaving us with a matrix of shape $16 \times 6990$.
Conceptually, there should be one (or a few) time samples in our traces where the exact value we are after (our $y$) is computed. By checking the correlation of our predicted power consumption (depending on $k$) with the real power consumption at a given time-step, we should be able to find out at which time points $y$ was computed, and which of our $k$ predicts the power consumption at that time point best.
Consequently, the key candidate that shows the highest absolute correlation value at any point during the trace is the one that predicts the power consumption at that point best and is thus the most likely candidate for the actual key part.
You can find this value by gathering the highest correlation value of each row in a list and then returning the index of the highest value in that list. __That should be the best-fitting key candidate.__ The binary representation (including `0b`) of that value is the solution to the challenge.

The below plot is a visualisation of this. Somewhere around time sample 3900, there is one key candidate whose power predictions exhibit significantly higher correlation than all others.

![[solution_plot.png]]