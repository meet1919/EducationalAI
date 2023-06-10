from langchain.chains.router.embedding_router import EmbeddingRouterChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.router import MultiPromptChain
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.chains.llm import LLMChain
from langchain.vectorstores import Chroma
from professor_prompts import SCIENCE_PROFESSOR_PROMPTS, COMMERCE_PROFESSOR_PROMPTS

load_dotenv(find_dotenv())

class Tutor:

    def __init__(self, professor_prompts):

        llm = ChatOpenAI(model_name='gpt-3.5-turbo')
        destination_chains = {}
        names_and_descriptions = []
        for p_info in professor_prompts:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain
            names_and_descriptions.append((name, p_info['description']))
        default_chain = ConversationChain(llm=llm, output_key="text")

        # Embedding Router chain
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
        
class ScienceTutor(Tutor):

    def __init__(self):
        super().__init__(SCIENCE_PROFESSOR_PROMPTS)
    
    def assist_with(self, query):
        return super().assist_with(query)
    
class CommerceTutor(Tutor):

    def __init__(self):
        super().__init__(COMMERCE_PROFESSOR_PROMPTS)

    def assist_with(self, query):
        return super().assist_with(query)