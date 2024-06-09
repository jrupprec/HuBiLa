import uuid
from typing import Optional
from components.experiment.AbstractBaseExperiment import AbstractBaseExperiment
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import json
import os
import subprocess
import time


class BaseExperiment(AbstractBaseExperiment):
    id = uuid.UUID
    processes = []

    def __init__(
        self
    ):
        self.id = uuid.uuid4()
    

    def run_agent_to_agent_conversation(
        self, agents: list, max_round: int, llm_config, init_chat_message: str
    ):
        groupchat = GroupChat(agents=agents, messages=[], max_round=max_round, speaker_selection_method="round_robin", allow_repeat_speaker=False)

        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        agents[0].initiate_chat(manager, message=init_chat_message)

        return groupchat

    def run_agent_to_user_conversation(
        self, agents: list, max_round: int, message_history: list, llm_config, init_chat_message: str
    ):
        groupchat = GroupChat(
            agents=agents, messages=message_history, max_round=max_round
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        agents[0].initiate_chat(manager, message=init_chat_message)

        return groupchat

    def start_fastchat(self, model_path):
        try:
            self.processes = []
            root_dir = os.path.join(os.path.dirname(__file__), '..', '..')
            fastchat_dir = os.path.join(root_dir, "FastChat")
            venv_activate = os.path.join(root_dir, ".venv", "Scripts", "activate")

            commands = [
                f"{venv_activate} && python -m fastchat.serve.controller",
                f"{venv_activate} && python -m fastchat.serve.model_worker --model-path {model_path}",
                f"{venv_activate} && python -m fastchat.serve.openai_api_server --host localhost --port 8000"
            ]

            for index, command in enumerate(commands):
                set_title = f"title {index}"
                full_command = f"{set_title} && cd {fastchat_dir} && {command}"
                process = subprocess.Popen(["start", "cmd", "/k", full_command], shell=True)
                self.processes.append(process)
        except Exception as e:
            print(e)

            
    def stop_fastchat(self):
        try:
            for index, process in enumerate(self.processes):
                title_pattern = f"{index}*"
                subprocess.run(f"taskkill /FI \"WINDOWTITLE eq {title_pattern}\" /IM cmd.exe", shell=True)
                time.sleep(5)
                print(f"Process {process} stopped.")
        except Exception as e:
            print(e)


    def save_conversation(self, groupchat: GroupChat, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder '{path}' created.")
            
        file_path = os.path.join(path, "conversation.json")
        
        with open(file_path, "w") as file:
            json.dump(groupchat.messages, file)
            
        print("Saved conversation successfully.")
        
    def save_log_history(content, id, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Folder '{path}' created.")
            
        with open(f"single-factor-experiments/logs/conversation-log-{id}.json", "w") as file:
            json.dump(content, file)
