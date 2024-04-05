from crewai import Task
from textwrap import dedent



class TurtlesTasks:
    def scrape_website_content(self,agent, search_terms,expected_output, website_url=None, description=None):
        if description is None:
            description = f"search and Scrape website content based on provided search term: {search_terms} and scrape the optional website URL."
        expected_output = f"Full content extracted from the search results based on the provided search terms {search_terms}."

        return Task(
            agent=agent,
            description=description,
            expected_output=expected_output,
            search_terms=search_terms,
            website_url=website_url
        )

    def craft_short_form_content(self, agent, expected_output, description=None):
        if description is None:
            description = "Craft compelling Blog content comprising of 500 words based on research from reasearch agent."
        expected_output = "Compelling blog content, should contain atleast 500 words ."

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    def generate_social_media_posts(self, agent,blog_content):
        return Task(description=dedent(f"""    
            **Task**: Generate Social Media Posts
            **Description**: Generate quirky and engaging social media posts from the content provided by the Blog/Writer agent {blog_content}.
                
        """),
            expected_output=f"""Social Media content of 280 characters based on blog content:{blog_content}""",
            agent=agent,
                    )