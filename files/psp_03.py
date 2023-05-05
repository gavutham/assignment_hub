import pandas as pd
from sklearn.linear_model import LinearRegression

# replace it with the path to your csv data file
data = pd.read_csv("data.csv")

# Linear Regression 1

x = data.iloc[:, 1].values.reshape(-1, 1)
y = data.iloc[:, 3].values
model = LinearRegression()
model.fit(x, y)
print("The value of regression parameters for estimated proxy size and actual LOC (added+modified) are")
print("β0:", model.intercept_)
print("β1:", model.coef_[0])
print()

# Linear Regression 2

y = data.iloc[:, 4].values
model.fit(x, y)
print("The value of regression parameters for estimated proxy size and actual time taken are")
print("β0:", model.intercept_)
print("β1:", model.coef_[0])
print()


# Linear Regression 3

x = data.iloc[:, 2].values.reshape(-1, 1)
y = data.iloc[:, 3].values
model = LinearRegression()
model.fit(x, y)
print("The value of regression parameters for planned LOC (added+modified) and actual LOC (added+modified) are")
print("β0:", model.intercept_)
print("β1:", model.coef_[0])
print()

# Linear Regression 4

y = data.iloc[:, 4].values
model = LinearRegression()
model.fit(x, y)
print("The value of regression parameters for planned LOC (added+modified) and actual time taken are")
print("β0:", model.intercept_)
print("β1:", model.coef_[0])
print()

