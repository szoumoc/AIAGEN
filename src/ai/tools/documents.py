from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from documents.models import Documents
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL



@tool
def search_query_documents(query: str, limit: int=5, config:RunnableConfig=None):
    """
    Search the most recent LIMIT documents for the current user with a maximum of 25.
    arguments are:
    - query: string or lookup search across title or content of the document
    - limit: number of documents to return, default is 5 
      
    """
    print(config)
    limit = 5
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    default_lookups = {
        "owner_id": user_id,
        "active": True,
        "title__icontains": query,
    }



    qs = Documents.objects.filter(**default_lookups).filter(
        Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    response_data = []
    for obj in qs[:limit]:
        response_data.append({
            "id": obj.id,
            "title": obj.title,
        })
    return response_data







@tool
def list_documents(limit: int=5, config:RunnableConfig={}):
    """
    list the most recent LIMIT documents for the current user with a maximum of 25.
    arguments are:
    - limit: number of documents to return
      
    """
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    qs = Documents.objects.filter(owner_id=user_id, active=True).order_by('-created_at')
    response_data = []
    for obj in qs[:limit]:
        response_data.append({
            "id": obj.id,
            "title": obj.title,
        })
    return response_data

@tool
def get_document(document_id:int, config:RunnableConfig):
    """
    Get the details of a document for the current user
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        obj = Documents.objects.get(id=document_id, active=True)
    except Documents.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    response_data =  {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data


@tool
def create_document(title: str, content: str, config:RunnableConfig):
    """
    Create a new document to store for the user.
    arguments are:

    - title: string max characters 120
    - content: long form text in many paragraphs or pages
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise ValueError("User ID is required to create a document.")
    document = Documents.objects.create(
        owner_id=user_id,
        title=title,
        content=content,
        active=True
    )
    response_data = {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at,
    }
    return response_data



@tool
def update_document(document_id: int,title: str=None, content: str=None, config:RunnableConfig={}):
    """
    Update an existing document for the user by document id and related arguments.
    arguments are:
    - document_id:the ID of the document {optional} (you can study the document id)
    - title: string max characters 120 {optional}
    - content: long form text in many paragraphs or pages {optional}
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise ValueError("User ID is required to create a document.")
    try:
        obj = Documents.objects.get(id=document_id, active=True)
    except Documents.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()

    # document = Documents.objects.create(
    #     owner_id=user_id,
    #     title=title,
    #     content=content,
    #     active=True
    # )
    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at,
    }
    return response_data





    

@tool
def delete_document(document_id: int, config:RunnableConfig):
    """
    Delete the document for the current user by document_id or use the search_query_documents()
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise ValueError("User ID is required to delete a document.")
    try:
        obj = Documents.objects.get(id=document_id, active=True)
    except Documents.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    obj.delete()
    response_data =  {"message": "success"}
    return response_data

document_tools = [
    list_documents, 
    get_document, 
    create_document, 
    delete_document,
    update_document,
    search_query_documents
]
