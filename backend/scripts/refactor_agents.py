import os
import glob
import re

files = glob.glob('/home/labuser/VSCODE_training/renewai-demo/backend/agents/*.py')
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Replace import
    content = re.sub(
        r'^from\s+prompts\.all_prompts\s+import\s+.*$',
        'import prompts.all_prompts as ap',
        content,
        flags=re.MULTILINE
    )
    
    # Replace variable usage (e.g. PLANNER_SYSTEM_PROMPT into ap.PLANNER_SYSTEM_PROMPT)
    prompt_names = [
        "PLANNER_SYSTEM_PROMPT", "PLANNER_USER_TEMPLATE",
        "CRITIQUE_SYSTEM_PROMPT", "CRITIQUE_USER_TEMPLATE",
        "EMAIL_AGENT_SYSTEM_PROMPT", "EMAIL_AGENT_USER_TEMPLATE",
        "WHATSAPP_AGENT_SYSTEM_PROMPT", "WHATSAPP_AGENT_USER_TEMPLATE",
        "VOICE_AGENT_SYSTEM_PROMPT", "VOICE_AGENT_USER_TEMPLATE",
        "HUMAN_QUEUE_MANAGER_SYSTEM_PROMPT", "HUMAN_QUEUE_USER_TEMPLATE",
        "ORCHESTRATOR_SYSTEM_PROMPT", "ORCHESTRATOR_USER_TEMPLATE"
    ]
    
    for p in prompt_names:
        content = re.sub(r'(?<!ap\.)\b' + p + r'\b', f'ap.{p}', content)
        
    with open(f, 'w') as file:
        file.write(content)
        
print("Successfully refactored all agent files to use dynamic prompts.")
