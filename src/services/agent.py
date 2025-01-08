from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 

class OpenAIAgent:
    
    def __init__(self):
        self.client = self.setup()
        self.interactive_mode()

    def setup(self)-> OpenAI:
        try:
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("oAI Agent Setup Complete")
        except Exception as e:
            logger.error(f"Error while setting up: {e}")
            raise
        return client

    def chat(self, input = str):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": input,
                    }
                ],
                model="gpt-4o",
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error("Error: {e}")
            raise

    def interactive_mode(self):
        """
        Enter an Interactive mode where the user can provide prompts via the terminal
        """
        logger.info("Interactive mode started. Type '.exit' to quit \n")
        while True:
            user_input = input("> ").strip()
            if user_input.lower() == ".exit":
                print("Exiting Interactive Mode. Goodbye!")
                break
            response = self.chat(user_input)
            print(f"AI: {response}")

        
if __name__ == "__main__":
    agent = OpenAIAgent()