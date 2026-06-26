"""
User Agent (v2)
Hybrid agent combining all three modules:
  1. Simple Reflex  — interest-to-career mapping (15 careers)
  2. Model-Based    — profile + psychosocial filtering and scoring
  3. Goal-Based     — balanced greedy scheduling with quality metrics
"""

from mesa import Agent
from datetime import datetime
from agents.modules.simple_reflex import SimpleReflexModule
from agents.modules.model_based import ModelBasedModule
from agents.modules.goal_based import GoalBasedModule


class UserAgent(Agent):
    """
    Hybrid UserAgent combining reactive, model-based, and goal-based reasoning.
    """

    def __init__(self, unique_id, model, profile):
        super().__init__(unique_id, model)

        self.username = profile['username']
        self.education = profile['education']
        self.interests = profile['interests']
        self.experience = profile.get('experience', '')
        self.time_availability = profile['time_availability']
        self.work_preference = profile['work_preference']
        self.motivation_level = profile.get('motivation_level', 5)

        # NEW: psychosocial data (v2)
        self.psychosocial_tags = profile.get('psychosocial_tags', [])
        self.confidence_level = profile.get('confidence_level', 5)

        # Instantiate modules
        self.simple_reflex = SimpleReflexModule()
        self.model_based = ModelBasedModule(profile)
        self.goal_based = GoalBasedModule(profile['time_availability'])

        # State
        self.recommended_careers = []
        self.daily_schedule = []
        self.current_day = 1
        self.completed = False
        self.completion_date = None
        self.total_days = 0
        self.total_tasks = 0

        self._initialize_learning_path()

    def _initialize_learning_path(self):
        """Build full learning path by composing all three modules."""
        potential_careers = self.simple_reflex.map_interests_to_careers(self.interests)
        self.recommended_careers = self.model_based.recommend_careers(potential_careers)

        if self.recommended_careers:
            self.daily_schedule = self.goal_based.generate_daily_schedule(
                self.recommended_careers
            )
            self.total_days = len(self.daily_schedule)
            for day in self.daily_schedule:
                for task in day['tasks']:
                    self.goal_based.progress[task['id']] = False
                    self.total_tasks += 1

    def complete_task(self, task_id):
        self.goal_based.update_progress(task_id, True)

    def get_progress(self):
        progress = self.goal_based.track_progress()
        if progress['goal_achieved'] and not self.completed:
            self.completed = True
            self.completion_date = datetime.now()
        return progress

    def get_motivation(self):
        progress = self.get_progress()
        return self.goal_based.generate_motivation(progress['percentage'])

    def get_scheduling_metrics(self):
        """Expose scheduling quality metrics for dashboard / paper evaluation."""
        return self.goal_based.get_scheduling_metrics()

    def get_status(self):
        return {
            'username': self.username,
            'education': self.education,
            'interests': self.interests,
            'careers': [c['career']['domain'] for c in self.recommended_careers],
            'score_breakdown': [
                {
                    'career': c['career']['domain'],
                    'score': c['score'],
                    'breakdown': c['score_breakdown'],
                    'estimated_days': c['estimated_days'],
                }
                for c in self.recommended_careers
            ],
            'progress': self.get_progress(),
            'motivation': self.get_motivation(),
            'scheduling_metrics': self.get_scheduling_metrics(),
            'current_day': self.current_day,
            'total_days': self.total_days,
            'completed': self.completed,
        }

    def step(self):
        pass