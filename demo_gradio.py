import gradio as gr
from principal_agent.coaching_agent import SchoolBot

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