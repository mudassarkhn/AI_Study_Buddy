from datetime import datetime, timedelta
from State.AI_Study_buddy_state import StudyBuddyState
from LLM.model import llm
import re
import json

def generate_study_plan(state: StudyBuddyState) -> StudyBuddyState:
    """Step 4: AI creates personalized study schedule"""
    print("📅 Generating study plan...")

    # ---- Fix exam_date parsing ----
    exam_date_raw = state["exam_date"]

    if isinstance(exam_date_raw, datetime):
        exam_date = exam_date_raw
    elif isinstance(exam_date_raw, str):
        exam_date = datetime.strptime(exam_date_raw, "%Y-%m-%d")
    else:
        raise ValueError("exam_date must be a string (YYYY-MM-DD) or datetime")

    today = datetime.now()

    days_available = (exam_date.date() - today.date()).days
    if days_available <= 0:
        days_available = 1  # prevent crash

    # ---- Prepare topics text ----
    topics_text = ""
    for topic in state["topics"]:
        topics_text += f"{topic['id']}. {topic['title']}.\n"

    # ---- Prompt ----
    prompt = f"""
Create a study schedule for these topics:

{topics_text}

Study Details:
- Days until exam: {days_available}
- Study time per day: {state['study_time_per_day']} minutes
- Exam date: {exam_date.strftime('%Y-%m-%d')}

Return ONLY a JSON array like:
[
  {{"date": "2025-01-15", "topic_id": 1, "topic_title": "topic_name","content":"content of the topic from text",completed": false}},
  {{"date": "2025-01-16", "topic_id": 2, "topic_title": "topic_name","content":"content of the topic from text",completed": false}}
]

Rules:
- Start from tomorrow
- Use valid JSON only
"""

    # ---- Call LLM ----
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)

    # ---- Parse JSON safely ----
    try:
        match = re.search(r"\[.*\]", content, re.DOTALL)
        study_plan = json.loads(match.group() if match else content)
    except Exception:
        # ---- Fallback plan (NO bugs now) ----
        study_plan = []
        for i, topic in enumerate(state["topics"]):
            day_number = i % days_available
            study_date = (today + timedelta(days=day_number + 1)).strftime("%Y-%m-%d")
            study_plan.append({
                "date": study_date,
                "topic_id": topic["id"],
                "topic_title": topic["title"],
                "completed": False
            })

    # ---- Save to state ----
    state["study_plan"] = study_plan
    state["messages"].append(f"✅ Created {len(study_plan)} -day study plan")
    state["print"] = study_plan

    return state

