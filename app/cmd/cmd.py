import asyncio
import asyncclick as click

from client.client import process_prompt

@click.command()
async def cli():
    """Simple CLI to fetch papers based on a prompt."""
    while True:
        prompt = click.prompt("Enter a prompt (or 'quit' to exit)")
        if prompt.strip().lower() in ["quit", ":q"]:
            break
        try:
            result = await process_prompt(prompt)
            click.echo("\n" + result + "\n")
        except Exception as e:
            click.echo(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(cli())
