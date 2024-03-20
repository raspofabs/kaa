int complex(int a, int b, int c) {
    if( a > 6 )
    {
        if( b < 4 )
            return 2;
        else
            return 5;
    }
    else
    {
        int x = 0;
        if( c < 3)
        {
            x = 4;
        }
        else
        {
            x = 7;
        }
        if( b > 8 )
            return 6 + x;
        else
            return 1 + x;
    }
    return 8;
}
