import os
import tempfile
# from langchain_community.llms import HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from io import BytesIO
import fitz
from dotenv import load_dotenv
load_dotenv()

async def load_pdf(file):
    context = ''
    for files in file:
        print(files)
        # s=files.file  
        s=await files.read()
        pdf_stream = BytesIO(s)
        print("***************",pdf_stream)
        with fitz.open(stream=pdf_stream) as pdf_file:
            num_pages = pdf_file.page_count
            for page_num in range(num_pages):
                page = pdf_file[page_num]
                page_text = page.get_text()
                context += page_text
    return context


async def fun_rag(inputs,file):
# def fun_rag(inputs,file):
    
    repo="mistralai/Mistral-7B-Instruct-v0.3"
    llm=HuggingFaceEndpoint(repo_id=repo,
        max_length=1024,
        temperature=0.5,
        huggingfacehub_api_token=os.getenv("api_key"))
    
    
    
    # for pdf
    # loader = PyMuPDFLoader(file)
    # docs=file.load()
    # text_split= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # split=text_split.split_documents(file)
    # vectorstore=Chroma.from_documents(documents=split,embedding=HuggingFaceEmbeddings())


    #direct text
    text_split= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split=text_split.split_text(file)
    # print("split:",split)
    vectorstore=Chroma.from_texts(texts=split,embedding=HuggingFaceEmbeddings())
    reteriver=vectorstore.as_retriever()
    # Always say "thanks for asking!" at the end of the answer.
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer as concise as possible.
    Only use the information provided in the context. Do not add any extra information. If you don't know, say "I don't know."
    {context}
    Question: {question}
    Answer:"""
    rag_prompt_custom = PromptTemplate.from_template(template)
    # def format_docs(docs):
    #     return "\n\n".join(doc.page_content for doc in docs)
    rag_chain=({"context": reteriver , "question": RunnablePassthrough()}|rag_prompt_custom|llm|StrOutputParser())
    ans=rag_chain.invoke(inputs)
    print(ans)
    return ans

    



