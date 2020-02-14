import pandas as pd
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('data/sampled_data.csv')

# Group into fields and create the mean of the pixels
df_grouped = df.groupby('fid').mean().reset_index()

# Separate between train and test
train = df_grouped.loc[df_grouped.label != 0]
test = df_grouped.loc[df_grouped.label == 0]

# Training set is the values of the pixels (from column 5 onwards), whereas label is the column 'label'.
X_train, y_train = train[train.columns[5:]], train['label']

# Baseline prediction
model = RandomForestClassifier(n_estimators=500)
model.fit(X_train.fillna(0), y_train)


# Get the predicted probabilities on the pixels columns of test set (columns 5 onwards)
preds = model.predict_proba(test[test.columns[5:]])

# Create a dataframe with the test Field ID's
prob_df = pd.DataFrame({
    'Field_ID':test['fid'].values
})
# Rename the label columns to make the submission
for c in range(1, 8):
    prob_df['Crop_ID_'+str(c)] = preds[:,c-1]

# Save the submission
prob_df.to_csv('MLSubmission.csv', index=False)
