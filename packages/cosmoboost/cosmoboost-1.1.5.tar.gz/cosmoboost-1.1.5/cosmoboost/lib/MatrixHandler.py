
"""
library containing coefficient matrices for the ODE and recursive equations
"""
__author__ = " Siavash Yasini"
__email__ = "yasini@usc.edu"

import numpy as np

#######################################################
#              B,C,M,Lp,L,S matrices
#######################################################


def get_Blm_Clm(delta_ell, lmax,s):
    """calculate the Blm coefficients for the aberration kernel ODE
    uses Eq. 23 in Dai, Chluba 2014 arXiv:1403.6117v2"""
    
    ell = np.arange(0,lmax+1)  # arange the ell array from lmin to lmax
                               # the Blm coefficients will be calcualted for these values
    ell = np.append(ell, np.zeros(delta_ell))
    
    L, M = np.meshgrid(ell, ell, indexing="ij")
                                 
    # initialize an zero matrix Blm of size (lmax,mmax=lmax)
    # undefined values (for example ell < m will return 0.)
    # Blm = np.zeros((lmax+1+delta_ell,lmax+1+delta_ell))
    # Clm = np.zeros((lmax+1+delta_ell,lmax+1+delta_ell))
    
    # Eq. 23 in Dai, Chluba 2014 arXiv:1403.6117v2
    Blm = np.sqrt((L**2-s**2)*np.true_divide(L**2-M**2, 4.0*L**2-1))

    # set the NaN values from division by zero and sqrt(-1) to 0.
    Blm[np.isnan(Blm)] = 0

    # calculate Clm from Blm
    Clm = np.true_divide(Blm, L)
    
    # set the NaN and inf values from division by zero and sqrt(-1) to 0.
    Clm[np.isnan(Clm)] = 0
    Clm[np.isinf(Clm)] = 0

    return Blm, Clm

def get_ML_matrix(delta_ell, lmax, lmin=0):
    """calculate the Mmatrix and Lmatrix:
    the Xmatrix returns the x index values for each element of the kernel matrix"""

    width = 2*delta_ell+1

    Mmatrix = np.concatenate([m*np.ones(lmax+1-max(lmin, m)) for m in range(0, lmax+1)])
    Lpmatrix = np.concatenate([np.arange(max(lmin, m), lmax+1) for m in range(0, lmax+1)])

    Mmatrix = np.tensordot(Mmatrix, np.ones(width), axes=0)
    Lpmatrix = np.tensordot(Lpmatrix, np.ones(width), axes=0)
    Lmatrix = Lpmatrix + np.arange(-delta_ell, delta_ell+1)

    return Mmatrix.astype(int),Lmatrix.astype(int)


def get_MLpL_matrix(delta_ell, lmax, lmin=0):
    """calculate the Mmatrix, Lpmatrix and Lmatrix:
    the Xmatrix returns the x index values for each element of the kernel matrix"""

    width = 2*delta_ell+1
    
    Mmatrix = np.concatenate([m*np.ones(lmax+1-max(lmin, m)) for m in range(0, lmax+1)])
    Lpmatrix = np.concatenate([np.arange(max(lmin, m), lmax+1) for m in range(0, lmax+1)])
        
    Mmatrix = np.tensordot(Mmatrix, np.ones(width), axes=0)
    Lpmatrix = np.tensordot(Lpmatrix, np.ones(width), axes=0)
    Lmatrix = Lpmatrix + np.arange(-delta_ell, delta_ell+1)

    return Mmatrix.astype(int), Lpmatrix.astype(int), Lmatrix.astype(int)


def get_S_matrix(Lmatrix, Mmatrix, s=0):
    """calculate the Smatrix:
    the Smatrix returns the s index values for each element of the kernel matrix for polarized observables"""
    
    Smatrix = s * np.true_divide(Mmatrix, Lmatrix*(Lmatrix+1))
    Smatrix[~np.isfinite(Smatrix)] = 0
    return Smatrix


#######################################################
#           Matrix Manipulation functions
#######################################################

def minus_one_LplusLp(delta_ell, lmax):
    """calculates (-1)**(l+lp)"""
 
    height, width = ((lmax+1)*(lmax+2)//2, 2*delta_ell+1)

    parity = delta_ell % 2
    row = (-1)**np.arange(parity, width+parity)
    minus_one = np.tensordot(np.ones(height), row, axes=0)
    
    return minus_one
    
    
def transpose(kernel, delta_ell):
    """calculates the transpose kernel (K_mlL)"""
    
    inv = np.zeros(kernel.shape)
    for i in range(2*delta_ell+1):
        inv[:, i] = shift(kernel[:, 2*delta_ell-i], i-delta_ell)
    
    return inv

# -------------------------------
# functions for shifting the rows
# and columns of the matrices
# -------------------------------

def shift_right(arr):
    arr = arr.T
    arr = np.roll(arr, 1, axis=0)
    arr[0] = 0
    arr = arr.T

    return arr


def shift_left(arr):
    arr = arr.T
    arr = np.roll(arr, -1, axis=0)
    arr[-1] = 0
    arr = arr.T

    return arr


def shift_up(arr):
    arr = np.roll(arr, -1, axis=0)
    arr[-1] = 0

    return arr


def shift_down(arr):
    arr = np.roll(arr, 1, axis=0)
    arr[0] = 0

    return arr


def shift(arr, j):
    """shift up +j / shift down -j"""
    if j == 0:
        return arr

    elif j > 0:

        arr = np.roll(arr, -j, axis=0)
        arr[-j:] = 0
        return arr

    elif j < 0:
        arr = np.roll(arr, -j, axis=0)
        arr[0:-j] = 0
        return arr


#######################################################
#           Index and binning functions
#######################################################

def mL2indx(m, L, lmax, lmin=0):
    """convert mL to column index
    Used for slicing the Kernel elements K.mLl (see tutorial)

    *lmin is always zero. It is merely presented in the args for clarity

    Usage example:

    m = 0
    L = 10
    lmax=100

    indx = cb.mL2indx(m, L, lmax)

    K_mL_slice = kernel.mLl[indx]

    """

    assert lmin==0
    #assert 0 <= m <= L, "m is outside of the valid range 0 <= m <= L"
    #assert 0 <= L <= lmax, "L is outside of the valid range 0 <= L <= lmax"
    return m*(2*lmax+1-m)//2+L


def getindxminmax(m, l, lmin, lmax):
    """find the min and max column indeces based on lmin and lmax """
    if m <= lmin:
        return l + (1+lmax)*m-lmin*(1+m)
    else:
        return (2*l-(1+lmin)*lmin+(2*lmax-m+1) * m)//2




