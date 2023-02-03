# Basketball Reference Stat Scraper

This is a storage place for some homebrewed stat scrapers for Basketball Reference. It scrapes every player/team's stats
throughout history (1980+)

## What It Does:

+ Scrapes and cleans per game and advanced stats from basketball reference.
+ Scrapes all basic stats for every player and team from 1980-Current and organizes them by year using pandas and
  requests

## Some Oddities:

+ Basketball Reference treats players that were traded as separate entries in the table. If they play for 3 teams, each
  team will have its own entry with the player's stats from that team as well as a TOT team with their total stats.
    + Currently, this is handled by dropping all duplicate players.
    + eventually I hope to change this so that I can combine each player's team stats into a single hybrid "Team" that
      is weighted by how long a player spent at each team. This isn't a perfect solution, but its the best idea I've
      had.

---

+ These go with the old scrapers (located in the "Old" folder.)
+ ~~Sometimes the traded players have an outrageous number of games per season (100+). This is a direct representation
  of the stats on the website. I don't know why, but it's not an error in the code.~~
    + ~~I'm an idiot. This bug only happens because I didn't realize that basketball reference already calculates total
      stats for each player's season.~~
    + ~~I was scraping total stats and then individual stats again and combining them into 1. So everyone's stats were
      doubled.~~

+ ~~The selenium scraper works using selenium instead of bs4 because the basketball reference website changes formatting
  several times throughout the years. It's easier to download bballref's stats directly instead of using 3-4
  custom-built solutions with bs4.~~

+ ~~The selenium scraper is SLOW. Like 15+ min slow. Plus it's trash. So don't use it unless you have a reason.~~

## Why I Did This:

+ I needed all stats for several projects I'm working on and this seemed like a fun project.

## What I Learned:

+ Web Scraping using Beautiful Soup 4.
+ Web Scraping using Selenium.
+ Data manipulation using Pandas.
+ Dataset Generation techniques.
+ Generating your own dataset is harder than it looks in tutorials.


