int one_if(int a) {
    int c = 1;
    while(a > 0) {
        c *= a;
        a--;
    }
    return c;
}
