import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import os

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(data):
    # Convert Date to datetime and extract Year, Month, Day
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data.drop(columns='Date', inplace=True)

    # Label encode Location and Store
    le = LabelEncoder()
    data['Location'] = le.fit_transform(data['Location'])
    data['Store'] = le.fit_transform(data['Store'])

    return data

# Standardize the data
def scale_data(X_train, X_test):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test

def split_data(data, target_column, test_size=0.2, random_state=42):
    X = data.drop(columns=target_column)
    y = data[target_column]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model

def save_model(model, filepath):
    joblib.dump(model, filepath)

def test_model(model, X_test, y_test):
    return model.score(X_test, y_test)

def main():
    # Load the data
    data = load_data('data/credit_card_records.csv')

    # Preprocess the data
    data = preprocess_data(data)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data, 'Fraudulent')

    # Scale the data
    X_train, X_test = scale_data(X_train, X_test)

    # Train the model
    model = train_model(X_train, y_train)

    # Ensure the 'data' directory exists
    os.makedirs('models', exist_ok=True)

    # Save the model
    save_model(model, 'models/model.pkl')

    # Test the model
    score = test_model(model, X_test, y_test)
    # print score is:
    print("Model accuracy is: ", score)
    return score

# This is the entry point of the script
# It will be executed when the script is run directly
# but not when it is imported as a module
# This is a common Python convention to allow or prevent parts of code from being run when the modules are imported
# It is a good practice to include this in your scripts
# to ensure that the script can be used as a module without executing the main code
# Test the model

if __name__ == "__main__":
    main()