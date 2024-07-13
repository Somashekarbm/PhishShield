from huggingface_hub import HfApi, HfFolder, upload_file
import os

# Path to your model folder
model_folder_path = r"C:\Users\Somashekar\OneDrive\Desktop\PhisShield\trained_models"

# Your Hugging Face username and repository name
hf_username = "somashekar2002"
hf_repo_name = "PhisShield"
repo_id = f"{hf_username}/{hf_repo_name}"

# Ensure you have a token for authentication
hf_token = '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'
if hf_token is None:
    raise ValueError("You need to log in to Hugging Face Hub. Run `huggingface-cli login` and follow the instructions.")

# Initialize API object
api = HfApi()

# Create repository if it doesn't exist
if not api.repo_exists(repo_id):
    api.create_repo(repo_id)

# Upload all .joblib models to the repository
for file_name in os.listdir(model_folder_path):
    full_file_name = os.path.join(model_folder_path, file_name)
    if os.path.isfile(full_file_name) and file_name.endswith('.joblib'):
        upload_file(
            path_or_fileobj=full_file_name,
            path_in_repo=file_name,
            repo_id=repo_id,
            token=hf_token
        )

print("All models have been uploaded successfully.")



'''TO LOAD AND FETCH ONE SINGLE MODEL 

from huggingface_hub import Repository
import joblib

# Path to your model file
model_path = "path/to/your/model.joblib"

# Create a repository object
repo = Repository(local_dir="local_model_repo", clone_from="username/repo_name")

# Copy your model to the local repo directory
import shutil
shutil.copy(model_path, "local_model_repo/model.joblib")

# Commit and push the model to the hub
repo.push_to_hub(commit_message="Initial commit")


TO FETCH IT-
from huggingface_hub import hf_hub_download
import joblib

# Download the model from the Hugging Face Hub
model_path = hf_hub_download(repo_id="username/repo_name", filename="model.joblib")

# Load the model
model = joblib.load(model_path)

# Now you can use the model for prediction
'''
