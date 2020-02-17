import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.aux_functions import neighbourhood_algorithm
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.preprocessing import StandardScaler

# 0. DATA LOADING (Previously has been created through creating_data_table.py script).
df = pd.read_csv('data/sampled_data.csv')

# 1. Feature Creation
# Group into fields and create the mean of the pixels
df_grouped = df.groupby('fid').mean().reset_index()

# Neighbourhood Algorithm: Detect which label have the fields next to each field
# (the closest fields based on a threshold).
matrix_distances = neighbourhood_algorithm(df=df_grouped,
                                           field_id='fid',
                                           label_col='label',
                                           x_coord_col='row_loc',
                                           y_coord_col='col_loc',
                                           threshold=50)

# We remove the column 0, which is neighbourhood with other test fields (no real label).
matrix_distances.drop(axis=1, columns=['0.0'], inplace=True)
matrix_distances = matrix_distances.rename(columns={"variable": 'fid'})
matrix_distances = matrix_distances.fillna(0)

# Set the number of neighbours in percentages.
percentage_distances = matrix_distances.set_index('fid')
percentage_distances = percentage_distances.div(percentage_distances.sum(axis=1), axis=0)
percentage_distances.reset_index(inplace=True)
df_grouped['fid'] = df_grouped['fid'].astype(str)
df_grouped = pd.merge(df_grouped, percentage_distances, left_on='fid', right_on='fid', how='left')

# Switch Tile variable to boolean
dummies_tile = pd.get_dummies(df_grouped['tile'], prefix='tile')
df_grouped = pd.merge(df_grouped, dummies_tile, how='left', left_index=True, right_index=True)
df_grouped.drop('tile', axis=1, inplace=True)

# Standard Scaler
scaled_df = df_grouped.copy()
col_names = df_grouped.columns[4:]
features = scaled_df[col_names]
scaler = StandardScaler().fit(features.values)
features = scaler.transform(features.values)
scaled_df[col_names] = features


# Separate between train and test
train = scaled_df.loc[scaled_df.label != 0]
test = scaled_df.loc[scaled_df.label == 0]

# 2. ML Model
# Training set is the values of the pixels (from column 5 onwards), whereas label is the column 'label'.
X_train, y_train = train[train.columns[5:]], train['label']

params = {}
params['learning_rate'] = [0.05]
params['objective'] = ['reg:squarederror']
params['max_depth'] = [3]

# GridSearch
model = xgb.XGBClassifier(learning_rate=0.05, objective='multi:softprob', scoring='neg_log_loss', max_depth=3, verbosity=2)
model.fit(X_train.fillna(0), y_train, verbose=True)

# 3. GENERATE PREDICTIONS AND SUBMIT
# Get the predicted probabilities on the pixels columns of test set (columns 5 onwards)
preds = model.predict_proba(test[test.columns[5:]])

# Create a dataframe with the test Field ID's
prob_df = pd.DataFrame({
    'Field_ID': test['fid'].values
})


# Rename the label columns to make the submission
for c in range(1, 8):
    prob_df['Crop_ID_' + str(c)] = preds[:, c - 1]

# Save the submission
prob_df.to_csv('MLSubmission.csv', index=False)
