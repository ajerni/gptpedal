from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from parameter_desc import PARAMDESC
from sel_default_values import default_values

from dotenv import load_dotenv

load_dotenv()


def generateEffect(query):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    system_template = """You are a python expert using the pyo library for audio signal processing.
    You will be asked to create a sound effect and your task is to generate a simple solution based on
    this description of the effects: {parameter_description}. Your response is always this
    selections dictionary: {dictionary_template}. In this dictionary you fill in the values of the
    parameters that you need to fill in.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template = "Create a sound effect for a: {input_question}. Reply with your filled in dictionary only."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    response_chain = LLMChain(llm=llm, prompt=chat_prompt)
    res = response_chain.run(
        parameter_description=PARAMDESC,
        dictionary_template=default_values,
        input_question=query,
    )
    print(res)
    return res
