from State.AI_Study_buddy_state import  StudyBuddyState
from DB.data_base import get_database
def save_plan(state: StudyBuddyState) -> StudyBuddyState:
    from datetime import datetime
    """Step 5: Save study plan to database"""
    print("💾 Saving study plan...")
    
    # Connect to database
    db = get_database()
    plans_collection = db['study_plans']
    
    # Prepare plan data
    plan_data = {
        "user_email": state['user_email'],
        "plan": state['study_plan'],
        "created_at": datetime.now()
    }
    
    # Save to database
    plans_collection.insert_one(plan_data)
    
    # Update state
    state['messages'].append("✅ Study plan saved successfully")
    
    return state