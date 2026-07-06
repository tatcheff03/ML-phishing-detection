import joblib
from sklearn.ensemble import RandomForestClassifier # random forest model
from sklearn.model_selection import train_test_split # splits the dataset into training and testing 
from sklearn.metrics import classification_report # generates classification metrics (accuracy, precision, recall, f1-score)
import pandas as pd

dataset= pd.read_csv('dataset.csv') # load dataset 

# split the dataset into features (X) and labels (y)
X = dataset.drop(columns=["label"])
y = dataset["label"]

# split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,      # 20%-testing, 80%-training
    random_state=42     # ensures reproducible split each time
)

# Initialize and train the Random Forest model
model = RandomForestClassifier(class_weight='balanced')
model.fit(X_train, y_train) 

# predictions on the test set
predictions = model.predict(X_test) 
# evaluate model performance using classification metrics 
# (outputs accuracy, precision, recall, f1-score)
print(classification_report(y_test, predictions)) 
# save trained model to file
joblib.dump(model, 'model.pkl') 