from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langchain_ollama.chat_models import ChatOllama
from states.graph_state import ShellState
from agent_factory import agent_factory
import asyncio

class ShellAgent(): 

    def expert(self, state: ShellState): 
        prompt = f"""
### Linux  Command Advisor 
        You are my linux command advisor your 
        responsible for recommending commands for me  
        based on the user prompt, at most one of the commands
        you recommend should solve what the usre wants. 

        user prompt is : {state['messages'][-1]}
        your response should be in markdown
        you should format your response as follows 
        and nothing more or nothing less: 

### the recommendation given to you is: 
        1. `command1`
        2. `command2`
        3. `command3`
        """

        llm = ChatOllama(model="unsloth",temperature=0)
        response = llm.invoke(prompt)
        return {'messages': response, 'prompt': state['messages'][-1].content}

    def runner(self, state: ShellState): 
        prompt = f"""
### Linux Shell Agent
        Your a linux shell Agent you execute 
        linux commands on the shell based on 
        what users prompt and the recommendations
        your supplied with. 

        the user prompt is : {state['prompt']}
        {state['messages'][-1].content}
        """

        pilot = agent_factory("Shell",{"configurable": {"thread_id": 1}})
        result = asyncio.run(pilot.Run(prompt))
        return {'messages': AIMessage(result)}
