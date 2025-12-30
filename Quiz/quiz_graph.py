from langgraph.graph import StateGraph, START, END
from Quiz.quizstate import QuizState
from Quiz.Nodes.fetch_topic import fetch_topic
from Quiz.Nodes.generate_quiz import generate_quiz
from Quiz.Nodes.evaluate_result import evaluate_result
from langgraph.checkpoint.memory import MemorySaver

# 1. Initialize Memory (Required for interrupts)
memory = MemorySaver()

graph=StateGraph(QuizState)
graph.add_node("fetch_topic",fetch_topic)
graph.add_node("generate_quiz",generate_quiz)
graph.add_node("evaluate_result",evaluate_result)

graph.set_entry_point("fetch_topic")
graph.add_edge("fetch_topic","generate_quiz")
graph.add_edge("generate_quiz","evaluate_result")
graph.add_edge("evaluate_result",END)

quiz_generate = graph.compile(checkpointer=memory,interrupt_before=["evaluate_result"])
# evaluate_anwer.invoke({

# 'user_email': 'hello@gmail.com',
# 'study_date': '2025-12-20',
# 'quiz_questions': [],
# 'messages':[],
# "quiz_id": "",
# "topic_id": ""
# })