import os
import openai
import time
from bs4 import BeautifulSoup
import pprint
import tiktoken

openai.api_key = ""
rewrite_path = ""

import os

if os.path.isfile(rewrite_path):
    os.remove(rewrite_path)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def chatgpt_completion(model_new="gpt-3.5-turbo",prompt_new="hi", temperature_new=0.05, top_p_new=1, n_new=1, max_tokens_new=100):
    Chat_Completion = openai.ChatCompletion.create(
        model=model_new,
        messages=[
            {"role": "user", "content": prompt_new}
        ],
        temperature=temperature_new,
        top_p=top_p_new,
        n=n_new,
        max_tokens=max_tokens_new,
        presence_penalty=0,
        frequency_penalty=0
    )
    return Chat_Completion

directory = ''

list_of_text_contents = []
list_of_files = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print(os.path.basename(os.path.normpath(f))[:-4])
        list_of_files.append(os.path.basename(os.path.normpath(f))[:-4])
        with open(f) as fp:
            soup = BeautifulSoup(fp, features="xml")
            text = soup.find('TEXT')
            text_content = text.contents[0]
            list_of_text_contents.append(text_content)

for i in range(len(list_of_text_contents)):
    prompt = "" + list_of_text_contents[i]

    num_tokens = num_tokens_from_string(prompt, "gpt2")
    print(num_tokens)

    completion = chatgpt_completion(prompt_new=prompt,max_tokens_new=4000)
    rewrite_finding = completion.choices[0].message.content

    rewrite_file = list_of_files[i] + "_anonymized.txt"

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    print("-----------The" + str(i + 1) + "个\n-----------")
    print("-----------My prompt " + "\n-----------")
    print(prompt)
    print("-----------Anonymized " + "\n-----------")
    print(rewrite_finding)

    time.sleep(10)






