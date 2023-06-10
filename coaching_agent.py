
from principal_prompts import PRINCIPAL_BOT_PREFIX, PRINCIPAL_BOT_FORMAT_INSTRUCTIONS, PRINCIPAL_BOT_SUFFIX
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from school_custom_tools import define_tools
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import gradio as gr
import time

load_dotenv(find_dotenv())

class SchoolBot:
    def __init__(self):
        llm = ChatOpenAI(model_name='gpt-3.5-turbo', max_tokens=2000)
        memory = ConversationBufferMemory(memory_key="chat_history", output_key='output')
        tools = define_tools()
        self.agent = initialize_agent(
            tools,
            llm,
            agent="conversational-react-description",
            verbose=True,
            memory=memory,
            return_intermediate_steps=True,
            agent_kwargs={
                'prefix': PRINCIPAL_BOT_PREFIX,
                'format_instructions': PRINCIPAL_BOT_FORMAT_INSTRUCTIONS,
                'suffix': PRINCIPAL_BOT_SUFFIX
            }
        )

    def assist_with(self, query):
        res = self.agent({"input": query[-1][0].strip()})
        query[-1][1] = ""
        for character in res['output']:
            query[-1][1] += character
            time.sleep(0.001)
            yield query

inputs = gr.inputs.Textbox(lines=7, label="Chat with AI")
outputs = gr.outputs.Textbox(label="Reply")

coachbarBot = SchoolBot()
with gr.Blocks(css='#chatbot {height: 80vh}') as demo:
    with gr.Column(scale=1):
        chatbot = gr.Chatbot(elem_id="chatbot", label='Chat with AI')
        query = gr.Textbox(placeholder='Ask anything', show_label=False)

        def user(user_message, history):
            return "", history + [[user_message, None]]

        query.submit(user, [query, chatbot], [query, chatbot], queue=False).then(
            coachbarBot.assist_with, chatbot, chatbot
        )

demo.queue()
demo.launch()