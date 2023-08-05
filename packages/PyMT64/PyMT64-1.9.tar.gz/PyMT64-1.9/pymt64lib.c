/* \file pymt64.c
 * \author R. Samadi
 * 
 * PyMT64 : 64-bit and thread safe version of the Mersenne Twister pseudorandom number generator
 * 
 * It is a C - Python interface based on the original C source code (mt19937-64.c)
 * by Takuji Nishimura and Makoto Matsumoto 
 *
 *
 * This is a free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this code.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright (C) 2012 by R. Samadi
 */
#include <Python.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <numpy/arrayobject.h>
#include <time.h>
#include "mt64mp.h"
#include "pymt64lib.h"

/* log-gamma function to support some of these distributions. The 
 * algorithm comes from SPECFUN by Shanjie Zhang and Jianming Jin and their
 * book "Computation of Special Functions", 1996, John Wiley & Sons, Inc.
 */
double loggam(double x)
{
    double x0, x2, xp, gl, gl0;
    long k, n;
    
    double a[10] = {8.333333333333333e-02,-2.777777777777778e-03,
         7.936507936507937e-04,-5.952380952380952e-04,
         8.417508417508418e-04,-1.917526917526918e-03,
         6.410256410256410e-03,-2.955065359477124e-02,
         1.796443723688307e-01,-1.39243221690590e+00};
    x0 = x;
    n = 0;
    if ((x == 1.0) || (x == 2.0))
    {
        return 0.0;
    }
    else if (x <= 7.0)
    {
        n = (long)(7 - x);
        x0 = x + n;
    }
    x2 = 1.0/(x0*x0);
    xp = 2*PI;
    gl0 = a[9];
    for (k=8; k>=0; k--)
    {
        gl0 *= x2;
        gl0 += a[k];
    }
    gl = gl0/x0 + 0.5*log(xp) + (x0-0.5)*log(x0) - x0;
    if (x <= 7.0)
    {
        for (k=1; k<=n; k++)
        {
            gl -= log(x0-1.0);
            x0 -= 1.0;
        }
    }
    return gl;
}

/*
  Adapted from rk_poisson_mult by Robert Kern (robert.kern@gmail.com)
*/

long rk_poisson_mult(UL64 * mt , int * mti , double lam)
{
  long X;
  double prod, U, enlam;
  enlam = exp(-lam);
  X = 0;
  prod = 1.0;
  while (1)
    {
      U =  genrand64_real2(mt,mti) ;  // random number on [0,1)-real-interval
      prod *= U;
      if (prod > enlam)
	{
	  X += 1;
	}
      else
	{
	  return X;
	}
    }
}
/*
  Adapted from rk_poisson_ptrs by Robert Kern (robert.kern@gmail.com)
*/
#define LS2PI 0.91893853320467267
#define TWELFTH 0.083333333333333333333333
long rk_poisson_ptrs(UL64 * mt , int * mti ,  double lam)
{
  long k;
  double U, V, slam, loglam, a, b, invalpha, vr, us;
  slam = sqrt(lam);
  loglam = log(lam);
  b = 0.931 + 2.53*slam;
  a = -0.059 + 0.02483*b;
  invalpha = 1.1239 + 1.1328/(b-3.4);
  vr = 0.9277 - 3.6224/(b-2);
  while (1)
    {
      U = genrand64_real2(mt,mti)  - 0.5;
      V = genrand64_real2(mt,mti)  ;
      us = 0.5 - fabs(U);
      k = (long)floor((2*a/us + b)*U + lam + 0.43);
      if ((us >= 0.07) && (V <= vr))
	{
	  return k;
	}
      if ((k < 0) ||
	  ((us < 0.013) && (V > us)))
	{
	  continue;
	}
      if ((log(V) + log(invalpha) - log(a/(us*us)+b)) <=
	  (-lam + k*loglam - loggam(k+1)))
	{
	  return k;
	}
    }
}
/*
  Adapted from rk_poisson by Robert Kern (robert.kern@gmail.com)
*/

long  poisson(UL64 * mt , int * mti , double lam )
{
  if (lam >= 10)
    {
      return rk_poisson_ptrs(mt,mti, lam);
    }
  else if (lam == 0)
    {
      return 0;
    }
  else
    {
      return rk_poisson_mult(mt,mti, lam);
    }
}

void uniformn(UL64 * mt , int * mti, double * x , long n )

{
  long i ;
  for (i=0l;i<n;i++)     x[i] =  genrand64_real1(mt,mti) ;
  
}

void poissonn(UL64 * mt , int * mti , double xm, double * x , long n )

{
  long i ;
  for (i=0l;i<n;i++)     x[i] = poisson(mt,mti,xm);
  
}

void poissonn_multlam( UL64 * mt , int * mti , double * xm, double * x , long n )
{
  long i ;
  for (i=0l;i<n;i++)   x[i] = poisson(mt,mti,xm[i]);
  
}

void normaln(UL64 * mt, int * mti , double * x , double * y, long n )
{
  long i ; 
  double  r1 , r2 , u ;
  for (i=0l;i<n;i++) {
    r1 =  genrand64_real1(mt,mti) ; 
    r2 =  genrand64_real1(mt,mti) ;
    u = sqrt(-2.*log(r1)) ;
    x[i] = u * cos(2.*PI * r2) ;
    y[i] = u * sin(2.*PI * r2) ;
  }
}


