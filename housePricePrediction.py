import pandas as pd 
import numpy  as np 
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error , mean_squared_error , r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder , StandardScaler 
import pickle

data = pd.read_csv("Housing.csv")
copy_data = data.copy()
# print(data.isnull().sum())  # handle missing data

# handle label data by encoding it
encoders = {}
for col in ["mainroad","guestroom","basement",
            "airconditioning","prefarea"]:
    le = LabelEncoder()
    copy_data[col+"_encoder"] = le.fit_transform(copy_data[col])
    encoders[col] = le        # save each encoder separately
le = LabelEncoder()


#for furnishingstatus it needs one-hot
# copy_data = pd.get_dummies(copy_data, columns=['furnishingstatus'] , dtype= int)

#scaling
standard_scale = StandardScaler()
copy_data["area_scaled"] = standard_scale.fit_transform(copy_data[["area"]])
# print(copy_data["area_scaled"])

# print(copy_data[["mainroad_encoder", "mainroad"]])

model = LinearRegression()
X = copy_data[[

"mainroad_encoder",
"parking",
"area_scaled",
"bedrooms",
"bathrooms",
"stories",
"prefarea_encoder",
"airconditioning_encoder",
"guestroom_encoder",
"basement_encoder"
]]
y = copy_data["price"]
model.fit(X ,y)
prediction_price =model.predict(X)
# accuracy
mae =mean_absolute_error(y ,prediction_price)
mse =mean_squared_error(y , prediction_price)
accuracy =r2_score(y , prediction_price)
rsme = np.sqrt(mse)

print(f"average error : {round(mae, 2)} , means square error: {round(mse, 2)} , accuracy of model: {round(accuracy,2)} reverse of mse: {rsme}")

#plot it 

plt.figure(figsize=(6,6))
plt.scatter(y, prediction_price, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()])  # perfect prediction line
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted House Prices")
plt.grid(True)
# plt.show()

with open("houseprediction.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "scaler": standard_scale,
        "encoders": encoders
    }, f)

print('save is saved')