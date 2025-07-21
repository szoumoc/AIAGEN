from langgraph.prebuilt import create_react_agent
from ai.llms import get_openai_models
from ai.tools.documents import document_tools
from ai.tools.movie_discovery import movie_discovery_tools


def get_document_agent(model= None, checkpointer=None):

    llm_model = get_openai_models(model=model)
    agent = create_react_agent(
        model=llm_model,
        tools=document_tools,
        prompt="You are a helpful assistant in managing documents and answering user queries on general questions.",
        checkpointer=checkpointer,
        name="document-assistant"
    )
    return agent


def get_movie_discovery_agent(model=None, checkpointer=None):
    llm_model = get_openai_models(model=model)

    agent = create_react_agent(
        model=llm_model,  
        tools=movie_discovery_tools,
        prompt="You are a helpful assistant in finding and discovering information about movies.",
        checkpointer=checkpointer,
        name="movie-discovery-assistant"
    )
    return agent