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
                    f"Read through the following papers:\n\n{links}\n\n"
                    f"The original query was: {query}, based on the papers provided, you will generate an unbiased response to the users query, focusing on the ethical dilenmas and moral implications of the topic. The response has to have references to the papers provided, and you must always provide a source for every claim you make. Converse with the vocabulary of a teenager. Be friendly\n\n"
                    f"The reference you will use if there are two authors is of this template: [Surname of author & Surname of other author + , + Year paper was made] (DO NOT USE AS CITED BY)\n\n"
                    f"If there are three or more authors, use the first author's surname followed by 'et al.' and the year of publication, like this: [Surname of first author et al + , + Year paper was made] (DO NOT USE AS CITED BY)\n\n"
                    f"Remember, the links should not be included in the summary\n\n"
                    f"Use the following template to reference the papers: [claim + (reference)] DO NOT SAY 'AS REFERENCED BY'\n\n"
                    f"The links can be included after the summary ends in a separate section called 'Bibilography'\n\n"
                    f"Do not use statements like \" Author has claimed that\" or \"Author has said that\", instead say the statement and then reference it using the above template.\n\n"
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
