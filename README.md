All the commands used in developement of the project.


-- git init
-- python -m venv env
-- source env/Scripts/activate
-- touch .gitignore
-- python.exe -m pip install --upgrade pip
-- pip install -r requirements.txt
-- pip list
-- pip install langchain_community langchain-openai : 

#
LangChain v0.1.0 and above split many integrations (including OpenAI) into separate packages, such as langchain_community and langchain_openai.
The old import path (from langchain.chat_models import ChatOpenAI) no longer works unless you have the new dependencies installed.