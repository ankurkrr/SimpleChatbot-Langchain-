from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
#os.environ["HF_TOKEN"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


app = FastAPI(
    title = "Langchain Server",
    version="1.0",
    description="Langchain API server"
)


add_routes(
    app,
    ChatOpenAI(),
    path="/openai"
)

model = ChatOpenAI()

llm = Ollama(model="gpt2")

prompt1 = ChatPromptTemplate.from_template("Write an eassy about {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write an poem about {topic} for a 5 years child with 100 words")


add_routes(
    app,
    prompt1|model,
    path="/essay"
)

add_routes(
    app,
    prompt2 | llm,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
