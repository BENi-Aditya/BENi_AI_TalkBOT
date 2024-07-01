# BENi AI Talkbot

BENi AI Talkbot is an all-rounder assistant powered by OpenAI's GPT-3.5 language model. It provides various functionalities including chat capabilities, weather updates, date/time functions, setting alarms, scheduling tasks, playing music, listening to stories, and engaging in conversational interactions like a friend.

<div align="center">
  <img src="https://raw.githubusercontent.com/BENi-Aditya/BENi_AI_TalkBOT/main/assets/git_logo.png" width="580" height="395">
</div>

</div>

## Technologies Used

- **OpenAI GPT-3.5**: Powering the conversational capabilities of the assistant.
- **Python**: Programming language used for backend development.
- **Requests**: Python library for making HTTP requests, used for fetching weather data.
- **python-dotenv**: Library for loading environment variables from a `.env` file.
- **OpenWeatherMap API**: Used to retrieve weather data.
- **YouTube Data API v3**: Enables music playback functionalities.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/BENi-AI-Talkbot.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd BENi-AI-Talkbot
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory and add your API keys:**

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key_here
    OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
    YOUTUBE_API_KEY=your_youtube_api_key_here
    ```

5. **Run the script:**

    ```bash
    python main.py
    ```

## Usage

- Start the script, and BENi will prompt you to speak or type questions.
- Ask questions related to weather, date/time, alarms, scheduling, music, stories, or engage in general conversation.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or new features to add, feel free to open an issue or create a pull request.

---

<div align="center">
  <h2>BENi AI Talkbot - Your All-Rounder Assistant</h2>
  <p>Chat, get weather updates, set alarms, schedule tasks, play music, listen to stories, and more!</p>
</div>
