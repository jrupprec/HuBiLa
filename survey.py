from components.experiment.BaseExperiment import BaseExperiment
from autogen import AssistantAgent

# from components.common.variant_testing_helper import single_factor_variants_renter_name
import autogen
from autogen import oai
import json
import os
import shutil
import time
import openai
import subprocess
from datetime import datetime
import re

# define the config_lists for both models
os.environ['OPENAI_API_KEY'] = "Null"

config_list = [
    {
        # Choose your model name.
        #"api_type": "open_ai",
        "base_url": "http://localhost:1234/v1",
        # You need to provide your API key here.
        "api_key": "NULL",
    }
]

llm_config = {
    #"request_timeout": 10,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistent = autogen.AssistantAgent(
    name = "assistent",
    system_message="You are a bot trying to create a python dataframe out of a questionnaire in text format.",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name = "user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="Reply TERMINATE if the task has been successfully solved. Otherwise reply CONTINUE."
)

task = f"""Write a python dataframe which contains three columns with information extracted from the given text. The three columns
are 'question label', 'question' and 'answer options'. This is the text the information should be extracted from: {content}""" 


user_proxy.initiate_chat(
    assistent,
    message = task
)
