# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import asyncio
import time
import threading
from config import DefaultConfig
import os
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_community.agent_toolkits import GmailToolkit
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

from datetime import datetime
from custom_functions.rag_functions import retriever_tool



CONFIG = DefaultConfig()


class MyBot(ActivityHandler):

    def __init__(self, adapter):
        self.adapter = adapter
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)
        prompt = turn_context.activity.text
        

        # await turn_context.send_activity(f"Processing .... {text}")
        asyncio.create_task(self.continue_conversation_task(conversation_reference, prompt))


    async def continue_conversation_task(self, conversation_reference, prompt):
    # This method uses the adapter to continue the conversation.
        await self.adapter.continue_conversation(
            conversation_reference,
            lambda turn_context: self._send_follow_up_message(turn_context, prompt),  # Pass the text to the follow-up method using a lambda function
            CONFIG.APP_ID
        )

    async def _send_follow_up_message(self, turn_context: TurnContext, prompt):
    # This method sends a follow-up message after some delay or processing.
          # Example delay to simulate async processing.
        answer = handleTask(prompt)
        print(answer)
        print("sending prompt back")
        await turn_context.send_activity(str(answer))


    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext,

    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")


global_prompt = hub.pull("hwchase17/openai-tools-agent")

def handleTask(taskMessage):
    model = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)


    search_tool = DuckDuckGoSearchRun()
    tools = []
    tools.append(search_tool)
    tools.append(retriever_tool)

    prompt = global_prompt
    for index, message in enumerate(prompt.messages):
        if isinstance(message, SystemMessagePromptTemplate):
            # Modify the template of the SystemMessagePromptTemplate
            # This step depends on the actual structure and attributes of SystemMessagePromptTemplate
            # Assuming it has a `prompt` attribute which in turn has a `template` attribute
            new_template = 'You are a helpful assistant called Donna. DO NOT return Code blocks in the generated output.'
            prompt.messages[index].prompt.template = new_template
            break 
    agent = create_openai_tools_agent(model, tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    answer = agent_executor.invoke(
    {
        "input": taskMessage
    }
)
    print("#######################################################################")
    return answer["output"]