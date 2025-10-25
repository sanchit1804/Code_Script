# data_science/streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Science Demo", layout="wide")

st.title("Small Streamlit Data Science App")
st.markdown("Upload a CSV, pick the target column, choose a model, and view metrics.")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV to get started. Example: a classification dataset with a target column.")
    st.stop()

# read csv
df = pd.read_csv(uploaded)
st.write("### Preview of uploaded data", df.head())

# choose target
all_columns = df.columns.tolist()
target = st.selectbox("Select target column (label)", options=all_columns)

# simple features selection: drop non-numeric by default but allow user to choose
st.write("Select feature columns (default: numeric columns excluding target)")
numeric = df.select_dtypes(include=[np.number]).columns.tolist()
default_features = [c for c in numeric if c != target]
features = st.multiselect("Features", options=all_columns, default=default_features)

if len(features) == 0:
    st.error("Please select at least one feature column.")
    st.stop()

# task type detection (very naive)
unique_vals = df[target].nunique()
task_type = "classification" if unique_vals <= 20 else "regression (not implemented)"
st.write(f"Detected: **{task_type}** (unique labels: {unique_vals})")

if task_type != "classification":
    st.warning("This demo only supports classification. Choose a categorical/binary target.")
    st.stop()

# train/test split params
test_size = st.sidebar.slider("Test size (%)", min_value=10, max_value=50, value=25) / 100.0
random_state = st.sidebar.number_input("Random state", min_value=0, max_value=9999, value=42)

# model selection
model_name = st.selectbox("Choose model", ["Logistic Regression", "Random Forest", "Baseline Dummy"])
if model_name == "Logistic Regression":
    model = LogisticRegression(max_iter=1000)
elif model_name == "Random Forest":
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
else:
    model = DummyClassifier(strategy="most_frequent")

# prepare data
X = df[features].copy()
y = df[target].copy()

# basic imputing and scaling pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("clf", model)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

with st.spinner("Training model..."):
    pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision_macro": precision_score(y_test, y_pred, average="macro", zero_division=0),
    "recall_macro": recall_score(y_test, y_pred, average="macro", zero_division=0),
    "f1_macro": f1_score(y_test, y_pred, average="macro", zero_division=0)
}

st.subheader("Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Accuracy", f"{metrics['accuracy']:.4f}")
col2.metric("Precision (macro)", f"{metrics['precision_macro']:.4f}")
col3.metric("Recall (macro)", f"{metrics['recall_macro']:.4f}")
col4.metric("F1 (macro)", f"{metrics['f1_macro']:.4f}")

st.subheader("Classification report")
st.text(classification_report(y_test, y_pred, zero_division=0))

st.subheader("Confusion matrix")
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
st.pyplot(fig)

# ROC AUC for binary problems
if len(np.unique(y_test)) == 2:
    try:
        y_score = pipeline.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_score)
        st.write(f"ROC AUC: **{auc:.4f}**")
        fpr, tpr, _ = roc_curve(y_test, y_score)
        fig2, ax2 = plt.subplots()
        ax2.plot(fpr, tpr)
        ax2.plot([0,1],[0,1],"--")
        ax2.set_xlabel("FPR")
        ax2.set_ylabel("TPR")
        ax2.set_title("ROC curve")
        st.pyplot(fig2)
    except Exception as e:
        st.info("Model does not provide probability predictions to compute ROC AUC.")

# feature importance (if model supports it)
st.subheader("Feature importances (if available)")
base_model = pipeline.named_steps["clf"]
if hasattr(base_model, "feature_importances_"):
    importances = base_model.feature_importances_
    fi = pd.Series(importances, index=features).sort_values(ascending=False)
    st.bar_chart(fi)
elif hasattr(base_model, "coef_"):
    coefs = np.abs(base_model.coef_).ravel()
    fi = pd.Series(coefs, index=features).sort_values(ascending=False)
    st.bar_chart(fi)
else:
    st.info("Selected model has no feature_importances_ or coef_.")
