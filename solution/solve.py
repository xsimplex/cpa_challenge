import numpy as np
from scipy.stats import pearsonr

import matplotlib.pyplot as plt

# Taken from the paper, also works as integers
PRESENT_SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

####
# Expects a single integer value for i
####
def possible_y(i):
    # k is a four bit value so we need to test for all 16 possible values
    # y = SBOX(in ^ k)
    return [PRESENT_SBOX[x] for x in i ^ np.arange(16)] 

####
# Expects an array of known inputs and calculates
# the value of y for each possible value for k
# as a matrix
# For an n-dim array of inputs and k possible key values
# this returns a n x k matrix
####
def get_value_prediction_matrix(inputs):
    return np.array([possible_y(x) for x in inputs])

####
# Calculates the Hamming Weight (i.e., the number of non-zero bits)
# for a single value
####
def hw(x):
    return x.bit_count()

####
# Turns the previously generated value-prediction matrix
# into a power-prediction matrix
# by replacing every value with its Hamming Weight
def get_power_prediction_matrix(vp_matrix):
    return np.vectorize(hw)(vp_matrix)

if __name__ == '__main__':
    # Load the known inputs
    inputs = np.genfromtxt('in.csv', dtype='i', delimiter=',')

    # Calculate the value prediction matrix for every input-key candidate combination
    vp_matrix = get_value_prediction_matrix(inputs)

    # Replace every value in the value-prediction matrix with its Hamming Weight
    pp_matrix = get_power_prediction_matrix(vp_matrix)

    # Load the power traces
    traces = np.genfromtxt('traces.csv', delimiter=',')

    corrs = np.zeros((16,6990))
    # For every key candidate and every trace,
    # compute the (absolute) column-wise correlation between the traces and the power predictions
    for k in range(16):
        for s in range(6990):
            corrs[k,s] = np.abs(pearsonr(traces[:,s], pp_matrix[:,k]))[0]

    # Find the highest absolute correlation per key candidate
    max_corrs = [np.max(corrs[k,:]) for k in range(16)]
    # Find the key candidate for which the max. absolute correlation is highest
    # This is the solution
    top_candidate = np.argmax(max_corrs)
    print("The key candidate with the highest absolute correlation is", format(top_candidate, '#06b'))

    # Optionally, for a more intuitive understanding,
    # you can plot the correlation of each key candidate across the power traces.
    fig, ax = plt.subplots()
    for i in range(16):
        # Highlight the plot of the top candidate in red and make all others gray
        c = 'red' if i == top_candidate else 'grey'
        ax.plot(corrs[i,:], label=str(i), color=c)

    ax.set_title('Correlation of the top key candidate vs. all others')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Abs. Correlation')
    plt.show()

