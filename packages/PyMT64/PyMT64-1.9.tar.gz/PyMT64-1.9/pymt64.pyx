'''
                     PyMT64
                     
PyMT64 is a Python version of the Mersenne Twister (MT) 64-bit pseudorandom number generator by Takuji Nishimura and Makoto Matsumoto (see http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt64.html and the references below).

This customised version is thread safe and was interfaced from C to Python (see pymt64.c)

This module provides the following methods:
- init : initialization of the state vector (mt) used by the pseudorandom number generator (PNG)
- uniform : generation of an uniform distribution
- normal : generation of two Normal distributions
- poisson : generation of a Poisson distribution

The period of the PNG is 2**19937-1.

Example:
    import pymt64
    seed = 143439545 seed # the initial seed
    mt = pymt64.init(seed) # initialisation of the state vector of MT
    u = pymt64.uniform(mt,10) # generation of an uniform distribution
    print (u)
   [0.12444525 0.22084376 0.31059967 0.45578589 0.84743752 0.28825306
    0.83320389 0.05085032 0.48682253 0.17667076]

For a complete example, see pymt64_test.py

Note: the state vector 'mt' returned by pymt64.init has 313 elements instead of the 312 elements of the original C code. This is because the 313th element store the associated counter (mti).

Change history:
1.9 : correct bug associated with the normal distribution
1.8 : include a missing file
1.7 : corrected data package contain
1.6 : correct wrong size of the state vector 
1.5 : module interface is now based on Cython, module now compatibily with python 3
1.4 : link problem fixed
1.3 : fixe a compilation problem regading the Numpy include directory
1.2 : the previous implementation of the poisson distribution was not thread safe
1.1 : fix a problem with the initialization of the seed  (in the previous version the seed set by init() was not taken into account such that the results were not reproductible)
1.0 : initial version


R. Samadi (LESIA, Observatoire de Paris), 22 Dec. 2012        

References:
   T. Nishimura, ``Tables of 64-bit Mersenne Twisters''
     ACM Transactions on Modeling and 
     Computer Simulation 10. (2000) 348--357.
   M. Matsumoto and T. Nishimura,
     ``Mersenne Twister: a 623-dimensionally equidistributed
       uniform pseudorandom number generator''
     ACM Transactions on Modeling and 
     Computer Simulation 8. (Jan. 1998) 3--30.
'''
import numpy as np
# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np
# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.double
ITYPE = np.int
U64TYPE = np.uint64
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.double_t DTYPE_t
ctypedef np.int_t ITYPE_t
ctypedef np.uint64_t U64TYPE_t
# "def" can type its arguments but not have a return type. The type of the
# arguments for a "def" function is checked at run-time when entering the
# function.

cimport cython
cdef int MTSIZE = 312
cdef extern from "mt64mp.h":
    ctypedef unsigned long long UL64
    cdef void init_genrand64(unsigned long long seed , UL64 * mt, int * mti);

cdef extern from "pymt64lib.h":
    cdef void uniformn(UL64 * mt , int * mti, double * x , long n ) ;
    cdef void poissonn(UL64 * mt , int * mti , double xm, double * x , long n ) ;
    cdef void normaln(UL64 * mt, int * mti , double * x , double * y, long n ) ;
    cdef void poissonn_multlam( UL64 * mt , int * mti , double * xm, double * x , long n )

def init(unsigned long long  seed ): 
    '''
    Function used to initialise the state vector mt used by the pseudorandom number generator.
    
    mt = init(seed)
    
    '''
    cdef np.ndarray [U64TYPE_t,ndim=1, mode='c'] mt = np.zeros([MTSIZE+1], dtype=U64TYPE) 
    cdef int counter = mt[MTSIZE]
    #      the state vector 'mt'  has MTSIZE+1  elements 
    # instead of the MTSIZE  elements of the original C code. 
    # This is because the last element stores the associated counter (mti).
    
    init_genrand64(seed , &mt[0] , &counter ) 
    mt[MTSIZE] = counter 

    return mt

def uniform(np.ndarray [U64TYPE_t,ndim=1, mode='c'] mt , int n):
    '''
    Generates n random numbers on [0,1]-real-interval
    
    x = uniform(mt,n)
    
    '''

    cdef np.ndarray [DTYPE_t,ndim=1, mode='c'] series = np.zeros(n, dtype=DTYPE) 
    cdef int counter = mt[MTSIZE]
    
    uniformn( &mt[0]  , &counter , &series[0], n) 
    mt[MTSIZE] = counter 
 
    return series 

def poisson(np.ndarray [U64TYPE_t,ndim=1, mode='c'] mt , double xm , int n):
    '''
    
    Generates a Poisson distribution of mean mu.

    x = poisson(mt,mu,n)
  
    '''

    cdef np.ndarray [DTYPE_t,ndim=1, mode='c'] series = np.zeros(n, dtype=DTYPE) 
    cdef int counter = mt[MTSIZE]
    
    poissonn( &mt[0] , &counter ,xm, &series[0], n) 
    mt[MTSIZE] = counter 
 
    return series 


def normal(np.ndarray [U64TYPE_t,ndim=1, mode='c'] mt ,  int n):
    
    '''
    Generates two random series of size n Normally distributed with zero mean and variance one.
    
    (x,y) = normal(mt,n)
    
    '''

    cdef np.ndarray [DTYPE_t,ndim=1, mode='c'] series1 = np.zeros(n, dtype=DTYPE) 
    cdef np.ndarray [DTYPE_t,ndim=1, mode='c'] series2 = np.zeros(n, dtype=DTYPE) 
    cdef int counter = mt[MTSIZE]
    
    normaln( &mt[0] , &counter , &series1[0], &series2[0], n) 
    mt[MTSIZE] = counter 
    return series1,series2 

def  poisson_multlam(np.ndarray [U64TYPE_t,ndim=1, mode='c'] mt , np.ndarray [DTYPE_t,ndim=1, mode='c'] xm):

    '''
    Generates a Poisson distribution. 
    While poisson() works with a single value of 'lambda', this functions considers multiple values of lambda. i.e one for each generated random number. lambda must have as many elements as the number of random values desired.
    
    x = poisson_multlamb(mt,lambda)    
    '''

    cdef np.ndarray [DTYPE_t,ndim=1, mode='c'] series = np.zeros(xm.size, dtype=DTYPE) 
    cdef int counter = mt[MTSIZE]
 
    poissonn_multlam( &mt[0] , &counter , &xm[0], &series[0], xm.size )
    mt[MTSIZE] = counter 
 
    return series 
