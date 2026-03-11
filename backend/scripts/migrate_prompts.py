import os
import sys

# Add the parent directory to sys.path so we can import from the backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sqlite_manager import db
import prompts.all_prompts as ap

def main():
    prompts_to_migrate = [
        "PLANNER_SYSTEM_PROMPT", "PLANNER_USER_TEMPLATE",
        "CRITIQUE_SYSTEM_PROMPT", "CRITIQUE_USER_TEMPLATE",
        "EMAIL_AGENT_SYSTEM_PROMPT", "EMAIL_AGENT_USER_TEMPLATE",
        "WHATSAPP_AGENT_SYSTEM_PROMPT", "WHATSAPP_AGENT_USER_TEMPLATE",
        "VOICE_AGENT_SYSTEM_PROMPT", "VOICE_AGENT_USER_TEMPLATE",
        "HUMAN_QUEUE_MANAGER_SYSTEM_PROMPT", "HUMAN_QUEUE_USER_TEMPLATE",
        "ORCHESTRATOR_SYSTEM_PROMPT", "ORCHESTRATOR_USER_TEMPLATE"
    ]
    
    migrated_count = 0
    for p_name in prompts_to_migrate:
        content = getattr(ap, p_name, None)
        if content:
            # Check if it already exists to avoid overwriting edits
            existing = db.get_prompt(p_name)
            if not existing:
                db.update_prompt(p_name, content)
                print(f"Migrated: {p_name}")
                migrated_count += 1
            else:
                print(f"Skipped (already exists): {p_name}")
                
    print(f"Successfully migrated {migrated_count} prompts to SQLite.")

if __name__ == "__main__":
    main()
