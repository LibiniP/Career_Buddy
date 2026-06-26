"""
Helper utility functions
"""

from IPython.display import display, HTML


def create_header(title, subtitle=""):
    """Create styled header"""
    html = f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>{title}</h1>
        {f"<p style='color: white; margin: 10px 0 0 0;'>{subtitle}</p>" if subtitle else ""}
    </div>
    """
    display(HTML(html))


def create_card(title, content, color="#4CAF50"):
    """Create styled card"""
    html = f"""
    <div style='border-left: 5px solid {color}; padding: 15px; 
                background: #f9f9f9; border-radius: 5px; margin: 10px 0;'>
        <h3 style='margin: 0 0 10px 0; color: {color};'>{title}</h3>
        <div>{content}</div>
    </div>
    """
    display(HTML(html))


def create_progress_bar(percentage, label="Progress"):
    """Create progress bar"""
    html = f"""
    <div style='margin: 20px 0;'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
            <span><strong>{label}</strong></span>
            <span><strong>{percentage:.1f}%</strong></span>
        </div>
        <div style='width: 100%; background: #e0e0e0; border-radius: 10px; height: 25px;'>
            <div style='width: {percentage}%; background: linear-gradient(90deg, #4CAF50, #8BC34A); 
                        height: 100%; border-radius: 10px; transition: width 0.3s;'></div>
        </div>
    </div>
    """
    display(HTML(html))


def create_metric(label, value, icon="📊"):
    """Create metric display"""
    html = f"""
    <div style='text-align: center; padding: 20px; background: white; 
                border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <div style='font-size: 30px;'>{icon}</div>
        <div style='font-size: 14px; color: #666; margin: 10px 0;'>{label}</div>
        <div style='font-size: 28px; font-weight: bold; color: #333;'>{value}</div>
    </div>
    """
    display(HTML(html))