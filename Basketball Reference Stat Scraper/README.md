# Basketball Reference Stat Scraper

This is a homebrewed stat scraper for Basketball Reference. It scrapes every player's stats throughout history (1980+)


## What It Does:

+ Scrapes and cleans stats from basketball reference.
+ Scrapes all basic stats for every player from 1980-Current and organizes them by year

## Some Oddities:

+ Basketball Reference treats players that were traded as seperate entries in the table. In cleaning, these players are combined into a single player and their team is changed to "Traded".

+ Sometimes the traded players have an outrageous number of games per season (100+). This is a direct representation of the stats on the website. I don't know why, but it's not an error in the code.

## Why I Did This:

+ I needed all stats for several projects I'm working on and this seemed like a fun project. 

## What I Learned:

+ Web Scraping using Beautiful Soup 4.
+ Data manipulation using Pandas.
+ Dataset Generation techniques.
+ Generating your own dataset is harder than it looks in tutorials.


