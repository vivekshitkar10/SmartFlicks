import os
import streamlit as st
import pickle
import gdown

# File ID from Google Drive (Your shared file link ID)
file_id = '1xLmlmFLb4Do-R77Twyk-tt4o3LAru7YJ'
file_name = 'similarity.pkl'  # Name for the file that will be downloaded

# Construct the download URL for Google Drive
url = f'https://drive.google.com/uc?id={file_id}'

# Download the file only if it is not already present
if not os.path.exists(file_name):
    gdown.download(url, file_name, quiet=False)

# Check if the downloaded file is indeed a pickle file
try:
    with open(file_name, 'rb') as f:
        similarity = pickle.load(f)
    st.write("Successfully loaded similarity.pkl!")
except Exception as e:
    st.write(f"Error loading similarity.pkl: {str(e)}")
    st.write("Please check the file format or try downloading it again.")

# Page branding
st.set_page_config(
    page_title="SmartFlicks 🎥",         # 🔤 Name shown on browser tab
    page_icon="🍿",                      # 🔣 Favicon (browser tab icon)
    layout="centered",                   # or "wide"
    initial_sidebar_state="auto"         # or "expanded", "collapsed"
)

st.title("Smart Movie Recommender 🤖💡")

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=3e7e2378273b45f83320fc8c16405bfa&language=en-US".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie):
    """Function that recommend top 5 movies"""
    movie_index = movies_dict[movies_dict['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_poster = []

    for i in movies_list:
        movie_id = movies_dict.iloc[i[0]].movie_id
        recommended_movies.append(movies_dict.iloc[i[0]].title)

        # Fetch Posters from API
        recommended_movie_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_poster


# Load full DataFrame (this is another large file you need to handle the same way)
movies_dict = pickle.load(open('movies.pkl', 'rb'))

# Pass only titles to the selectbox
movie_titles = movies_dict['title'].values

# Movie selection
Selected_Movie_name = st.selectbox(
    "🍿 Pick a Movie",
    movie_titles)

st.write("You selected :", Selected_Movie_name)

if st.button("Recommend"):
    st.write("🎬 Here are your Recommendations :")
    names, posters = recommend(Selected_Movie_name)

    # Create 5 columns to show recommended movies
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            col.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="{posters[idx]}" style="height: 220px; object-fit: cover; border-radius: 5px;"/>
                    <p style="text-align: center; font-weight: ; margin-top: 10px;">{names[idx]}</p>
                </div>
                """, unsafe_allow_html=True)
