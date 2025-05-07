import streamlit as st
import pickle
import requests
from pyarrow.compute import index  # Ensure you need this import, as it's not used in the code below

# Page branding
st.set_page_config(
    page_title="SmartFlicks 🎥",         # 🔤 Name shown on browser tab
    page_icon="🍿",                      # 🔣 Favicon (browser tab icon)
    layout="centered",                   # or "wide"
    initial_sidebar_state="auto"         # or "expanded", "collapsed"
)

st.title("Smart Movie Recommender 🤖💡")

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3e7e2378273b45f83320fc8c16405bfa&language=en-US")
    data = response.json()
    return f"http://image.tmdb.org/t/p/w500/{data['poster_path']}"

def recommend(movie):
    """Function that recommends top 5 movies"""
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

# Load full DataFrame
movies_dict = pickle.load(open('movies.pkl', 'rb'))

# Ensure movie_titles is a clean list
movie_titles = movies_dict['title'].values.tolist()

# Try loading the similarity.pkl file
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("The similarity file could not be loaded. Please try again later.")
    similarity = None  # Prevent further errors if similarity is not loaded

if similarity:  # Ensure the similarity matrix is loaded before proceeding
    Selected_Movie_name = st.selectbox(
        "🍿 Pick a Movie",
        [""] + movie_titles,
        index=0
    )

    def recom():
        """Gives movie recommendations only after selecting a Movie"""
        if st.button("Recommend"):
            st.write("🎬 Here are your Recommendations :")
            names, posters = recommend(Selected_Movie_name)

            # Display recommendations in 5 columns
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    # Centered Movie Title using HTML and styling
                    col.markdown(f"""
                        <div style="display: flex; flex-direction: column; align-items: center;">
                            <img src="{posters[idx]}" style="height: 220px; object-fit: cover; border-radius: 5px;"/>
                            <p style="text-align: center; margin-top: 10px;">{names[idx]}</p>
                        </div>
                        """, unsafe_allow_html=True)

    if Selected_Movie_name != "":
        st.write("You selected :", Selected_Movie_name)
        recom()
    else:
        st.write("Please select a movie name to get recommendations")
else:
    st.write("Please wait while we load the similarity data.")
