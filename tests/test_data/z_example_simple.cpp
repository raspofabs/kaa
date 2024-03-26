// taken from the data-oriented-design git repo and annotated by me
// Original work reproduced under:
// The MIT License (MIT)
// Copyright (c) 2018 Richard Fabian
// https://github.com/raspofabs/dodbooksourcecode/blob/main/speculativewaste.cpp

std::pair<int,int> Simple() {
	int good = 0;
	int taller = 0;
    // for = 1 + 5 == 6
	for( int i = 0; i < NUM_IN_TEST; ++i ) {
		A &a = AInfoVec[i];
        // if = e1 + 3 + 1 = 5
		if( a.canStandOnOneLeg && a.hasTheirOwnHair ) {
			good += 1;
            // if = e0 + 2 + 1 = 3
			if( BInfoMap.find( i ) != BInfoMap.end() ) {
                // if = e0 + 1 + 1 = 2
				if( BInfoMap[i].height > 185 ) {
					taller += 1;
				}
			}
		}
	}
	return std::pair<int,int>(good,taller);
}
