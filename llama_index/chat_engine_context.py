"""
ContextChatEngine is a simple chat mode built on top of a retriever over your data.

For each chat interaction:

first retrieve text from the index using the user message
set the retrieved text as context in the system prompt
return an answer to the user message
This approach is simple, and works for questions directly related to the knowledge base and general interactions.

If you're opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
"""

import openai
import os

os.environ["OPENAI_API_KEY"] = "API_KEY_HERE"
openai.api_key = os.environ["OPENAI_API_KEY"]

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

data = SimpleDirectoryReader(input_dir="./data/paul_graham/").load_data()
index = VectorStoreIndex.from_documents(data)

from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about an essay discussing Paul Grahams life."
    ),
)
response = chat_engine.chat("Hello!")
print(response)

# > Hello! How can I assist you today?

response = chat_engine.chat("What did Paul Graham do growing up?")

print(response)

# > Growing up, Paul Graham had a keen interest in writing and programming. He spent a lot of time writing short stories, although he admits that they weren't particularly good. In terms of programming, he started working with computers in 9th grade when he had access to an IBM 1401 computer at his school. He learned an early version of Fortran and experimented with writing programs on punch cards. However, he found it challenging to figure out what to do with the computer since he didn't have much data to work with. It wasn't until microcomputers became available that he truly delved into programming, starting with a kit-built microcomputer called the Heathkit. Eventually, he convinced his father to buy a TRS-80, which allowed him to write simple games, create a word processor, and explore programming further.

response = chat_engine.chat("Can you tell me more?")

print(response)

# Reset conversation state
chat_engine.reset()

response = chat_engine.chat("Hello! What do you know?")
print(response)

# > Hi there! I know a lot about Paul Graham's life. He is an entrepreneur, programmer, and investor who is best known for co-founding the venture capital firm Y Combinator. He is also the author of several essays on technology and startups, including the influential essay "Hackers and Painters". He has had a long and successful career in the tech industry, and his experiences have shaped his views on entrepreneurship and technology.

# Streaming Support

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
data = SimpleDirectoryReader(input_dir="./data/paul_graham/").load_data()

index = VectorStoreIndex.from_documents(data)

chat_engine = index.as_chat_engine(chat_mode="context", llm=llm)

response = chat_engine.stream_chat("What did Paul Graham do after YC?")
for token in response.response_gen:
    print(token, end="")

# > After stepping down from his role at Y Combinator (YC), Paul Graham focused on pursuing different interests. Initially, he decided to dedicate his time to painting and see how good he could become with focused practice. He spent most of 2014 painting, but eventually ran out of steam and stopped.

# > Following his break from painting, Graham returned to writing essays and also resumed working on Lisp, a programming language. He delved into the core of Lisp, which involves writing an interpreter in the language itself. Graham continued to write essays and work on Lisp in the years following his departure from YC.

