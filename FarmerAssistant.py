from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage # Import message types
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import Image, display
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceBgeEmbeddings # create vector embeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader # extract text from pdf files
from langchain.vectorstores import Chroma # stores vector embeddings in a vector db
from langchain.chains import RetrievalQA # Combines a retriever (like Chroma) with a language model to generate answers based on retrieved documents.
from langchain.prompts import PromptTemplate # Structures input to ensure the model generates the desired output.
from langchain.text_splitter import RecursiveCharacterTextSplitter # Splits large text documents into smaller chunks for more efficiency
import os
import requests

working_dir = os.getcwd()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ API KEY is not set in the .env file")

class State(TypedDict):
    query: str
    category: str
    sentiment: str
    weather: str
    response: str
    chat_history: List[BaseMessage] # Use BaseMessage for flexibility (HumanMessage, AIMessage)

llm = ChatGroq(
    groq_api_key = GROQ_API_KEY,
    temperature=0,
    model_name = "llama-3.3-70b-versatile"
)
mental_health_pdf_path = os.path.join(working_dir, "Farmer AI Assistant", "RAG Model Documents", "mental_health_Document.pdf")
def create_vector_db():
  loader = DirectoryLoader('/content/data/', glob='*.pdf', loader_cls=PyPDFLoader) # can contain multiple documents
  documents = loader.load()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap = 50)
  texts = text_splitter.split_documents(documents)
  embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
  vector_db = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
  vector_db.persist()

  print("Chroma DB created and data saved")

  return vector_db

def setup_qa_chain(vector_db, llm):
  retriever = vector_db.as_retriever()
  prompt_templates = """ You are a compassionate mental health chatbot. Respond thoughtfully to the following question based on the provided context:
    {context}
    User: {question}
    Chatbot: """

  PROMPT = PromptTemplate(
      template=prompt_templates, input_variables=["context", "question"]
  )

  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      chain_type="stuff",
      retriever=retriever,
      return_source_documents=True,
      chain_type_kwargs={"prompt": PROMPT},
  )

  return qa_chain

  # persist_directory specifies the directory where the vector database will be stored on disk. This allows you to save and reload the vector embeddings instead of recomputing them every time.

def categorize(state: State) -> State:
  "Technical, Billing, General"
  prompt = ChatPromptTemplate.from_template(
      "Categorize the following Farmer query into one of these categories: "
      "Financial, Personal, Farming Assistance, Education, Government Schemes, Plant Disease. Query: {query}"
  )
  chain = prompt | llm
  category = chain.invoke({"query": state["query"]}).content
  return {**state, "category": category}

def analyze_sentiment(state: State) -> State:
  prompt = ChatPromptTemplate.from_template(
      "Analyze the sentiment of the following customer query"
      "Response with either 'Positive', 'Neutral' , or 'Negative'. Query: {query}"
  )
  chain = prompt | llm
  sentiment = chain.invoke({"query": state["query"]}).content
  return {**state, "sentiment": sentiment}

def handle_Financial(state: State) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Financial support agent."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}")
    ])
    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "chat_history": state["chat_history"]}).content.strip()
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response or "I'm sorry, I couldn't process your request.", "chat_history": new_history}

def handle_Weather(state: State) -> State:
    response = "Please visit the Weather information page of this website"
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response, "chat_history": new_history}

def handle_Personal(state: State) -> State:
    response = "Error: Default response if QA chain fails."
    try:
        if 'qa_chain' not in globals():
             print("Error: QA Chain (qa_chain) not found in global scope.")
             response = "Error: QA Chain for personal queries not initialized."
        else:
            global qa_chain
            result = qa_chain.invoke({"query": state["query"]})
            response = result.get("result", "I'm sorry, I couldn't find relevant information in my documents for your query.")

    except Exception as e:
        print(f"Error during RAG query for Personal category: {e}")
        response = f"An error occurred while processing your personal query: {e}"

    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response, "chat_history": new_history}


def handle_Farming_Assistance(state: State) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Farming Assistance AI. Provide practical advice and support."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}")
    ])
    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "chat_history": state["chat_history"]}).content.strip()
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response or "I'm sorry, I couldn't provide farming assistance.", "chat_history": new_history}

