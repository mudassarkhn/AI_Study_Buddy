from fastapi import FastAPI
from pydantic import BaseModel
from typing import List,Dict,Optional
from app.Graph import study_graph
from Quiz.quiz_graph import quiz_generate
from DB.data_base import get_database
app=FastAPI()
from fastapi.exceptions import HTTPException
from pymongo import MongoClient
from DB.data_base import get_database
from datetime import datetime


class StudyPlanReq(BaseModel):
    user_email: str
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    raw_text: Optional[str] = None
    topics_no: int
    study_time_per_day: str
    exam_date: str
    
class GenerateQuizRequest(BaseModel):
    user_email: str
    study_date: str



@app.get("/health")
def check_health():
    return {
        "API Status" : "okay",
        "Graph Workflow" : True if study_graph else False
    }
@app.post("/generate-plan")

def generate_plan(data: StudyPlanReq):
    
    user_input_dict={
        "user_email":data.user_email,
        "file_path": data.file_path,
        "file_type": data.file_type,
        "raw_text": data.raw_text,
        "topics_no": data.topics_no,
        "study_time_per_day": data.study_time_per_day,
        "exam_date": data.exam_date,
        "messages": [],
        "topics": [],
        "study_plan": []
        
    }

    result=study_graph.invoke(user_input_dict)

    return {
        "message": "Study plan generated successfully",
        "topics": result.get("topics"),
        "study_plan": result.get("study_plan"),
        "logs": result.get("messages")
    }
@app.post("/generate-quiz")
def start_quiz(req: GenerateQuizRequest):
    config = {"configurable": {"thread_id": req.user_email}}
    state = {
        "user_email": req.user_email,
        "study_date": req.study_date,
        "messages": [],
        "user_answers": [],
        "print": []
    }

    result = quiz_generate.invoke(state,config=config)

    return {
        "quiz_id": result.get("quiz_id"),
        "topic_title": result.get("topic_title"),
        "questions": result.get("quiz_questions"),
        "logs": result.get("messages")
    }

db = get_database()
quiz_collection = db["quizzes"]
quiz_result_collection = db["quizzes_result"]


# =====================================================
# Request Schema
# =====================================================
class QuizSubmission(BaseModel):
    user_email: str
    user_answers: List[str]  # Must contain exactly 10 answers


# =====================================================
# Store Quiz Result Function
# =====================================================
def store_quiz_result(
    user_email: str,
    topic_id: int,
    topic_title: str,
    score: int,
    total: int,
    details: list
):
    result_doc = {
        "user_email": user_email,
        "topic_id": topic_id,
        "topic_title": topic_title,
        "score": score,
        "out_of": total,
        "details": details,
        "submitted_at": datetime.utcnow()
    }

    quiz_result_collection.insert_one(result_doc)


# =====================================================
# Submit Quiz Endpoint
# =====================================================
@app.post("/submit-quiz")
def submit_quiz(data: QuizSubmission):
    # 1️⃣ Fetch quiz by email
    quiz_doc = quiz_collection.find_one({"user_email": data.user_email})

    if not quiz_doc:
        raise HTTPException(status_code=404, detail="Quiz not found for this user")

    questions = quiz_doc.get("questions", [])

    if len(questions) != 10:
        raise HTTPException(
            status_code=400,
            detail="Quiz must contain exactly 10 questions"
        )

    if len(data.user_answers) != 10:
        raise HTTPException(
            status_code=400,
            detail="You must submit exactly 10 answers"
        )

    score = 0
    results = []

    # 2️⃣ Compare answers
    for idx, question in enumerate(questions):
        correct_answer = question["correct"].upper()
        user_answer = data.user_answers[idx].upper()

        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1

        results.append({
            "question_no": idx + 1,
            "question": question["question"],
            "correct_answer": correct_answer,
            "user_answer": user_answer,
            "is_correct": is_correct
        })

    # 3️⃣ Store result in MongoDB
    store_quiz_result(
        user_email=data.user_email,
        topic_id=quiz_doc.get("topic_id"),
        topic_title=quiz_doc.get("topic_title"),
        score=score,
        total=10,
        details=results
    )

    # 4️⃣ Response
    return {
        "user_email": data.user_email,
        "topic_id": quiz_doc.get("topic_id"),
        "topic_title": quiz_doc.get("topic_title"),
        "score": score,
        "out_of": 10,
        "details": results
    }