#include<np05_06.h>
#include "definiciones_icr.c"

void loop()
{
    PORTB = 255; 
    Delayms(100);
    PORTB = 0; 
    Delayms(100);
}
