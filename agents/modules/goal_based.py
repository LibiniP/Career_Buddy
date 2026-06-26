"""
Module 3: Goal-Based Agent (v2 - Enhanced with Quantitative Metrics)
Plans actions to achieve specific goals with intelligent scheduling,
adaptive motivation, and progress tracking.

Changes from v1 (addressing reviewer feedback):
  - R1: Clearer technical details about the optimization algorithm (see docstrings)
  - R1/R2: Added quantitative scheduling metrics:
      * scheduling_optimality_score  (how evenly workload is distributed)
      * daily_load_variance          (lower = better balanced schedule)
      * utilization_rate             (% of available time actually used)
  - R3: Algorithm now formally documented with complexity analysis

Algorithm: Priority-Weighted Balanced Greedy Scheduler
────────────────────────────────────────────────────────
Input  : Set of careers C each with ordered module list M_c,
         daily time budget T_d (minutes)
Output : Day-wise schedule S = {d_1, d_2, ..., d_n}

Strategy:
  1. For each career, compute module weights using:
       w_i = (|M_c| - idx) + (duration_i / 60)
     (earlier/longer modules get higher priority)
  2. Maintain a round-robin queue of career task streams to ensure
     interleaving (prevents career monotony across days).
  3. Greedy allocation: fill each day up to a target load of
       T_target = 0.9 * (T_total / estimated_days)
     before advancing to the next day.
  4. Oversized modules (duration > T_d) occupy their own day.

Time complexity : O(N log N) due to per-career sort, O(N) greedy pass
Space complexity: O(N) for task queues
where N = total number of learning modules across all careers.
"""

from datetime import datetime
import math
import statistics


