# About My Project

Student Name:  Oliver Lang
Student Email:  ojlang@syr.edu

### What it does
It uses Poly Market's Gamma Markets API to pull all markets, active and inactive. Then I separate by active markets, and then pull some basic stats about them.
It allows user to choose all of the columns in a select box, and allows them to download that filtered dataframe.
### How you run my project
Run 1_all_markets.py to get all markets, should be over 23000 markets
Run 2_active_markets.py, filters for only active markets
Run 3_st_active.py as a streamlit

Only run the tests after running 2_active_markets.py
test for all_markets checks if the ids are unique, and that there are at least 23000, since it keeps inactive markets, that number should never decrease
test for active_markets checks that active is True for all of them

### Other things you need to know

So I've had a relative interest in finance for the past few years,
particularly blockchain stuff because I think the fact it has been a 
sort of legal gray area makes it quite interesting. Unintentionally, 
somewhere along the way I found PolyMarket, which is a prediction 
market where users bet and set the priceline themselves. Considering 
the efficient market hypothesis, I would consider Polymarket an 
inefficient market, meaning there are probably some unseen opportunities.
Each and every question which is up for wager is considered it's own 
market. 

Some French guy made like 80 million or so off of an election that
he couldn't even vote for, just seems like an interesting thing to
look into.

I would like to point out that to access and make bets on the site
normally you need to VPN to another country that allows it, yet for
some reason they allow you to actually make bets with their CLOB API 
from anywhere. 