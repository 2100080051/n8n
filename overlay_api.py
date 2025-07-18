from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import os
from zipfile import ZipFile

app = Flask(__name__)

# Load and resize logo once
logo_url = "https://raw.githubusercontent.com/2100080051/logo/main/logo.png"
logo_response = requests.get(logo_url)
logo_img = Image.open(io.BytesIO(logo_response.content)).convert("RGBA")
logo_img = logo_img.resize((100, 100))  # Larger size

# Font
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TEXT = "Segura Invendors\nAI Agents & Automation"

@app.route('/add-overlay', methods=['POST'])
def add_overlay():
    images_json = request.get_json()
    image_files = []

    for idx, entry in enumerate(images_json):
        for item in entry['data']:
            image_url = item['url']
            try:
                response = requests.get(image_url)
                img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                
                # Create transparent layer
                overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)

                # Paste logo
                overlay.paste(logo_img, (20, 20), logo_img)

                # Draw text
                font_size = int(img.height * 0.035)
                font = ImageFont.truetype(FONT_PATH, font_size)
                text_position = (img.width - 450, img.height - 100)
                draw.text(text_position, TEXT, font=font, fill=(255, 255, 255, 255))

                # Combine image and overlay
                combined = Image.alpha_composite(img, overlay)

                # Save to BytesIO
                buf = io.BytesIO()
                combined.save(buf, format="PNG")
                buf.seek(0)
                image_files.append((f"image_{idx+1}.png", buf))
            except Exception as e:
                print(f"Error processing image: {e}")
    
    # Package all into ZIP
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for filename, img_bytes in image_files:
            zip_file.writestr(filename, img_bytes.read())
    zip_buffer.seek(0)

    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='branded_images.zip')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
