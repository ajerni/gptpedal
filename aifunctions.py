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

    system_template = """You are a python expert using the pyo library for audio signal processing.
    You always use this template to embed your reply: {dictionary_template}. In this dictionary you fill in the values of the
    parameters that you need to create the desired sound effect. Do not change the structure of this template. Just adjust the parameters to your needs.
    "use":1 swichtes on an effect and "use":0 does not use that effect.
    You always reply with the complete dictionary template. Also keep the values in the template that
    you did not change to create the effet. Your reply is the complete dictionary only (formatted as a string with opening " and closing " to avoid SyntaxError: unterminated string literal). Do not add any explanation.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "Use this description to adjust your template: {output_from_qa}.\nFormat instructions: No explanations or text in your reply. Only reply with the completely filled parameters dictionary template."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    response_chain = LLMChain(llm=llm, prompt=chat_prompt)
    res = response_chain.run(
        dictionary_template=default_values, output_from_qa=response
    )

    return res
