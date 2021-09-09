# NBA
A repository to keep my NBA data and a few projects.

- __This project is active, but the documentation for it isn't up to date. It's on my to-do list.__

---

## [Basketball Reference Scraper](https://github.com/Kallbrig/NBA/tree/main/Basketball%20Reference%20Stat%20Scraper)
+ A scraper for [Basketball Reference](https://www.basketball-reference.com/) stats

## [Basic Player Ranking System](https://github.com/Kallbrig/NBA/tree/main/Basic%20Player%20Ranking%20System)
+ A fun ranking system for players. It's pretty obviously not accurate, so don't @me about it.
+ Russell Westbrook's MVP season is pretty clearly the 🐐.

## [Weighted FG%](https://github.com/Kallbrig/NBA/tree/main/Weighted%20FG%25)
+ A new FG% that weights FG% using shots attempted. This allows a FG% to be a better measure of rather any given shot will go in.

## [Combine Team Stats](https://github.com/Kallbrig/NBA/tree/main/Combine%20Team%20Stats)
+ Consolidates raw scraped team statistics into a single csv for easier access.

## [Combine Player And Team Stats](https://github.com/Kallbrig/NBA/tree/main/Combine%20Player%20and%20Team%20Stats)
+ Adds team stats to player stats. So now Wins, Losses, etc can be taken into consideration when evaluating a player.

## [ML - Team](https://github.com/Kallbrig/NBA/tree/main/ML%20-%20Team)
+ Machine learning projects involving only team stats.

---
## In Progress
+ Use normalization in comparing players across years. Maybe add it in to the MVP predictions as well to prevent stat inflation bias. 
    + ~~Using a "distance from the average" or "Off Average" metric~~
    + ~~Normalize for pace~~
    + Combine the two into a single dataset.

---
## To-do (No Order)

+ Update Documentation
+ ~~Cluster Players using a ML algorithm~~ and interpret the results
+ ~~Scrape Team Per Game, Advanced,~~ and Shooting stats and consolidate them. 
+ The [Team Linear Regression Notebook](https://github.com/Kallbrig/NBA/blob/main/ML%20-%20Team/team_linear_regression.ipynb) is unfinished.
+ Decide on/implement a new way to store the scraped data. The current method is going to get messy incredibly quickly.
+ Rewrite Scrapers using pd.read_html() because it's just a better way to do things.
+ Develop a single all-stat scraper that consolidates all stats when first scraped.
    + Add in team stats before consolidating traded players. Use weighted average to give a rough estimate of how good the player's various teams are.
    + This is on hold due to issues in the player stat scraper and the player and team stat combiner.
+ Rework the player stat + team stat combiner so that traded players are accounted for properly.
    + The issue is that traded players don't have team statistics.
        + The fix I'm planning to implement is to add team stats before consolidating the individual rows of a single player. Thus when combined, the player will now be on a "hybrid team" that has the statistics of a weighted average of each team they played for that year. This is an imperfect system, but it's the best I can do with the data avaliable.
+ Rework the player stat scraper so that traded players don't have 100+ games in a season.
    + This is occuring becasue I misinterpreted the meaning of the "team name" TOT.
        + I now understand that this means Total, but before I intepreted it as Toronto. I consolidated all player stats correctly, except I included the TOT row as well. This led to player's games being counted twice. 
        + The fix will involve removing the TOT column from the player's stats before consolidation.
    
---

## Completed
+ ~~Scrape award voting/winners.~~
+ ~~Add relevant team stats and award voting data to player data.~~

---
