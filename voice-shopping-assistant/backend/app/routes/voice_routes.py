from flask import Blueprint, request, jsonify
from app.nlp_processor import process_command
from app.voice_processor import transcribe_audio

bp = Blueprint('voice', __name__, url_prefix='/api/voice')

@bp.route('/process', methods=['POST'])
def process_voice_command():
    """Process voice command and extract intent"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        result = process_command(text)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/transcribe', methods=['POST'])
def transcribe():
    """Transcribe audio to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio file is required'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'en-US')
        
        audio_content = audio_file.read()
        result = transcribe_audio(audio_content, language)
        
        if result.get('error'):
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = {
        'en-US': 'English (US)',
        'en-GB': 'English (UK)',
        'es-ES': 'Spanish',
        'fr-FR': 'French',
        'de-DE': 'German',
        'it-IT': 'Italian',
        'ja-JP': 'Japanese',
        'zh-CN': 'Chinese (Mandarin)',
        'hi-IN': 'Hindi'
    }
    return jsonify({'languages': languages}), 200
