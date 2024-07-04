import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data from CSV into pandas DataFrame
data = data = pd.read_csv('TrainingMode.csv', encoding='latin1')

# Feature selection (including new features)
features = ['home_team_price', 'away_team_price', 'home_team_spread', 'away_team_spread']
target = ['bet_type', 'chosen_team']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

# Initialize and train a Random Forest classifier for bet type prediction
clf_bet_type = RandomForestClassifier(n_estimators=100, random_state=42)
clf_bet_type.fit(X_train, y_train['bet_type'])

# Make predictions on the testing set for bet type
y_pred_bet_type = clf_bet_type.predict(X_test)

# Initialize and train a Random Forest classifier for chosen team prediction
clf_chosen_team = RandomForestClassifier(n_estimators=100, random_state=42)
clf_chosen_team.fit(X_train, y_train['chosen_team'])

# Make predictions on the testing set for chosen team
y_pred_chosen_team = clf_chosen_team.predict(X_test)

# Evaluate the model for bet type
accuracy_bet_type = accuracy_score(y_test['bet_type'], y_pred_bet_type)
print(f"Model accuracy for bet type prediction: {accuracy_bet_type}")

# Evaluate the model for chosen team
accuracy_chosen_team = accuracy_score(y_test['chosen_team'], y_pred_chosen_team)
print(f"Model accuracy for chosen team prediction: {accuracy_chosen_team}")
