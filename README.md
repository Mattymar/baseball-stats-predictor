# baseball-stats-predictor
For this project, my goal was to get a sense of a baseball hitter's true ability by taking some of the variance out of the batting average statistic. The premise was to look only at advanced stats that were not heavily influenced by randomness and then beat the baseline prediction of the player's previous season's batting average.

Baseball is known as a game where you can do seemingly everything right and still fail.  As a hitter, you can hit a ball as hard as possible, but if you hit it right at a fielder, you're out.  There's a common saying in the game that "it all evens out", but it's been shown that even a full season's stats can be heavily influenced by luck.

Still, there are stats like Hard Hit %, which uses the exit velocity of the ball off the bat, that can measure the true abilities of a hitter.  My aim was to use this type of stat, without the aid of the baseline stat itself, to beat the baseline for a player's next season's batting average.

## Data
For the project, I scraped data from FanGraphs.com, with particular emphasis on batted ball and advanced stats.  Due to the availability of some of the statistical categories, I was only able to go back as far as 2008.

The other limitation was number of at bats a player had in a season.  Batting average varies wildly early in the season, so I only attempted to predict batting averages for players with at least 350 ABs. I relaxed this to 250 ABs for the previous season's stats (the stats that went into the model), since that should be enough ABs to get an indication of the batted ball and advanced stats that I used.

*NOTE: An astute analyst would say, "Hey, but your baseline predictions are going to suffer a tad since they're including some predictions from small sample sizes with wider variances." This is true, but our focus was on building a strong model, so I wanted the extra data. I can assure you, that we beat the baseline by a similar margin even with stricter standards. I'll add those results to the notebook when I get a chance.*

##The Approach
I urge you to take a look at the master notebook for a full run-through of my approach to this problem.  Essentially, I took most of the batted ball and advanced stats that weren't results oriented.  The only real results oriented stats that I used were strikeout rate and HR/FB ratio.  I included these stats since they added important insights to the model, without adding noise to the variance I was trying to eliminate.

I also looked at some interactions between categories. For example, I tried combining hard hit percentage with line drive percentage, with the idea being that the value gained by hitting the ball hard may be diminished if you are hitting mostly ground balls or fly balls with few line drives.

One of my strongest features turned out to be an interaction of hard hit percentage with contact percentage and swing percentage. This feature highlights the fact that more aggressive hitters who make consistent contact tend to have higher batting averages that perhaps more patient hitters who may sacrifice a few hits for an increase in on-base percentage, while also adding a few extra strikeouts.

The scope of some of these interactions really requires a full blog post to do them justice.

In addition to interactions, I tested a few extreme features.  The idea behind these was that many batted ball stats like pull percentage may have multiple phases in their impact on batting average. For example, extreme pull hitters may lose significant points in batting average due to team's being able to apply a shift.  That would suggest that batting average is inversely proportional to pull %, but it's likely that the benefits of decreasing one's pull rate diminish at a certain point.  Because of this, I wanted my model to capture the extremes. I also added a "sprayer" category, to capture players who hit the ball to all fields, which tends to be related to higher batting averages, however the benefits of "spraying" tended to be masked by the opposite field percentage category.

In a nutshell, this project was a major task in feature engineering. I only really scratched the surface of what's possible with the available data. In the future, I have plans to programatically test some more interactions and extremes.

## Results
Model MSE: 0.000511388264567  
Baselin MSE: 0.000925244219653

The current best model has an R-squared of .4655 using Elastic Net regularization with cross validation. This model does quite a bit better than the baseline of using the previous season's batting average.

**Some Highlights**
Chris Johnson (2013) Previous Season: .321 -- Model Prediction: .261 -- Actual: .263  
Dan Uggla (2010) Previous Season: .287 -- Model Prediction: .245 -- Actual:\
 .233 