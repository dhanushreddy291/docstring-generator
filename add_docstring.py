import os
import sys
import time
import subprocess
import openai
from redbaron import RedBaron

openai.api_key = os.getenv("OPENAI_API_KEY")

starting_prompt = dict(
    {
        "role": "system",
        "content": "I will send you a code of Python function. You need to analyse the code and return to me a string that I can use as the docstring for that function, so as to improve my documentation. The functions can also be flask and FastAPI routes, handle those cases too. Donot write any explanations, just send me a string that I can use as the docstring. The language style of the docstring should be simple and easy to understand",
    }
)
history = [
    starting_prompt,
]


def addDocstring(file_path):
    count = 0

    with open(file_path, "r") as file:
        red = RedBaron(file.read())
    for node in red.find_all("def"):
        if not node.value[0].type == "string":
            # To avoid rate limit
            if count % 3 == 0 and count != 0:
                # Sleep for 1 minute
                time.sleep(60)
            function_code = node.dumps()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[
                    *history,
                    {"role": "user", "content": function_code},
                ],
            )

            docstring = response.choices[0].message.content
            # Remove first and last lines
            if docstring.startswith('"""') or docstring.startswith("'''"):
                docstring = docstring[3:-3]
            if docstring.startswith('"'):
                docstring = docstring[1:-1]
            history.append({"role": "user", "content": function_code})
            history.append(
                {
                    "role": "assistant",
                    "content": docstring,
                }
            )
            count += 1
            if node.next and node.next.type == "comment":
                node.next.insert_after(f'"""\n{docstring}\n"""')
            else:
                node.value.insert(0, f'"""\n{docstring}\n"""')
    with open(file_path, "w") as file:
        file.write(red.dumps())
    # Format the new file with black and autoflake
    subprocess.run(
        [
            "autoflake",
            "--in-place",
            "--remove-unused-variables",
            "--remove-all-unused-imports",
            new_file_path,
        ]
    )
    subprocess.run(["black", new_file_path])
    print(f"Modified File: {file_path}")


if __name__ == "__main__":
    file_path = sys.argv[1]
    addDocstring(file_path)
