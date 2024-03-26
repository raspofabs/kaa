const std::string tennis_score(int p1Score, int p2Score) {
    std::string score = "";
    std::string P1res = "";
    std::string P2res = "";
    // score is 30 * 32400 * 144 ??? 139968000????
    //
    // 30
    if (p1Score == p2Score && p1Score < 4) // if e1 + 9 = 10
    {
        // spc 8
        if (p1Score==0)
            score = "Love";
        if (p1Score==1)
            score = "Fifteen";
        if (p1Score==2)
            score = "Thirty";
        score += "-All";
    }
    if (p1Score==p2Score && p1Score>2) // if e1 + 2 = 3
        score = "Deuce";
    
    // 32400
    // 100
    if (p1Score > 0 && p2Score==0) // if e1 + 9 = 10
    {
        // spc 8
        if (p1Score==1)
            P1res = "Fifteen";
        if (p1Score==2)
            P1res = "Thirty";
        if (p1Score==3)
            P1res = "Forty";
        
        P2res = "Love";
        score = P1res + "-" + P2res;
    }
    if (p2Score > 0 && p1Score==0) // if e1 + 9 = 10
    {
        // spc 8
        if (p2Score==1)
            P2res = "Fifteen";
        if (p2Score==2)
            P2res = "Thirty";
        if (p2Score==3)
            P2res = "Forty";
        
        P1res = "Love";
        score = P1res + "-" + P2res;
    }
    
    // 324
    if (p1Score>p2Score && p1Score < 4) // if e1 + 17 = 18
    {
        // spc 16
        if (p1Score==2)
            P1res="Thirty";
        if (p1Score==3)
            P1res="Forty";
        if (p2Score==1)
            P2res="Fifteen";
        if (p2Score==2)
            P2res="Thirty";
        score = P1res + "-" + P2res;
    }
    if (p2Score>p1Score && p2Score < 4) // if e1 + 17 = 18
    {
        // spc 16
        if (p2Score==2)
            P2res="Thirty";
        if (p2Score==3)
            P2res="Forty";
        if (p1Score==1)
            P1res="Fifteen";
        if (p1Score==2)
            P1res="Thirty";
        score = P1res + "-" + P2res;
    }
    
    // 144
    // 9
    if (p1Score > p2Score && p2Score >= 3) // if e1 + 2 = 3
    {
        score = "Advantage player1";
    }
    
    if (p2Score > p1Score && p1Score >= 3) // if e1 + 2 = 3
    {
        score = "Advantage player2";
    }
    
    // 16
    if (p1Score>=4 && p2Score>=0 && (p1Score-p2Score)>=2) // if e2 + 2 = 4
    {
        score = "Win for player1";
    }
    if (p2Score>=4 && p1Score>=0 && (p2Score-p1Score)>=2) // if e2 + 2 = 4
    {
        score = "Win for player2";
    }
    return score;
    
}
