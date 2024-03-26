// taken from Emily Bache's git-repo, annotated by me
// Original work reproduced under:
// The MIT License (MIT)
// Copyright (c) 2015 @emilybache
// https://github.com/emilybache/Tennis-Refactoring-Kata/blob/main/cpp/tennis3.cc

const std::string tennis_score(int p1, int p2) {
    std::string s;
    std::string p1N = "player1";
    std::string p2N = "player2";
    if ((p1 < 4 && p2 < 4) && (p1 + p2 < 6)) { // e2 + 2 + 8 = 12?
        std::string p[4] = {"Love", "Fifteen", "Thirty", "Forty"}; 
        s = p[p1];
        return (p1 == p2) ? s + "-All" : s + "-" + p[p2]; // 2
    } else { // 8
        if (p1 == p2) // 2
            return "Deuce";
        s = p1 > p2 ? p1N : p2N; // 2
        return ((p1-p2)*(p1-p2) == 1) ? "Advantage " + s : "Win for " + s; // 2
    }
}
