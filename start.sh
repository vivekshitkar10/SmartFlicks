#!/bin/bash

# Check if similarity.pickle is already downloaded
if [ ! -f "similarity.pickle" ]; then
  echo "Downloading similarity.pickle from Google Drive..."
  gdown https://drive.google.com/uc?id=1xLmlmFLb4Do-R77Twyk-tt4o3LAru7YJ -O similarity.pickle
fi

# Start the Streamlit app
streamlit run app.py
