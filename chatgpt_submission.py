import os
import openai
import time
from bs4 import BeautifulSoup
import pprint
import tiktoken

openai.api_key = "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"
rewrite_path = "/Users/ericliu/Desktop/chatgpt_anonymization/rewrite/rewrite.txt"

# import required module
import os

if os.path.isfile(rewrite_path):# 如果原先有生成的文本就先删除
    os.remove(rewrite_path)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
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
        # stop=5,
        max_tokens=max_tokens_new,
        presence_penalty=0,
        frequency_penalty=0
    )
    return Chat_Completion

# assign directory
directory = '/Users/ericliu/Desktop/chatgpt_anonymization/testing-PHI-Gold-fixed'

list_of_text_contents = []
list_of_files = []

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(os.path.basename(os.path.normpath(f))[:-4])
        list_of_files.append(os.path.basename(os.path.normpath(f))[:-4])
        with open(f) as fp:
            soup = BeautifulSoup(fp, features="xml")
            text = soup.find('TEXT')
            text_content = text.contents[0]
            list_of_text_contents.append(text_content)

for i in range(len(list_of_text_contents)):
    prompt = "Please anonymize the following clinical note. Specifically, replace all the following information with the term “[redacted]”: redact any strings that might be a name or acronym or initial, redact any strings separated by the \/ symbol, redact patients' names, doctors' names and the strings in front of M.D. or after Dr., redact pager names and medical staff names, redact any strings that look like something years old or age 37, redact any dates and IDs and numbers and record dates, redact locations and addresses and clinic names, redact professions and ages and contacts, redact any acronyms and initials.: \n" + list_of_text_contents[i]  # 即输入到messages的content里的内容

    # firstpart, secondpart = prompt[:len(prompt) // 2], prompt[len(prompt) // 2:]

    num_tokens = num_tokens_from_string(prompt, "gpt2")
    print(num_tokens)

    # if 4050 - num_tokens_from_string(prompt, "gpt2") <= 2:
    #     continue

    if 4050-num_tokens <= 2:
        continue
    #
    # if 4050-num_tokens <= 2:
    #     prompt = firstpart

    completion = chatgpt_completion(prompt_new=prompt,max_tokens_new=4050-num_tokens)
    rewrite_finding = completion.choices[0].message.content

    rewrite_file = "/Users/ericliu/Desktop/chatgpt_anonymization/rewrite_no_ditch_long_inputs/" + list_of_files[i] + "_anonymized.txt"

    with open(rewrite_file, "w") as f:
        f.write(rewrite_finding)

    print("-----------第" + str(i + 1) + "个\n-----------")
    print("-----------My prompt " + "\n-----------")
    print(prompt)
    print("-----------Anonymized " + "\n-----------")
    print(rewrite_finding)

    time.sleep(10)# 国内测试10-15s的请求间隔以上可以稳定请求100次以上






