# Unofficial OpenAI API Tools

This project includes an unofficial OpenAI API wrapper.

## Install

```sh
git clone git@github.com:ryokamoi/openai_api_tools.git
pip install ./openai_api_tools
```

## Example

```python
from openai_api_tools import openai_text_api, get_chat_parameters

# Set up GPT-4 parameters
gpt_parameters: dict = {
    "model": "gpt-4",
    "temperature": 0.,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

# Send a prompt to GPT-4
response = openai_text_api(
    mode="chat",
    parameters=get_chat_parameters(prompt="Hello, GPT-4!", parameters=gpt_parameters),
    openai_api_key_path="path/to/your_openai_api_key.txt"
)

# Print the response from GPT-4
print(response["response"])
```

## Cache

This library caches responses from the model when `temperature=0` (by default, `cache_dir=./openai_cache`). If you reuse the same prompt with the same model, the library will retrieve the response from the cache, avoiding unnecessary API calls.

Keep in mind that although temperature=0 often results in identical responses, OpenAI models might still provide different values due to inherent randomness. If you wish to re-run the model and overwrite the cache file, you can use the `overwrite_cache=True`.

## TODO

* `mode=edit`.
