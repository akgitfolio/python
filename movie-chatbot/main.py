from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

movie_genres = ["action", "adventure", "comedy", "drama", "horror", "sci-fi", "thriller"]
api_endpoint = "http://www.omdbapi.com/?apikey=YOUR_API_KEY&"

def recommend_movie(user_preferences):
    params = {"type": "movie", "plot": "short", "r": "json"}
    for key, value in user_preferences.items():
        if value:
            params[key] = value

    response = requests.get(api_endpoint, params=params)
    data = response.json()

    if data.get("Response") == "True":
        movie = data.get("Search")[0]
        return f"I recommend watching {movie.get('Title')} ({movie.get('Year')}). It's a {movie.get('Genre')} movie starring {movie.get('Actors')} and directed by {movie.get('Director')}."
    else:
        return "Sorry, I couldn't find a movie that matches your preferences."

class ActionRecommendMovie(Action):
    def name(self):
        return "action_recommend_movie"

    def run(self, dispatcher, tracker, domain):
        user_preferences = {
            "genre": tracker.get_slot("genre"),
            "actor": tracker.get_slot("actor"),
            "director": tracker.get_slot("director"),
            "mood": tracker.get_slot("mood")
        }

        recommendation = recommend_movie(user_preferences)
        dispatcher.utter_message(text=recommendation)

        return []

class AskForGenre(Action):
    def name(self):
        return "action_ask_genre"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="What kind of movie are you in the mood for? (e.g., action, comedy, drama)")
        return []

class AskForActorOrDirector(Action):
    def name(self):
        return "action_ask_actor_or_director"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Is there a specific actor or director you like? (optional)")
        return []

class AskForMood(Action):
    def name(self):
        return "action_ask_mood"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="What kind of mood are you looking for? (e.g., happy, sad)")
        return []

domain_yml = """
intents:
  - recommend_movie

entities:
  - genre
  - actor
  - director
  - mood

slots:
  genre:
    type: text
  actor:
    type: text
  director:
    type: text
  mood:
    type: text

responses:
  utter_ask_genre:
    - text: "What kind of movie are you in the mood for? (e.g., action, comedy, drama)"
  utter_ask_actor_or_director:
    - text: "Is there a specific actor or director you like? (optional)"
  utter_ask_mood:
    - text: "What kind of mood are you looking for? (e.g., happy, sad)"

actions:
  - action_recommend_movie
  - action_ask_genre
  - action_ask_actor_or_director
  - action_ask_mood
"""

stories_yml = """
stories:
  - story: recommend a movie
    steps:
      - intent: recommend_movie
      - action: action_ask_genre
      - action: action_ask_actor_or_director
      - action: action_ask_mood
      - action: action_recommend_movie
"""

with open("domain.yml", "w") as domain_file:
    domain_file.write(domain_yml)

with open("data/stories.yml", "w") as stories_file:
    stories_file.write(stories_yml)