def handle_general(state: State)->State:
  prompt = ChatPromptTemplate.from_messages([
      ("system", "Provide a general support response to the following query"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("human", "{query}")
  ])
  chain = prompt | llm
  response = chain.invoke({"query": state["query"], "chat_history": state["chat_history"]}).content
  new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
  return {**state, "response": response or "I'm sorry, I couldn't provide response to your query.", "chat_history": new_history}

def handle_Education(state: State) -> State:
    response = "Please Check the educational related videos provided in our website."
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response, "chat_history": new_history}

def handle_Government_Schemes(state: State) -> State:
    response = "Please visit the Government Schemes Page of Our website for more information regarding this."
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response, "chat_history": new_history}

def handle_Plant_Disease(state: State) -> State:
    response = "Please Visit the Crop Care Page of Our Website for more information regarding this."
    new_history = state["chat_history"] + [HumanMessage(content=state["query"]), AIMessage(content=response)]
    return {**state, "response": response, "chat_history": new_history}

def escalate(state: State) -> State:
  return {"response": "This query has been escalate to a human agent due to its negative sentiment"}

def route_query(state: State) -> str:
    # Get category and sentiment, converting to lowercase for case-insensitive matching
    category = state.get("category", "").lower()
    sentiment = state.get("sentiment", "").lower()
    query = state.get("query", "").lower()

    # First check for negative sentiment
    if sentiment == "negative":
        return "escalate"

    # Then check categories (using case-insensitive matching)
    if "financial" in category:
        return "handle_Financial"
    elif "weather" in category:
        return "handle_Weather"
    elif "personal" in category:
        return "handle_Personal"
    elif "education" in category:
        return "handle_Education"
    elif "government" in category or "scheme" in category:
        return "handle_Government_Schemes"
    
    # Check for farming assistance vs plant disease detection
    elif "farming" in category or "agriculture" in category:
        # If query contains disease-related keywords but is about protection/prevention/management
        if any(word in query for word in ["disease", "pest", "infection", "sick", "illness"]):
            if any(word in query for word in ["how to", "prevent", "protect", "manage", "control", "treat", "solution", "remedy"]):
                return "handle_Farming_Assistance"
            # If query is specifically about disease detection/verification
            elif any(word in query for word in ["check", "verify", "detect", "identify", "diagnose", "test"]):
                return "handle_Plant_Disease"
            else:
                return "handle_Farming_Assistance"
        return "handle_Farming_Assistance"
    
    # Only route to Plant Disease if it's specifically about disease detection/verification
    elif "plant" in category or "disease" in category or "crop" in category:
        if any(word in query for word in ["check", "verify", "detect", "identify", "diagnose", "test"]):
            return "handle_Plant_Disease"
        return "handle_Farming_Assistance"
    else:
        return "handle_general"

