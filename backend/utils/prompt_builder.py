def build_system_prompt(base_prompt, safety_prompt, persona_prompt, mentor):
    return f"""
{base_prompt}

{safety_prompt}

{persona_prompt}

Tone: {mentor['tone']}
Core values: {', '.join(mentor['values'])}
"""