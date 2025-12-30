from langgraph.graph import StateGraph,END,START
from Nodes.file_processing import file_processing
from Nodes.generate_study_plan import generate_study_plan
from Nodes.save_study_plan import save_plan
from Nodes.semantic_chunker import semantic_chunker
from Nodes.store_topic import store_topics


from State.AI_Study_buddy_state import StudyBuddyState
# 13. LANGGRAPH DEFINITION
# -------------------------------
workflow = StateGraph(StudyBuddyState)

workflow.add_node("file_processing", file_processing)
# workflow.add_node("clean_text", clean_text_node)
workflow.add_node("semantic_chunker", semantic_chunker)
workflow.add_node("store_topics", store_topics)
workflow.add_node("generate_study_plan", generate_study_plan)
workflow.add_node("save_plan", save_plan)


workflow.add_edge(START, "file_processing")
workflow.add_edge("file_processing", "semantic_chunker")
workflow.add_edge("semantic_chunker", "store_topics")
workflow.add_edge("store_topics", "generate_study_plan")
workflow.add_edge("generate_study_plan","save_plan")
workflow.add_edge("save_plan", END)


study_graph = workflow.compile()
# study_graph.invoke({
#     "file_path": "./Resources/ICT_notes.pdf",
#     "file_type": "pdf",
#     "raw_text": None,
#     "study_time_per_day": 240,
#     "exam_date": "2025-12-22",
#     "user_email": "jones@gmail.com",
#     "topics_no": 3,
#    })