"""
Profile Setup UI Component (v2)
Adds:
  - Psychosocial trait multi-select (addresses R1/R3 psychosocial implementation)
  - Confidence level slider
  - All 15 career interest options (addresses R3 scalability)
"""

import ipywidgets as widgets
from IPython.display import display, clear_output
from utils.helpers import create_header
from utils.validators import validate_profile
from config.career_database import PSYCHOSOCIAL_TAG_REGISTRY


def show_profile_setup(model, username, users_db, output_area):
    """
    Display profile setup page with psychosocial trait collection.

    Args:
        model: CareerBuddyModel instance
        username: Current username
        users_db: User database
        output_area: Output widget
    """
    create_header("📝 Profile Setup", f"Welcome, {username}! Let's build your career profile.")

    # ── Basic Profile Widgets ────────────────────────────────────────────────
    education = widgets.Dropdown(
        options=[
            ('Select your education', ''),
            ('High School', 'high-school'),
            ('Graduate', 'graduate'),
            ('Post Graduate', 'postgraduate'),
        ],
        description='Education:',
        style={'description_width': '160px'},
    )

    # All 15 career interests (expanded from original 6)
    interests = widgets.SelectMultiple(
        options=[
            'teaching', 'cooking', 'writing', 'design', 'crafts', 'fitness',
            'data_entry', 'translation', 'social_media', 'bookkeeping',
            'ecommerce', 'counseling', 'photography', 'video_editing', 'voice_over',
        ],
        description='Interests (hold Ctrl to select multiple):',
        style={'description_width': '160px'},
        layout=widgets.Layout(height='160px', width='500px'),
    )

    experience = widgets.Textarea(
        placeholder='e.g., Homemaker for 5 years, Part-time teacher',
        description='Experience:',
        style={'description_width': '160px'},
        layout=widgets.Layout(height='80px'),
    )

    time_availability = widgets.FloatSlider(
        value=2.0, min=0.5, max=8.0, step=0.5,
        description='Time (hrs/day):',
        style={'description_width': '160px'},
        readout_format='.1f',
    )

    work_preference = widgets.Dropdown(
        options=[
            ('Select preference', ''),
            ('Remote', 'remote'),
            ('Flexible Hours', 'flexible'),
            ('Part Time', 'part-time'),
            ('Full Time', 'full-time'),
        ],
        description='Work Preference:',
        style={'description_width': '160px'},
    )

    motivation = widgets.IntSlider(
        value=5, min=1, max=10,
        description='Motivation Level:',
        style={'description_width': '160px'},
    )

    # ── NEW: Psychosocial Trait Selection ────────────────────────────────────
    psych_label = widgets.HTML(
        "<h4 style='margin-top:20px;'>🧠 Tell us about yourself (select all that apply):</h4>"
        "<p style='color:#666; font-size:13px;'>These help us match careers to your personality.</p>"
    )
    psychosocial_traits = widgets.SelectMultiple(
        options=list(PSYCHOSOCIAL_TAG_REGISTRY.keys()),
        description='Your traits:',
        style={'description_width': '160px'},
        layout=widgets.Layout(height='150px', width='500px'),
    )

    # ── NEW: Confidence Level ────────────────────────────────────────────────
    confidence_label = widgets.HTML(
        "<h4 style='margin-top:15px;'>💪 How confident are you about starting something new?</h4>"
    )
    confidence_level = widgets.IntSlider(
        value=5, min=1, max=10,
        description='Confidence:',
        style={'description_width': '160px'},
    )
    confidence_hint = widgets.HTML(
        "<p style='color:#888; font-size:12px;'>1 = Very nervous &nbsp;|&nbsp; 5 = Neutral &nbsp;|&nbsp; 10 = Very confident</p>"
    )

    submit_btn = widgets.Button(
        description='Generate My Career Plan ✨',
        button_style='primary',
        icon='check',
        layout=widgets.Layout(width='250px', height='45px'),
    )

    logout_btn = widgets.Button(
        description='Logout',
        button_style='danger',
        icon='sign-out',
    )

    message_area = widgets.Output()

    def on_submit(b):
        with message_area:
            clear_output()

            # Derive psychosocial tags from selected trait statements
            selected_traits = list(psychosocial_traits.value)
            all_psych_tags = []
            for trait in selected_traits:
                all_psych_tags.extend(PSYCHOSOCIAL_TAG_REGISTRY.get(trait, []))
            unique_psych_tags = list(set(all_psych_tags))

            profile = {
                'education': education.value,
                'interests': list(interests.value),
                'experience': experience.value,
                'time_availability': time_availability.value,
                'work_preference': work_preference.value,
                'motivation_level': motivation.value,
                'psychosocial_tags': unique_psych_tags,     # NEW
                'confidence_level': confidence_level.value,  # NEW
            }

            valid, msg = validate_profile(profile)
            if not valid:
                print(f"❌ {msg}")
                return

            print("✅ Creating your personalized learning path...")
            print("🔍 Module 1: Mapping interests to careers...")
            print("📊 Module 2: Filtering and scoring with psychosocial alignment...")
            print("📅 Module 3: Generating balanced daily schedule...")

            agent = model.add_user(username, profile)

            print(f"\n✅ Success! Found {len(agent.recommended_careers)} matching career paths!")
            print(f"📚 Total: {agent.total_tasks} learning modules")
            print(f"📅 Duration: {agent.total_days} days")

            # Print scheduling quality metrics
            metrics = agent.get_scheduling_metrics()
            print(f"\n📈 Schedule Quality:")
            print(f"   Optimality Score : {metrics['scheduling_optimality_score']:.2%}")
            print(f"   Utilization Rate : {metrics['utilization_rate']:.2%}")

            # Print score breakdown for top career
            if agent.recommended_careers:
                top = agent.recommended_careers[0]
                print(f"\n🎯 Top Match: {top['career']['domain']} (Score: {top['score']:.3f})")
                bd = top['score_breakdown']
                print(f"   Education fit      : {bd['education']:.3f}")
                print(f"   Work-type fit      : {bd['work_type']:.3f}")
                print(f"   Time feasibility   : {bd['time_feasibility']:.3f}")
                print(f"   Psychosocial fit   : {bd['psychosocial_fit']:.3f}")
                print(f"   Difficulty fit     : {bd['difficulty_fit']:.3f}")

            print("\n🚀 Loading your dashboard...")

            import time
            time.sleep(1)

            with output_area:
                clear_output(wait=True)
                from ui.dashboard import show_dashboard
                show_dashboard(model, username, output_area)

    def on_logout(b):
        with output_area:
            clear_output(wait=True)
            from ui.auth import show_login_page
            show_login_page(model, users_db, output_area)

    submit_btn.on_click(on_submit)
    logout_btn.on_click(on_logout)

    form = widgets.VBox([
        education,
        interests,
        experience,
        time_availability,
        work_preference,
        motivation,
        psych_label,
        psychosocial_traits,
        confidence_label,
        confidence_level,
        confidence_hint,
        widgets.HBox([submit_btn, logout_btn]),
        message_area,
    ])

    display(form)