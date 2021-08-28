# NBA
A repository to keep my NBA data and a few projects.

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

## To-do (No Order)
+ Scrape award voting/winners. (In Progress)
+ ~~Scrape~~ Team Per Game, Advanced, and Shooting stats and consolidate them. 
+ The [Team Linear Regression Notebook](https://github.com/Kallbrig/NBA/blob/main/ML%20-%20Team/team_linear_regression.ipynb) is unfinished.
+ Decide on/implement a new way to store the scraped data. The current method is going to get messy incredibly quickly.
+ Use normalization in comparing players across years. Maybe add it in to the MVP predictions as well to prevent stat inflation bias. 
    + Maybe use a "distance from the average" metric.
+ Rewrite Scrapers using pd.read_html() because it's just a better way to do things.
    + Feel bad because I just discovered this 2 days ago.
+ Add relevant ~~team stats~~ and award voting data to player data.
+ Develop a single all-stat scraper that consolidates all stats when first scraped.
    + Add in team stats before consolidating traded players. Use weighted average to give a rough estimate of how good the player's various teams are.
---
