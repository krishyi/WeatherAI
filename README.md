# WeatherAI
1. Ollama is required for this project to work. It can be installed here: https://ollama.com/download/windows
2. To run this project, enter "ollama pull mistral" in terminal, followed by "ollama serve"
3. If you cannot type ollama serve, enter task manager, and close all instances of ollama, before retyping ollama serve in terminal. In order to gain access to all NOAA data, this command is crucial.
4. Next, enter python ai_helper.py in terminal. 
5. The responses may take some time, upwards of 1-3 minutes. To reduce this time, it is recommended to close background programs/tasks to minimize memory usage. 
6. If the AI is not able to gather data for a certain date, try the format YYYY-DD-MM (ex. May 15 2023 -> 2023-05-15)
7. In case data after 2021 is not available, close terminal, reopen, and redo steps 2-4. This should fix the issue.
8. If you have any questions about my code, please feel free to contact me at kkapoor1@umbc.edu
