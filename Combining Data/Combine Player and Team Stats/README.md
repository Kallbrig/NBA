# Combine Player and Team Stats

This combines basic player stats and team stats into a single csv

---

* Not going to lie I did the improved version because I forgot I wrote the original version.
* The improved version is better though. 
    * It doesn't rely on the os module. That was a workaround because I didn't know better.
    * I also learned about the apply function and right/left/inner/outer merging in pandas.
    * It also adds in the Win% column.
    
# Some things to know:
* The improved version leaves traded players' team stats blank.
    * This is done because they don't have a team per say. 
    * The only solution I see to this is to add team stats in before the entries are combined into one. This would give a weighted average to the team stats. It's not perfect, but I see it as a good alternative to leaving them blank.
    * For now I'm leaving them blank and just dropping traded players from the table later in the process, but I'll add the above workaround to the To-Do