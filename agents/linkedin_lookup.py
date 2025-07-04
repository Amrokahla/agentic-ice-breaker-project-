import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from tools.tools import get_profile_url_tavily


def lookup(name: str):
    llm = ChatGoogleGenerativeAI(model= "gemini-2.0-flash", google_api_key= os.environ['GEMENI_API_KEY'])

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                        Your answer should contain only a URL"""
    
    prompt = PromptTemplate(template= template, input_variables=['name_of_person'])

    tools_for_agent = [
        Tool(
            name= "Crawl google for linkedin profile page",
            func= get_profile_url_tavily,
            description= "usefull when you need to get linkedin profile url"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm= llm, tools= tools_for_agent, prompt= react_prompt)
    agent_excutor = AgentExecutor(agent= agent, tools= tools_for_agent, verbose= True)

    result = agent_excutor.invoke(input= {"input": prompt.format_prompt(name_of_person = name)})

    linkedin_url = result['output']
    return linkedin_url

if __name__ == '__main__':
    linkedin_profile_url = lookup("amr kahla")
    print(linkedin_profile_url)