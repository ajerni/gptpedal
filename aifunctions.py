from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# from parameter_desc import PARAMDESC
from sel_default_values import default_values

from dotenv import load_dotenv

load_dotenv()


def generateEffect(query):
    loader = TextLoader("descriptions.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    similars = vectorstore.similarity_search(query=query, k=3)
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
    response = qa_chain.run(input_documents=similars, question=query)
    print(response)

    system_template = """You are a python expert using the pyo library for audio signal processing.
    You always use this template to embed your reply: {dictionary_template}. In this dictionary you fill in the values of the
    parameters that you need to create the desired sound effect. "use":1 swichtes on an effect and "use":0 does not use that effect.
    You always reply with the filled in parameters dictionary only.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "Create a sound effect for: {input_question}. Reply with the filled in parameters dictionary only."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    response_chain = LLMChain(llm=llm, prompt=chat_prompt)
    res = response_chain.run(
        dictionary_template=default_values, input_question=response
    )
    print(res)
    return res
