""" flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops, ImageStat

app = Flask(__name__)

# Handle GET request (e.g., from browser visit)
@app.route('/', methods=['GET'])
def index():
    return "Flask image overlay API is running. Use POST with image_url, logo_url, and text."

# Handle POST request to overlay logo and text
@app.route('/', methods=['POST'])
def overlay_logo_and_text():
    try:
        data = request.json
        image_url = data.get('image_url')
        logo_url = data.get('logo_url')
        overlay_text = data.get('text')

        if not image_url or not logo_url or not overlay_text:
            return jsonify({'error': 'Missing image_url, logo_url or text'}), 400

        # Download main image
        image_response = requests.get(image_url)
        if not image_response.ok:
            return jsonify({'error': 'Failed to download main image'}), 400

        try:
            base_image = Image.open(BytesIO(image_response.content)).convert("RGBA")
        except Exception as e:
            return jsonify({'error': 'Main image could not be processed'}), 500

        # Download logo
        logo_response = requests.get(logo_url)
        if not logo_response.ok:
            return jsonify({'error': 'Failed to download logo image'}), 400

        try:
            logo_image = Image.open(BytesIO(logo_response.content)).convert("RGBA")
        except Exception as e:
            return jsonify({'error': 'Logo image could not be processed'}), 500

        # Resize logo to 10% of image width
        logo_width = int(base_image.width * 0.1)
        logo_ratio = logo_width / logo_image.width
        logo_height = int(logo_image.height * logo_ratio)
        logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # Paste logo (top-left corner with 20px padding)
        base_image.paste(logo_image, (20, 20), logo_image)

        # Draw text (bottom-right corner with custom size and alignment)
        draw = ImageDraw.Draw(base_image)
        font_size = int(base_image.height * 0.035)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(overlay_text, font=font)
        text_position = (base_image.width - text_width - 40, base_image.height - text_height - 40)

        draw.text(text_position, overlay_text, font=font, fill=(255, 255, 255, 255))

        # Save result in memory
        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        return app.response_class(output.getvalue(), mimetype='image/png')

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)"""


"""from flask import Flask, request, jsonify
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

        if not image_url or not logo_url or not overlay_text:
            return jsonify({'error': 'Missing image_url, logo_url or text'}), 400

        # Download main image
        image_response = requests.get(image_url)
        if not image_response.ok:
            return jsonify({'error': 'Failed to download main image'}), 400
        base_image = Image.open(BytesIO(image_response.content)).convert("RGBA")

        # Download logo
        logo_response = requests.get(logo_url)
        if not logo_response.ok:
            return jsonify({'error': 'Failed to download logo image'}), 400
        logo_image = Image.open(BytesIO(logo_response.content)).convert("RGBA")

        # Resize logo (10% of image width)
        logo_width = int(base_image.width * 0.1)
        logo_ratio = logo_width / logo_image.width
        logo_height = int(logo_image.height * logo_ratio)
        logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # Paste logo (top-left corner with 20px padding)
        base_image.paste(logo_image, (20, 20), logo_image)

        # Add text (bottom-right corner)
        draw = ImageDraw.Draw(base_image)
        font_size = int(base_image.width * 0.03)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Get bounding box of text
        text_bbox = draw.textbbox((0, 0), overlay_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_position = (
            base_image.width - text_width - 20,
            base_image.height - text_height - 20
        )

        draw.text(text_position, overlay_text, font=font, fill=(255, 255, 255, 255))

        # Save to memory
        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        return app.response_class(output.getvalue(), mimetype='image/png')

    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)"""

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

        if not image_url or not logo_url or not overlay_text:
            return jsonify({'error': 'Missing image_url, logo_url or text'}), 400

        image_response = requests.get(image_url)
        if not image_response.ok:
            return jsonify({'error': 'Failed to download main image'}), 400

        base_image = Image.open(BytesIO(image_response.content)).convert("RGBA")

        logo_response = requests.get(logo_url)
        if not logo_response.ok:
            return jsonify({'error': 'Failed to download logo image'}), 400

        logo_image = Image.open(BytesIO(logo_response.content)).convert("RGBA")

        # Resize logo (larger than before)
        logo_image.thumbnail((160, 160))  # Increased from 100x100

        # Paste logo at top-left corner
        base_image.paste(logo_image, (20, 20), logo_image)

        # Add overlay text at bottom-right
        draw = ImageDraw.Draw(base_image)

        # Dynamically scale font size based on image width
        font_size = int(base_image.width * 0.035)  # Larger than before
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Text position (bottom-right corner with padding)
        text_width, text_height = draw.textbbox((0, 0), overlay_text, font=font)[2:]
        text_position = (base_image.width - text_width - 20, base_image.height - text_height - 20)
        draw.text(text_position, overlay_text, font=font, fill=(255, 255, 255, 255))

        # Save to memory
        output = BytesIO()
        base_image.save(output, format='PNG')
        output.seek(0)

        return app.response_class(output.getvalue(), mimetype='image/png')

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)


