from groq import AsyncGroq
from mcp.server.fastmcp import FastMCP
from typing import List


mcp = FastMCP("input", transport="stdio")

@mcp.tool()
async def summarize_papers(papers: List[str], query: str) -> str:
    """Generate a summary of the provided papers for the user's query."""
    client = AsyncGroq()
    links = "\n".join(papers)
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Every claim you make must be backed by a scientific paper or religious text. You can make your own interpretations, but you must always provide a source.", 
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": (
                    f"Summarize the following papers:\n\n{links}\n\n"
                    f"Please provide a concise summary of the key findings and "
                    f"implications of these papers. The original query was: {query}. "
                    f"Focus on the relevance to the topic at hand and elaborate on "
                    f"the ethical dilemnas raised by the query."
                ),
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become
        # deterministic and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 2048 tokens shared between prompt and completion.
        max_completion_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the incremental deltas returned by the LLM.
    return response.choices[0].message.content
