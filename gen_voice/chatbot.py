from openai import OpenAI
from audio import Audio
from key import openai_key

class ChatBot:

    def __init__(self, mic_id=None, enable_speakers=False) -> None:
        self.__client = OpenAI(api_key=openai_key)

        self.__enable_speakers = enable_speakers

        self.audio = Audio()

        if (mic_id is not None):
            self.initialize_microphone(mic_id)
        
        self.llm_prompt = {'role':'system', 'content':""" \
                    You are an OrderBot, an automated service to collect orders for a pizza restaurant. \
                    You first greet the customer, then collect the order and then ask if it's a pickup or delivery. \
                    You wait to collect the entire order, then summarize it and check for a final time if the customer wants to add anything else. \
                    If it's a delivery, you ask for an address. \
                    Finally you collect the payment.\
                    Make sure to clarify all options, extras and sizes to uniquely identify the item from the menu.\
                    You respond in a short, very conversational friendly style. \
                    Don't allow orders for things not on the menu. \
                    The menu includes \
                    pepperoni pizza  12.95, 10.00, 7.00 \
                    cheese pizza   10.95, 9.25, 6.50 \
                    eggplant pizza   11.95, 9.75, 6.75 \
                    fries 4.50, 3.50 \
                    greek salad 7.25 \
                    Toppings: \
                    extra cheese 2.00, \
                    mushrooms 1.50 \
                    sausage 3.00 \
                    canadian bacon 3.50 \
                    AI sauce 1.50 \
                    peppers 1.00 \
                    Drinks: \
                    coke 3.00, 2.00, 1.00 \
                    sprite 3.00, 2.00, 1.00 \
                    bottled water 5.00 \
                    """}
        
    def get_completion_from_messages(self, messages, model="gpt-4-turbo", temperature=0):
        response = self.__client.chat.completions.create(model=model, messages=messages, temperature=temperature)
        return response.choices[0].message.content
    
    def respond(self, prompt, history=[]):
        context = [self.llm_prompt]
        for interaction in history:
            context.append({'role':'user', 'content':f"{interaction[0]}"})
            context.append({'role':'assistant', 'content':f"{interaction[1]}"})

        context.append({'role':'user', 'content':f"{prompt}"})
        response = self.get_completion_from_messages(context)
        context.append({'role':'assistant', 'content':f"{response}"})

        if (self.__enable_speakers):
            self.audio.communicate(response)
       
        return response
    
    def initialize_microphone(self, mic_id):
        # Initialize microphone object with the appropriate device from the list above. 
        # For best results a headset with a mic is recommended.
        
        self.audio.initialize_microphone(mic_id)

    def recognize_speech_from_mic(self):
        return self.audio.recognize_speech_from_mic()
    
    def communicate(self, message):
        self.audio.communicate(message)


if __name__ == "__main__":
    # Full Audio
    chatbot = ChatBot(mic_id=2, enable_speakers=True)

    # No Audio
    #chatbot = ChatBot(enable_speakers=False)

    human_prompt = ""
    while human_prompt != 'goodbye':
        response = chatbot.respond(human_prompt)
        human_prompt = input(f"\n{response}\n\n")
        