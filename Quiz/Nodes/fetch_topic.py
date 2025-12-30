from app.DB.data_base import get_database
from Quiz.quizstate import QuizState

# ============ NODE 1: FETCH TOPIC ============
# ============ NODE 1: FETCH TOPIC ============
def fetch_topic(state: QuizState) -> QuizState:

    print(f"\n📚 [NODE 1] Fetching topic for {state['study_date']}...")
    
    # Connect to database
    db = get_database()
    
    # Get user's study plan
    study_plan = db.study_plans.find_one({"user_email": state['user_email']})
    
    if not study_plan:
        state['messages'].append("❌ No study plan found")
        return state
    
    # Find topic for this date
    topic_for_today = None
    for task in study_plan['plan']:
        if task['date'] == state['study_date']:
            topic_for_today = task
            break
    
    if not topic_for_today:
        state['messages'].append(f"❌ No topic for {state['study_date']}")
        return state
    
    # Mark as completed
    for task in study_plan['plan']:
        if task['date'] == state['study_date']:
            task['completed'] = True
    
    db.study_plans.update_one(
        {"user_email": state['user_email']},
        {"$set": {"plan": study_plan['plan']}}
    )
    
    # Get full topic details
    topics = db.topics.find_one({"user_email": state['user_email']})
    
    if topics:
        for topic in topics['topics']:
            if topic['id'] == topic_for_today['topic_id']:
                # Save to state
                state['topic_id'] = topic['id']
                state['topic_title'] = topic['title']
                # state['topic_content'] = topic.get('content', topic.get('summary', ''))
                state['messages'].append(f"✅ Found topic: {topic['title']}")
                state['messages'].append("✅ Marked as completed")
                break
    
    return state

