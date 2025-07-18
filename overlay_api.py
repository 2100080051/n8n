from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])

def overlay_logo_and_text():
    try:
        data = request.json
        image_url = data.get('image_url')
        logo_url = data.get('logo_url')
        overlay_text = data.get('text')

        # Validate inputs
        if not image_url or not logo_url or not overlay_text:
            return jsonify({'error': 'Missing image_url, logo_url or text'}), 400

        # Download main image
        image_response = requests.get(image_url)
        if not image_response.ok:
            return jsonify({'error': 'Failed to download main image'}), 400

        try:
            base_image = Image.open(BytesIO(image_response.content)).convert("RGBA")
        except Exception as e:
            print("Failed to open base image")
            print("Headers:", image_response.headers)
            print("Content (first 200 bytes):", image_response.content[:200])
            return jsonify({'error': 'Main image could not be processed'}), 500

        # Download logo
        logo_response = requests.get(logo_url)
        if not logo_response.ok:
            return jsonify({'error': 'Failed to download logo image'}), 400

        try:
            logo_image = Image.open(BytesIO(logo_response.content)).convert("RGBA")
        except Exception as e:
            print("Failed to open logo image")
            print("Headers:", logo_response.headers)
            print("Content (first 200 bytes):", logo_response.content[:200])
            return jsonify({'error': 'Logo image could not be processed'}), 500

        # Resize logo dynamically (10% of base image width)
        logo_width = int(base_image.width * 0.1)
        logo_height = int(logo_image.height * (logo_width / logo_image.width))
        logo_image = logo_image.resize((logo_width, logo_height), Image.ANTIALIAS)

        # Paste logo (top-left corner with padding)
        padding = 20
        base_image.paste(logo_image, (padding, padding), logo_image)

        # Add text (bottom-right corner)
        draw = ImageDraw.Draw(base_image)

        # Use truetype font with size proportional to image width
        try:
            font_size = max(20, int(base_image.width * 0.035))  # Min 20pt
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(overlay_text, font=font)
        text_x = base_image.width - text_width - padding
        text_y = base_image.height - text_height - padding

        draw.text((text_x, text_y), overlay_text, font=font, fill=(255, 255, 255, 255))

        # Save to memory
        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        return app.response_class(output.getvalue(), mimetype='image/png')

    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
