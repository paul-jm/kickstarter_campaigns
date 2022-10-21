# Kickstarter Campaign Forecasting

Kickstarter would like to reduce its proportion of `failed` campaigns, i.e. campaigns for which the amount of money pledged by backers is inferior to the user's initial goal.

## Data

The plublic dataset comes from Kickstarter - `data/input/ks_dataset.xlsx`.

## Pipeline

Pipeline is detailed and commented `pipeline.ipynb`.
Requirements are listed in `requirements.txt`.
Several auxiliary functions are in `functions/` for different steps of the code.

## Outcome

The goal is to forecast the `pledge_usd` variable - the amount raised by each campaign by taking into account the campaign name, duration, month launched, the currency & country of origin, as well as the product's main category.

The prediction can be suggested as a goal to every user, in order for them to decide whether their original objective was too ambitious. By deploying an XGBoost model - parameters are not optimized as there is significant overfitting, assuming all campaigners used our prediction as their objective, we have reduced significantly the proportion of failed campaigns.