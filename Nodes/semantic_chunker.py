from State.AI_Study_buddy_state import StudyBuddyState
import re
import json
from LLM.model import llm
def semantic_chunker(state: StudyBuddyState) -> StudyBuddyState:
    text=state["extracted_text"][:8000]
    semantic_prompt = f"""Read this study material {text} and split the whole text semantic study topics.

    RULES:
    - No of topics specify by the user:{state['topics_no']}
    - Titles must come from the text itself
    - Do NOT rewrite content
    - Do NOT include explanations
    - Do NOT include content

    OUTPUT FORMAT (JSON ONLY):
    [
    {{ "id": 1, "title": "Topic or chapter name from the text", "content": "exact content of the title from text" }},
    {{ "id": 2, "title": "Topic or chapter name from the text","content": "exact content of the title from text" }}
    ]
    """

    response = llm.invoke(semantic_prompt)

    try:
        content = response.content
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        topics = json.loads(json_match.group())
    except Exception as e:
        raise ValueError(f"LLM failed to return valid topic titles: {e}")

    # Deterministic content splitting
    words = state["extracted_text"].split()
    chunk_size = len(words) // len(topics)

    for i, topic in enumerate(topics):
        start = i * chunk_size
        end = start + chunk_size if i < len(topics) - 1 else len(words)
        topic["content"] = " ".join(words[start:end])

    state["topics"] = topics
    state["messages"].append(f"✅ Created {len(topics)} topics")
    state["print"] = json.dumps(topics, indent=2)

    return state
