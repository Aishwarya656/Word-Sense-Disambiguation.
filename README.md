# Word Sense Disambiguation using NLP and WordNet

A Flask web application that uses WordNet to display candidate meanings and NLTK's simplified Lesk algorithm as an educational WSD baseline.

## Features
- Single target-word analysis.
- Auto-detect and analyze multiple distinct words with multiple WordNet senses.
- Candidate sense inventory with definitions, examples, lemmas/synonyms, and hypernyms.
- Summary statistics for sentence length and analyzed ambiguous-word candidates.
- CSV export for single-word or multi-word analysis.
- Example sentence buttons and responsive interface.
- Report template with a test-case table.

## Setup (Windows, Python 3.12 recommended)
```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m nltk.downloader wordnet omw-1.4
python app.py
```
Open http://127.0.0.1:5000.

If the `venv` already exists, activate it instead of creating it again. Run commands from the folder containing `app.py` and `requirements.txt`.

## Limitations
Simplified Lesk is a baseline and may predict an incorrect sense. The multi-word mode finds words with multiple WordNet entries, which does not guarantee each word is ambiguous in the sentence. Test and report actual results rather than claiming perfect accuracy.
