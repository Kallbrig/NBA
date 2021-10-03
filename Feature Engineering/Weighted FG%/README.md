# Weighted FG%

This is a measure of league FG% that takes into account how much a player shoots.

## Some Notes:

+ After some time has passed, I realize that this is probably not useful.
+ Taking Total League FG / Total League FGA will do the same thing. 

## What It Does:

+ Calculates the weighted average of Field Goal Percentages using Field Goal Attempts as a weight.

## Why I Did This:

+ After messing about with average stats for a while, I realized that when taking the average of a per-game percentage, It weighted players who shot different number of shots the same.
+ This means that a player who shot 0.2 shots per game counts the same as a player who shot 15 shots per game. This weighted FG% fixes that.

## What I Learned:

+ A little more familiarity with Numpy


