void qac_example() {
    int n;
    if ( n )
    {
    } /* block 1, paths 1 */
    else if ( n )
    {
        if ( n )
        {
        } /* block 2, paths 1 */

        else
        {
        } /* block 3, paths 1 */

        /* block 4, paths block2+block3 = 2 */

        switch ( n )
        {
            case 1 : break;
            case 2 : break;
            case 3 : break;
            case 4 : break;
            default: break;
        } /* block 5, paths = 5 */

    } /* block 6, paths block4*block5 = 10 */
    else
    {
        if ( n )
        {
        } /* block 7, paths 1 */

        else
        {
        } /* block 8, paths 1 */
    } /* block 9, paths block7+block8 = 2 */
    /* block 10, paths block1+block6+block9 = 13 */

    if ( n )
    {
    } /* block 11, paths 1 */

    else
    {
    } /* block 12, paths 1 */
    /* block 13, paths block11+block12 = 2 */

    /* outer block, paths block10*block13 = 26 */
}
