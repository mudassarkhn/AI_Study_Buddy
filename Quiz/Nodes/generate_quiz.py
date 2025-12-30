import json, re
from datetime import datetime
from app.DB.data_base import get_database
from app.LLM.model import llm
from Quiz.quizstate import QuizState
# ============ NODE 2: GENERATE QUIZ ============
# ============ NODE 2: GENERATE QUIZ ============
def generate_quiz(state: QuizState) -> QuizState:
    """
    Node 2: Use AI to create quiz questions
    """
    print(f"\n❓ [NODE 2] Generating quiz questions...")
    
    # Check if we have topic
    if not state.get('topic_title'):
        state['messages'].append("❌ No topic found to create quiz")
        return state
    
    # Initialize AI
    
    # Create prompt
    prompt = f"""
    Create a simple 10 multiple choice quiz questions about this topic:
    
    Topic: {state['topic_title']}
    
    Return ONLY a JSON array like this:
    [
        {{
            "question": "What does ICT stand for?",
            "options": ["A) Information and Communication Technology", "B) Internet Computer Tech", "C) International Coding Team", "D) Data Processing"],
            "correct": "A"
        }}
    ]
    """
    
    # Get AI response
    response = llm.invoke(prompt)
    
    # Extract questions
    try:
        text = response.content
        json_part = re.search(r'\[.*\]', text, re.DOTALL)
        if json_part:
            questions = json.loads(json_part.group())
        else:
            questions = json.loads(text)
        
        state['quiz_questions'] = questions
        state['total_questions'] = len(questions)
        state['messages'].append(f"✅ Created {len(questions)} questions")
        
    except:
        # Fallback question
        questions = [{
            "question": f"What is {state['topic_title']}?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A"
        }]
        state['quiz_questions'] = questions
        state['total_questions'] = 1
        state['messages'].append("✅ Created 1 question (fallback)")
    
    # Save quiz to database
    db = get_database()
    quiz_data = {
        "user_email": state['user_email'],
        "date": state['study_date'],
        "topic_id": state['topic_id'],
        "topic_title": state['topic_title'],
        "questions": state['quiz_questions'],
        "created_at": datetime.now()
    }
    
    result = db.quizzes.insert_one(quiz_data)
    state['quiz_id'] = str(result.inserted_id)
    state['messages'].append(f"✅ Quiz saved with ID: {state['quiz_id']}")
    state['print'].append(f"quiz Mcqs:\n ,{state['quiz_questions']}")
    
    
    return state
