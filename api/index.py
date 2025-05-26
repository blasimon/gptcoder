from flask import Flask, request, render_template, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pandas as pd
import io
import os
import openai

app = Flask(__name__, template_folder="../templates")

# Set up Flask-Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["30 per minute"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form["api_key"]
        model = request.form["model"]
        temp = float(request.form["temperature"])
        max_tokens = int(request.form["max_tokens"])
        prompt_template = request.form["instructions"]
        file = request.files["file"]

        df = pd.read_csv(file)
        if len(df) > 3001:
            return "Too many rows. Please upload a file with 3000 rows or fewer.", 400

        column = request.form["column_to_code"]
        if column not in df.columns:
            return f"Column '{column}' not found in CSV.", 400
        results = []
        client = openai.OpenAI(api_key=api_key)

        for i, row in df.iterrows():
            prompt = f"{prompt_template}\n{row[column]}"
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temp,
                    max_tokens=max_tokens,
                    timeout=20
                )
                output = response.choices[0].message.content
            except Exception as e:
                output = f"Error: {str(e)}"
            results.append(output)

        df["GPT_Response"] = results
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv",
                         as_attachment=True, download_name="coded_output.csv")

    return render_template("form.html")


# New POST route `/code` to handle AJAX-based GPT requests.
@app.route("/code", methods=["POST"])
@limiter.limit("10 per minute")
def code_api():
    data = request.get_json()
    prompt = data.get("prompt")
    model = data.get("model")
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 100)
    api_key = data.get("api_key")

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=20
        )
        output = response.choices[0].message.content
        return {"response": output}
    except Exception as e:
        return {"error": str(e)}, 500