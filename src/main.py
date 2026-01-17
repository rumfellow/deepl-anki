from flask import Flask, render_template, request, jsonify
import deepl
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Configure your DeepL API key here
DEEPL_API_KEY = os.environ.get('DEEPL_API_KEY', 'your-api-key-here')
translator = deepl.Translator(DEEPL_API_KEY)

# File to store translations
TRANSLATIONS_FILE = 'translations.tsv'

def save_translation(word, translation, source_lang='ES', target_lang='EN'):
    """Save the word and translation to a TSV file for Anki import"""
    with open(TRANSLATIONS_FILE, 'a', encoding='utf-8') as tsvfile:
        tsvfile.write(f"{word}\t{translation}\n")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """Translate a word using DeepL API"""
    data = request.get_json()
    word = data.get('word', '').strip()
    source_lang = data.get('source_lang', 'ES')
    target_lang = data.get('target_lang', 'EN')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    try:
        # Translate using DeepL
        result = translator.translate_text(
            word, 
            source_lang=source_lang,
            target_lang=target_lang
        )
        translation = result.text
        
        # Save to disk
        save_translation(word, translation, source_lang, target_lang)
        
        return jsonify({
            'word': word,
            'translation': translation,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """Get translation history"""
    if not os.path.isfile(TRANSLATIONS_FILE):
        return jsonify([])
    
    translations = []
    with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as tsvfile:
        for line in tsvfile:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    translations.append({
                        'word': parts[0],
                        'translation': parts[1]
                    })
    
    return jsonify(translations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
