# Week 9 – Chatbot Development using Ollama

## Project title
Building an Interactive AI Chatbot using Ollama

## Domain
Education

## Objective
- Build a command-line chatbot using Python and a local Ollama LLM.
- Keep conversation history so answers can use earlier messages.
- Save each conversation with a timestamp in CSV and text log files.
- Prepare a simple foundation for LangChain integration in Week 10.

## Requirements
- Python 3.10 or newer
- Ollama installed and running
- `llama3.2` model downloaded

## Setup
1. Install Ollama from https://ollama.com/
2. Open a terminal and run: `ollama pull llama3.2`
3. Start/check the model: `ollama run llama3.2`
4. In another terminal, go to this project folder.
5. Install Python dependency: `pip install -r requirements.txt`
6. Run the chatbot: `python chatbot.py`
7. Type a question. Type `exit` to finish.

## Files
- `chatbot.py`: main chatbot program
- `dataset/sample_questions.csv`: 22 sample questions across factual, reasoning, coding and general conversation
- `dataset/chat_history.csv`: timestamped user/assistant conversation history
- `dataset/responses.csv`: response records for evaluation
- `dataset/chatbot_logs.txt`: readable event log
- `notebook/Week9_Chatbot_Development.ipynb`: notebook for setup, execution and observations

## How context works
The program stores user and assistant messages in a `messages` list and sends the conversation to Ollama each turn. This helps the model answer follow-up questions. The current conversation is kept in memory while the script is running; CSV files store a record for later review.

## Evaluation and limitations
Strengths:
- Runs with a local model after the model is downloaded.
- Supports follow-up questions within the current session.
- Saves timestamped conversation records.
- Can answer factual, reasoning, coding and general questions.

Limitations:
- Responses may be incorrect, incomplete or outdated.
- The model may be slow on computers with limited memory.
- Conversation context resets when the program is restarted.
- CSV logs may contain personal text; do not enter passwords or sensitive information.
- Review coding answers before using them.

## Observation template
After testing, record:
1. Question asked
2. Whether the response was correct
3. Whether it was complete and easy to understand
4. Any prompt improvement needed

## Future enhancement
In Week 10, the message handling can be adapted to a LangChain chat model and prompt template.
