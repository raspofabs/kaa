int extended_switch(int a) {
    switch(a)
    {
    case 0:
    case 1:
        return 2;
    case 2:
    case 3:
        return 8;
    case 4:
    case 5:
        return 12;
    default:
        return 0;
    }
}
