# Comparison sorter for noisy preferences
## Problem
Let's say you have a list of things (e.g books) you might want to create a ranked ordering of them from most liked to least liked. You could do pairwise comparisons until you had looked at every option at least once and then, if your preferences are transtitive, you should have an acyclic directed graph which you can go and turn into an ordering. The problem is that if your preferences are not transative, which they will likely not be, or if you might change your mind over time then this model is far to rigid and in fact will completely fail most of the time as you will probably have preference cycles. So we want some way of ordering items in a list that is robust to noisy preferences, i.e ones that may not always be transative.

## Solution
This solution inspired by Gwern's resorter algorithm (https://www.gwern.net/Resorter#source-code). It allows a user to make pairwise comparisons of elements of a group and then uses the choix library to come up with an ordering based on bradley terry model for pairwise comparisons. This uses likelihood estimators to judge what is probably more prefered based on a directed graph.   

## Implementation
### Set up
You need to have an csv file with all of your options in the left most column, you will also need to change the name of this file to the filename in the code (or visa versa). This will be updated after every run.

### Comparing
When faced with a comparison you can press 1,2,8,0:
* 1 for prefer the first option
* 2 for prefer second option
* 8 for draw
* 0 stop comparisons and generate scores

To try to make the comparisons as useful as possible the program looks through 10 pairings at random and sees if any have a <60% chance of being correctly predicted based on past information. If it finds such a pairing it will present that to the user as this will likely clarify a pairing with high uncertainty. Otherwise it will present a random pair.

### Scoring 
Once we have a relative ordering we want to actually assign a score out 10 to our options. One way to do this is to rank the bottom 10% with a 1, next 10% with a 2 etc. This is not super useful though, we probably care a lot more about what the very best items were then what the worst ones were. I've chosen boundaries so that the buckets of scores are linearly decreasing in size¹: 
* the first bucket has around 18% of all options
* next bucket has 16%
* next has 14% etc... 
 
This means that the top bucket (scoring 10) will have our top 2% of options in so we get much finer graind delimination for our top choices. The program will only give scores to items that have shown up in at least one comparison.

### Resorting
After the scores have been calculated a numpy array is made with the items in the correct order and with the scores of the appropirate bucket given to them in the next column. If you didn't compare all the options then the ones not compared will be left at the bottom of the list unscored.

After the first run through in all subsequent runs the program will automatically add comparisons for all the items that have a past score to the comparison list (if we had a>b>c in our list then we will automatically have (a,b) and (b,c) added). 

<li>
¹This differs from the buckets Gwern used that had a shape closer to 1/x. If you have a very large corpus his shaping is probably better as it deliminates more at the top end, becuase I was only dealing with around 100 or so entries I dindn't need that much accuracy and as the ratings can be a bit fuzzy this might have lead to over precision. 

