from typing import Any, Dict, Optional

from prompt_versions_manager import PromptVersionsManager
from pydantic import BaseModel, Field


class Prompt(BaseModel):
    directory: str
    prompt_name: str
    version: str
    prompt_template: Optional[str] = None
    prompt_variables: Dict[str, Any] = Field(default_factory=dict)


class PromptManager:
    @staticmethod
    def create_prompt(prompt: Prompt) -> str:
        chat_manager = PromptVersionsManager.setup(prompt.directory)

        chat_manager.version(prompt.version).set(
            prompt.prompt_name, prompt.prompt_template, overwrite=True
        )

        rendered_prompt = chat_manager.version(prompt.version).t(
            prompt.prompt_name, **prompt.prompt_variables
        )

        return rendered_prompt

    @staticmethod
    def load_prompt(prompt: Prompt) -> str:
        chat_manager = PromptVersionsManager.setup(prompt.directory)

        prompt_string = chat_manager.version(prompt.version).t(
            prompt.prompt_name, **prompt.prompt_variables
        )

        return prompt_string

    @staticmethod
    def get_or_create_prompt(prompt: Prompt) -> str:
        """
        Loads the prompt if it already exists for the given version.
        Otherwise, creates a new entry using the provided prompt_template.
        """
        try:
            return PromptManager.load_prompt(prompt)
        except (KeyError, FileNotFoundError):
            return PromptManager.create_prompt(prompt)


if __name__ == "__main__":
    prompt = Prompt(
        directory="chat",
        prompt_name="greet",
        version="v2",
        prompt_template="Hello {name}, as a {role}, please assist with the following task: {task}.",
        prompt_variables={
            "name": "Alice",
            "role": "Senior Developer",
            "task": "code review",
        },
    )
    created_prompt = PromptManager.create_prompt(prompt)
    print(created_prompt)

    loaded_prompt = PromptManager.load_prompt(prompt)
    print(loaded_prompt)

    result_prompt = PromptManager.get_or_create_prompt(prompt)
    print(result_prompt)
