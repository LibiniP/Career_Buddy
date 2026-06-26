# 🎯 CareerBuddy AI Agent System

A professional multi-agent career guidance system built with Mesa framework implementing hybrid agent architecture.

## 📋 Overview

CareerBuddy uses three types of AI agents to provide personalized career recommendations:
- **Module 1**: Simple Reflex Agent (Interest Mapping)
- **Module 2**: Model-Based Reflex Agent (Career Recommendation)
- **Module 3**: Goal-Based Agent (Schedule & Progress Tracking)

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
jupyter nbextension enable --py widgetsnbextension
```

### Run Application
```bash
python run.py
```

Or in Jupyter Notebook:
```python
from run import start_application
start_application()
```

## 📁 Project Structure

- `agents/` - Mesa agent implementations
- `models/` - Model classes and logic
- `ui/` - User interface components
- `config/` - Configuration and data
- `utils/` - Helper functions
- `data/` - User data storage

## 🎓 Architecture

### Agent Modules
1. **Simple Reflex**: IF-THEN rules for interest mapping
2. **Model-Based**: Profile-based career filtering with scoring
3. **Goal-Based**: Schedule generation and progress tracking

### Key Classes
- `UserAgent`: Hybrid agent with all 3 modules
- `CareerBuddyModel`: Multi-agent system manager
- `UIComponents`: Interactive interface elements

## 📖 Documentation

See individual module documentation for details.

## 🤝 Contributing

This is an educational project demonstrating agent-based AI systems.