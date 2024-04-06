from typing import Optional
import threading

class RPMController:
    _timer: Optional[threading.Timer] = None

import os
import streamlit as st
from crewai import Crew, Process
from textwrap import dedent
from agents import TurtlesAgents
from tasks import TurtlesTasks
from dotenv import load_dotenv

load_dotenv()

# Define the correct username and password
CORRECT_USERNAME = os.getenv("YOUR_APP_USERNAME")
CORRECT_PASSWORD = os.getenv("YOUR_APP_PASSWORD")

def authenticate(username, password):
    return username == CORRECT_USERNAME and password == CORRECT_PASSWORD

class Crew1:
    def __init__(self):
        self.agents = TurtlesAgents()
        self.tasks = TurtlesTasks()

    def run(self, search_terms, website_url=None, researcher_task_description=None, blog_writer_task_description=None):
        researcher_scraper = self.agents.researcher_scraper()
        blog_writer = self.agents.blog_writer()

        scrape_website_content_task = self.tasks.scrape_website_content(
            agent=researcher_scraper,
            search_terms=search_terms,
            website_url=website_url,
            description=researcher_task_description,
            expected_output=" Extracted content from the website includes relevant text, images, and metadata related to the provided search terms. The output provides a comprehensive summary of the webpage content, including key information and insights gathered from the target website."
        )

        craft_short_form_content_task = self.tasks.craft_short_form_content(
            agent=blog_writer,
            description=blog_writer_task_description,
            expected_output="Compelling blog content, should contain at least 500 words ."
        )

        crew = Crew(
            agents=[researcher_scraper, blog_writer],
            tasks=[scrape_website_content_task, craft_short_form_content_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result

class Crew2:
    def __init__(self):
        self.agents = TurtlesAgents()
        self.tasks = TurtlesTasks()

    def run(self, blog_content):
        social_media_influencer = self.agents.social_media_influencer()

        generate_social_media_posts_task = self.tasks.generate_social_media_posts(
            blog_content=blog_content,
            agent=social_media_influencer,
        )

        crew = Crew(
            agents=[social_media_influencer],
            tasks=[generate_social_media_posts_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result




def main():
    st.title("Turtles Crew-AI")

    # Check if the user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Ask for username and password
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
            else:
                st.error("Incorrect username or password. Please try again.")
                return

    # If not logged in, return early to prevent displaying the app
    if not st.session_state.logged_in:
        return

    st.sidebar.title("Research and Blog Team")
    search_terms = st.sidebar.text_input("Search Terms")
    website_url = st.sidebar.text_input("Website URL (optional)")
    researcher_task_description = st.sidebar.text_area("Researcher Task Description")
    blog_writer_task_description = st.sidebar.text_area("Blog Writer Task Description")

    if st.sidebar.button("Run Crew 1"):
        crew1 = Crew1()
        crew1_result = crew1.run(search_terms, website_url, researcher_task_description, blog_writer_task_description)
        st.subheader("Crew 1 Result")
        st.write(crew1_result)

    st.sidebar.title("Social Media Team")
    blog_content = st.sidebar.text_area("Blog Content")

    if st.sidebar.button("Run Crew 2"):
        crew2 = Crew2()
        crew2_result = crew2.run(blog_content)
        st.subheader("Crew 2 Result")
        st.write(crew2_result)

if __name__ == "__main__":
    main()
