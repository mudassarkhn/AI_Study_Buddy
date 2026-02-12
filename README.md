# AI Study Buddy 📚🤖

An intelligent study companion that transforms your study materials into personalized learning plans, daily quizzes, and adaptive learning schedules using AI-powered agents built with LangGraph.

## 🌟 Overview

AI Study Buddy is an autonomous learning system that helps students optimize their study time by:
- Automatically processing and chunking study materials into manageable topics
- Creating personalized study plans based on available time and preferences
- Generating daily quizzes to reinforce learning
- Tracking progress and adapting future study plans based on performance
- Providing automated reminders and motivation

## ✨ Key Features

### 📄 Smart Document Processing
- Supports multiple file formats (PDF, DOCX, TXT)
- Automatic text extraction and content cleaning
- Intelligent topic/chapter segmentation using AI
- Semantic chunking based on logical content divisions

### 🎯 Personalized Study Planning
- Customizable study schedule based on:
  - Number of topics/chapters to cover
  - Available study time per day
  - Target completion date or total duration
- AI-generated daily study roadmap
- Flexible plan adjustments

### 📝 AI-Generated Quizzes
- Automatic quiz generation from studied topics
- Interactive question-answer evaluation
- Performance tracking and weak topic identification
- Adaptive difficulty based on user performance

### 📊 Progress Tracking
- Real-time performance monitoring
- Weak topic identification and reinforcement
- Study streak tracking
- Completion percentage and accuracy metrics

### 🔄 Adaptive Learning
- Automatic plan adjustments based on:
  - Time spent on topics
  - Quiz performance
  - Identified weak areas
- Dynamic schedule optimization

## 🏗️ Architecture

This project is built using **LangGraph**, a framework for building stateful, multi-agent applications with LLMs. The system consists of multiple specialized AI agents working together:

### Agent Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (File + Preferences)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           File Processing Agent                              │
│  • Extracts text from uploaded files                        │
│  • Cleans and preprocesses content                          │
│  • Segments into logical chunks/topics                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Study Plan Generator Agent                         │
│  • Analyzes extracted topics                                │
│  • Creates daily study schedule                             │
│  • Maps topics to specific dates                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Daily Reminder System                              │
│  • Scheduled triggers                                        │
│  • Sends study reminders                                    │
│  • Motivational messages                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Quiz Generator Agent                               │
│  • Creates topic-specific quizzes                           │
│  • Interactive Q&A sessions                                 │
│  • Immediate feedback                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Performance Evaluator                              │
│  • Scores quiz responses                                    │
│  • Identifies weak topics                                   │
│  • Updates progress metrics                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Plan Adjustment Agent                              │
│  • Reviews performance data                                 │
│  • Adjusts future study schedule                            │
│  • Optimizes for weak areas                                 │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
AI_Study_Buddy/
├── DB/                      # Database connection and models
├── LLM/                     # LLM configurations and handlers
├── Nodes/                   # LangGraph node definitions
│   ├── file_processor.py
│   ├── study_planner.py
│   ├── quiz_generator.py
│   └── performance_evaluator.py
├── Quiz/                    # Quiz generation logic
├── Resources/               # Utilities and helpers
├── State/                   # LangGraph state management
├── Graph.py                 # Main LangGraph workflow definition
├── main.py                  # Application entry point
├── AI Study Buddy.ipynb     # Development notebook
├── input-example.json       # Example input configuration
├── requirements.txt         # Python dependencies
└── __init__.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (for data storage)
- OpenAI API key or compatible LLM endpoint

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mudassarkhn/AI_Study_Buddy.git
cd AI_Study_Buddy
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=your_mongodb_connection_string
```

5. **Configure MongoDB**
Ensure MongoDB is running and accessible at the URI specified in your `.env` file.

## 💻 Usage

### Basic Usage

1. **Run the application**
```bash
python main.py
```

2. **Upload your study material**
Provide:
- Study material file (PDF/DOCX/TXT)
- Number of topics/chapters to divide content into
- Available study time per day (e.g., "2 hours")
- Start date or total duration

3. **Receive your personalized study plan**
The system will generate a daily schedule mapping each topic to specific dates.

4. **Follow daily reminders**
You'll receive notifications with:
- Today's study topic
- Recommended duration
- Motivational messages

5. **Complete daily quizzes**
After studying, take AI-generated quizzes to reinforce learning.

6. **Track your progress**
Monitor your performance, completion rate, and weak areas.

### Example Input

See `input-example.json` for a sample configuration:

```json
{
  "file_path": "path/to/your/textbook.pdf",
  "preferences": {
    "num_topics": 10,
    "study_time_per_day": "2 hours",
    "start_date": "2024-03-01",
    "duration_days": 30
  }
}
```

### Using the Jupyter Notebook

For development and testing, you can use the provided notebook:

```bash
jupyter notebook "AI Study Buddy.ipynb"
```

## 🛠️ Technology Stack

- **LangGraph**: Multi-agent orchestration and workflow management
- **LangChain**: LLM integration and chain building
- **OpenAI API**: Language model backend (configurable)
- **MongoDB**: Document storage for topics, plans, and progress
- **Python**: Core programming language
- **Jupyter**: Interactive development and testing

## 📋 Core Components

### LangGraph Nodes

1. **File Processing Node**
   - Extracts and cleans text from uploaded files
   - Performs semantic chunking of content

2. **Study Plan Generator Node**
   - Creates personalized daily study schedules
   - Optimizes time allocation across topics

3. **Quiz Generator Node**
   - Generates contextual questions from study material
   - Adapts difficulty based on performance

4. **Performance Evaluator Node**
   - Scores quiz responses
   - Identifies areas needing improvement

5. **Plan Adjuster Node**
   - Dynamically updates study schedule
   - Allocates more time to challenging topics

### State Management

The system maintains state across the following dimensions:
- Extracted topics and content chunks
- Current study plan and progress
- Quiz history and performance metrics
- Weak topics requiring additional focus

## 🔧 Configuration

### Customizing the LLM

Edit the LLM configuration in the `LLM/` directory to use different models:
- OpenAI GPT-4/GPT-3.5
- Anthropic Claude
- Local models via Ollama
- Any OpenAI-compatible endpoint

### Database Configuration

Configure MongoDB settings in `DB/` to customize:
- Connection parameters
- Database name
- Collection schemas

## 📊 Features in Detail

### Intelligent Topic Segmentation
The system uses AI to identify natural topic boundaries in your study material, ensuring logical and coherent content chunks.

### Adaptive Learning Path
Based on quiz performance, the system automatically:
- Extends time for difficult topics
- Reduces time for mastered content
- Suggests review sessions for weak areas

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- File upload size limitations may affect very large documents
- Quiz generation quality depends on source material clarity
- Initial setup requires MongoDB configuration

## 🔮 Future Enhancements

- [ ] Support for video lecture transcripts
- [ ] Spaced repetition algorithm integration
- [ ] Multi-language support
- [ ] Mobile app for quiz interaction
- [ ] Voice-based quiz mode
- [ ] Collaborative study groups
- [ ] Integration with calendar apps
- [ ] Gamification features (badges, leaderboards)

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

## 🙏 Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)

---

**Happy Studying! 📚✨**