def main():
  print("Initializing LLM...")

  # Declare qa_chain as global so handler functions can access it
  global qa_chain

  db_path = mental_health_pdf_path # This is the PDF *file* path
  persist_dir = "./chroma_db" # This is the Chroma *directory*

  # --- Database Loading/Creation Logic ---
  # Consider unifying the path logic. Currently uses db_path for checking
  # but create_vector_db uses '/content/data/' and persists to './chroma_db'.
  # The loading logic uses db_path as persist_directory which is incorrect.

  vector_db = None # Initialize vector_db
  embeddings = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  # Correctly check if the PERSIST DIRECTORY exists
  if os.path.exists(persist_dir) and os.path.isdir(persist_dir):
      print(f"Loading existing vector DB from {persist_dir}")
      try:
          vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
          print("Vector DB loaded successfully.")
      except Exception as e:
          print(f"Error loading vector DB from {persist_dir}: {e}")
          print("Will attempt to recreate the database.")
          vector_db = None # Reset on loading error
  else:
      print(f"Persistence directory '{persist_dir}' not found.")

  # If DB loading failed or directory didn't exist, try to create it
  if vector_db is None:
      print("Attempting to create vector database...")
      # Make sure the source directory for create_vector_db is correct
      # Currently hardcoded to '/content/data/' inside create_vector_db
      # It should likely use the directory containing mental_health_pdf_path
      pdf_directory = os.path.dirname(mental_health_pdf_path)
      print(f"Using PDF directory: {pdf_directory}") # For debugging
      try:
          # Modify create_vector_db to accept paths if possible
          # For now, assuming it uses the correct path or '/content/data/' is intended
          loader = DirectoryLoader(pdf_directory, glob='*.pdf', loader_cls=PyPDFLoader) # Load from correct dir
          documents = loader.load()
          if not documents:
              raise ValueError(f"No PDF documents found in {pdf_directory}")
          text_splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap = 50)
          texts = text_splitter.split_documents(documents)
          vector_db = Chroma.from_documents(texts, embeddings, persist_directory=persist_dir)
          vector_db.persist()
          print(f"Chroma DB created and data saved to {persist_dir}")
      except Exception as e:
          print(f"Error creating vector database: {e}")
          print("Failed to initialize vector database. Personal queries may not work.")
          # Handle the error appropriately - maybe exit or disable personal queries


  # --- QA Chain Setup ---
  if vector_db:
      print("Setting up QA chain...")
      try:
          qa_chain = setup_qa_chain(vector_db, llm)
          print("QA chain setup complete.")
      except Exception as e:
          print(f"Error setting up QA chain: {e}")
          qa_chain = None # Ensure qa_chain is None if setup fails
  else:
      print("QA chain setup skipped as vector_db initialization failed.")
      qa_chain = None

  # --- Chat Loop ---
  # Initialize chat history
  chat_history = []

  print("\n--- Chatbot Ready (Type 'exit' to quit) ---")
  while True:
      query = input("\nHuman: ").strip()
      if query.lower() == "exit":
          print("Exiting the chatbot.")
          break
      if not query:
          continue

      # Prepare the input state for the graph
      current_state = {
          "query": query,
          "chat_history": chat_history
          # Other state keys like category, sentiment, response will be populated by the graph
      }

      # Invoke the graph
      try:
          # Use .stream for intermediate steps or .invoke for final result
          final_state = app.invoke(current_state)
          answer = final_state.get("response", "Sorry, I encountered an issue processing your query.")
          print(f"\nChatbot: {answer}")
          # Update the history for the next turn using the final state's history
          chat_history = final_state.get("chat_history", chat_history) # Update history from graph output
      except Exception as e:
          print(f"\nError during graph execution: {e}")
          # Optionally, decide how to handle history on error (e.g., revert?)

workflow = StateGraph(State)

workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_Financial", handle_Financial)
workflow.add_node("handle_Weather", handle_Weather)
workflow.add_node("handle_Personal", handle_Personal)
workflow.add_node("handle_Farming_Assistance", handle_Farming_Assistance)
workflow.add_node("handle_Education", handle_Education)
workflow.add_node("handle_Government_Schemes", handle_Government_Schemes)
workflow.add_node("handle_Plant_Disease", handle_Plant_Disease)
workflow.add_node("handle_general", handle_general)
workflow.add_node("escalate", escalate)

workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_conditional_edges(
    "analyze_sentiment",
    route_query,{
        "handle_Financial" : "handle_Financial",
        "handle_Weather" :  "handle_Weather",
        "handle_Personal" : "handle_Personal",
        "handle_Farming_Assistance": "handle_Farming_Assistance",
        "handle_Education": "handle_Education",
        "handle_Government_Schemes": "handle_Government_Schemes",
        "handle_Plant_Disease": "handle_Plant_Disease",
        "handle_general" : "handle_general",
        "escalate": "escalate"
    }
)

workflow.add_edge("handle_Financial", END)
workflow.add_edge("handle_Weather", END)
workflow.add_edge("handle_Personal", END)
workflow.add_edge("handle_Farming_Assistance", END)
workflow.add_edge("handle_Education", END)
workflow.add_edge("handle_Government_Schemes", END)
workflow.add_edge("handle_Plant_Disease", END)
workflow.add_edge("handle_general", END)
workflow.add_edge("escalate", END)

workflow.set_entry_point("categorize")

app  = workflow.compile()

if __name__ == "__main__":
  main()

