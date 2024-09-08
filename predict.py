import joblib
import pandas as pd
from preprocess import preprocess_url
from huggingface_hub import hf_hub_download

def load_model_from_hf_hub(model_name, hf_username, hf_repo_name):
    model_path = hf_hub_download(repo_id=f"{hf_username}/{hf_repo_name}", filename=model_name)
    model = joblib.load(model_path)
    return model

# Example usage
hf_username = "somashekar2002"
hf_repo_name = "PhisShield"
model_name = "malicious_url_model_extratreeclf.joblib"  # Replace with the actual model name you want to load

# Load the model from Hugging Face Hub
model = load_model_from_hf_hub(model_name, hf_username, hf_repo_name)

def load_model_and_predict(url):
    # Load the trained model from the Hugging Face hub
    clf = model
    #or if u want the faster execution of code just use this code-
    #clf='C:\Users\Somashekar\OneDrive\Desktop\PhisShield\trained_models\model_name'
    # Preprocess the URL
    features = preprocess_url(url)

    # Convert features to DataFrame (assuming the model was trained on a DataFrame)
    feature_names = ['URL_Length', '@', '?', '-', '=', '.', '#', '%', '+', '$', '!', ',', '//', 
                     'Abnormal_URL', 'Has_HTTPS', 'Digit_Count', 'Letter_Count', 'Has_Shortening_Service', 
                     'Has_IP_Address', 'Has_javascript_Code', 'Has_Text_Encoding']
    
    feature_df = pd.DataFrame([features], columns=feature_names)

    # Make prediction
    prediction = clf.predict(feature_df)
    print("Classes in the model:", clf.classes_)

    return prediction[0]  # Return the prediction for the single instance

# Example usage:
url = "http://example.com/somepath?query=1"
prediction = load_model_and_predict(url)
print("Prediction:", prediction)
