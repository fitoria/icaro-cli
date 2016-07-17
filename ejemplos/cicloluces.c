#include<np05_06.h>
#include "definiciones_icr.c"

void loop()
{
    int i=1;
    while (i<=128){
        PORTB = i; 
        Delayms(300);
        i *= 2;
    }
}
