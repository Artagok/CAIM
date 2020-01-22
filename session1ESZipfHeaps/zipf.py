import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Global a
a = 1;

def f(rank, b=1, c=1):
    return c/(rank+b)**a;

if __name__ == '__main__':
    
    words = [];
    words_log = [];
    words_f = [];
    words_f_log = [];

    for line in reversed(open("words.txt").readlines()):
        line = line.strip();
        num = line.split(',');
        num = float(num[0]);
        words.append(num);
        words_log.append(np.log(num));

    # Array of ranks [1, 2, 3, 4, ...]
    ranks = range(1, len(words)+1);

    # Curve fitting
    popt, pcov = curve_fit(f, ranks, words);
    b = popt[0];
    c = popt[1];
    print(b, c);

    # Apply function f 
    words_f = map(lambda rank: f(rank, b, c), ranks);
    words_f_log = map(lambda x: np.log(x), words_f);

    '''###  Curve fit plot ###
    plot_raw   = plt.plot(words,   c='r', linewidth=2.0);   # Raw
    plot_zipfs = plt.plot(words_f, c='b', linewidth=2.0, ls='--');   # Zipf's
    plt.legend(["Real","Zipfs"]);
    plt.axis([0, 500, 0, 210000]);
    plt.ylabel('Frequency');
    plt.xlabel('Rank (most to less frequent)')
    plt.show();'''

    '''### log-log plot ###'''
    plot_raw   = plt.plot(np.log(range(1,len(words_log)+1)),   words_log,   c='r', linewidth=2.0);   # Raw
    plot_zipfs = plt.plot(np.log(range(1,len(words_f_log)+1)), words_f_log, c='b', linewidth=2.0, ls='--');   # Zipf's
    plt.legend(["Real","Zipfs"]);
    plt.ylabel('log(Frequency)');
    plt.xlabel('log(Rank) [most to less frequent]');
    plt.show();

# 61825 Words