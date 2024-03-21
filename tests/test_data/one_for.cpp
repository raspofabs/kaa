int one_for(int a) {
    int b = 10;
    for(int c = 0; c < a; ++c) {
        b += a;
        a -= c;
    }
    return b;
}
