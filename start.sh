#!/bin/bash
# Log the download process
echo "Starting the download of similarity.pkl"
gdown --no-cookies https://drive.google.com/uc?id=1xLmlmFLb4Do-R77Twyk-tt4o3LAru7YJ -O similarity.pkl
echo "Download completed."

# Check if the file exists
if [ -f similarity.pkl ]; then
    echo "similarity.pkl file downloaded successfully."
else
    echo "similarity.pkl download failed."
    exit 1
fi

# Start the Streamlit app
streamlit run app.py
