"""
Completion Certificate UI Component
Displays completion certificate and next steps
"""

import ipywidgets as widgets # Import widgets for interactive UI elements in Jupyter
from IPython.display import display, clear_output, HTML # Import display functions and HTML rendering
from utils.helpers import create_header # Custom helper functions (like headers)
from utils.certificate import generate_certificate_image, image_to_base64 # Certificate generation utilities
from datetime import datetime # Import datetime to show award date
import os # To handle file paths and saving files


def show_completion_page(model, username, output_area):
    """
    Display completion certificate page with downloadable image
    This function creates and displays a Completion Certificate page after the user finishes their learning program in CareerBuddy.
    Args:
        model: CareerBuddyModel instance
        username: Current username
        output_area: Output widget for dynamic content
    """
    agent = model.get_agent(username)  # Get the user's agent/profile from the model
    if not agent: # If user not found, exit function
        return
    
    # Get primary career domain from recommended careers
    # agent.recommended_careers = [{"career": {"domain": "Graphic Designer", "modules": [...]}},{"career": {"domain": "Handmade Products Seller",modules": [...]}},]
    # Fetch user profile & their top recommended career to display on certificate
    career_name = agent.recommended_careers[0]['career']['domain'] if agent.recommended_careers else "Career Path"

    # Display page header - Shows a nice visual banner saying “Congratulations!”
    create_header("🎉 Congratulations!", "You've completed your learning journey!")
    
    # Define path to save the certificate image
    cert_path = f"{username}_certificate.png"
    try:
        # Generate a certificate image for the user
        generate_certificate_image(username, career_name, cert_path)
        # Convert the image to base64 for HTML embedding
        cert_base64 = image_to_base64(cert_path)
        
        # display() - Renders and displays an object in a Jupyter notebook cell
        # Display the certificate image in the notebook
        display(HTML(f"""
        <div style='text-align: center; margin: 30px 0;'>
            <img src='data:image/png;base64,{cert_base64}' 
                 style='max-width: 100%; border: 5px solid #4CAF50; border-radius: 15px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);' />
        </div>
        """))
        # Flag to indicate certificate image exists
        cert_exists = True
    except Exception as e:
        # Handle image generation errors
        print(f"⚠️ Could not generate certificate image: {e}")
        print("Displaying text certificate instead...")
        cert_exists = False
        
        # Fallback: Display certificate as HTML content
        display(HTML(f"""
        <div style='border: 8px solid #4CAF50; padding: 60px; border-radius: 15px; 
                    text-align: center; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    margin: 30px 0; box-shadow: 0 10px 40px rgba(0,0,0,0.3);'>
            <div style='background: white; padding: 40px; border-radius: 10px;'>
                <h1 style='color: #4CAF50; font-size: 48px; margin: 0 0 20px 0;'>🏆 Certificate of Completion</h1>
                <p style='font-size: 24px; color: #666; margin: 10px 0;'>This certifies that</p>
                <h2 style='color: #667eea; font-size: 56px; font-weight: bold; margin: 20px 0; 
                           text-transform: uppercase;'>{username}</h2>
                <p style='font-size: 24px; color: #666; margin: 10px 0;'>has successfully completed:</p>
                <h3 style='color: #333; font-size: 36px; font-weight: bold; margin: 30px 0; 
                           padding: 20px; background: #f0f0f0; border-radius: 10px;'>{career_name}</h3>
                <div style='margin-top: 50px; padding-top: 30px; border-top: 3px solid #4CAF50;'>
                    <p style='color: #888; font-size: 18px;'>Awarded on</p>
                    <p style='color: #333; font-size: 22px; font-weight: bold;'>{datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
        </div>
        """))
    
    # If certificate image exists, add download button
    if cert_exists:
        download_btn = widgets.Button(
            description='📥 Download Certificate',
            button_style='success',
            icon='download',
            layout=widgets.Layout(width='250px', height='50px')
        )
        
        def on_download(b):
            try:
                # Trigger download via JavaScript in Jupyter
                display(HTML(f"""
                <script>
                var link = document.createElement('a');
                link.href = 'data:image/png;base64,{cert_base64}';
                link.download = '{username}_certificate.png';
                link.click();
                </script>
                """))
                # Inform user
                print(f"✅ Certificate downloaded as '{username}_certificate.png'")
                print(f"📁 Also saved in current directory: {os.path.abspath(cert_path)}")
            except Exception as e:
                # Handle download errors
                print(f"⚠️ Download failed: {e}")
                print(f"📁 Certificate saved at: {os.path.abspath(cert_path)}")

         # Attach click handler to button
        download_btn.on_click(on_download)
        # Display download button
        display(download_btn)
    
    # Display user's progress statistics
    progress = agent.get_progress()
    display(HTML("<h3 style='margin-top: 30px;'>📊 Your Achievement Statistics</h3>"))
    # Total tasks completed
    display(widgets.HBox([
        widgets.HTML(f"""
        <div style='text-align: center; padding: 20px; background:#e3f2fd;
                    border-radius: 10px; margin:5px; flex:1;'>
            <div style='font-size: 26px;'>📚</div>
            <div style='font-size: 14px; color:#555;'>Total Tasks</div>
            <div style='font-size: 32px; font-weight:bold; color:#2196F3;'>{progress['total']}</div>
        </div>
        """),
         # Total days invested
        widgets.HTML(f"""
        <div style='text-align: center; padding: 20px; background:#e8f5e9;
                    border-radius: 10px; margin:5px; flex:1;'>
            <div style='font-size: 26px;'>📅</div>
            <div style='font-size: 14px; color:#555;'>Days Invested</div>
            <div style='font-size: 32px; font-weight:bold; color:#4CAF50;'>{agent.total_days}</div>
        </div>
        """),
        # Number of recommended career paths
        widgets.HTML(f"""
        <div style='text-align: center; padding: 20px; background:#f3e5f5;
                    border-radius: 10px; margin:5px; flex:1;'>
            <div style='font-size: 26px;'>🎯</div>
            <div style='font-size: 14px; color:#555;'>Career Paths</div>
            <div style='font-size: 32px; font-weight:bold; color:#9C27B0;'>{len(agent.recommended_careers)}</div>
        </div>
        """)
    ]))
    
     
    display(HTML("""
        <div style='background:#fff3cd; border-left: 5px solid #ffc107;
                    padding:20px; border-radius:5px; margin-top:30px;'>
            <h3>🚀 Next Steps - Ready To Launch Your Career!</h3>
            <ul style='line-height:1.9;'>
                <li><strong>Build Your Portfolio:</strong> Showcase real projects</li>
                <li><strong>Network:</strong> Join professional communities</li>
                <li><strong>Apply for roles:</strong> Start job hunting</li>
                <li><strong>Keep Learning:</strong> Stay up-to-date with trends</li>
                <li><strong>Get Certified:</strong> Additional credentials boost your profile</li>
            </ul>
        </div>
    """))
    
    # Action buttons: Dashboard, LinkedIn Guide, Share
    dashboard_btn = widgets.Button(description='← Back to Dashboard', button_style='info')
    linkedin_btn = widgets.Button(description='💼 LinkedIn Guide', button_style='success')
    share_btn = widgets.Button(description='🔗 Share on LinkedIn', button_style='primary')

     # Dashboard button click handler
    def on_dashboard(b):
        with output_area:
            clear_output(wait=True) # clear_output(wait=True)
            from ui.dashboard import show_dashboard
            show_dashboard(model, username, output_area)
    
    def on_linkedin(b):
        with output_area:
            clear_output(wait=True) # wait=True ensures the output is cleared before new output is displayed.
            from ui.linkedin_guide import show_linkedin_guide
            show_linkedin_guide(model, username, output_area)
    
    def on_share(b):
        # Create LinkedIn share text based on careers
        # careers → ['Graphic Designer', 'Handmade Products Seller']
        careers = [c['career']['domain'] for c in agent.recommended_careers]
        share_text = f"Excited to share that I've completed my learning journey in {' and '.join(careers)}! 🎉" 
        
        # Open LinkedIn share URL 
        import webbrowser
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://careerbuddy.com"
        
        try:
            webbrowser.open(linkedin_url)
            print("✅ Opening LinkedIn... Share your achievement!")
            print(f"\n📝 Suggested post:\n{share_text}")
            # Fallback: display share text and URL
        except:
            print(f"📝 Copy this to share on LinkedIn:\n\n{share_text}")
            print(f"\n🔗 LinkedIn Share: {linkedin_url}")

      # Attach handlers to buttons - execute when the button is clicked
    dashboard_btn.on_click(on_dashboard)
    linkedin_btn.on_click(on_linkedin)
    share_btn.on_click(on_share)

    # Display action buttons in a horizontal layout - arranges child widgets horizontally in a row.
    display(widgets.HBox([dashboard_btn, linkedin_btn, share_btn]))