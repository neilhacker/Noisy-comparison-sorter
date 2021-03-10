# comparisonSorter
This is inspired by Gwerns resorter algorithm (https://www.gwern.net/Resorter#source-code). It allows a user to make pairwise comparisons of elements of a group and then uses the choix library to come up with an ordering based on bradley terry model for pairwise comparisons. 

</p>
##Comparing
</br>
When faced with a comparison you can press 1,2,8,0 (1 for prefer L, 2 for prefer R, 8 for draw, 0 for abort programme). </br></br>
to maintain some level of order but also alow for changes over time when you use the programe after the first time it will do a run through of all the items that have a score and automatically add a comparison for each of these to the comparisson list (if we had a>b>c then we will autmatically have (a,b) and (b,c) added). This means that if you were to open and then shut the program immediatly no values would change but that if you made comparisons that contradicted the ordering at the beginning of the session that would have the potential to change the ordering at the end. Contrast this with something like just being presented with a merge sort the first time you compare items and then only get to add new items in, there would be no ability to change the relative ordering of items as your views change.</br></br>
To try to make the comparisons as useful as possible the program looks through 10 pairings at random and sees if any have a <60% chance of being correctly predicted based on past information. If it finds such a pairing it will present that to the user as this will likely clarify a pairing with high uncertainty. Otherwise it will present a random pair.

</p>
##Scoring 
</br>
Once we have a relative ordering I've chosed boudnaries so that the buckets of scores are linearly decreasing in size (the first bucket has around 18% of all options, next bucket has 16% then 14% etc. This means that the top bucket (scoring 10) will have our top 2% of options in.</br></br>
This differs from the buckets Gwern used that had a shape closer to 1/x. If you have a very large corpus his shaping is probably better as it deliminates more at the top end, becuase I was only dealing with around 100 or so entries I dindn't need that much accuracy and as the ratings can be a bit fuzzy this might have lead to over precision. 
</br></br>
The program will only assing scores to items that have shown up in at least one comparison.

