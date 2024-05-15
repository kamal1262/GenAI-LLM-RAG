# AWS Summit Sydney 2024

## demo for AI AGentic workflow for snowflake  and Amazon Bedrock using GenAI


1. install the dependency files as per requirements.txt
2. to run this script, OpenAI key  and snowflake credentials will be required required. Please update the revant credentials in ```.env``` file
3. A RAG is developed in Amazo Bedrock using suburb profile data. you need to have AWS credentials to access the bedrock knowledge base (RAG). Copy the access credntials and paste it into your console before running the following 
4. To run the streamlit app, you need to run the followin command from the root sirectory 

Optipnal: 
5. if you want to have google search to work, you will need to provide GOOGLE_API_KEY and GOOGLE_CSE_ID in .env file as well

```
streamlit run main.py
```

### NB: The whole system can be developed using Amazon Bedrock only, Langchain latest version has some bug on db_chain module. Hence, OpenAI is used temporarily. 