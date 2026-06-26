from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class CareerBuddyModel(Model):
    """
    Multi-Agent System Model for CareerBuddy application.
    This class manages multiple UserAgent instances, schedules agent actions,
    and collects system-wide statistics for analytics and monitoring.
    """

    def __init__(self):
        """Initialize the model and its components."""
        super().__init__()  # Initialize parent Model class

        # Scheduler is responsible for activating each agent once per step.
        # RandomActivation activates agents in random order at each step.
        self.schedule = RandomActivation(self)

        # Dictionary to map usernames to their corresponding UserAgent instances.
        # This allows quick lookup of agents by username.
        self.agents_dict = {}

        # DataCollector is a Mesa component used for collecting model and agent data
        # during each step for later analysis or visualization.
        self.datacollector = DataCollector(
            # Model-level reporters collect summary statistics using lambdas.
            model_reporters={
                "Total Users": lambda m: len(m.schedule.agents),
                "Active Users": lambda m: sum(1 for a in m.schedule.agents if not a.completed),
                "Completed Users": lambda m: sum(1 for a in m.schedule.agents if a.completed),
                # Calculate average progress percentage across all agents using a helper method.
                "Average Progress": lambda m: self._get_average_progress(m)
            },
            # Agent-level reporters capture per-agent data attributes.
            agent_reporters={
                "Username": "username",  # Direct attribute access
                "Progress": lambda a: a.get_progress()['percentage'],  # Call agent method for progress
                "Completed": "completed"  # Boolean attribute
            }
        )

    @staticmethod
    def _get_average_progress(model):
        """
        Static helper method to calculate average completion progress of all agents.
        Args:
            model (CareerBuddyModel): The running model instance.
        Returns:
            float: Average progress percentage (0 if no agents).
        """
        if len(model.schedule.agents) == 0:
            return 0
        # Sum up each agent's progress percentage and divide by total agents count.
        return sum(a.get_progress()['percentage'] for a in model.schedule.agents) / len(model.schedule.agents)

    def add_user(self, username, profile):
        """
        Add a new user agent to the system with given username and profile.
        This initializes a UserAgent instance, assigns a unique ID, and registers it.
        
        Args:
            username (str): Unique username string for the user.
            profile (dict): Profile data containing user-specific settings.

        Returns:
            UserAgent: The newly created agent instance.
        """
        # Importing UserAgent locally to avoid circular dependencies.
        from agents.user_agent import UserAgent

        # Unique ID for the new agent is the current count of agents.
        user_id = len(self.schedule.agents)

        # Embed the username into the profile dict for agent reference.
        profile['username'] = username

        # Instantiate the UserAgent passing its ID, the model reference, and profile.
        agent = UserAgent(user_id, self, profile)

        # Add the agent to the scheduler so it will be stepped by the model.
        self.schedule.add(agent)

        # Register the agent in agents_dict for fast lookup by username.
        self.agents_dict[username] = agent

        # Return the new agent instance for further usage if needed.
        return agent

    def get_agent(self, username):
        """
        Retrieve the UserAgent instance associated with the given username.
        
        Args:
            username (str): The username to lookup.
            
        Returns:
            UserAgent or None: UserAgent instance if found, None otherwise.
        """
        # Use dictionary get method for safe retrieval avoiding exception if missing.
        return self.agents_dict.get(username)

    def get_statistics(self):
        """
        Generate overall system-level statistics about users and progress.
        
        Returns:
            dict: A dictionary with keys 'total_users', 'active_users',
                  'completed_users', and 'average_progress'.
        """
        # If no agents currently in model, return zeroed stats directly.
        if len(self.schedule.agents) == 0:
            return {
                'total_users': 0,
                'active_users': 0,
                'completed_users': 0,
                'average_progress': 0
            }

        # Calculate detailed statistics based on agent data.
        total = len(self.schedule.agents)
        active = sum(1 for a in self.schedule.agents if not a.completed)  # Agents not completed
        completed = sum(1 for a in self.schedule.agents if a.completed)
        # Average progress as a float rounded to 2 decimals for readability.
        avg_progress = sum(a.get_progress()['percentage'] for a in self.schedule.agents) / total

        # Return all collected statistics in a single dictionary.
        return {
            'total_users': total,
            'active_users': active,
            'completed_users': completed,
            'average_progress': round(avg_progress, 2)
        }

    def step(self):
        """
        Advance the model by one simulation step.
        This calls the scheduler's step method which activates each agent to act.
        Then collects data after all agents have stepped.
        """
        self.schedule.step()  # Let all agents perform their behaviors once
        self.datacollector.collect(self)  # Collect data after the step completes