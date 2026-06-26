"""
Certificate Generator with Image Export
"""

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont # Python Imaging Library = opening, manipulating, and saving image files
import io
import base64


def generate_certificate_image(username, career, save_path="certificate.png"):
    """
    Generate a professional certificate image
    
    Args:
        username (str): User's name
        career (str): Career domain
        save_path (str): Path to save certificate
        
    Returns:
        str: Path to saved certificate
    """
    # Create image with white background
    width, height = 1200, 800  # Canvas size in pixels
    img = Image.new('RGB', (width, height), color='white') # Background white
    draw = ImageDraw.Draw(img) # Object that allows drawing shapes & text
    
    # Draw border
    border_color = (76, 175, 80)  # Green color (RGB)
    # Outer thick border
    draw.rectangle([(20, 20), (width-20, height-20)], outline=border_color, width=10)
    # Inner thin border
    draw.rectangle([(30, 30), (width-30, height-30)], outline=border_color, width=3)
    
    # Draw decorative corner elements
    corner_size = 50
    # Top left
    draw.line([(40, 40), (40+corner_size, 40)], fill=border_color, width=5)
    draw.line([(40, 40), (40, 40+corner_size)], fill=border_color, width=5)
    # Top right
    draw.line([(width-40, 40), (width-40-corner_size, 40)], fill=border_color, width=5)
    draw.line([(width-40, 40), (width-40, 40+corner_size)], fill=border_color, width=5)
    # Bottom left
    draw.line([(40, height-40), (40+corner_size, height-40)], fill=border_color, width=5)
    draw.line([(40, height-40), (40, height-40-corner_size)], fill=border_color, width=5)
    # Bottom right
    draw.line([(width-40, height-40), (width-40-corner_size, height-40)], fill=border_color, width=5)
    draw.line([(width-40, height-40), (width-40, height-40-corner_size)], fill=border_color, width=5)
    
    # Try to use custom fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        career_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        career_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Title
    title = "🏆 CERTIFICATE OF COMPLETION"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0] # Centers horizontally using (width - text_width)/2
    draw.text(((width - title_width) / 2, 80), title, fill=(76, 175, 80), font=title_font)
    
    # Subtitle
    subtitle = "This certifies that"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) / 2, 180), subtitle, fill=(100, 100, 100), font=subtitle_font)
    
    # Username (centered, uppercase)
    username_upper = username.upper() # Converts the user’s name to uppercase for certificate styling
    name_bbox = draw.textbbox((0, 0), username_upper, font=name_font)
    name_width = name_bbox[2] - name_bbox[0] # Measures width for centering
    draw.text(((width - name_width) / 2, 240), username_upper, fill=(102, 126, 234), font=name_font)
    
    # Underline for name
    draw.line([((width - name_width) / 2, 330), ((width + name_width) / 2, 330)], fill=(102, 126, 234), width=3) # Draws a horizontal underline below the name.
    
    # Description
    desc = "has successfully completed the learning track:"
    desc_bbox = draw.textbbox((0, 0), desc, font=text_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    draw.text(((width - desc_width) / 2, 360), desc, fill=(100, 100, 100), font=text_font)
    
    # Career (highlighted box) - Creates a highlighted rounded rectangle area around the career name.
    career_bbox = draw.textbbox((0, 0), career, font=career_font)
    career_width = career_bbox[2] - career_bbox[0]
    box_padding = 20
    box_x = (width - career_width) / 2 - box_padding
    box_y = 420
    draw.rectangle([(box_x, box_y), (box_x + career_width + 2*box_padding, box_y + 60)], 
                   fill=(240, 240, 240), outline=(76, 175, 80), width=2)
    draw.text(((width - career_width) / 2, box_y + 10), career, fill=(51, 51, 51), font=career_font)
    
    # Date section
    date_text = f"Awarded on {datetime.now().strftime('%B %d, %Y')}"
    date_bbox = draw.textbbox((0, 0), date_text, font=text_font)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text(((width - date_width) / 2, 550), date_text, fill=(100, 100, 100), font=text_font)
    
    # Signature section
    signature_line_y = 650
    draw.line([(width - 350, signature_line_y), (width - 100, signature_line_y)], fill=(0, 0, 0), width=2)
    
    # Signature text (stylized)
    signature = "CareerBuddy Team"
    sig_bbox = draw.textbbox((0, 0), signature, font=text_font)
    sig_width = sig_bbox[2] - sig_bbox[0]
    draw.text(((width - 350 + (250 - sig_width) / 2), signature_line_y + 10), 
              signature, fill=(51, 51, 51), font=text_font)
    
    # Title under signature
    sig_title = "Director of Education"
    sig_title_bbox = draw.textbbox((0, 0), sig_title, font=small_font)
    sig_title_width = sig_title_bbox[2] - sig_title_bbox[0]
    draw.text(((width - 350 + (250 - sig_title_width) / 2), signature_line_y + 45), 
              sig_title, fill=(120, 120, 120), font=small_font)
    
    # Quote at bottom - Motivational quote placed at the bottom.
    quote = '"Excellence is not a destination; it is a continuous journey."'
    quote_bbox = draw.textbbox((0, 0), quote, font=small_font)
    quote_width = quote_bbox[2] - quote_bbox[0]
    draw.text(((width - quote_width) / 2, height - 80), quote, fill=(76, 175, 80), font=small_font)
    
    # Save certificate
    img.save(save_path, 'PNG', quality=95)
    
    return save_path


def image_to_base64(image_path):
    """Convert image to base64 for display in HTML"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8') # Convert the binary image data to a str of base 64 ; convert the str of bse 64 to utf8