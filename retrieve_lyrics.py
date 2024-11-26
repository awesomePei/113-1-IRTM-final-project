import lyricsgenius
import os
token = ""  # 這裡放 token
genius = lyricsgenius.Genius(token)

# 清理 data
genius.skip_non_songs = True  # Skip non-song items like interviews
genius.excluded_terms = ["(Remix)", "(Live)"]  # Exclude certain song types
genius.remove_section_headers = True  # Clean up lyrics by removing headers

# Function to fetch and save all lyrics
def save_all_lyrics_by_artist(artist_name):
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Create the base 'lyrics' folder at the same level as the script
    base_directory = os.path.join(script_directory, "lyrics")
    
    # Create the artist's subdirectory inside the base directory
    artist_folder = os.path.join(base_directory, artist_name.replace(" ", "_"))
    os.makedirs(artist_folder, exist_ok=True)

    # Initialize the artist object with an unlimited max_songs
    artist = genius.search_artist(artist_name, max_songs=None)
    print(f"Fetched {len(artist.songs)} songs by {artist.name}.")

    # Save each song's lyrics into a separate file
    for song in artist.songs:
        # Sanitize file name to avoid invalid characters
        safe_title = "".join(c for c in song.title if c.isalnum() or c in " _-").strip()
        file_path = os.path.join(artist_folder, f"{safe_title}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"{song.title}\n\n{song.lyrics}")
        print(f"Saved lyrics of '{song.title}' to '{file_path}'.")

# 這邊要改歌手名
artist_name = "Alecia Beth Moore"  # Replace with your desired artist
save_all_lyrics_by_artist(artist_name)