int one_dowhile(int a) {
    int c = 1;
    do {
        c *= a;
        a--;
    }
    while(a > 0);
    return c;
}
