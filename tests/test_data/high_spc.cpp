int complicated(int a, int b) {
    int c = 0;

    if( a > 6 )
        c += 2;
    else
        c += 4;

    if( a < 2 )
        c += 3;
    else
        c += 7;

    if( b > 8 )
        c += 6;
    else
        c += 1;

    if( b < 4 )
        c += 2;
    else
        c += 5;

    // 16 by this point
    if(n) {} // 32
    if(n) {} // 64
    if(n) {} // 128
    if(n) {} // 256

    return c;
}
