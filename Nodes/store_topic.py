from pymongo import MongoClient
from datetime import datetime
from State.AI_Study_buddy_state import StudyBuddyState
from DB.data_base import get_database
def store_topics(state: StudyBuddyState) -> StudyBuddyState:
    """Step 3: Save all topics to MongoDB database"""
    print("💾 Storing topics in database...")
    
    
    #connect to MongoDB 
    db = get_database()
    topics_collection = db['topics']
    
    # Prepare data to save
    topic_data = {
        "user_email": state['user_email'],
        "topics": state['topics'],
        "created_at": datetime.now()
    }
    
    # Save to database
    topics_collection.insert_one(topic_data)
    
    # Update state
    state['messages'].append(f"✅ Saved {len(state['topics'])} topics to database")
    
    return state