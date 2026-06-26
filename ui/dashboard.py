"""
Dashboard UI Component (v2)
Additions addressing reviewer feedback:
  - R1/R2: Scheduling quality metrics panel (optimality, utilization, variance)
  - R1/R2: User satisfaction rating widget (1-5 stars) for empirical data collection
  - R2:    Score breakdown per career (education, work, time, psychosocial, difficulty)
  - R3:    Difficulty level and income indicator per career card
"""

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from utils.helpers import create_header, create_progress_bar


def show_dashboard(model, username, output_area):
    """
    Display main CareerBuddy dashboard.

    Args:
        model: CareerBuddyModel instance
        username: Current username
        output_area: Output widget
    """
    agent = model.get_agent(username)
    if not agent:
        from ui.profile_setup import show_profile_setup
        show_profile_setup(model, username, {}, output_area)
        return

    create_header("📊 CareerBuddy Dashboard", f"Welcome back, {username}!")

    overall_progress = agent.get_progress()

    # ── Completion Banner ─────────────────────────────────────────────────────
    if overall_progress['percentage'] == 100:
        display(HTML("""
        <div style='background: linear-gradient(135deg, #4CAF50, #8BC34A);
                    padding: 20px; border-radius: 10px; text-align: center;
                    color: white; font-size: 18px; font-weight: bold; margin: 20px 0;'>
            🎉 Congratulations! You've completed all tasks!
        </div>
        """))
        cert_btn = widgets.Button(
            description='🎓 View Certificate', button_style='success', icon='trophy'
        )
        def on_cert_click(b):
            with output_area:
                clear_output(wait=True)
                from ui.completion import show_completion_page
                show_completion_page(model, username, output_area)
        cert_btn.on_click(on_cert_click)
        display(cert_btn)

    # ── Statistics Row ────────────────────────────────────────────────────────
    display(HTML("<h3>📈 Your Statistics</h3>"))
    display(widgets.HBox([
        widgets.HTML(f"""
        <div style='text-align:center; padding:20px; background:white;
                    border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,.1); margin:5px;'>
            <div style='font-size:30px;'>🎯</div>
            <div style='font-size:13px; color:#666; margin:8px 0;'>Career Paths</div>
            <div style='font-size:28px; font-weight:bold;'>{len(agent.recommended_careers)}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:20px; background:white;
                    border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,.1); margin:5px;'>
            <div style='font-size:30px;'>📅</div>
            <div style='font-size:13px; color:#666; margin:8px 0;'>Current Day</div>
            <div style='font-size:28px; font-weight:bold;'>{agent.current_day} / {agent.total_days}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:20px; background:white;
                    border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,.1); margin:5px;'>
            <div style='font-size:30px;'>✅</div>
            <div style='font-size:13px; color:#666; margin:8px 0;'>Progress</div>
            <div style='font-size:28px; font-weight:bold;'>{overall_progress['completed']} / {overall_progress['total']}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:20px; background:white;
                    border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,.1); margin:5px;'>
            <div style='font-size:30px;'>📊</div>
            <div style='font-size:13px; color:#666; margin:8px 0;'>Completion</div>
            <div style='font-size:28px; font-weight:bold;'>{overall_progress['percentage']:.1f}%</div>
        </div>"""),
    ]))

    create_progress_bar(overall_progress['percentage'], "Overall Progress")

    # ── NEW: Scheduling Quality Metrics Panel ─────────────────────────────────
    metrics = agent.get_scheduling_metrics()
    display(HTML("<h3>⚙️ Schedule Quality Metrics</h3>"))
    display(widgets.HBox([
        widgets.HTML(f"""
        <div style='text-align:center; padding:15px; background:#e8f5e9;
                    border-radius:10px; margin:5px; min-width:140px;'>
            <div style='font-size:22px;'>🎯</div>
            <div style='font-size:12px; color:#555; margin:5px 0;'>Optimality Score</div>
            <div style='font-size:22px; font-weight:bold; color:#2e7d32;'>
                {metrics['scheduling_optimality_score']:.0%}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:15px; background:#e3f2fd;
                    border-radius:10px; margin:5px; min-width:140px;'>
            <div style='font-size:22px;'>⚡</div>
            <div style='font-size:12px; color:#555; margin:5px 0;'>Utilization Rate</div>
            <div style='font-size:22px; font-weight:bold; color:#1565c0;'>
                {metrics['utilization_rate']:.0%}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:15px; background:#fff3e0;
                    border-radius:10px; margin:5px; min-width:140px;'>
            <div style='font-size:22px;'>📋</div>
            <div style='font-size:12px; color:#555; margin:5px 0;'>Avg Tasks/Day</div>
            <div style='font-size:22px; font-weight:bold; color:#e65100;'>
                {metrics['avg_tasks_per_day']}</div>
        </div>"""),
        widgets.HTML(f"""
        <div style='text-align:center; padding:15px; background:#f3e5f5;
                    border-radius:10px; margin:5px; min-width:140px;'>
            <div style='font-size:22px;'>📉</div>
            <div style='font-size:12px; color:#555; margin:5px 0;'>Load Variance</div>
            <div style='font-size:22px; font-weight:bold; color:#6a1b9a;'>
                {metrics['daily_load_variance']:.0f} min²</div>
        </div>"""),
    ]))

    # ── Motivation Banner ─────────────────────────────────────────────────────
    motivation = agent.get_motivation()
    display(HTML(f"""
    <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                padding:20px; border-radius:10px; text-align:center; color:white;
                font-size:18px; font-weight:bold; margin:20px 0;'>
        💡 {motivation}
    </div>
    """))

    # ── Career Paths with Score Breakdown ────────────────────────────────────
    display(HTML("<h3>📚 Your Career Paths</h3>"))
    for career_info in agent.recommended_careers:
        career = career_info['career']
        bd = career_info.get('score_breakdown', {})
        income = career.get('avg_monthly_income_inr', 0)
        difficulty = career_info.get('difficulty_level', '')

        breakdown_html = ""
        if bd:
            breakdown_html = f"""
            <details style='margin-top:8px;'>
              <summary style='cursor:pointer; color:#667eea; font-size:13px;'>
                  📊 Score Breakdown (Total: {career_info['score']:.3f} / 1.0)
              </summary>
              <div style='font-size:12px; color:#555; margin-top:6px; line-height:1.8;'>
                  Education fit: {bd.get('education',0):.3f} &nbsp;|&nbsp;
                  Work-type: {bd.get('work_type',0):.3f} &nbsp;|&nbsp;
                  Time: {bd.get('time_feasibility',0):.3f} &nbsp;|&nbsp;
                  Psychosocial: {bd.get('psychosocial_fit',0):.3f} &nbsp;|&nbsp;
                  Difficulty: {bd.get('difficulty_fit',0):.3f}
              </div>
            </details>"""

        display(HTML(f"""
        <div style='border-left:5px solid #4CAF50; padding:15px;
                    background:#f9f9f9; border-radius:5px; margin:10px 0;'>
            <h4 style='margin:0 0 8px 0;'>{career['domain']}</h4>
            <p style='margin:4px 0;'>📚 Modules: {len(career['modules'])} &nbsp;|&nbsp;
               📅 Est. Days: {career_info['estimated_days']} &nbsp;|&nbsp;
               🎚️ Level: {difficulty.capitalize()} &nbsp;|&nbsp;
               💰 ~₹{income:,}/month</p>
            {breakdown_html}
        </div>
        """))

    # ── NEW: User Satisfaction Rating ─────────────────────────────────────────
    display(HTML("""
    <div style='background:#fff8e1; border:1px solid #ffe082; padding:15px;
                border-radius:8px; margin:15px 0;'>
        <h4 style='margin:0 0 8px 0;'>⭐ How satisfied are you with your career recommendations?</h4>
        <p style='font-size:12px; color:#888; margin:0;'>Your feedback helps improve the system.</p>
    </div>
    """))
    satisfaction_slider = widgets.IntSlider(
        value=3, min=1, max=5, step=1,
        description='Satisfaction:',
        style={'description_width': '120px'},
    )
    satisfaction_labels = widgets.HTML(
        "<p style='font-size:12px; color:#888;'>1 = Very Unsatisfied &nbsp;|&nbsp; "
        "3 = Neutral &nbsp;|&nbsp; 5 = Very Satisfied</p>"
    )
    rate_btn = widgets.Button(description='Submit Rating', button_style='warning')
    rating_out = widgets.Output()

    def on_rate(b):
        with rating_out:
            clear_output()
            score = satisfaction_slider.value
            print(f"✅ Thank you! You rated your experience: {'⭐' * score} ({score}/5)")
            # In a real deployment this would write to a DB / analytics endpoint
            if hasattr(agent, '_satisfaction_scores'):
                agent._satisfaction_scores.append(score)
            else:
                agent._satisfaction_scores = [score]

    rate_btn.on_click(on_rate)
    display(widgets.VBox([satisfaction_slider, satisfaction_labels, rate_btn, rating_out]))

    # ── Day Schedule ──────────────────────────────────────────────────────────
    display(HTML(f"<h3>📅 Day {agent.current_day} Schedule</h3>"))

    prev_btn = widgets.Button(description='← Previous', disabled=(agent.current_day == 1))
    next_btn = widgets.Button(description='Next →', disabled=(agent.current_day == agent.total_days))
    refresh_btn = widgets.Button(description='🔄 Refresh', button_style='info')
    logout_btn = widgets.Button(description='Logout', button_style='danger')

    def on_prev(b):
        agent.current_day = max(1, agent.current_day - 1)
        with output_area:
            clear_output(wait=True)
            show_dashboard(model, username, output_area)

    def on_next(b):
        agent.current_day = min(agent.total_days, agent.current_day + 1)
        with output_area:
            clear_output(wait=True)
            show_dashboard(model, username, output_area)

    def on_refresh(b):
        with output_area:
            clear_output(wait=True)
            show_dashboard(model, username, output_area)

    def on_logout(b):
        with output_area:
            clear_output(wait=True)
            from ui.auth import show_login_page
            show_login_page(model, {}, output_area)

    prev_btn.on_click(on_prev)
    next_btn.on_click(on_next)
    refresh_btn.on_click(on_refresh)
    logout_btn.on_click(on_logout)

    display(widgets.HBox([prev_btn, next_btn, refresh_btn, logout_btn]))

    # ── Today's Tasks ─────────────────────────────────────────────────────────
    if agent.current_day <= len(agent.daily_schedule):
        today_schedule = agent.daily_schedule[agent.current_day - 1]
        today_completed = sum(
            1 for task in today_schedule['tasks']
            if agent.goal_based.progress.get(task['id'], False)
        )
        today_total = len(today_schedule['tasks'])
        today_pct = (today_completed / today_total * 100) if today_total > 0 else 0

        display(HTML(
            f"<p><strong>Today's Progress:</strong> {today_completed}/{today_total} "
            f"({today_pct:.0f}%)</p>"
        ))
        create_progress_bar(today_pct, "Today's Tasks")
        display(HTML("<h4>📝 Today's Tasks</h4>"))

        for task in today_schedule['tasks']:
            task_id = task['id']
            is_completed = agent.goal_based.progress.get(task_id, False)

            checkbox = widgets.Checkbox(value=is_completed, description='', indent=False)
            task_html = widgets.HTML(f"""
            <div style='padding:15px; margin:5px 0;
                        background:{"#d4edda" if is_completed else "white"};
                        border-left:4px solid {"#28a745" if is_completed else "#007bff"};
                        border-radius:5px;'>
                <h4 style='margin:0; {"text-decoration:line-through;" if is_completed else ""}'>{task['task']}</h4>
                <p style='margin:5px 0 0; color:#666;'>
                    📌 {task['career']} &nbsp;•&nbsp; ⏱️ {task['duration']} min
                </p>
            </div>
            """)

            def make_handler(tid):
                def handler(change):
                    if change['new']:
                        agent.complete_task(tid)
                    else:
                        agent.goal_based.progress[tid] = False
                    import time
                    time.sleep(0.3)
                    with output_area:
                        clear_output(wait=True)
                        show_dashboard(model, username, output_area)
                return handler

            checkbox.observe(make_handler(task_id), names='value')
            display(widgets.HBox([checkbox, task_html]))

        display(HTML(f"""
        <div style='background:#e3f2fd; padding:15px; border-radius:5px; margin-top:20px;'>
            <p style='margin:0;'><strong>⏱️ Total time today:</strong>
            {today_schedule['total_time']} minutes
            ({today_schedule['total_time']/60:.1f} hours)</p>
        </div>
        """))