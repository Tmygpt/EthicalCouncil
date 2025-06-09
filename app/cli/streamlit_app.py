import asyncio
from contextlib import redirect_stdout
import io
import os
import sys
import streamlit as st
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from client.client import process_prompt


class StreamlitWriter(io.StringIO):
    """Streamlit-compatible writer that updates a placeholder as text streams."""

    def __init__(self, placeholder: "st.delta_generator.DeltaGenerator") -> None:
        super().__init__()
        self.placeholder = placeholder

    def write(self, s: str) -> int:
        written = super().write(s)
        self.placeholder.markdown(self.getvalue())
        return written


thinking_messages = [
    "Consulting the wisdom of the ancients...",
    "Aligning moral compasses...",
    "Contemplating the greater good...",
    "Reading ancient scrolls...",
    "Summoning ethical wisdom...",
    "Compiling universal truths...",
    "Deliberating with the Council of Elders...",
    "Cross-referencing moral doctrines...",
    "Pondering timeless dilemmas...",
    "Examining shades of gray...",
    "Balancing conflicting virtues...",
    "Searching ancient libraries...",
    "Consulting the archives of wisdom..." ,
    "Invoking the voices of reason...",
    "Exploring ethical frontiers...",
    "Unraveling moral paradoxes...",
]


async def shuffle_thinking(placeholder, done_flag):
    while not done_flag["done"]:
        message = random.choice(thinking_messages)
        placeholder.text(message)
        await asyncio.sleep(1.5)


async def main(prompt, placeholder):
    output_buffer = StreamlitWriter(placeholder)
    done_flag = {"done": False}

    async def run_process():
        with redirect_stdout(output_buffer):
            await process_prompt(prompt)
        done_flag["done"] = True

    # Run both tasks concurrently
    await asyncio.gather(run_process(), shuffle_thinking(placeholder, done_flag))


st.title("Council of Ethical Dilemmas")
prompt = st.text_area("The Council awaits your moral conundrum...")

if st.button("Summon the Council") and prompt.strip():
    placeholder = st.empty()
    asyncio.run(main(prompt, placeholder))
