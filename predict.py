import joblib
import pandas as pd
from preprocess import preprocess_url
from huggingface_hub import hf_hub_download

# Dictionary mapping model IDs to their respective file names
model_names = {
    "0": "malicious_url_model_adaclf.joblib",
    "1": "malicious_url_model_extratreeclf.joblib",
    "2": "malicious_url_model_rfclf.joblib",
    "3": "malicious_url_model_sgdclf.joblib"
}

# Mapping from type to category
type_to_category = {
    "benign": 0,
    "defacement": 1,
    "phishing": 2,
    "malware": 3
}

# Load model from Hugging Face Hub
def load_model_from_hf_hub(model_id, hf_username, hf_repo_name):
    model_name = model_names[model_id]
    model_path = hf_hub_download(repo_id=f"{hf_username}/{hf_repo_name}", filename=model_name)
    model = joblib.load(model_path)
    return model

# Function to load model and predict probabilities
def load_model_and_predict(url, model_id):
    hf_username = "somashekar2002"
    hf_repo_name = "PhisShield"

    # Load the trained model from Hugging Face Hub
    model = load_model_from_hf_hub(model_id, hf_username, hf_repo_name)

    # Preprocess the URL
    features = preprocess_url(url)

    # Convert features to DataFrame (assuming the model was trained on a DataFrame)
    feature_names = ['URL_Length', '@', '?', '-', '=', '.', '#', '%', '+', '$', '!', ',', '//', 
                     'Abnormal_URL', 'Has_HTTPS', 'Digit_Count', 'Letter_Count', 'Has_Shortening_Service', 
                     'Has_IP_Address', 'Has_javascript_Code', 'Has_Text_Encoding']
    
    feature_df = pd.DataFrame([features], columns=feature_names)

    # Make prediction probabilities
    probabilities = model.predict_proba(feature_df)[0]

    # Map class labels to human-readable names using type_to_category
    class_names = {v: k for k, v in type_to_category.items()}

    # Determine the class with the highest probability
    max_prob_index = probabilities.argmax()
    predicted_class = class_names[model.classes_[max_prob_index]]

    # Prepare the output dictionary
    output = {
        "class": predicted_class,
        "probabilities": {
            class_names[model.classes_[i]]: float(probabilities[i]) for i in range(len(model.classes_))
        }
    }

    return output

if __name__ == "__main__":
    # Example usage:
    url = "http://example.com/somepath?query=1"
    model_id = "2"  # Should be a string matching one of the keys in model_names
    prediction = load_model_and_predict(url, model_id)
    print("Prediction:", prediction)
