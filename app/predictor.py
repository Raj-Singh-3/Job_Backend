import joblib
import numpy as np
import pandas as pd

# Load trained XGBoost model and encoders
xgb_model = joblib.load("/home/raj-ubn/Desktop/Project/Fake-Job-Post-Detection/backend/app/xgboost_model.pkl")  # Load trained model
label_encoders = joblib.load("/home/raj-ubn/Desktop/Project/Fake-Job-Post-Detection/backend/app/label_encoder.pkl")  # Load label encoders
# tfidf_vectorizer = joblib.load("./backend/models/tfidf_vectorizer.pkl")  # Load TF-IDF (if used)


def preprocess_data(job_data):
    """Convert chatbot-extracted job post data into a format suitable for the model"""
    job_df = pd.DataFrame([job_data])  # Convert dict to DataFrame

    # ✅ List of categorical columns that require encoding
    categorical_cols = [
        "Job_Title", "Job_Location", "Department", "Profile", "Type_of_Employment",
        "Experience", "Qualification", "Type_of_Industry", "Operations",
        "Telecommunication", "Company_Logo", "Job_Benefits"
    ]

    for col in categorical_cols:
        if col in job_df.columns:
            try:
                # ✅ Apply Label Encoding using pre-saved mappings
                job_df[col] = job_df[col].map(label_encoders[col]).fillna(-1).astype(int)
            except KeyError:
                print(f"Warning: {col} contains unseen values. Assigning default encoding (-1).")
                job_df[col] = -1  # Assign default encoding for unseen categories

    # ✅ Apply TF-IDF on Job Description
    # job_desc_tfidf = tfidf_vectorizer.transform(job_df["Job_Description"])
    job_df.drop(columns=["Job_Description"], inplace=True)  # Remove text column

    # ✅ Convert to numpy and concatenate TF-IDF features
    # job_features = np.hstack((job_df.values, job_desc_tfidf.toarray()))

    return job_features  # Ready for prediction


def predict_fraud(job_data):
    """Predict whether the job post is fraudulent"""
    try:
        # ✅ Preprocess the job data
        job_features = preprocess_data(job_data)

        # ✅ Make prediction using XGBoost
        fraud_prediction = xgb_model.predict(job_features)[0]

        return "Yes" if fraud_prediction == 1 else "No"

    except Exception as e:
        print(f"Error in fraud detection: {str(e)}")
        return "Unknown"




# import joblib
# import numpy as np
# import pandas as pd

# # Load trained XGBoost model and encoders
# xgb_model = joblib.load("backend/models/xgboost_model.pkl")  # Load trained model
# label_encoders = joblib.load("backend/models/label_encoders.pkl")  # Load label encoders
# tfidf_vectorizer = joblib.load("backend/models/tfidf_vectorizer.pkl")  # Load TF-IDF (if used)



# def preprocess_data(job_data):
#     """Convert chatbot-extracted job post data into a format suitable for the model"""
#     job_df = pd.DataFrame([job_data])  # Convert dict to DataFrame

#     # ✅ Apply Label Encoding for categorical columns
#     categorical_cols = ["job_title", "job_location", "department", "profile", "type_of_employment", "qualification", "type_of_industry"]
#     for col in categorical_cols:
#         job_df[col] = label_encoders[col].transform(job_df[col])  # Apply saved encoders

#     # ✅ Apply TF-IDF on Job Description
#     job_desc_tfidf = tfidf_vectorizer.transform(job_df["job_description"])
#     job_df.drop(columns=["job_description"], inplace=True)  # Remove text column

#     # ✅ Convert to numpy and concatenate TF-IDF features
#     job_features = np.hstack((job_df.values, job_desc_tfidf.toarray()))

#     return job_features  # Ready for prediction


# def predict_fraud(job_data):
#     """Predict whether the job post is fraudulent"""
#     try:
#         # ✅ Preprocess the job data
#         job_features = preprocess_data(job_data)

#         # ✅ Make prediction using XGBoost
#         fraud_prediction = xgb_model.predict(job_features)[0]

#         return "Yes" if fraud_prediction == 1 else "No"

#     except Exception as e:
#         print(f"Error in fraud detection: {str(e)}")
#         return "Unknown"
