# If we want to keep campaigns that are only successful or failed
keep_only_finished_campaigns = True

# Remove catgory col because too fragmented
remove_cat_col = True

# Set datestring to make output immutable
from datetime import datetime
date_string = datetime.now().strftime("%Y%m%d_%H%M")

# NLP params
min_df = 20
max_df = 0.1

# Algo params
seed = 1
test_size = 0.2

# XGBoost params
eval_metric = 'rmse'
learning_rate = 0.025
n_estimators = 750
max_depth = 50
colsample_bytree = 0.5
subsample = 0.5