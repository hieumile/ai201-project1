
import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="BU CS Professor Reviews") as demo:
    gr.Markdown("## BU CS Professor Unofficial Guide")
    gr.Markdown("Ask questions about BU CS professors based on real student reviews.")

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What do students say about Sullivan's teaching style?"
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()