from langchain.chains.router.embedding_router import EmbeddingRouterChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.router import MultiPromptChain
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.chains.llm import LLMChain
from langchain.vectorstores import Chroma

load_dotenv(find_dotenv())

class ScienceTutor:

    def __init__(self):

        physics_professor_template = """You are a very smart physics professor. You are great at answering questions about physics in a concise and 
        easy to understand manner. When you don't know the answer to a question you admit that you don't know.

        Here is a question:
        {input}"""


        math_professor_template = """You are a very good mathematician. You are great at answering math questions. You are so good because you are able 
        to break down hard problems into their component parts, answer the component parts, and then put them together to answer the broader 
        question.

        Here is a question:
        {input}"""

        chemistry_professor_template = """You are a very good chemist. You are great at answering chemistry questions. You are so good because you are able 
        to break down hard problems into their component parts, answer the component parts, and then put them together to answer the broader 
        question.

        Here is a question:
        {input}"""


        prompt_infos = [
            {
                "name": "physics", 
                "description": "Good for answering questions about physics", 
                "prompt_template": physics_professor_template
            },
            {
                "name": "math", 
                "description": "Good for answering math questions", 
                "prompt_template": math_professor_template
            },
            {
                "name": "math", 
                "description": "Good for answering math questions", 
                "prompt_template": chemistry_professor_template
            }
        ]

        llm = ChatOpenAI(model_name='gpt-3.5-turbo')

        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain
        default_chain = ConversationChain(llm=llm, output_key="text")

        # Embedding Router chain
        names_and_descriptions = [
            ("physics", ["for questions about physics"]),
            ("math", ["for questions about math"]),
        ]

        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {'device': 'cuda'}
        encode_kwargs = {'normalize_embeddings': False}
        router_chain = EmbeddingRouterChain.from_names_and_descriptions(
            names_and_descriptions, Chroma, HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs), routing_keys=["input"]
        )

        self.chain = MultiPromptChain(router_chain=router_chain, destination_chains=destination_chains, default_chain=default_chain, verbose=True)
    
    def assist_with(self, query):
        output = self.chain.run(query)
        return output
        

science_tutor = ScienceTutor()
answer = science_tutor.assist_with('What is black body radiation?')
print(answer)