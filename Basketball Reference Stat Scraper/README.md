# Basketball Reference Stat Scraper

This is a homebrewed stat scraper for Basketball Reference. It scrapes every player/team's stats throughout history (1980+)


## What It Does:

+ Scrapes and cleans stats from basketball reference.
+ Scrapes all basic stats for every player from 1980-Current and organizes them by year using bs4
+ Scrapes all basic and advanced team stats from 1980-Current and organizes them by year using selenium


## Some Oddities:

+ Basketball Reference treats players that were traded as seperate entries in the table. In cleaning, these players are combined into a single player and their team is changed to "Traded".

+ Sometimes the traded players have an outrageous number of games per season (100+). This is a direct representation of the stats on the website. I don't know why, but it's not an error in the code.

+ The selenium scraper works using selenium instead of bs4 because the basketball reference website changes formatting several times throughout the years. It's easier to download bballref's stats directly instead of using 3-4 custom built solutions with bs4.

+ The selenium scaper is SLOW. Like 15+ min slow. This is definitely partly due to my slow internet, but I added an excessive amount of time.sleep() into it to counteract that. If your internet isn't as slow as mine, it can definitely be sped up.

## Why I Did This:

+ I needed all stats for several projects I'm working on and this seemed like a fun project. 

## Still To-Do (Will I Ever Get To These?)

+ A bs4 based team stat scraper. It will be 10,000x faster.
+ Add scraped data to the repository.
+ Reorganize file structure in the repository
+ Update team stat scraper to be faster when I get back to better internet

## What I Learned:

+ Web Scraping using Beautiful Soup 4.
+ Web Scraping using Selenium.
+ Data manipulation using Pandas.
+ Dataset Generation techniques.
+ Generating your own dataset is harder than it looks in tutorials.


