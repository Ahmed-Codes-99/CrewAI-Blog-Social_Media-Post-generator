import os
import sys
from crewai import Crew, Process
from textwrap import dedent
from agents import TurtlesAgents
from tasks import TurtlesTasks
from dotenv import load_dotenv

load_dotenv()

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
            expected_output="Compelling blog content, should contain atleast 500 words ."
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

if __name__ == "__main__":
    print("## Welcome to Turtles Crews AI!")
    print("--------------------------------")

    # Crew 1
    search_terms = input(dedent("Please provide search terms for Crew 1: "))
    website_url = input(dedent("Please provide the website URL for Crew 1 (optional, press Enter if none): "))
    researcher_task_description = input(dedent("Please provide the task description for the researcher_scraper agent in Crew 1: "))
    blog_writer_task_description = input(dedent("Please provide the task description for the blog_writer agent in Crew 1: "))

    crew1 = Crew1()
    crew1_result = crew1.run(search_terms, website_url, researcher_task_description, blog_writer_task_description)

    # Crew 2
    blog_content = crew1_result
    
    crew2 = Crew2()
    crew2_result = crew2.run(blog_content)

    print("\n\n########################")
    print("## Here is your Crew 1 result:")
    print("########################\n")
    print(crew1_result)

    print("\n\n########################")
    print("## Here is your Crew 2 result:")
    print("########################\n")
    print(crew2_result)

