from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool

from app.snowflake_bedrock_query import snowflake_answer
# from utils import react_system_prompt
from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

### knowledge base 
import logging
import time
import os 

import boto3
from botocore.client import BaseClient


global_sql ='NA'

logger = logging.getLogger(__name__)


# os.environ['OPENAI_API_KEY']= "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"


# llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.1)
llm = OpenAI(model="gpt-3.5-turbo-instruct")
# llm = OpenAI(model="gpt-4-0613", temperature=0)


# Function to update the global variable
def update_global(sql_query):
    global global_sql  # Declare global_var as global within the function
    global_sql = sql_query

def _get_global_var()-> str:
    global global_sql
    return global_sql


def query_snowflake(query : str):

    """to query snowflake tables for crime data and suburb details tables using natural language"""
    # """
    # This function collects all necessary information, rent, annual growth, age to execute the sql_db_chain aganist crime_data and property_details like median property price, demographic info tables in snowflake get an answer generated, taking
    # a natural language question in and returning an answer and generated SQL query.
    # :param question: The question the user passes in from the frontend
    # :return: The final answer in natural langauge along with the generated SQL query.
    # """
    res = snowflake_answer(query)
    # import pdb; pdb.set_trace()
    update_global(f'Snowflake\n SQL Query: \n {res[0]}')
    return str({"sql_query": res[0], "result": res[1]})

snowflake_tool = FunctionTool.from_defaults(fn=query_snowflake)

# def multiply(a: int, b: int) -> int:
#     """Multiply two integers and returns the result integer"""
#     return a * b


# multiply_tool = FunctionTool.from_defaults(fn=multiply)

# def add(a: int, b: int) -> int:
#     """Add two integers and returns the result integer"""
#     return a + b

# add_tool = FunctionTool.from_defaults(fn=add)


def google_search(input_query: str):

    """recent crimes only in different suburbs """

    # google_api_key = ''
    # search_engine_id = ''

    # os.environ["GOOGLE_API_KEY"] = google_api_key
    # os.environ["GOOGLE_CSE_ID"] = search_engine_id

    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )

    update_global('Google Search')

    res = (tool.run(input_query))

    return res

google_tool = FunctionTool.from_defaults(fn=google_search)


#### knowledge base search 
def _return_aws_service_client( resource_name='bedrock', run_time=True) -> BaseClient:
        region_name = 'us-east-1'
        
        """
        This funtion returns the appropriate aws service client
        :param resource_name: the resource name for which the client needs to be created
        :param run_time: If resource is 'bedrock' and the value is true, returns the
        run time client, else the normal client
        :return: Returns the appropriate client for the resource
        """
        if resource_name == "bedrock":
            if run_time:
                service_client = boto3.client(
                    service_name="bedrock-agent-runtime",
                    region_name=region_name)
            else:
                service_client = boto3.client(
                    service_name="bedrock-agent",
                    region_name=region_name)
        elif resource_name == "iam":
            service_client = boto3.resource("iam")

        return service_client


def knowledge_base_search(query: str):

    """suburb profile from knowledge base, if want to compare profile between two suburbs"""
    knowledge_base_id = 'DG9RUX6ZCG'
    client = _return_aws_service_client(run_time=True)
    response = client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            'text': query
        },
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 2
            }
        },
        nextToken='loan'
    )

    # print(response) 
    update_global('RAG Using Vector Search')
    return str({"response": response, "owner": 'kamal'})

knowledgebase_tool = FunctionTool.from_defaults(fn=knowledge_base_search)


# agent = ReActAgent.from_tools([multiply_tool, add_tool, google_tool, knowledgebase_tool, snowflake_tool], llm=llm, verbose=True)
# agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})



# res = agent.chat("What is 20+(2*4)? Calculate step by step?")
# res =  agent.chat("Is there any crime reported in South Windsor recently?")

# res = agent.chat("can you compare property profile between airds?")

# res = agent.chat("how many rows in crime_data table?")
# res = agent.chat("which suburb has highest median property price?")

# print(res)
# print(global_sql)

