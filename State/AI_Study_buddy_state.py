from typing import TypedDict, Optional,List,Dict
class StudyBuddyState(TypedDict):
    # user_id: str

    # File-based inputs
    file_path: Optional[str] = None
    # Topic-based input
    file_type: Optional[str] = None
    raw_text: Optional[str] = None
    # user_preference: str
    topics_no: int
    study_time_per_day: str
    exam_date: str
    user_email: str
   

    # Processing data
    extracted_text: Optional[str]
    topics: List[Dict]
    study_plan: List[Dict]


    # progress_data: Dict
    messages: List[str]
    print: str
    