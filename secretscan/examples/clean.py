# Clean example - secrets come from environment, not hardcoded.
import os

AWS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
print("Loaded from environment, not hardcoded.")
