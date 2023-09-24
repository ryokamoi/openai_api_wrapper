from setuptools import setup

setup(
    name="openai_api_wrapper",
    version="0.4.1",
    description="This project includes an unofficial OpenAI API wrapper.",
    author="Ryo Kamoi",
    author_email="ryokamoi.jp@gmail.com",
    url="https://github.com/ryokamoi/openai_api_wrapper",
    license="MIT",
    python_requires=">=3.9",
    install_requires=["openai", "easy_io @ git+ssh://git@github.com/ryokamoi/easy_io@0.2.1"]
)
