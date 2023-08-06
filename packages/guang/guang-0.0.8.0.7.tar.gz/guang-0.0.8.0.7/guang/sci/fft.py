import numpy as np
import cupy as cp

def fft_conv1d(a,b):
    n = len(a)+len(b)-1
    N = 2**(int(np.log2(n))+1)
    A = np.fft.fft(a, N)
    B = np.fft.fft(b, N)
    return np.fft.ifft(A*B)[:n]

def fft_conv1d_cupy(a,b):
	
    n = len(a)+len(b)-1
    N = 2**(int(cp.log2(n))+1)
    A = cp.fft.fft(a, N)
    B = cp.fft.fft(b, N)
    return cp.fft.ifft(A*B)[:n]

def fft_conv2d(a, b):

    ha, wa = a.shape
    hb, wb = b.shape
    w = wa + wb - 1
    h = ha + hb - 1
    Nw = 2**(int(np.log2(w))+1)
    Nh = 2**(int(np.log2(h))+1)
    A = np.fft.fft2(a, (Nh, Nw))
    B = np.fft.fft2(b, (Nh, Nw))
    return np.fft.ifft2(A*B)[:h, :w]

def fft_conv2d_cupy(a, b):
	
    ha, wa = a.shape
    hb, wb = b.shape
    w = wa + wb - 1
    h = ha + hb - 1
    Nw = 2**(int(np.log2(w))+1)
    Nh = 2**(int(np.log2(h))+1)
    A = cp.fft.fft2(a, (Nh, Nw))
    B = cp.fft.fft2(b, (Nh, Nw))
    return cp.fft.ifft2(A*B)[:h, :w]

