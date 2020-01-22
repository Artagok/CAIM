import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def f(n, k, beta):
    return k*(n**beta);

if __name__ == '__main__':

    N = [] # Total words of each index 
    D = [] # Different words of each index

    indexes = ["words.txt", "words2.txt", "words3.txt", "words4.txt", "words5.txt"];

    for index in indexes:
        n = 0;
        d = 0;
        for line in reversed(open(index).readlines()):
            line = line.strip();
            num = line.split(',');
            num = float(num[0]);
            #words.append(num);
            #words_log.append(np.log(num));
            n = n + num;
            d = d + 1;
        N.append(n);
        D.append(d);
    

    N_log = map(lambda x: np.log(x), N);
    D_log = map(lambda x: np.log(x), D);
    
    # Curve fitting
    popt, pcov = curve_fit(f, N, D);
    k = popt[0];
    beta = popt[1];
    print(k, beta);

    # Apply function f 

    fit_arr     = map(lambda n: f(n, k, beta), N);
    fit_arr_log = map(lambda x: np.log(x), fit_arr);

    ###  Curve fit plot ###
    plot_raw   = plt.plot(N, D, c='r', linewidth=2.0);   # Raw
    plot_heaps = plt.plot(N, fit_arr, c='b', linewidth=2.0, ls='--');   # Heaps
    plt.legend(["Real","Heap"], loc="upper left");
    #plt.axis([0, 500, 0, 210000]);
    plt.ylabel('#Different words');
    plt.xlabel('#Total words')
    plt.show();

    '''### log-log plot ###
    plot_raw   = plt.plot(N_log, D_log,   c='r', linewidth=2.0);   # Raw
    plot_heaps = plt.plot(N_log, fit_arr_log, c='b', linewidth=2.0, ls='--');   # Heaps
    plt.legend(["Real","Heap"], loc="upper left");
    plt.ylabel('#Different words');
    plt.xlabel('#Total words');
    plt.show();'''
