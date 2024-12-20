from flask import Flask, render_template, request

app = Flask(__name__)

# 假設的歌曲資料
songs = [
    {"title": "Song 1", "emotion": "joy", "score": 80},
    {"title": "Song 2", "emotion": "sadness", "score": 75},
    {"title": "Song 3", "emotion": "anger", "score": 85},
    {"title": "Song 4", "emotion": "fear", "score": 90},
]

# 主頁（顯示情緒標籤按鈕）
@app.route('/')
def home():
    emotions = ["joy", "sadness", "anger", "fear"]
    return render_template('index.html', emotions=emotions)

# 根據情緒顯示歌曲推薦
@app.route('/recommend')
def recommend():
    selected_emotion = request.args.get('emotion')
    if not selected_emotion:
        return "No emotion selected", 400

    # 篩選並排序歌曲
    filtered_songs = [song for song in songs if song['emotion'] == selected_emotion]
    filtered_songs.sort(key=lambda x: x['score'], reverse=True)

    return render_template('recommend.html', emotion=selected_emotion, songs=filtered_songs)

# 歌詞分析頁面
@app.route('/lyrics-analysis', methods=['GET', 'POST'])
def lyrics_analysis():
    if request.method == 'POST':
        lyrics = request.form.get('lyrics')
        if not lyrics:
            flash("請輸入歌詞進行分析！", "danger")
            return redirect(url_for('lyrics_analysis'))

        # 簡單的歌詞情緒分析邏輯
        if "sad" in lyrics:
            emotion = "sadness"
        elif "happy" in lyrics:
            emotion = "joy"
        elif "angry" in lyrics:
            emotion = "anger"
        elif "fear" in lyrics:
            emotion = "fear"
        else:
            emotion = "unknown"

        return render_template('lyrics_result.html', lyrics=lyrics, emotion=emotion)

    return render_template('lyrics_analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
