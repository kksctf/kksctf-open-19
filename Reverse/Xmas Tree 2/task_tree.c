#include <stdio.h>
#include <stdlib.h>
#define C char
#define CC char**
#define SP short*
#define I int
#define R return
#define U unsigned
#define P printf

void

                                         p
                                       (C*a,
                                    I i){P("%c"
                                      ,a[i]);
                                     }int main

                                         (
                                        I i
                                       ,CC c
                                      ){C _1[
                                    19]="_a""cd"
                                  "eh""ik""lm""no"
                                "pr""su""wy""\0";if
                             (i<2)R 1;I _2=atoi(c[1]);
                                       if(((
                                      U C* )&
                                     _2)[ 0]==
                                   0xAF){if(((SP
                                 )&_2)[1]==0x3174)
                               {if(((_2>>22)&0xFF)==
                            0xC5){if(*(((C*)((&_2)+2))-
                         7)==0x19){if(((((SP)(((C*)(&_2))+
                      13)-5)[0]>>0)&0xff)==0x31){P("kks{");p(
                   _1, 2);p(_1,_2 >> 24&0xFF00);p(_1,((_2&1)<<2)
                                       |2);p
                                      (_1 ,((
                                     _2 >>24)&
                                    0xF) *10+((
                                  _2>>16)&0xF));p
                                (_1,_2>>31);p(_1,((
                              C*)&_2)[1]-11);p(_1,6);
                           p(_1,(_2+10)&0x0000000f);p(_1
                        ,014);p(_1,i<<2);p(_1,i<<2>>1) ;p(_1
                     ,000*003);p(_1,"P"[0]-69);p(_1,(_2>>4)%16)
                 ;p(_1,2147483648l>>28);p(_1,(*(U C*)&_2)-0x9e);p(_1
             ,000);I n=2<<5,m=5;while((m<11)&&(n>>=2)){p(_1,n);p(_1,m);m
         *=2;}p(_1,'_'-'_');P("%c",0x76+(_2>>28));p(_1,10+((_2>>24)&0xf));p(
     _1,*(((C*)&_2)+3)%16+14);p(_1,1+2+3+4+5+6+7+8+9-45);p(_1,(P("%s","")+1)%16)
 ,p(_1,13),p(_1,((C*)(&_2))[2]%16),P("_");p(_1,5-02);p(_1,0x4-(-9));p(_1,003-(-12));
                                      p(_1,2-
                                      (-010))
                                      ;P("%c"
                                      ,_1[7])
                                      ;  P  (
                                      "}\n");
                                      }} }} }
                                      R 0 ; }
