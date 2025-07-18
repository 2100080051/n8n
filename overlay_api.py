    from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["POST"])
def overlay():
    try:
        data = request.get_json()

        image_url = data.get("image_url")
        logo_url = data.get("logo_url")
        overlay_text = data.get("text", "SeguraInvendors")

        if not image_url or not logo_url:
            return jsonify({"error": "Missing 'image_url' or 'logo_url'"}), 400

        # Download main image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content)).convert("RGBA")

        # Download logo
        logo_response = requests.get(logo_url)
        logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")

        # Resize logo to fit top-right (adjust size as needed)
        logo_size = (100, 100)
        logo = logo.resize(logo_size)

        # Paste logo at top-right corner
        image.paste(logo, (image.width - logo_size[0] - 10, 10), logo)

        # Draw text at bottom-left
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        text_position = (10, image.height - 30)
        draw.text(text_position, overlay_text, font=font, fill="white")

        # Save final image to a buffer (you can later return or save it)
        output_buffer = BytesIO()
        image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        # Just respond with success (you can change to return the image if needed)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
