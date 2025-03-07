import subprocess

def summarize_text(text: str):
    """
    Summarizes the given text using the local Ollama (LLama 3.1 8B) model.
    Adjust the subprocess command according to your local setup.
    """
    try:
        # Example: Call Ollama via the command line.
        cmd = ["ollama", "run", "llama3:8b", text]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        summary = result.stdout.strip()
        return summary
    except Exception as e:
        return f"Error during summarization: {e}"
