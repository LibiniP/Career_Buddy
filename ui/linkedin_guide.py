"""
LinkedIn Profile Optimization Guide
"""

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from utils.helpers import create_header
from datetime import datetime


def show_linkedin_guide(model, username, output_area):
    """
    Display LinkedIn optimization guide
    
    Args:
        model: CareerBuddyModel instance
        username: Current username
        output_area: Output widget for dynamic content
    """
    # Retrieve agent object for this user (contains recommended careers, schedule, progress etc.)
    agent = model.get_agent(username)

    # Display page header using custom function
    create_header("💼 LinkedIn Profile Optimization Guide", "Boost your professional presence")

    # Extract list of career domains from recommended careers
    careers = [c['career']['domain'] for c in agent.recommended_careers]
    headline = " | ".join(careers)  # Creates a single string combining all career domains, separated by " | "
    
    # Headline 
    display(HTML("<h3>1️⃣ Update Your Headline</h3>"))
    display(HTML("<p>Your headline appears below your name and is crucial for visibility.</p>"))
    # Text input widget prefilled with generated headline
    headline_widget = widgets.Text(
        value=headline,
        description='Headline:',
        layout=widgets.Layout(width='100%'), # Specifies layout properties for widgets, like width, height, margin, flex
        style={'description_width': '100px'}
    )
    display(headline_widget)
    
    # Summary
    display(HTML("<h3>2️⃣ Craft Your About Section</h3>")) # Auto-generated summary text using program values from agent
    summary = f"""Motivated professional with newly acquired skills in {', '.join(careers)}.

Successfully completed comprehensive training covering {agent.total_tasks} learning modules across {agent.total_days} days of dedicated practice.

Passionate about leveraging these skills to create value and drive results. Ready to contribute to innovative projects and collaborate with forward-thinking teams.

Key areas of expertise:
{chr(10).join('• ' + career for career in careers)}

Let's connect and explore opportunities!"""
    
    summary_widget = widgets.Textarea(
        value=summary,
        description='Summary:',
        layout=widgets.Layout(width='100%', height='200px'),
        style={'description_width': '100px'}
    )
    display(summary_widget)
    
    # Skills
    display(HTML("<h3>3️⃣ Add Your Skills</h3>"))
    display(HTML("<p>Add these skills to increase your profile visibility:</p>"))
    
    skills_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;'>"
    all_skills = careers.copy()
    for career_info in agent.recommended_careers:
        for module in career_info['career']['modules']:
            skill = module['name'].replace('Learn ', '').replace('Create ', '').replace('Build ', '').replace('Record ', '')
            if skill not in all_skills:
                all_skills.append(skill)
    
    for skill in all_skills[:15]:
        skills_html += f"<span style='background: #4CAF50; color: white; padding: 8px 16px; border-radius: 20px; font-size: 14px;'>{skill}</span>"
    skills_html += "</div>"
    display(HTML(skills_html))
    
    # Certifications
    display(HTML("<h3>4️⃣ Add Certifications</h3>"))
    for career_info in agent.recommended_careers:
        display(HTML(f"""
        <div style='background: #f9f9f9; padding: 15px; border-left: 4px solid #4CAF50; 
                    margin: 10px 0; border-radius: 5px;'>
            <p style='margin: 0; font-weight: bold; font-size: 16px;'>{career_info['career']['domain']} - CareerBuddy Certification</p>
            <p style='margin: 5px 0; color: #666;'>Issued by: CareerBuddy AI Learning Platform</p>
            <p style='margin: 5px 0; color: #666;'>Issue Date: {datetime.now().strftime('%B %Y')}</p>
            <p style='margin: 5px 0; color: #666;'>Skills: {len(career_info['career']['modules'])} modules completed</p>
        </div>
        """))
    
    # Post template
    display(HTML("<h3>5️⃣ Share Your Achievement</h3>"))
    post_text = f"""🎉 Excited to share that I've completed my learning journey in {' and '.join(careers)}!

Through {agent.total_days} days of focused learning and {agent.total_tasks} practical modules, I've gained hands-on experience in:
{chr(10).join('✓ ' + career for career in careers)}

Ready to apply these skills and contribute to meaningful projects. Open to opportunities and collaborations!

#CareerDevelopment #NewSkills #Learning #ProfessionalGrowth #{careers[0].replace(' ', '')}"""
    
    post_widget = widgets.Textarea(
        value=post_text,
        description='LinkedIn Post:',
        layout=widgets.Layout(width='100%', height='180px'),
        style={'description_width': '120px'}
    )
    display(post_widget)
    
    share_btn = widgets.Button(description='📢 Share on LinkedIn', button_style='primary', icon='share')
    def share_linkedin(b):
        import webbrowser
        linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=https://careerbuddy.com"
        try:
            webbrowser.open(linkedin_url)
            print("✅ Opening LinkedIn share dialog...")
        except:
            print(f"🔗 LinkedIn Share URL: {linkedin_url}")
            print(f"📝 Copy the post text above to share!")
    share_btn.on_click(share_linkedin)
    display(share_btn)
    
    # Job search resources
    display(HTML("<h3>6️⃣ Job Search Resources</h3>"))
    for career_info in agent.recommended_careers:
        display(HTML(f"""
        <div style='background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #ddd;'>
            <h4 style='margin-top: 0; color: #667eea;'>{career_info['career']['domain']}</h4>
            <p style='margin: 5px 0;'><strong>Recommended Platforms:</strong></p>
            <ul style='margin: 5px 0; padding-left: 20px;'>
                <li>LinkedIn Jobs - Search: "{career_info['career']['domain']}"</li>
                <li>Indeed.com - Filter by Remote/Flexible</li>
                <li>Upwork/Fiverr - Start with freelance projects</li>
                <li>AngelList - For startup opportunities</li>
                <li>Remote.co - Remote-only positions</li>
            </ul>
        </div>
        """))
    
    # Action buttons
    back_btn = widgets.Button(description='← Back to Certificate', button_style='info')
    dashboard_btn = widgets.Button(description='🏠 Dashboard', button_style='warning')
    
    def on_back(b):
        with output_area:
            clear_output(wait=True)
            from ui.completion import show_completion_page
            show_completion_page(model, username, output_area)
    
    def on_dashboard(b):
        with output_area:
            clear_output(wait=True)
            from ui.dashboard import show_dashboard
            show_dashboard(model, username, output_area)
    
    back_btn.on_click(on_back)
    dashboard_btn.on_click(on_dashboard)
    
    display(widgets.HBox([back_btn, dashboard_btn]))