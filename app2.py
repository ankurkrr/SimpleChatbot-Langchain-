from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import language_tool_python
import pymongo
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load OpenAI API key from environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACKING_V2'] = 'true'

# MongoDB Connection
try:
    client = pymongo.MongoClient("mongodb+srv://ankurkrr:ankurwavey.2@aichatbot.yx0xccr.mongodb.net/?retryWrites=true&w=majority&appName=aichatbot")
    db = client["aichatbot"]
    users_collection = db["mistakes"]
except Exception as e:
    st.error("Failed to connect to the database. Please check your MongoDB connection.")
    st.stop()

# Supported Languages
LANGUAGES = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Italian': 'it', 'Portuguese': 'pt', 'Dutch': 'nl', 'Russian': 'ru',
    'Japanese': 'ja', 'Chinese': 'zh', 'Korean': 'ko', 'Arabic': 'ar',
    'Turkish': 'tr', 'Hindi': 'hi'
}

# MongoDB Helper Functions
def create_user_profile(name, native_lang, target_lang, level):
    user_data = {
        "name": name,
        "native_language": native_lang,
        "target_language": target_lang,
        "level": level,
        "mistakes": [],
        "chat_history": []
    }
    users_collection.insert_one(user_data)

def get_user_data(name):
    return users_collection.find_one({"name": name})

def update_mistakes(name, mistake):
    users_collection.update_one({"name": name}, {"$push": {"mistakes": mistake}})

# Prompt Generation
def generate_prompt(name, target_lang, level):
    base_prompt = f"""You are an experienced {target_lang} teacher. Your student {name} wants to learn {target_lang}.
    Adapt the conversation based on the student's level: {level}.
    - Beginner: Start with simple words and phrases.
    - Intermediate: Engage in structured conversations with grammar correction.
    - Advanced: Use idioms, complex sentences, and real-life scenarios.
    Provide feedback on mistakes and maintain a list of errors.
    
    Student's input: {{input}}
    Teacher's response:"""
    return base_prompt

# Mistake Detection
tool = language_tool_python.LanguageTool('en-US')  # Use the appropriate language code

def detect_mistakes(user_input):
    matches = tool.check(user_input)
    mistakes = [match.message for match in matches]
    return mistakes

# Streamlit Framework
st.title("AI Language Teacher")
name = st.text_input("Enter your name:")
native_language = st.selectbox("Select your Native Language:", list(LANGUAGES.keys()))
learning_language = st.selectbox("Select the Language you want to learn:", list(LANGUAGES.keys()))
level = st.selectbox("Select your proficiency level:", ["Beginner", "Intermediate", "Advanced"])

if st.button("Start Learning"):
    user_data = get_user_data(name)
    if not user_data:
        create_user_profile(name, native_language, learning_language, level)

    # Generate and store the prompt in session state
    st.session_state.prompt = generate_prompt(name, learning_language, level)
    
    # Start conversation
    st.session_state.chat_history = []
    st.session_state.chat_history.append(f"👩‍🏫 {learning_language} Teacher: Hello {name}, let's start learning!")

if "chat_history" in st.session_state:
    for chat in st.session_state.chat_history:
        st.write(chat)

    user_input = st.text_input("Your Response:", key="user_input")

    if st.button("Send"):
        if "prompt" not in st.session_state:
            st.error("Please click 'Start Learning' to begin the conversation.")
        else:
            with st.spinner("Generating response..."):
                # Generate the GPT response using the stored prompt and user input
                chain = ChatPromptTemplate.from_template(st.session_state.prompt) | ChatOpenAI(model="gpt-3.5-turbo") | StrOutputParser()
                response = chain.invoke({'input': user_input})['output']

                # Detect mistakes and store them
                mistakes = detect_mistakes(user_input)
                if mistakes:
                    update_mistakes(name, mistakes)

                # Update conversation
                st.session_state.chat_history.append(f"🧑‍🎓 You: {user_input}")
                st.session_state.chat_history.append(f"👩‍🏫 {learning_language} Teacher: {response}")
                
                # Convert bot response to speech (optional)
                # text_to_speech(response, LANGUAGES[learning_language])
    
    # Show mistakes
    user_data = get_user_data(name)
    if user_data and "mistakes" in user_data and user_data["mistakes"]:
        st.subheader("Mistakes & Improvements:")
        for mistake in user_data["mistakes"]:
            st.write(f"⚠️ {mistake}")