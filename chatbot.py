import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load your CSV dataset
df = pd.read_csv('synthetic_price_history.csv')
df['date'] = pd.to_datetime(df['date'])

# Sort and label data
df = df.sort_values(by=["product", "date"])
df['future_price'] = df.groupby('product')['price'].shift(-1)
df = df.dropna()
df['label'] = df.apply(lambda row: 'Buy' if row['price'] < row['future_price'] else 'Wait', axis=1)

# Features and labels
X = df[['product', 'price']]
y = df['label']

# Encode labels (Buy/Wait)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Preprocessing pipeline for product (one-hot) + pass through price
preprocessor = ColumnTransformer(
    transformers=[
        ('prod', OneHotEncoder(handle_unknown='ignore'), ['product'])
    ], remainder='passthrough'
)

# Create pipeline with preprocessing and classifier
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Save model and label encoder
joblib.dump(pipeline, 'price_model_with_product.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

# Evaluate
y_pred = pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

