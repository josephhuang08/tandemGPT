import gradio as gr
from setup import Setup

# Callback function to show generated AI audio block 
def show_audio(generate, bot_msg):
    if generate:
        filename = setup.audio_file(bot_msg)
        return gr.Audio(value=filename)

def show_record():
    return gr.Button(value="Record", size='sm', visible=True)

with gr.Blocks() as demo:
    setup = Setup()
    # header
    gr.Markdown("<center><h1>TandemGPT</h1></center>")

    # settings contains language, silence duration and start button
    gr.Markdown("<h2>Settings</h2>")
    with gr.Row():
        lang = gr.Radio(["english", "german", "chinese"], label="Select Language", value="english")
        silence_duration = gr.Slider(1,5, label="Silence duration", step=1)
        generate_AI_speach = gr.Checkbox(label="Generate AI speach", value=True)
        save_button = gr.Button(value="Save", size='sm')
    
    # user
    with gr.Row():
        gr.Markdown("<h2>User</h2>")
        record_button = gr.Button(value="Record", size='sm', visible=False)
    with gr.Accordion("View user message"):
        user_msg = gr.Textbox(show_label=False)
    with gr.Accordion("Correction and suggestions", open=False):
        correction = gr.Markdown()

    # bot
    gr.Markdown("<h2>Bot</h2>")
    with gr.Accordion("View bot message", open=False):
        bot_msg = gr.Textbox(show_label=False)
    with gr.Accordion("Explanation", open=False):
        explanation = gr.Markdown()
    audio = gr.Audio()
    
    # actions
    save_button.click(fn=setup.save, inputs=[lang, silence_duration])
    save_button.click(fn=show_record, outputs= record_button)
    record_button.click(fn=setup.record, outputs=user_msg)
    user_msg.change(fn=setup.get_bot_msg, inputs=user_msg, outputs=bot_msg)
    user_msg.change(fn=setup.get_correction, inputs=user_msg, outputs=correction)
    bot_msg.change(fn=setup.get_explanation, inputs=bot_msg, outputs=explanation)
    bot_msg.change(fn=show_audio, inputs=[generate_AI_speach, bot_msg], outputs=audio)
    live=True

if __name__ == "__main__":
    demo.queue(max_size=20).launch(share=True)