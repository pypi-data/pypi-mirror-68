#!/usr/bin/env python
import numpy as np
import pymt64 


N = 10 # number of threads


# master seed value
seed = 12338



# initialisation of the master seed
np.random.seed(seed)

# mt is the stage vector of the Mersenne Twister pseudorandom number generator
# in the case of multrithreading, each thread must have its own vector mt



seeds = np.random.randint(0,2**32,N)
mt = np.zeros((N,313),dtype=np.uint64)

# initialize each mt vector
for i in range(N):
	mt[i,:] = pymt64.init(seeds[i])


# for each thread generate various type of random variable
for i in range(N):

	# generating a uniform distribution
	x = pymt64.uniform(mt[i,:],1)

	# generating a Poisson distribution
	lam = 10. # the characteristic mean 'lambda'
	y = pymt64.poisson(mt[i,:],lam,1)

	# generating two independent Normal distributions
	(u,v) = pymt64.normal(mt[i,:],1)
	

	print (i,x,y,u,v)

