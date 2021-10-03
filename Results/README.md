# Individual Award Winners

+ This is where I use SkLearn ML algorithms to predict individual awards

---

## Some Notes:

+ These algorithms are "learning" what an MVP, MIP, etc. by looking at other years. NOT by actually understanding what
  makes that player good.
    + This means that SMOTY predictions aren't concerned with rather the player actually came off the bench or not.
    + MIP predictions aren't concerned with improvement year over year. They're only taking into consideration what
      previous winners look like.
+ There are inherent flaws in using previous years as a guide to pick the next winner.
    + Firstly, there are so few samples (40 years) that the system heavily weights previous winners.
        + For example, MJ won MVP so many times, the system puts a lot of stock into players with similar stats.
        + MJ played like MJ year after year with slight variations, so regardless of if a player is better, it will
          likely pick MJ again.
    + Secondly, if a player comes along that puts up stats different from anyone who has come before them (Think Stephen
      Curry), The system isn't likely to pick them.