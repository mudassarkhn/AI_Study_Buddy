from app.DB.data_base import get_database
from app.LLM.model import llm
from Quiz.quizstate import QuizState
from datetime import datetime
def evaluate_result(state: QuizState) -> QuizState:

    """
    Node 3: Check user's answers and calculate score
    """
    print(f"\n✏️ [NODE 3] Checking answers...")
    
    # Check if we have answers
    if not state.get('user_answers'):
        state['messages'].append("❌ No answers to check")
        return state

    # Count correct answers
    correct = 0
    total = len(state['quiz_questions'])
    
    for i, question in enumerate(state['quiz_questions']):
        if i < len(state['user_answers']):
            user_ans = state['user_answers'][i].upper()
            correct_ans = question['correct'].upper()
            if user_ans == correct_ans:
                correct += 1
    
    # Calculate score
    score = (correct / total * 100) if total > 0 else 0
    
    # Save to state
    state['correct_count'] = correct
    state['score'] = score
    state['messages'].append(f"✅ Score: {score}% ({correct}/{total})")
    
    # Save to database
    db = get_database()
    db.quiz_results.insert_one({
    "user_email": state.get('user_email', 'unknown@mail.com'),
    "quiz_id": state.get('quiz_id'),
    "topic_id": state.get('topic_id'),
    "score": score,
    "correct": correct,
    "total": total,
    "date": datetime.now()
})
    
    state['messages'].append("✅ Results saved to database")
    
    return state