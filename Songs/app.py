import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

def load_songs(lyrics_folder, csv_file):
    songs = []
    # 讀取情緒分類的 CSV 檔案
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        emotion_map = {row[0]: row[1] for row in reader}

    # 讀取 lyrics 資料夾中的歌詞檔案
    for filename in os.listdir(lyrics_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(lyrics_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) < 2:
                    continue
                title = lines[0].strip()  # 第一行是歌名
                lyrics = ''.join(lines[1:]).strip()  # 剩下的是歌詞
                emotion = emotion_map.get(filename.split('.')[0], 'unknown')  # 根據檔名查詢情緒
                # 添加歌曲資訊到列表
                songs.append({
                    "id": filename.split('.')[0],  # 唯一 ID，使用檔名
                    "title": title,
                    "lyrics": lyrics,
                    "emotion": emotion,
                })
    return songs


# # 假設的歌曲資料
# songs = [
#     {"title": "Song 1", "emotion": "joy", "score": 80},
#     {"title": "Song 2", "emotion": "sadness", "score": 75},
#     {"title": "Song 3", "emotion": "anger", "score": 85},
#     {"title": "Song 4", "emotion": "fear", "score": 90},
# ]

# 設定資料路徑
LYRICS_FOLDER = '/Users/cindychang/Documents/school/大三/IRTM/PA4/data'  # 歌詞資料夾路徑
CSV_FILE = '/Users/cindychang/Documents/school/大三/IRTM/PA3/output.csv'  # CSV 檔案路徑

# 載入歌曲資料
songs = load_songs(LYRICS_FOLDER, CSV_FILE)

# 主頁（顯示情緒標籤按鈕）
@app.route('/')
def home():
    # 獲取所有唯一的情緒分類
    emotions = list(set(song['emotion'] for song in songs))
    return render_template('index.html', emotions=emotions)

# 根據情緒顯示歌曲推薦
@app.route('/recommend')
def recommend():
    selected_emotion = request.args.get('emotion')
    if not selected_emotion:
        return "No emotion selected", 400

    # 篩選並排序歌曲
    filtered_songs = [song for song in songs if song['emotion'] == selected_emotion]
    filtered_songs.sort(key=lambda x: len(x['lyrics']), reverse=True)  # 按歌詞長度排序作為示例

    return render_template('recommend.html', emotion=selected_emotion, songs=filtered_songs)

@app.route('/song/<song_id>')
def song_details(song_id):
    # 查找符合的歌曲
    song = next((s for s in songs if str(s.get('id')) == song_id), None)
    if not song:
        return "歌曲不存在", 404

    # 傳遞歌曲詳細資訊給模板
    return render_template('songs.html', song=song)


# # 主頁（顯示情緒標籤按鈕）
# @app.route('/')
# def home():
#     emotions = ["joy", "sadness", "anger", "fear"]
#     return render_template('index.html', emotions=emotions)

# # 根據情緒顯示歌曲推薦
# @app.route('/recommend')
# def recommend():
#     selected_emotion = request.args.get('emotion')
#     if not selected_emotion:
#         return "No emotion selected", 400

#     # 篩選並排序歌曲
#     filtered_songs = [song for song in songs if song['emotion'] == selected_emotion]
#     filtered_songs.sort(key=lambda x: x['score'], reverse=True)

#     return render_template('recommend.html', emotion=selected_emotion, songs=filtered_songs)

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
