from langchain.embeddings import OpenAIEmbeddings

# from langchain.text_splitter import (
#     RecursiveCharacterTextSplitter,
#     CharacterTextSplitter,
# )
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

# from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import json

with open("sel_default_values.txt", "r") as f:
    default_values = json.load(f)


from dotenv import load_dotenv

load_dotenv()


def generateEffect(query):
    # loader = TextLoader("descriptions.txt")
    # documents = loader.load()
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # vectorstore = FAISS.from_documents(docs, embeddings)

    # vectorstore.save_local("./", "faiss_index")
    vectorstore = FAISS.load_local("./", embeddings, "faiss_index")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    similars = vectorstore.similarity_search(query=query, k=3)
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
    response = qa_chain.run(input_documents=similars, question=query)
    print(response)

    system_template = """You are a python expert using the pyo library for audio signal processing.
    You always use this template to embed your reply: {dictionary_template}. In this dictionary you fill in the values of the
    parameters that you need to create the desired sound effect. Do not change the structure of this template. Just adjust the parameters to your needs.
    "use":1 swichtes on an effect and "use":0 does not use that effect.
    You always reply with a complete dictionary template for the effects you used. Your reply is the complete dictionary only (formatted as a string with opening " and closing " to avoid SyntaxError: unterminated string literal). Do not add any explanation.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "Use this description to adjust your template: {output_from_qa}.\n{format_instructions}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt],
    )

    format_instructions = """
    The output should be formatted like the input template but only contain the used effects and with opening " and closing " arround the whole output to allow conversion from string to dict later on.
    Here is the output schema:
    ```
    {default_values}
    ```
    """

    response_chain = LLMChain(llm=llm, prompt=chat_prompt)
    res = response_chain.run(
        dictionary_template=default_values,
        output_from_qa=response,
        format_instructions=format_instructions,
    )

    return res


def createNewClass(query):
    # loader = TextLoader("effects_full.txt")
    # documents = loader.load()
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # vectorstore = FAISS.from_documents(docs, embeddings)

    # vectorstore.save_local("./", "faiss_effects_full")
    vectorstore = FAISS.load_local("./", embeddings, "faiss_effects_full")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    similars = vectorstore.similarity_search(query=query, k=3)
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
    response = qa_chain.run(input_documents=similars, question=query)
    print(response)
