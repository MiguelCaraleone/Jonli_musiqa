from flask import Flask, request, send_file, jsonify
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    # Ovozni qabul qilish
    if 'audio' not in request.files:
        return jsonify({"error": "Ovoz topilmadi"}), 400
        
    audio_file = request.files['audio']
    genre = request.form.get('genre', 'default')
    
    user_voice_path = "temp_voice.webm"
    audio_file.save(user_voice_path)
    
    # Fon musiqasini tanlash (janrga qarab)
    # Sizda turli janrlar uchun musiqa fayllari bo'lishi kerak (masalan: o'zbek.mp3, pop.mp3)
    bg_music_path = f"backgrounds/{genre}.mp3" 
    
    # Agar o'sha janr uchun musiqa bo'lmasa, umumiy faylni ishlatish
    if not os.path.exists(bg_music_path):
        bg_music_path = "background.mp3"
    
    try:
        # Ovozni mp3 ga o'girish va qirqish (30 sekund)
        user_voice = AudioSegment.from_file(user_voice_path)
        user_voice = user_voice[:30000] 
        
        if os.path.exists(bg_music_path):
            bg = AudioSegment.from_file(bg_music_path)
            bg = bg[:30000] 
            bg = bg - 10 # Musiqa ovozini pasaytirish (foydalanuvchi ovozi eshitilishi uchun)
            
            # Birlashtirish
            final_audio = bg.overlay(user_voice)
        else:
            final_audio = user_voice
            
        output_path = "final_demo.mp3"
        final_audio.export(output_path, format="mp3")
        
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
