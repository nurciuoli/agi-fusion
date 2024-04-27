import ollama as o
import base64
#chat func
def chat(user_msg,stream=True):
    messages = [
    {
        'role': 'user',
        'content': user_msg,
    },
    ]

    for part in o.chat('llama3', messages=messages, stream=stream):
        print(part['message']['content'], end='', flush=True)

    # end with a newline
    print()

#generate func
def generate(prompt,stream=True):
    for part in o.generate('llama3', prompt, stream=stream):
        print(part['response'], end='', flush=True)

#generate with image func
def generate_w_images(prompt,images,stream=True):
    for response in o.generate('llava', prompt, images=images, stream=stream):
        print(response['response'], end='', flush=True)
    print()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# agent class framework
class LlamaAgent:
    def __init__(self,system_prompt = 'You are a helpful chat based assistant'):
        self.system_prompt = system_prompt
        self.messages=[
    {
        'role': 'system',
        'content': system_prompt,
    },
    ]
    #chat with agent and continue conversation
    def chat(self,user_msg,stream=True):
        self.messages.append(
        {
            'role': 'user',
            'content': user_msg,
        })
        print('===============================================================')
        print('                             USER')
        print('===============================================================')
        print(user_msg)
        msg_temp=''
        print('===============================================================')
        print('                          ASSISTANT')
        print('===============================================================')
        for part in o.chat('llama3', messages=self.messages, stream=stream):
            print(part['message']['content'], end='', flush=True)
            msg_temp+=part['message']['content']

        # end with a newline
        print()

        self.messages.append(
            {
            'role': 'assistant',
            'content': msg_temp,
        })
