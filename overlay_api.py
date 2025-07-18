from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['POST'])
def overlay_image():
    try:
        data = request.json
        image_url = data.get('image_url')
        logo_url = data.get('logo_url')
        text = data.get('text', '')

        # Fetch image and logo
        base_image = Image.open(BytesIO(requests.get(image_url).content)).convert("RGBA")
        logo_image = Image.open(BytesIO(requests.get(logo_url).content)).convert("RGBA")

        # Resize logo - make it larger
        logo_width = int(base_image.width * 0.15)
        logo_ratio = logo_width / logo_image.width
        logo_height = int(logo_image.height * logo_ratio)
        logo_image = logo_image.resize((logo_width, logo_height), Image.LANCZOS)

        # Paste logo at top-left corner
        base_image.paste(logo_image, (20, 20), logo_image)

        # Add text at bottom-right corner
        draw = ImageDraw.Draw(base_image)
        font_size = int(base_image.width * 0.04)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text_width, text_height = draw.textsize(text, font=font)
        x = base_image.width - text_width - 30
        y = base_image.height - text_height - 30
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))  # White text

        # Output
        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
