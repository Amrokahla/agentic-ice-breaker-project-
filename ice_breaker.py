from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

from agents.linkedin_lookup import lookup
from utils.linkedin import scrape_linkedin

def ice_breaker(name):
    username = lookup(name)
    linkedin_data = scrape_linkedin(profile_url= username)

    summary_temp = """
        given the information {information} about a person I want you to create:
        1- a short summary
        2- a 2 interesting facts about them
    """

    summary_prom_temp = PromptTemplate(input_variables=["information"], template=summary_temp)

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])

    chain = summary_prom_temp | llm | StrOutputParser()

    res = chain.invoke(input={'information': linkedin_data})
    print(res)



if __name__ == '__main__':
    load_dotenv()
    ice_breaker("Adham Assy")


