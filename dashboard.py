import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
import chromadb

chroma_client = chromadb.PersistentClient(
    "kevin_db",
)

collection = chroma_client.create_collection(
    name="visit_lisboa",
    get_or_create=True,
)

_ = load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))

st.set_page_config(
    page_title="Kevin Demo",
    page_icon="🧊",
    # layout="wide",
    # initial_sidebar_state="expanded",
)


@st.cache_data()
def get_user_profiles():
    return pd.read_csv("data/user-profiles.csv")


@st.cache_data()
def get_visit_lisboa_events():
    return pd.read_json("data/visit_lisboa.json")


def get_recommendation(prompt):
    response = requests.post(
        # the model is a MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF
        # hosted locally using LM studio
        "http://localhost:1234/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.5,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop": ["\n"],
        },
    )
    return response.json()


def get_chroma_recommendation(prompt_list: list[str], amount_recommendations=1):
    response = collection.query(
        query_texts=prompt_list,
        n_results=amount_recommendations,
    )
    documents = response.get("documents")[0]
    metadatas = response.get("metadatas")[0]
    return pd.DataFrame(
        [
            {
                "title": metadatas[i].get("title"),
                "date": metadatas[i].get("date"),
                "description": documents[i],
            }
            for i in range(len(documents))
        ]
    )


def query_places_api(query, city):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={
            "query": query,
            "key": os.getenv("GOOGLE_PLACES_API_KEY"),
        },
    )
    data = [
        {
            "name": row.get("name"),
            "google_maps_link": f"https://www.google.com/maps/place/?q=place_id:{row.get('place_id')}",
            "rating": row.get("rating"),
            "price_level": row.get("price_level"),
            "types": row.get("types"),
            "address": row.get("formatted_address"),
        }
        for row in response.json().get("results")
    ]
    return pd.DataFrame(data)


# Set the title of the app
st.title("Kevin Demo")

user_profiles_df = get_user_profiles()

chosen_user_profile = st.selectbox("Choose a user profile", user_profiles_df["Profile"])

selected_df = user_profiles_df[user_profiles_df["Profile"] == chosen_user_profile]
current_city = st.text_input("Enter your current city:", "Lisbon")
user_input = st.text_area(
    "Enter your prompt here:",
    height=250,
    value=f"""I am a {chosen_user_profile} who is 
    {selected_df['Age'].values[0]} years old and works as a {selected_df['Occupation'].values[0]}.

    I like to travel {selected_df['Travel Style'].values[0]} and go on trips {selected_df['Travel Frequency'].values[0]}.

    My preferred destinations are {selected_df['Preferred Destinations'].values[0]}.

    I prefer to stay in {selected_df['Accommodation'].values[0]} and do {selected_df['Activities'].values[0]}.

    My interests include {selected_df['Interests'].values[0]}.

    My budget is {selected_df['Budget'].values[0]} and I am {selected_df['Tech Savvy'].values[0]}.

    """.replace(
        "    ", ""
    ).replace(
        "\n", " "
    ),
)

# Add a button
if st.button("Submit"):
    initial_prompt = f"{user_input} Please write a google search query for me to find the best restaurants in {current_city}."

    response = get_recommendation(initial_prompt)

    st.write(response.get("choices")[0].get("message").get("content"))

    query = response.get("choices")[0].get("message").get("content")

    places = query_places_api(query, current_city)

    st.data_editor(
        places.sort_values("rating", ascending=False),
        column_config={
            "google_maps_link": st.column_config.LinkColumn(
                "google_maps_link",
                display_text="Open in Google Maps",
            )
        },
        use_container_width=True,
    )

    initial_prompt = f"Please extract the nouns from the following text: {user_input}"

    response = get_recommendation(initial_prompt)

    suggested_query = response.get("choices")[0].get("message").get("content")
    # st.write(suggested_query)

    selected_df = get_chroma_recommendation(
        prompt_list=[suggested_query],
        amount_recommendations=5,
    )

    st.dataframe(
        selected_df,
        use_container_width=True,
    )