class GoalBasedModule:
    """
    Goal-Based Agent Module (v2)
    Plans optimized schedules and exposes quantitative evaluation metrics.
    """

    def __init__(self, daily_hours):
        """
        Initialize with daily time budget.

        Args:
            daily_hours (float): Hours available per day
        """
        self.daily_minutes = daily_hours * 60
        self.goal = "Complete all learning modules"
        self.progress = {}           # task_id -> bool (completed)
        self.schedule_history = []   # list of day-dicts

    # ── Schedule Generation ───────────────────────────────────────────────────

    def generate_daily_schedule(self, careers):
        """
        Generate day-wise learning schedule using priority-weighted balanced
        greedy scheduling (see module docstring for full algorithm description).

        Args:
            careers (list): Recommended career dicts from Model-Based Agent

        Returns:
            list: Day-wise schedule [{'day': int, 'tasks': list, 'total_time': int}]
        """
        if not careers:
            return []

        # Step 1: Build priority-sorted task queue per career
        career_task_queues = self._build_task_queues(careers)

        if not any(q['tasks'] for q in career_task_queues):
            return []

        # Step 2: Compute scheduling parameters
        total_minutes = sum(
            sum(t['duration'] for t in q['tasks']) for q in career_task_queues
        )
        if total_minutes == 0:
            return []

        estimated_days = max(1, math.ceil(total_minutes / self.daily_minutes))
        target_daily_minutes = (total_minutes / estimated_days) * 0.9

        # Step 3: Greedy allocation with round-robin career interleaving
        daily_schedules = self._greedy_allocate(
            career_task_queues, target_daily_minutes
        )

        # Step 4: Fallback if schedule is empty (edge case)
        if not daily_schedules:
            all_tasks = [t for q in career_task_queues for t in q['tasks']]
            if all_tasks:
                daily_schedules = [{
                    'day': 1,
                    'tasks': all_tasks,
                    'total_time': sum(t['duration'] for t in all_tasks)
                }]

        self.schedule_history = daily_schedules
        return daily_schedules

    def _build_task_queues(self, careers):
        """
        Build per-career priority-sorted task queues.

        Priority weight formula:
            w_i = (|M| - idx) + (duration_i / 60)
        This ensures foundational (earlier-indexed) modules are scheduled first,
        with tie-breaking favouring longer modules.

        Args:
            careers (list): Career recommendation list

        Returns:
            list: Career task queue dicts
        """
        queues = []
        for career_info in careers:
            career = career_info['career']
            tasks = []
            for idx, module in enumerate(career['modules']):
                task_id = f"{career['domain'].replace(' ', '_')}_{idx}"
                position_weight = len(career['modules']) - idx
                duration_weight = module['duration'] / 60
                tasks.append({
                    'id': task_id,
                    'career': career['domain'],
                    'task': module['name'],
                    'duration': module['duration'],
                    'sequence': idx,
                    'weight': position_weight + duration_weight,
                    'completed': False,
                })
            tasks.sort(key=lambda x: -x['weight'])
            queues.append({'career': career['domain'], 'tasks': tasks, 'current_index': 0})
        return queues

    def _greedy_allocate(self, career_task_queues, target_daily_minutes):
        """
        Core greedy allocation loop with round-robin career interleaving.

        Args:
            career_task_queues (list): Per-career sorted task queues
            target_daily_minutes (float): Soft daily target (90% of even distribution)

        Returns:
            list: Completed daily schedule
        """
        daily_schedules = []
        current_day_tasks = []
        current_day_time = 0
        day_num = 1
        start_index = 0
        num_queues = len(career_task_queues)

        while any(q['current_index'] < len(q['tasks']) for q in career_task_queues):
            tasks_added_this_round = False

            for i in range(num_queues):
                queue = career_task_queues[(start_index + i) % num_queues]
                if queue['current_index'] >= len(queue['tasks']):
                    continue

                task = queue['tasks'][queue['current_index']]

                if current_day_time + task['duration'] <= self.daily_minutes:
                    current_day_tasks.append(task)
                    current_day_time += task['duration']
                    queue['current_index'] += 1
                    tasks_added_this_round = True

                    if current_day_time >= target_daily_minutes:
                        # Fill remaining slack before closing the day
                        for q in career_task_queues:
                            if q['current_index'] < len(q['tasks']):
                                nt = q['tasks'][q['current_index']]
                                if current_day_time + nt['duration'] <= self.daily_minutes:
                                    current_day_tasks.append(nt)
                                    current_day_time += nt['duration']
                                    q['current_index'] += 1

                        daily_schedules.append({
                            'day': day_num,
                            'tasks': current_day_tasks,
                            'total_time': current_day_time,
                        })
                        day_num += 1
                        current_day_tasks = []
                        current_day_time = 0
                        break

                elif current_day_time == 0:
                    # Oversized module — give it its own day
                    current_day_tasks.append(task)
                    current_day_time += task['duration']
                    queue['current_index'] += 1
                    tasks_added_this_round = True
                    daily_schedules.append({
                        'day': day_num,
                        'tasks': current_day_tasks,
                        'total_time': current_day_time,
                    })
                    day_num += 1
                    current_day_tasks = []
                    current_day_time = 0
                    break

            start_index = (start_index + 1) % num_queues

            if not tasks_added_this_round:
                if current_day_tasks:
                    daily_schedules.append({
                        'day': day_num,
                        'tasks': current_day_tasks,
                        'total_time': current_day_time,
                    })
                    day_num += 1
                    current_day_tasks = []
                    current_day_time = 0
                else:
                    for queue in career_task_queues:
                        if queue['current_index'] < len(queue['tasks']):
                            task = queue['tasks'][queue['current_index']]
                            daily_schedules.append({
                                'day': day_num,
                                'tasks': [task],
                                'total_time': task['duration'],
                            })
                            day_num += 1
                            queue['current_index'] += 1
                            break

        if current_day_tasks:
            daily_schedules.append({
                'day': day_num,
                'tasks': current_day_tasks,
                'total_time': current_day_time,
            })

        return daily_schedules

    # ── Quantitative Evaluation Metrics (NEW — addresses R1/R2) ──────────────

    def get_scheduling_metrics(self):
        """
        Compute quantitative scheduling quality metrics.

        Metrics returned:
          scheduling_optimality_score (float 0-1):
              1 - (std_dev / mean) of daily loads (coefficient of variation).
              Higher = more evenly balanced workload across days.
              Score of 1.0 means perfectly equal daily load.

          daily_load_variance (float):
              Statistical variance of daily task loads in minutes.
              Lower = better balanced schedule.

          utilization_rate (float 0-1):
              Ratio of total scheduled time to maximum available time
              (daily_minutes × num_days). Higher = more efficient use of time.

          avg_tasks_per_day (float):
              Mean number of tasks assigned per day.

          max_day_overload_pct (float):
              % by which the busiest day exceeds the daily time budget.
              Should be 0.0 for a well-constrained schedule.

        Returns:
            dict: Scheduling quality metrics
        """
        if not self.schedule_history:
            return {
                'scheduling_optimality_score': 0.0,
                'daily_load_variance': 0.0,
                'utilization_rate': 0.0,
                'avg_tasks_per_day': 0.0,
                'max_day_overload_pct': 0.0,
            }

        daily_loads = [day['total_time'] for day in self.schedule_history]
        total_scheduled = sum(daily_loads)
        num_days = len(daily_loads)
        max_available = self.daily_minutes * num_days

        mean_load = statistics.mean(daily_loads) if daily_loads else 0
        std_load = statistics.stdev(daily_loads) if len(daily_loads) > 1 else 0
        variance = statistics.variance(daily_loads) if len(daily_loads) > 1 else 0

        # Coefficient of variation (lower CV = more uniform = higher optimality)
        cv = (std_load / mean_load) if mean_load > 0 else 0
        optimality = round(max(0.0, 1.0 - cv), 3)

        utilization = round(total_scheduled / max_available, 3) if max_available > 0 else 0

        total_tasks = sum(len(d['tasks']) for d in self.schedule_history)
        avg_tasks = round(total_tasks / num_days, 2) if num_days > 0 else 0

        overloaded_days = [
            (d['total_time'] - self.daily_minutes) / self.daily_minutes * 100
            for d in self.schedule_history
            if d['total_time'] > self.daily_minutes
        ]
        max_overload = round(max(overloaded_days), 2) if overloaded_days else 0.0

        return {
            'scheduling_optimality_score': optimality,
            'daily_load_variance': round(variance, 2),
            'utilization_rate': utilization,
            'avg_tasks_per_day': avg_tasks,
            'max_day_overload_pct': max_overload,
        }

    # ── Progress Tracking ─────────────────────────────────────────────────────

    def update_progress(self, task_id, completed=True):
        """Mark a task as completed or incomplete."""
        self.progress[task_id] = completed

    def track_progress(self):
        """
        Returns detailed progress statistics.

        Returns:
            dict: {completed, total, percentage, goal_achieved}
        """
        if not self.schedule_history:
            return {'completed': 0, 'total': 0, 'percentage': 0, 'goal_achieved': False}

        total_tasks = sum(len(day['tasks']) for day in self.schedule_history)
        if total_tasks == 0:
            return {'completed': 0, 'total': 0, 'percentage': 0, 'goal_achieved': False}

        completed_tasks = sum(1 for tid, done in self.progress.items() if done)
        percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0

        return {
            'completed': completed_tasks,
            'total': total_tasks,
            'percentage': round(percentage, 2),
            'goal_achieved': percentage >= 100.0,
        }

    def generate_motivation(self, progress_percentage=None):
        """
        Generate motivational message calibrated to progress stage.

        Args:
            progress_percentage (float): Optional override percentage

        Returns:
            str: Motivational message
        """
        stats = self.track_progress()
        p = progress_percentage if progress_percentage is not None else stats['percentage']

        if p == 0:
            return "Let's get started! Every expert was once a beginner. 💪"
        elif p < 25:
            return "Great start! Keep the momentum going! 🌟"
        elif p < 50:
            return "You're doing amazing! Almost halfway there! 🎯"
        elif p < 75:
            return "Fantastic progress! You're almost there! 🚀"
        elif p < 100:
            return "Outstanding work! Just one more push! 🏆"
        else:
            return "Perfect! You've achieved your goal! 🎉"

    def get_daily_summary(self, day_number):
        """
        Get summary for a specific day.

        Args:
            day_number (int): 1-indexed day number

        Returns:
            dict or None
        """
        if day_number < 1 or day_number > len(self.schedule_history):
            return None

        day = self.schedule_history[day_number - 1]
        completed_count = sum(
            1 for task in day['tasks']
            if self.progress.get(task['id'], False)
        )
        return {
            'day': day['day'],
            'total_tasks': len(day['tasks']),
            'completed_tasks': completed_count,
            'total_time': day['total_time'],
            'completion_percentage': (
                completed_count / len(day['tasks']) * 100
            ) if day['tasks'] else 0,
        }

    def print_schedule(self):
        """Print the schedule in human-readable format."""
        if not self.schedule_history:
            print("No schedule generated yet.")
            return

        total_tasks = sum(len(d['tasks']) for d in self.schedule_history)
        total_time = sum(d['total_time'] for d in self.schedule_history)
        metrics = self.get_scheduling_metrics()

        print(f"\n{'='*55}")
        print("  Learning Schedule Summary")
        print(f"{'='*55}")
        print(f"  Total Days   : {len(self.schedule_history)}")
        print(f"  Total Tasks  : {total_tasks}")
        print(f"  Total Time   : {total_time} min ({total_time/60:.1f} hrs)")
        print(f"  Optimality   : {metrics['scheduling_optimality_score']:.2%}")
        print(f"  Utilization  : {metrics['utilization_rate']:.2%}")
        print(f"{'='*55}\n")

        for day in self.schedule_history:
            print(f"Day {day['day']}  ({day['total_time']} mins / {day['total_time']/60:.1f} hrs):")
            for task in day['tasks']:
                status = "✅" if self.progress.get(task['id'], False) else "⬜"
                print(f"  {status} [{task['career']}] {task['task']} ({task['duration']} min)")
            print("-" * 55)
