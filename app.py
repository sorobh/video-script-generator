# Bring in dependencies
import os 
from apikey import apikey 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

#Set up env
os.environ['OPENAI_API_KEY'] = apikey
wiki = WikipediaAPIWrapper()

# App framework
st.title('🤖 Short Film-Script Generator 🤖')
prompt = st.text_input('Plug in your prompt here') 




### Creating Prompt templates ###
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write me a youtube video title about {topic}'
)

context_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'], 
    template='Given the title "{title}, understand relevant context from Wikipedia research: {wikipedia_research}'
)

script_template = PromptTemplate(
    input_variables=['context', 'segment_number'], 
    template='Write a script for a short film that has 5 acts- an interesting hook for opening, a challenge, a climax, a resolution, and an ending. Understand the context "{context}" of previous act, and build on it. Chronological position of each act is represented by segment number "{segment_number}" and each act builds on top of the previous one. Create a coherent script such that the 5 acts together complete one story'
)

summary_template = PromptTemplate(
    input_variables=['script_segment'], 
    template='Summarize the key points of this script segment: {script_segment} so that they can be used as context for the next act'
)


# Handling Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
context_memory = ConversationBufferMemory(input_key='title', memory_key='context_history')
script_memory = ConversationBufferMemory(input_key='composite_key', memory_key='chat_history')
summary_memory = ConversationBufferMemory(input_key='script_segment', memory_key='summary_history')




# LLMs & Chains
llm = OpenAI(temperature=0.9)

title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)

context_chain = LLMChain(llm=llm, prompt=context_template, verbose=True, output_key='context', memory=context_memory)

script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True, output_key='summary', memory=summary_memory)



# Function to create a composite key without the title
def create_composite_key(segment_number):
    return f"segment:{segment_number}"

# Function to extract context using the summarization chain
def extract_context(segment_script):
    summary = summary_chain.run(script_segment=segment_script)
    return summary


# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 

    full_script = ""
    context = ""  # Initialize context
    for segment_number in range(1, 6):  # Loop for 5 segments
        # Update context using the previous script segment and Wikipedia research
        if segment_number > 1:  # From the second segment onwards
            context_input = {
                'script_segment': full_script,  # Use the full script generated so far
                'wikipedia_research': wiki_research
            }
            context = summary_chain.run(context_input)  # Update context

        composite_key = create_composite_key(segment_number)
        inputs = {
            'composite_key': composite_key,
            'context': context,
            'segment_number': segment_number
        }

        segment_script = script_chain.run(inputs)
        full_script += segment_script + "\n"  # Append each segment


### Display the results ###

    st.write(title) 
    st.write(full_script)  # Display the full script

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)