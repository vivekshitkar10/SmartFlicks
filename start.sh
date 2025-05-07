#!/bin/bash
echo "Downloading similarity.pkl from Dropbox..."
wget "https://www.dropbox.com/scl/fi/z4p5rj7p21kucbxqy1l8p/similarity.pkl?rlkey=3s6krcfdh6jtnzslag8mf2j56&st=5hzrlev9&dl=1" -O similarity.pkl

if [ -f similarity.pkl ]; then
    echo "Download successful."
else
    echo "Download failed."
    exit 1
fi

streamlit run app.py
