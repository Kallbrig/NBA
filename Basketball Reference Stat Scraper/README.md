# Basketball Reference Stat Scraper

This is a storage place for some homebrewed stat scrapers for Basketball Reference. It scrapes every player/team's stats
throughout history (1980+)


## What It Does:

+ Scrapes and cleans stats from basketball reference.
+ Scrapes all basic stats for every player from 1980-Current and organizes them by year using bs4
+ Scrapes all basic and advanced team stats from 1980-Current and organizes them by year using selenium
+ It does more than this, but I outsourced a good bit of the voting scraping, so most of that only works in Google Colab
  and isn't stored here.


## Some Oddities:

+ Basketball Reference treats players that were traded as separate entries in the table. In cleaning, these players are
  combined into a single player and their team is changed to "Traded".
    + This needs to be fixed to create hybrid "teams". These teams will be a combination of the teams the player played
      for in a single year.

+ Sometimes the traded players have an outrageous number of games per season (100+). This is a direct representation of
  the stats on the website. I don't know why, but it's not an error in the code.
    + I'm an idiot. This bug only happens because I didn't realize that basketball reference already calculates total
      stats for each player's season.
    + I was scraping total stats and then individual stats again and combining them into 1. So everyone's stats were
      doubled.

+ The selenium scraper works using selenium instead of bs4 because the basketball reference website changes formatting
  several times throughout the years. It's easier to download bballref's stats directly instead of using 3-4
  custom-built solutions with bs4.

+ The selenium scaper is SLOW. Like 15+ min slow. Plus it's trash. So don't use it unless you have a reason.

## Why I Did This:

+ I needed all stats for several projects I'm working on and this seemed like a fun project. 

## What I Learned:

+ Web Scraping using Beautiful Soup 4.
+ Web Scraping using Selenium.
+ Data manipulation using Pandas.
+ Dataset Generation techniques.
+ Generating your own dataset is harder than it looks in tutorials.


