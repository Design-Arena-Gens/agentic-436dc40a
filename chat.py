import requests
import pyttsx3

# Configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "tinyllama"  # or "tinyllama:latest"

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1.0)  # Max volume

def speak(text):
    """Speak the given text using TTS"""
    engine.say(text)
    engine.runAndWait()

def chat_with_ollama():
    """Main chat loop"""
    print("🧠✨ Welcome to the TinyLLaMA Chat! Type 'exit' to quit.\n")

    messages = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye, brave explorer!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "messages": messages,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            reply = data.get("message", {}).get("content", "")

            print(f"TinyLLaMA: {reply}")
            speak(reply)  # 🔊 Speak the response aloud

            messages.append({"role": "assistant", "content": reply})

        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
        except requests.exceptions.Timeout:
            print("⏱️ Error: Request timed out. The model might be taking too long to respond.")
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error communicating with Ollama: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    chat_with_ollama()
