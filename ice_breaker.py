from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

from agents.linkedin_lookup import lookup
from utils.linkedin import scrape_linkedin
from output_parser import person_intel_parser, PersonIntel

def ice_breaker(name: str) -> tuple[PersonIntel, str]:
    username = lookup(name)
    linkedin_data = scrape_linkedin(profile_url= username)

    summary_temp = """
        given the information {information} about a person I want you to create:
        1- a short summary
        2- a 2 interesting facts about them
        
        \n{format_instructions}
    """

    summary_prom_temp = PromptTemplate(
        input_variables=["information"], template=summary_temp,
        partial_variables= {"format_instructions": person_intel_parser.get_format_instructions()})

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])

    #chain = summary_prom_temp | llm | StrOutputParser()
    chain = summary_prom_temp | llm | person_intel_parser
    res: PersonIntel = chain.invoke(input={'information': linkedin_data})

    return res, linkedin_data.get('photoUrl')


if __name__ == '__main__':
    load_dotenv()
    ice_breaker("Amro Kahla")


