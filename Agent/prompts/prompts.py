import os

# Get the directory where this file is located
module_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(module_dir, 'college_assistant.md'), 'r', encoding='utf-8') as f:
    college_assistant_system_prompt = f.read()