import asyncio
from contextlib import redirect_stdout
import io
import streamlit as st

from client.client import process_prompt

st.title("Ethical Research Assistant")

prompt = st.text_area("What ethical dilemmas are we exploring today?")

if st.button("Submit") and prompt.strip():
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        asyncio.run(process_prompt(prompt))
    st.text(output_buffer.getvalue())