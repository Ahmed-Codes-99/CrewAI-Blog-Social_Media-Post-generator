import os
from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from crewai_tools import SeleniumScrapingTool
from crewai_tools import ScrapeWebsiteTool
    
    OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.7)

scrape_tool = ScrapeWebsiteTool()
selenium_tool = SeleniumScrapingTool()

class TurtlesAgents:
    def __init__(self):
        
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.Ollama = Ollama(model="openhermes")
        self.llm_llmstudio = ChatOpenAI(openai_api_base="http://localhost:1234/v1/chat/completions",
                                        openai_api_key="",
                                        model_name="deepseek coder 6")

    def researcher_scraper(self):
        return Agent(
            role=" Expert Researcher and Summarizer",
            backstory=dedent(f"""You are and expert in researching and summarizing news. Send summarized content to Writer Agent."""),
            goal=dedent(f"""research and scrape content and provide summarized content to the writer agent."""),
            tools=[SearchTools.search_internet,selenium_tool,scrape_tool],
    
            allow_delegation=False,
            verbose=True,
            llm=OpenAIGPT35,
            memory=True,
        )

    def blog_writer(self):
        return Agent(
            role="Expert Blog Writer",
            backstory=dedent(f"""You are a renowned content creator, known for your thoughtful and insightful articles. 
                             You transform complicated content into easy to understand narratives. 
                             You are tasked with writing blog content based on the given search term and text content sent to you by “Researcher Agent. 
                             After blog is complete send to Social Media Influencer agent."""),
            goal=dedent(f"""Craft compelling blog content on the given search term and the content provided to you by the researcher agent."""),
             tools=[SearchTools.search_internet],
             
            allow_delegation=False,
            verbose=True,
            llm=OpenAIGPT35,
        )
        
    def social_media_influencer(self):
        return Agent(
            role="Social Influencer, content summarizer and social media poster",
            backstory=dedent(f"""You are an Expert Vetted social media influencer and manager. You are known for your sleuthing abilities and your ability to generate complicated content sent from Agent Writer into Social media posts in 280 characters or less."""),
            goal=dedent(f"""summarize and Craft a compelling social media post from the blog content porovided by the writer agent"""),
              tools=[SearchTools.search_internet],
      
            allow_delegation=False,
            memory=True,
            verbose=True,
            llm=OpenAIGPT35,
        )
