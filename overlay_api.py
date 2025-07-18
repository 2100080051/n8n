from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Overlay API is live 🚀"}), 200

@app.route("/overlay", methods=["POST"])
def overlay():
    data = request.get_json()

    image_url = data.get("image_url")
    logo_url = data.get("logo_url")
    text = data.get("text", "")

    if not image_url or not logo_url:
        return jsonify({"error": "Missing image_url or logo_url"}), 400

    try:
        # Download base image and logo
        image = Image.open(BytesIO(requests.get(image_url).content))

        logo_response = requests.get(logo_url)

        image = Image.open(BytesIO(image_response.content)).convert("RGBA")
        logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")

        # Resize logo
        logo = logo.resize((100, 100))

        # Paste logo at bottom-right corner
        image.paste(logo, (image.width - 110, image.height - 110), logo)

        # Add white text at bottom-left
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, image.height - 30), text, fill="white", font=font)

        # Output image
        output = BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
