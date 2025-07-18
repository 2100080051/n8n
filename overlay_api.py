from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/overlay', methods=['POST'])
def overlay():
    base_url = request.json.get("base_url")
    logo_url = request.json.get("logo_url")
    text = request.json.get("text", "SeguraInvendors")

    # Load base image
    base_response = requests.get(base_url)
    base_img = Image.open(BytesIO(base_response.content)).convert("RGBA")

    # Load logo
    logo_response = requests.get(logo_url)
    logo_img = Image.open(BytesIO(logo_response.content)).convert("RGBA")

    # Resize logo
    logo_img = logo_img.resize((150, 150))

    # Paste logo (bottom-right)
    base_img.paste(logo_img, (base_img.width - 160, base_img.height - 160), logo_img)

    # Add text
    draw = ImageDraw.Draw(base_img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    draw.text((20, base_img.height - 60), text, fill="white", font=font)

    # Save to buffer
    output = BytesIO()
    base_img.save(output, format="PNG")
    output.seek(0)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

