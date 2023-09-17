from typing import Union, Optional, Literal
import os
import time
from pathlib import Path
import json
import hashlib

import openai


ParamsType = dict[str, Union[str, float]]


def text2hash(string: str) -> str:
    hash_object = hashlib.sha512(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()

    return hex_dig


def get_cache_path(cache_dir: Path, parameters: dict) -> Path:
    return cache_dir / f"{text2hash(str(sorted(parameters.items())))}.json"


def _read_cached_output(cache_path: Path) -> dict:
    if cache_path.exists():
        print(f"read cache from {cache_path}")
        with open(cache_path, "r") as f:
            output_dict = json.load(f)
        return output_dict
    
    return {}


def load_cache(cache_dir: Path, parameters: dict) -> dict:
    cache_path = get_cache_path(cache_dir, parameters)
    
    cached_output = {}
    if parameters["temperature"] < 0.000001:  # if temperature == 0
        cached_output = _read_cached_output(cache_path)
    
    return cached_output


def dump_cached_output(output_dict: dict, cache_dir: Path, parameters: dict):
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = get_cache_path(cache_dir, parameters)
    if parameters["temperature"] < 0.00001:  # == 0
        with open(cache_path, "w") as f:
            json.dump(output_dict, f, indent=4)


def get_chat_parameters(prompt: str, parameters: ParamsType) -> ParamsType:
    return dict(messages=[{"role": "user", "content": prompt}], **parameters)


def get_edit_parameters(input_sentence: str, instruction: str, parameters: ParamsType):
    return dict(input=input_sentence, instruction=instruction, **parameters)


def openai_text_api(mode: Literal["complete", "chat", "edit"], parameters: ParamsType,
                    openai_api_key_path: Optional[Path]=Path("../openai_api_key.txt"),
                    sleep_time: int=1,
                    cache_dir: Optional[Path]=Path("./openai_cache"), overwrite_cache: bool=False,
                    organization: str = None):
    """OpenAI API wrapper for text completion, chat, and edit."""

    # load cache
    if not overwrite_cache and cache_dir is not None:
        cached_output = load_cache(cache_dir, parameters)
        if len(cached_output) > 0:
            return cached_output
    
    if organization is not None:
        openai.organization = organization
    
    if openai_api_key_path is None or not openai_api_key_path.exists():
        raise ValueError(f"{openai_api_key_path} does not exist.")
    
    with open(openai_api_key_path, "r") as f:
        api_key = f.read().strip()
    openai.api_key = api_key
    
    # prompt
    if mode == "chat":
        prompt = parameters["messages"][-1]["content"]
    elif mode == "complete":
        prompt = parameters["prompt"]
    else:
        raise NotImplementedError()
    
    # openai api
    for try_count in range(10):
        try:
            if mode == "chat":
                response = openai.ChatCompletion.create(**parameters)
            elif mode == "complete":
                response = openai.Completion.create(**parameters)
            elif mode == "edit":
                raise NotImplementedError()
            else:
                raise ValueError(f"{mode} is not a valid value for the mode parameter. Please choose from 'chat', 'complete', or 'edit'.")
        except Exception as e:
            print("Exception occurred in OpenAI API:\n")
            print(str(e))
            if "This model's maximum context length is" in str(e):
                response = None
                break
            
            if try_count == 9:
                raise Exception("OpenAI API failed for 10 times for this example. Please try again later.")
            
            sleep_seconds = 5
            print(f"\nRetrying after {sleep_seconds} seconds...")
            time.sleep(sleep_seconds)
            
            continue
        break
        
    # output dict
    output_dict = {
        "prompt": prompt, "response": response,
    }
    
    # dump cache
    if cache_dir is not None:
        dump_cached_output(output_dict, cache_dir, parameters)
    
    # avoid too many access
    time.sleep(sleep_time)    
    return output_dict
