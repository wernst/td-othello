import numpy as np

def main():
    m = np.matrix('1 2; 3 4')
    print(sigmoid(m))
    print(sigmoid_prime(m))

def sigmoid(x):
    return 1/(1+np.exp(-1*x))


def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

if __name__ == '__main__':
    main()
