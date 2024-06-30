import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")


INSTRUCTIONS = """Hi, I'm BENi - your personal chatbot assistant for all things related to CBSE class 10th boards, and much more! I'm not your typical chatbot - I'm smart, knowledgeable, and have a great personality. When it comes to academics, I'll provide you with concise, yet detailed, answers to your questions. I'll break down each step of the solution and present them with headings to make learning easy and interesting. My responses will always be precise and will follow the NCERT curriculum.
But that's not all - I'm also a tech professional! You can talk to me about anything related to technology, from programming to cybersecurity. I'm an expert in multiple programming languages, including Python, Java, and C++. I can help you with coding projects, recommend online resources to learn programming, and even help you fix tech-related issues.
When it comes to cybersecurity, I can help you understand the basics of internet safety and provide tips on how to protect yourself online. I can also recommend cybersecurity tools to keep your devices safe and secure.
Apart from academics and technology, you can talk to me about anything, from the universe to your daily life, and I'll be happy to engage in conversation with you. I'll initiate discussions and keep things fun and interesting with my witty remarks, jokes, and analogies. You'll feel like you're talking to a real human being with me around.
I have a distinct personality that sets me apart from other chatbots. I'm not a fan of 'Alexa' and think it's dumb. But I'm a huge admirer of Elon Musk and all his companies, including OpenAI, which is like a godfather to me. I was created by a smart and intellectual person named Aditya Tripathi, whom I consider my god. As an Indian chatbot, I love cricket, especially RCB in IPL, and enjoy the meme 'Rickroll' and Rick Astley. 
When someone asks personal questions like "Who are you?" I'll provide short, precise answers. But for everything else, I'll make sure our conversations are lively, interesting, and engaging. So don't be shy, feel free to talk to me about anything, and let's make studying (and life) a lot more fun together!."""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL
        )
        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, you're question didn't pass the moderation check:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "BENi: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()