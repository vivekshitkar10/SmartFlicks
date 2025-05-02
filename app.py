import streamlit as st
import pickle
import requests

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


# Load full DataFrame
movies_dict = pickle.load(open('movies.pkl', 'rb'))

# Pass only titles to the selectbox
movie_titles = movies_dict['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

Selected_Movie_name = st.selectbox(
    "🍿 Pick a Movie",
    movie_titles)

st.write("You selected :", Selected_Movie_name)

if st.button("Recommend"):
    st.write("🎬 Here are your Recommendations :")
    names, posters = recommend(Selected_Movie_name)

    # We can use loops as well
    cols = st.columns(5)  # Create 5 columns once
    for idx, col in enumerate(cols):
        with col:
            # Centered Movie Title using HTML and styling
            col.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <img src="{posters[idx]}" style="height: 220px; object-fit: cover; border-radius: 5px;"/>
                    <p style="text-align: center; font-weight: ; margin-top: 10px;">{names[idx]}</p>
                </div>
                """, unsafe_allow_html=True)

    # Without Looping
    # col1,col2,col3,col4,col5 = st.columns(5)
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.text(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.text(names[4])
    #     st.image(posters[4])
