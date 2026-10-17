from flask import Flask, render_template, request, send_file
from wsd import analyze_sentence, analyze_all_ambiguous_words
import csv
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    sentence = ""
    target_word = ""
    mode = "single"
    if request.method == "POST":
        sentence = request.form.get("sentence", "").strip()
        target_word = request.form.get("target_word", "").strip()
        mode = request.form.get("mode", "single")
        if not sentence:
            result = {"error": "Please enter a sentence."}
        else:
            try:
                if mode == "all":
                    result = {"mode": "all", **analyze_all_ambiguous_words(sentence)}
                elif not target_word:
                    result = {"error": "Please enter a target word for single-word analysis."}
                else:
                    result = {"mode": "single", **analyze_sentence(sentence, target_word)}
            except RuntimeError as exc:
                result = {"error": str(exc)}
    return render_template("index.html", result=result, sentence=sentence, target_word=target_word, mode=mode)

@app.route("/download", methods=["POST"])
def download():
    sentence = request.form.get("sentence", "").strip()
    target_word = request.form.get("target_word", "").strip()
    mode = request.form.get("mode", "single")
    try:
        if mode == "all":
            data = analyze_all_ambiguous_words(sentence).get("results", [])
        else:
            one = analyze_sentence(sentence, target_word)
            data = [one] if not one.get("error") else []
    except RuntimeError as exc:
        return str(exc), 400
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Sentence", "Target Word", "Predicted Sense", "Prediction Definition", "Candidate Sense", "Candidate Definition", "Part of Speech", "Examples"])
    for item in data:
        pred = item.get("predicted") or {}
        for sense in item.get("senses", []):
            writer.writerow([sentence, item.get("target_word", ""), pred.get("name", ""), pred.get("definition", ""), sense["name"], sense["definition"], sense["part_of_speech"], " | ".join(sense["examples"])])
    output = io.BytesIO(buffer.getvalue().encode("utf-8-sig"))
    output.seek(0)
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="wsd_results.csv")

if __name__ == "__main__":
    app.run(debug=True)
