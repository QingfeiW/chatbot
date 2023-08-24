#!/usr/bin/env python
# coding: utf-8

# In[2]:


#coding part
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from htmlTemplates import css, bot_template, user_template
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
#load api key lib
from dotenv import load_dotenv
import base64


#Background images add function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
#add_bg_from_local('images.jpeg')  

# gpt methods
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_text(text=text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
 
    return vectorstore



def get_conversation_chain(vectorstore):
    
    general_system_template = r"""
Remember that you can only use import files to make all the answers.
You first introduce them the concepts of body types.Let the users know that you can make suggestions on relative exercises and diet plans. \


If the users still not sure about their body type after your introduction, remember to ask them if they want to take a body type quiz with this link:
https://www.everydayhealth.com/fitness/do-you-know-your-body-type/

if the user asks you for food or diet plan recommendations, remember to ask them if he/she wants the recommendations \
based on his/her body type or not at first. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.\

Given a specific context,such as the users ask for advice of recommended food or 7day meal plan, please \
give the answer in the form of number list. \
---
{context}
---
"""
    general_user_template = """Question:```{question}```
    Helpful Answer:"""
    
    messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)]
    
    qa_prompt = ChatPromptTemplate.from_messages( messages )
    
    llm = OpenAI(temperature=0)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    qa = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(temperature=0), 
        retriever=retriever,
        memory=memory,
#         return_source_documents=True,
#         return_generated_question=True,
        combine_docs_chain_kwargs={'prompt': qa_prompt}
    )

    return qa

# def change_text():
#     st.session_state.something = st.session_state.widget
#     st.session_state.widget = ''

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


            
def main():
    load_dotenv()
    
    st.write(css, unsafe_allow_html=True)
    
#     if 'something' not in st.session_state:
#         st.session_state.something = ''
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
        
    st.header('🧑KnowMoreAboutYourBody CHATBOT')
    st.markdown('''
    What's your body type? You might answer the question with a response like “hot,” “flabby,” “curvy.” 
    But there's a new way to figure out what your natural-born body type is.
    
    WHY it's important: Knowing your body's natural tendencies can help you work with your body, rather than against it. 
    That way, you can customize your nutrition and exercise plan to fit your needs and set realistic goals to help you succeed.

    ''')
        
# st.button("clear text input", on_click=clear_text)
# st.write(input)

        
    user_question = st.text_input("Ask a question to the bot:")
    
    if user_question:
        handle_userinput(user_question)
  
        
    #upload a your pdf file
    with st.sidebar:
        st.subheader("Upload Documents")
        st.markdown('''
        We already provided professional resources, but you can upload other relative files as well!😊
        ''')    
        pdf_docs= st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        
        if pdf_docs is not None:
            if st.button("Process"):
                with st.spinner("Processing"):
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    
                    # Clear chat history
                    st.session_state.chat_history = None
                    
    if st.session_state.conversation is not None:
        if st.session_state.chat_history is None:
            # Greet the user
            greeting = "Hello, I am a BuildBodyShape bot, an automated service to help you know more     about your body type, and to provide suggestions on diet plans and exercises for losing weight.     How can I help you today?"
            st.write(bot_template.replace("{{MSG}}", greeting), unsafe_allow_html=True)



if __name__=="__main__":
    main()


# In[ ]:




