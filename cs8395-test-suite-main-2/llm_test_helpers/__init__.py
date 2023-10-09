import argparse

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

def get_llm(llm_name):
    if llm_name == "chatgpt-latest":
        return ChatOpenAI()
    elif llm_name == "openai-latest":
        return OpenAI()
    elif llm_name == "openai-latest-1024":
        return OpenAI(max_tokens=1024)
    
    raise ValueError(f"LLM '{llm_name}' not found!")


def get_args(argv):
    argv = argv[1:]
    parser = argparse.ArgumentParser(description="Run LLM test suites")
    parser.add_argument("--model", help="Model to run all test suites against", required=True)
    return parser.parse_args(argv)