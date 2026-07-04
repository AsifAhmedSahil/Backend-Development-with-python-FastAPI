from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score
import pandas as pd
import joblib

print("Loading Datasets")

data = fetch_california_housing()

# x means input data and y means scikit learn theke all price k nibe means y amne predict kroar try kortesi

x = pd.DataFrame(data.data,columns=data.feature_names)
y = data.target

# print number of rows
print(f"total records: {x.shape[0]}")

# split the data
# test_size = 0.2 mane holo 20% data test er jonno baki 80% amr training e 
#  random state = random shuffle hobe data jokhon code k run krbo
# x_train = train data 80% , x_test = test 20% data , same as y 

X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.2,random_state=42)

# Training a model
# here n_estimators=100 , means more tree is acuracy more
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# here fit mane train hoise ei data er upor 
model.fit(X_train,Y_train)

# predict krbo 20% test data er upor
y_pred = model.predict(X_test)
mae = mean_absolute_error(Y_test,y_pred)
r2 = r2_score(Y_test,y_pred)

print(f"average error: ${mae * 100000:,.0f}")

# save as file

joblib.dump(model,"house_model.joblib")
joblib.dump(list(x.columns),"house_features.joblib")


