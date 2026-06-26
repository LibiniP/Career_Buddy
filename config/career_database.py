"""
Career Database Configuration (Expanded - v2)
Expanded from 6 to 15 career domains to address scalability concerns.
Each career now includes:
  - psychosocial_fit: maps to confidence/self-efficacy profile tags
  - difficulty_level: beginner / intermediate / advanced
  - avg_monthly_income_inr: indicative earning potential
  - peer_reviewed_source: domain reference for academic grounding

Reviewer feedback addressed:
  - R3: Dataset too limited (only 6 careers) → expanded to 15
  - R1/R3: Psychosocial factors not implemented → added psychosocial_fit tags
  - R2/R3: Scalability concerns → modular dict structure supports easy extension
"""

CAREER_DATABASE = {
    # ── Original 6 careers (retained, lightly enhanced) ──────────────────────
    'teaching': {
        'domain': 'Online Home Tutor',
        'modules': [
            {'name': 'Create lesson plan', 'duration': 30},
            {'name': 'Learn classroom management', 'duration': 60},
            {'name': 'Design teaching materials', 'duration': 45},
            {'name': 'Record sample video', 'duration': 90},
            {'name': 'Join tutoring platform', 'duration': 60},
        ],
        'education_req': ['graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time', 'full-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['nurturing', 'communicative', 'patient'],
        'avg_monthly_income_inr': 15000,
        'peer_reviewed_source': 'Eidson (2024), Int. J. Economic & Mgmt Studies',
    },
    'cooking': {
        'domain': 'Food Content Creator',
        'modules': [
            {'name': 'Photography basics', 'duration': 60},
            {'name': 'Learn video editing basics', 'duration': 90},
            {'name': 'Cook & record recipe', 'duration': 120},
            {'name': 'Social media setup', 'duration': 45},
            {'name': 'Build content calendar', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['creative', 'expressive', 'self-motivated'],
        'avg_monthly_income_inr': 12000,
        'peer_reviewed_source': 'Howison et al. (2024), ACM Web Conf.',
    },
    'writing': {
        'domain': 'Content Writer',
        'modules': [
            {'name': 'SEO fundamentals', 'duration': 60},
            {'name': 'Learn copywriting', 'duration': 75},
            {'name': 'Write sample articles', 'duration': 90},
            {'name': 'Client communication basics', 'duration': 45},
            {'name': 'Create portfolio website', 'duration': 120},
        ],
        'education_req': ['graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time', 'full-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['analytical', 'detail-oriented', 'communicative'],
        'avg_monthly_income_inr': 18000,
        'peer_reviewed_source': 'Soni et al. (2025), arXiv',
    },
    'design': {
        'domain': 'Graphic Designer',
        'modules': [
            {'name': 'Design principles course', 'duration': 90},
            {'name': 'Color theory basics', 'duration': 60},
            {'name': 'Typography fundamentals', 'duration': 45},
            {'name': 'Learn Canva/Figma', 'duration': 120},
            {'name': 'Create portfolio pieces', 'duration': 150},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time', 'full-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['creative', 'aesthetic', 'self-motivated'],
        'avg_monthly_income_inr': 20000,
        'peer_reviewed_source': 'Alsaif et al. (2022), Computers, 11(11)',
    },
    'crafts': {
        'domain': 'Handmade Products Seller',
        'modules': [
            {'name': 'Product photography', 'duration': 60},
            {'name': 'Learn pricing strategies', 'duration': 45},
            {'name': 'Setup online store', 'duration': 90},
            {'name': 'Marketing on social media', 'duration': 75},
            {'name': 'Customer service basics', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['creative', 'entrepreneurial', 'patient'],
        'avg_monthly_income_inr': 10000,
        'peer_reviewed_source': 'Rahman (2023), Int. J. Academic Research in Business',
    },
    'fitness': {
        'domain': 'Online Fitness Coach',
        'modules': [
            {'name': 'Learn nutrition basics', 'duration': 120},
            {'name': 'Get certified online', 'duration': 180},
            {'name': 'Create workout plans', 'duration': 90},
            {'name': 'Build online presence', 'duration': 60},
            {'name': 'Client onboarding process', 'duration': 45},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['nurturing', 'energetic', 'communicative'],
        'avg_monthly_income_inr': 22000,
        'peer_reviewed_source': 'Howison et al. (2024), ACM Web Conf.',
    },

    # ── New 9 careers (added to address R3 scalability concern) ──────────────
    'data_entry': {
        'domain': 'Freelance Data Entry Specialist',
        'modules': [
            {'name': 'MS Excel / Google Sheets basics', 'duration': 60},
            {'name': 'Touch typing speed improvement', 'duration': 45},
            {'name': 'Data accuracy and validation', 'duration': 30},
            {'name': 'Freelance platform registration', 'duration': 30},
            {'name': 'First project walkthrough', 'duration': 45},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['detail-oriented', 'patient', 'analytical'],
        'avg_monthly_income_inr': 8000,
        'peer_reviewed_source': 'Deshpande et al. (2024), Int. J. Multidisciplinary Research',
    },
    'translation': {
        'domain': 'Freelance Translator / Transcriptionist',
        'modules': [
            {'name': 'Language proficiency assessment', 'duration': 45},
            {'name': 'Transcription tools (Otter, Rev)', 'duration': 60},
            {'name': 'CAT tools basics (OmegaT)', 'duration': 75},
            {'name': 'Build translation portfolio', 'duration': 90},
            {'name': 'Register on ProZ / Upwork', 'duration': 30},
        ],
        'education_req': ['graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time', 'full-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['communicative', 'detail-oriented', 'analytical'],
        'avg_monthly_income_inr': 16000,
        'peer_reviewed_source': 'Rubulnika (2024), Engineering for Rural Development',
    },
    'social_media': {
        'domain': 'Social Media Manager',
        'modules': [
            {'name': 'Platform algorithms overview', 'duration': 45},
            {'name': 'Content planning & scheduling', 'duration': 60},
            {'name': 'Canva for social graphics', 'duration': 60},
            {'name': 'Analytics and insights reading', 'duration': 45},
            {'name': 'Client pitch and onboarding', 'duration': 60},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['expressive', 'entrepreneurial', 'communicative'],
        'avg_monthly_income_inr': 14000,
        'peer_reviewed_source': 'Vineela et al. (2023), IJRASET',
    },
    'bookkeeping': {
        'domain': 'Home-Based Bookkeeper',
        'modules': [
            {'name': 'Basic accounting principles', 'duration': 90},
            {'name': 'Tally / QuickBooks basics', 'duration': 120},
            {'name': 'Invoice and payroll basics', 'duration': 60},
            {'name': 'GST filing overview', 'duration': 45},
            {'name': 'First client simulation', 'duration': 60},
        ],
        'education_req': ['graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time', 'full-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['analytical', 'detail-oriented', 'patient'],
        'avg_monthly_income_inr': 18000,
        'peer_reviewed_source': 'Burke (2002), User Modeling & User-Adapted Interaction',
    },
    'ecommerce': {
        'domain': 'E-Commerce Reseller',
        'modules': [
            {'name': 'Meesho / Amazon seller setup', 'duration': 45},
            {'name': 'Product sourcing strategies', 'duration': 60},
            {'name': 'Listing optimization', 'duration': 45},
            {'name': 'Order and inventory management', 'duration': 60},
            {'name': 'Customer returns handling', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['entrepreneurial', 'detail-oriented', 'self-motivated'],
        'avg_monthly_income_inr': 12000,
        'peer_reviewed_source': 'Rahman (2023), Int. J. Academic Research in Business',
    },
    'counseling': {
        'domain': 'Online Wellness / Counseling Guide',
        'modules': [
            {'name': 'Basic counseling skills course', 'duration': 120},
            {'name': 'Active listening techniques', 'duration': 60},
            {'name': 'Grief and stress management basics', 'duration': 90},
            {'name': 'Build a support community page', 'duration': 45},
            {'name': 'Ethical and boundary guidelines', 'duration': 60},
        ],
        'education_req': ['graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['nurturing', 'empathetic', 'patient'],
        'avg_monthly_income_inr': 20000,
        'peer_reviewed_source': 'Chen & Lappano (2023), Career Counselling for Mothers',
    },
    'photography': {
        'domain': 'Freelance Photographer / Photo Editor',
        'modules': [
            {'name': 'Smartphone photography masterclass', 'duration': 90},
            {'name': 'Lightroom / Snapseed editing', 'duration': 75},
            {'name': 'Building an Instagram portfolio', 'duration': 60},
            {'name': 'Pricing and client contracts', 'duration': 45},
            {'name': 'Upload to stock photo platforms', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['creative', 'aesthetic', 'expressive'],
        'avg_monthly_income_inr': 11000,
        'peer_reviewed_source': 'Howison et al. (2024), ACM Web Conf.',
    },
    'video_editing': {
        'domain': 'Freelance Video Editor',
        'modules': [
            {'name': 'DaVinci Resolve / CapCut basics', 'duration': 90},
            {'name': 'Transitions and color grading', 'duration': 75},
            {'name': 'Subtitling and audio sync', 'duration': 60},
            {'name': 'Build a YouTube/Reel demo reel', 'duration': 90},
            {'name': 'Freelance platform setup', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'intermediate',
        'psychosocial_fit': ['creative', 'detail-oriented', 'self-motivated'],
        'avg_monthly_income_inr': 17000,
        'peer_reviewed_source': 'Soni et al. (2025), arXiv',
    },
    'voice_over': {
        'domain': 'Voice-Over Artist',
        'modules': [
            {'name': 'Voice modulation basics', 'duration': 60},
            {'name': 'Home studio setup (low-cost)', 'duration': 45},
            {'name': 'Audacity audio editing', 'duration': 75},
            {'name': 'Build demo reel', 'duration': 90},
            {'name': 'Register on Voices.com / Fiverr', 'duration': 30},
        ],
        'education_req': ['high-school', 'graduate', 'postgraduate'],
        'work_types': ['remote', 'flexible', 'part-time'],
        'difficulty_level': 'beginner',
        'psychosocial_fit': ['expressive', 'communicative', 'creative'],
        'avg_monthly_income_inr': 13000,
        'peer_reviewed_source': 'Soni et al. (2025), arXiv',
    },
}


# ── Psychosocial Tag Registry ─────────────────────────────────────────────────
# Maps self-reported traits (collected in profile) to career psychosocial_fit tags.
# Addresses R1/R3 feedback: "claim of psychosocial factors not supported in implementation"
PSYCHOSOCIAL_TAG_REGISTRY = {
    'I enjoy helping others': ['nurturing', 'empathetic'],
    'I am creative': ['creative', 'aesthetic', 'expressive'],
    'I like working with numbers': ['analytical', 'detail-oriented'],
    'I prefer working independently': ['self-motivated', 'entrepreneurial'],
    'I am energetic and health-focused': ['energetic', 'nurturing'],
    'I am good at communication': ['communicative', 'expressive'],
    'I am patient and methodical': ['patient', 'detail-oriented'],
}


def get_psychosocial_score(user_tags, career_key):
    """
    Compute psychosocial alignment score between user self-reported traits and career fit.

    Args:
        user_tags (list): Tags derived from user's psychosocial responses
        career_key (str): Career database key

    Returns:
        float: Score between 0.0 and 1.0 (proportion of career tags matched)
    """
    if career_key not in CAREER_DATABASE:
        return 0.0
    career_tags = set(CAREER_DATABASE[career_key].get('psychosocial_fit', []))
    if not career_tags:
        return 0.0
    matched = len(set(user_tags) & career_tags)
    return round(matched / len(career_tags), 2)


def validate_career_database():
    """
    Validate the career database structure.

    Returns:
        tuple: (bool: is_valid, list: error_messages)
    """
    errors = []
    required_fields = ['domain', 'modules', 'education_req', 'work_types',
                        'difficulty_level', 'psychosocial_fit', 'avg_monthly_income_inr']
    valid_education = ['high-school', 'graduate', 'postgraduate']
    valid_work_types = ['remote', 'flexible', 'part-time', 'full-time']

    for career_key, career_data in CAREER_DATABASE.items():
        for field in required_fields:
            if field not in career_data:
                errors.append(f"{career_key}: Missing field '{field}'")

        if 'modules' in career_data:
            if not career_data['modules']:
                errors.append(f"{career_key}: modules list is empty")
            for idx, module in enumerate(career_data['modules']):
                if 'name' not in module:
                    errors.append(f"{career_key}: Module {idx} missing 'name'")
                if 'duration' not in module:
                    errors.append(f"{career_key}: Module {idx} missing 'duration'")
                elif module['duration'] <= 0:
                    errors.append(f"{career_key}: Module {idx} has invalid duration")

        for edu in career_data.get('education_req', []):
            if edu not in valid_education:
                errors.append(f"{career_key}: Invalid education '{edu}'")

        for wt in career_data.get('work_types', []):
            if wt not in valid_work_types:
                errors.append(f"{career_key}: Invalid work type '{wt}'")

    return (len(errors) == 0, errors)


def get_career_statistics():
    """
    Get statistics about the career database.

    Returns:
        dict: Summary statistics across all careers
    """
    total_careers = len(CAREER_DATABASE)
    total_modules = sum(len(c['modules']) for c in CAREER_DATABASE.values())
    total_duration = sum(
        sum(m['duration'] for m in c['modules']) for c in CAREER_DATABASE.values()
    )
    difficulty_dist = {}
    for c in CAREER_DATABASE.values():
        d = c.get('difficulty_level', 'unknown')
        difficulty_dist[d] = difficulty_dist.get(d, 0) + 1

    return {
        'total_careers': total_careers,
        'total_modules': total_modules,
        'avg_modules_per_career': round(total_modules / total_careers, 2),
        'total_duration_minutes': total_duration,
        'avg_duration_per_career_minutes': round(total_duration / total_careers, 2),
        'difficulty_distribution': difficulty_dist,
    }


# Validate on import
is_valid, validation_errors = validate_career_database()
if not is_valid:
    print("⚠️ Career Database Validation Warnings:")
    for error in validation_errors:
        print(f"  - {error}")
