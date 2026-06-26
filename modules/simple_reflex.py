"""
Module 1: Simple Reflex Agent (v2)
Uses IF-THEN rules to map user interests to career domains.
Extended to support 15 career domains (up from 6).
No memory or state - purely reactive.
"""

from config.career_database import CAREER_DATABASE


class SimpleReflexModule:
    """
    Simple Reflex Agent Module
    Implements IF-THEN rules for interest-to-career mapping.
    """

    @staticmethod
    def map_interests_to_careers(interests):
        """
        Maps user interests to career domains using simple IF-THEN rules.

        Args:
            interests (list): List of user interest strings

        Returns:
            list: Matched career information dictionaries
        """
        mapped_careers = []

        for interest in interests:
            normalized = interest.lower().strip()
            if normalized in CAREER_DATABASE:
                career_data = CAREER_DATABASE[normalized]
                mapped_careers.append({
                    'interest': interest,
                    'domain': career_data['domain'],
                    'modules': career_data['modules'],
                    'education_req': career_data['education_req'],
                    'work_types': career_data['work_types'],
                    'difficulty_level': career_data.get('difficulty_level', 'beginner'),
                    'psychosocial_fit': career_data.get('psychosocial_fit', []),
                    'avg_monthly_income_inr': career_data.get('avg_monthly_income_inr', 0),
                })

        return mapped_careers

    @staticmethod
    def get_all_interest_keys():
        """
        Returns all valid interest keys from the career database.

        Returns:
            list: Sorted list of career domain keys
        """
        return sorted(CAREER_DATABASE.keys())