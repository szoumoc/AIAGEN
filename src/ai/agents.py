from langgraph.prebuilt import create_react_agent
from ai.llms import get_openai_models
from ai.tools import (document_tools)  # Assuming you have a weather tool defined


def get_document_agent(model= None, checkpointer=None):

    llm_model = get_openai_models(model=model)
    agent = create_react_agent(
        model=llm_model,
        tools=document_tools,
        prompt="You are a helpful assistant in managing documents and answering user queries on general questions.",
        checkpointer=checkpointer,
    )
    return agent
