from typing import TypedDict, List, Dict

# ============ STATE CLASS ============
class QuizState(TypedDict):
    """
    This holds all the information that flows through the nodes
    Think of it like a shared notebook that each function can read and write to
    """
    # Input from user
    user_email: str
    study_date: str  
    user_answers: List[str]  
    
    # Data that gets filled by nodes
    topic_id: int
    topic_title: str
    topic_content: str
    quiz_id: str
    quiz_questions: List[Dict]
    
    # Results
    score: float
    correct_count: int
    total_questions: int
    
    # Messages for tracking
    messages: List[str]
    print: List[str]



