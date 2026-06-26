"""
Module 2: Model-Based Reflex Agent (v2)
Uses internal model of user profile and world state.
Maintains memory and context for better recommendations.

Changes from v1 (addressing reviewer feedback):
  - R1/R3: Added psychosocial alignment scoring (score component 4)
  - R2/R3: Added difficulty-level compatibility check
  - R2:    Added bias mitigation — education is now a soft filter with
           score bonus rather than hard exclusion for marginal cases
  - Score breakdown returned per career for full transparency/explainability
"""

from config.career_database import get_psychosocial_score


class ModelBasedModule:
    """
    Model-Based Reflex Agent Module (v2)
    Scores and ranks careers using user profile + psychosocial alignment.
    """

    # Scoring weights — must sum to 1.0 for interpretability
    W_EDUCATION   = 0.35   # alpha: education compatibility
    W_WORK        = 0.25   # beta:  work-type preference match
    W_TIME        = 0.15   # gamma: time feasibility
    W_PSYCH       = 0.15   # delta: psychosocial alignment (NEW in v2)
    W_DIFFICULTY  = 0.10   # epsilon: difficulty-level suitability (NEW in v2)

    MAX_FEASIBLE_DAYS = 45  # relaxed from 30 to reduce education-level bias

    def __init__(self, user_profile):
        """
        Initialize with user profile (internal state).

        Args:
            user_profile (dict): education, work_preference, time_availability,
                                 psychosocial_tags (optional), confidence_level (optional)
        """
        self.profile = user_profile
        self.education = user_profile['education']
        self.work_preference = user_profile['work_preference']
        self.time_availability = user_profile['time_availability']  # hours/day
        # New: psychosocial tags derived from user's self-reported traits
        self.psychosocial_tags = user_profile.get('psychosocial_tags', [])
        # New: self-reported confidence level (1-10); affects difficulty filtering
        self.confidence_level = user_profile.get('confidence_level', 5)

    def recommend_careers(self, potential_careers):
        """
        Filters and ranks careers using a weighted multi-criteria scoring model.

        Scoring rubric (max = 1.0):
          - Education match    : 0.35
          - Work-type match    : 0.25
          - Time feasibility   : 0.15
          - Psychosocial fit   : 0.15  ← NEW
          - Difficulty fit     : 0.10  ← NEW

        Bias mitigation:
          - High-school educated users are NOT excluded from graduate-preferred
            careers; instead they receive a reduced (but non-zero) education score.
          - This avoids over-penalising users with lower formal education who
            may have equivalent informal experience (Chakraborty & Baltes, 2025).

        Args:
            potential_careers (list): Careers from Simple Reflex module

        Returns:
            list: Scored and ranked career recommendations with full score breakdown
        """
        suitable_careers = []

        for career in potential_careers:
            career_key = career.get('interest', '').lower().strip()

            # ── 1. Education score (soft, bias-mitigated) ────────────────────
            if self.education in career['education_req']:
                edu_score = self.W_EDUCATION          # full score
            elif self._is_adjacent_education(career['education_req']):
                edu_score = self.W_EDUCATION * 0.5    # partial credit — avoids hard exclusion
            else:
                edu_score = 0.0

            # ── 2. Work-preference score ─────────────────────────────────────
            work_score = self.W_WORK if self.work_preference in career['work_types'] else 0.0

            # ── 3. Time feasibility score ────────────────────────────────────
            total_minutes = sum(m['duration'] for m in career['modules'])
            daily_minutes = self.time_availability * 60
            days_needed = total_minutes / daily_minutes if daily_minutes > 0 else 999
            time_score = self.W_TIME if days_needed <= self.MAX_FEASIBLE_DAYS else 0.0

            # ── 4. Psychosocial alignment score (NEW) ────────────────────────
            psych_ratio = get_psychosocial_score(self.psychosocial_tags, career_key)
            psych_score = self.W_PSYCH * psych_ratio

            # ── 5. Difficulty suitability score (NEW) ────────────────────────
            diff_score = self._difficulty_score(career.get('difficulty_level', 'beginner'))

            # ── Aggregate weighted score ─────────────────────────────────────
            total_score = edu_score + work_score + time_score + psych_score + diff_score

            # Minimum gate: education + work preference must clear 50% of their combined weight
            min_gate = (self.W_EDUCATION + self.W_WORK) * 0.5
            if (edu_score + work_score) >= min_gate:
                suitable_careers.append({
                    'career': career,
                    'score': round(total_score, 3),
                    'score_breakdown': {
                        'education': round(edu_score, 3),
                        'work_type': round(work_score, 3),
                        'time_feasibility': round(time_score, 3),
                        'psychosocial_fit': round(psych_score, 3),
                        'difficulty_fit': round(diff_score, 3),
                    },
                    'estimated_days': int(days_needed) + 1,
                    'difficulty_level': career.get('difficulty_level', 'beginner'),
                    'avg_monthly_income_inr': career.get('avg_monthly_income_inr', 0),
                })

        # Sort by composite score descending
        suitable_careers.sort(key=lambda x: x['score'], reverse=True)
        return suitable_careers

    def _is_adjacent_education(self, education_req):
        """
        Checks if user's education is one step below the minimum required.
        Used for bias-mitigated partial credit.

        Args:
            education_req (list): Career's required education levels

        Returns:
            bool: True if user is "adjacent" (one level below minimum)
        """
        edu_ladder = ['high-school', 'graduate', 'postgraduate']
        user_idx = edu_ladder.index(self.education) if self.education in edu_ladder else -1
        for req in education_req:
            req_idx = edu_ladder.index(req) if req in edu_ladder else -1
            if req_idx == user_idx + 1:   # user is exactly one rung below
                return True
        return False

    def _difficulty_score(self, difficulty_level):
        """
        Maps user confidence level (1-10) to difficulty level compatibility.

        Mapping:
          confidence 1-3  → beginner careers score highest
          confidence 4-6  → intermediate careers score highest
          confidence 7-10 → advanced careers score highest

        Args:
            difficulty_level (str): 'beginner', 'intermediate', or 'advanced'

        Returns:
            float: Difficulty fit component score
        """
        c = self.confidence_level
        mapping = {
            'beginner':     1.0 if c <= 4 else (0.7 if c <= 6 else 0.4),
            'intermediate': 0.5 if c <= 3 else (1.0 if c <= 7 else 0.7),
            'advanced':     0.2 if c <= 4 else (0.6 if c <= 6 else 1.0),
        }
        return self.W_DIFFICULTY * mapping.get(difficulty_level, 0.5)
