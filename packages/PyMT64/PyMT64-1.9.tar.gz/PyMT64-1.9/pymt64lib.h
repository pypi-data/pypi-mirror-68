#include "mt64mp.h"

#define PI acos(-1.)

void uniformn(UL64 * mt , int * mti, double * x , long n ) ;

void poissonn(UL64 * mt , int * mti , double xm, double * x , long n ) ;

void normaln(UL64 * mt, int * mti , double * x , double * y, long n ) ;

void poissonn_multlam( UL64 * mt , int * mti , double * xm, double * x , long n ) ;
