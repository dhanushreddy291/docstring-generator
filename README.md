# Docstring Generator GitHub Action

![Github Actions Workflow](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/byirq6owyvmgr5eypz3o.png)

This is a GitHub Action that automatically generates docstrings for Python functions using OpenAI's GPT-3 API.

## Usage

To use this GitHub Action in your own repository, follow these steps:

1.  Set up an OpenAI API key by signing up for their [beta program](https://beta.openai.com/signup/). Once you have an API key, create a new secret called `OPENAI_API_KEY` in your repository's settings and set the value to your API key.
    
2.  Create a new workflow file (e.g. `.github/workflows/add_docstring.yml`) in your repository with the following contents:

```yaml
# Define the name of the Github Action workflow and the event that triggers it
name: Run add_docstring
on:
  push:
    branches:
      - "main"

# Define the jobs that will run as part of this Github Action
jobs:
  build:
    # Specify the environment where the jobs will run
    runs-on: ubuntu-latest
    # Set the permissions of the job (in this case, the job will write to the repository, so needs write permissions)
    permissions:
      contents: write
    # Define the steps that will be executed as part of this job
    steps:
      # Step 1: Check out the code repository
      - name: Check out repository
        uses: actions/checkout@v3

      # Step 2: Set up Python and install dependencies
      - name: Set up Python and install dependencies
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          cache: "pip"
      - run: pip install -r .github/requirements.txt

      # Step 3: Run the add_docstring script
      - name: Run add_docstring script
        run: bash .github/run_add_docstring.sh .github/add_docstring.py
        env:
          # Pass the OpenAI API key as an environment variable
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      # Step 4: Check if any changes were made
      - name: Check for changes
        id: changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "::set-output name=has_changes::true"
          fi
          
      # Step 5: Commit and push changes to the code repository if any changes were made
      - name: Commit and push changes
        if: steps.changes.outputs.has_changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Add docstrings to .py files"
          git push origin HEAD:${{ github.ref }}
```

3.  Create a `run_add_docstring.sh` file in the `.github` directory of your repository with the following contents:

```bash
#!/bin/bash
add_docstring_script=$1
for file in $(find . -name "add_docstring.py" -prune -o -name "*.py" -print)
do
    python $add_docstring_script $file
done
```

4.  Add the `add_docstring.py` script to your repository's `.github` directory.

```python
# Import necessary libraries
import os
import sys
import time
import subprocess
import openai
from redbaron import RedBaron

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set starting prompt and history for OpenAI chatbot
# Modify it according to your use case (this is just an example)
starting_prompt = dict(
    {
        "role": "system",
        "content": "I will send you a code of Python function. You need to analyse the code and return to me a string that I can use as the docstring for that function, so as to improve my documentation. The functions can also be routes of a Web App, handle those cases too. Donot write any explanations, just send me a string that I can use as the docstring. The language style of the docstring should be simple and easy to understand and it should be in Google Style Multi-Line format",
    }
)
history = [
    starting_prompt,
]


# Define function to add docstring to Python functions
def addDocstring(filePath):
    """
    Adds docstring to Python functions using OpenAI API

    Args:
        filePath (str): Path to the Python file

    Returns:
        None
    """
    currentTime = time.time()

    # Open the Python file using RedBaron library
    with open(filePath, "r", encoding="utf-8") as file:
        code = RedBaron(file.read())

    # Loop through all functions in the Python file
    for node in code.find_all("def"):
        # Check if function already has a docstring
        if not node.value[0].type == "string":
            # To avoid OpenAI rate limit (only free trial accounts have rate limit, comment the code below if you have a paid account)
            # Free trial accounts have a hard cap of 1 request every 20 seconds
            if time.time() - currentTime < 20:
                # Sleep for remaining time
                time.sleep(20 - (time.time() - currentTime) + 1)

            # Extract the function code
            function_code = node.dumps()

            # Send the function code to ChatGPT API for generating docstring (offcourse use GPT4 API if you hace access to it)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=[
                    *history,
                    {"role": "user", "content": function_code},
                ],
            )

            currentTime = time.time()

            # Extract the generated docstring from the OpenAI response
            docstring = response.choices[0].message.content

            # Remove the quotes from the generated docstring if present
            if docstring.startswith('"""') or docstring.startswith("'''"):
                docstring = docstring[3:-3]
            if docstring.startswith('"'):
                docstring = docstring[1:-1]

            # Add the function code and generated docstring to history
            history.append({"role": "user", "content": function_code})
            history.append(
                {
                    "role": "assistant",
                    "content": docstring,
                }
            )

            # Insert the generated docstring to the Function node
            if node.next and node.next.type == "comment":
                node.next.insert_after(f'"""\n{docstring}\n"""')
            else:
                node.value.insert(0, f'"""\n{docstring}\n"""')

    # Write the modified Python file back to disk
    with open(filePath, "w", encoding="utf-8") as file:
        file.write(code.dumps())

    # Format the new file with autoflake and black
    subprocess.run(
        [
            "autoflake",
            "--in-place",
            "--remove-unused-variables",
            "--remove-all-unused-imports",
            filePath,
        ]
    )
    subprocess.run(["black", filePath])


# Run the function if this script is called directly
if __name__ == "__main__":
    filePath = sys.argv[1]
    addDocstring(filePath)
```
    
5.  Create a `requirements.txt` file in the `.github` directory of your repository with the following contents:

```text
openai
redbaron
autoflake
black
```

6.  Commit and push these changes to your repository's `main` branch.

When you push changes to your repository's `main` branch, this GitHub Action will run and automatically add docstrings to any Python functions in your repository that don't already have them.

# Demo

![An Image showing the demo of Github Action](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/iujaq0r56xvq9mw7emee.png)

## Rate Limiting

OpenAI's GPT-3 API has a rate limit of 1 requests every 20 seconds on free trial. To avoid hitting this rate limit, the GitHub Action includes a `time.sleep(20)` statement after every API call. If you are on a paid account, you can comment it.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.