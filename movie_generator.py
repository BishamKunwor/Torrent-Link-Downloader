import requests
from random import randint
import os  # This helps to create folders from python program
import shutil  # This module removes a folder which contains multiple files

main_directory = "Movies_List"  # Root Directory Name

movie_count = requests.get(
    'https://yts.mx/api/v2/list_movies.json').json()['data']['movie_count']  # Gets total movies in server of yts.mx

# Execution of main program starts from this function


def generate_movies():
    user_input = int(
        input("Enter total no of movies you want to recieve: ")) + 1
    writing_into_file(user_input)
    print(" ____                      _                 _ \n|  _ \\  _____      ___ __ | | ___   __ _  __| |\n| | | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |\n| |_| | (_) \\ V  V /| | | | | (_) | (_| | (_| |\n|____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\n                                               \n  ____                      _      _           _ \n / ___|___  _ __ ___  _ __ | | ___| |_ ___  __| |\n| |   / _ \\| '_ ` _ \\| '_ \\| |/ _ \\ __/ _ \\/ _` |\n| |__| (_) | | | | | | |_) | |  __/ ||  __/ (_| |\n \\____\\___/|_| |_| |_| .__/|_|\\___|\\__\\___|\\__,_|\n                     |_|                         \n")


def writing_into_file(user_input):

    global movie_count, main_directory
    movie_count /= 20
    movie_count = int(movie_count)

    try:
        os.makedirs(main_directory)
    except:
        # Removes non-empty folder by shutil
        shutil.rmtree(main_directory)
        os.makedirs(main_directory)

    print(" ____  _             _   _             \n/ ___|| |_ __ _ _ __| |_(_)_ __   __ _ \n\\___ \\| __/ _` | '__| __| | '_ \\ / _` |\n ___) | || (_| | |  | |_| | | | | (_| |\n|____/ \\__\\__,_|_|   \\__|_|_| |_|\\__, |\n                                 |___/ \n ____                      _                 _ \n|  _ \\  _____      ___ __ | | ___   __ _  __| |\n| | | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |\n| |_| | (_) \\ V  V /| | | | | (_) | (_| | (_| |\n|____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\n                                               \n")

    written_movie_count = 1

    while True:

        # Stops while loop if user input equals to total files created
        if written_movie_count == user_input:
            break

        head = {"page": randint(1, movie_count)}
        r = requests.get('https://yts.mx/api/v2/list_movies.json',
                         params=head).json()['data']['movies']

        unexpected_token = False
        for movie in r:
            movie_directory_name = f".\\{main_directory}\\{movie['title']} ({str(movie['year'])})"
            if written_movie_count == user_input:
                break

            checker = ('?', ':', '/', '\\', '*', '<', '>', '|', '"')
            for char in movie['title']:
                if char in checker:
                    unexpected_token = True

            if unexpected_token:
                unexpected_token = False
                continue

            try:
                os.makedirs(movie_directory_name)
            except:
                continue

            print(
                f"....................Downloading movie {written_movie_count}....................")

            with open(f"{movie_directory_name}\\Additional Information.txt", "w") as movie_info_file:
                movie_info_file.write(
                    f"Title: {movie['title']}\nReleased Year: {movie['year']}\nRatings: {movie['rating']}\nLanguage: {movie['language']}\n")

                summary = movie['summary'].split(". ")
                summary = ".\n         ".join(summary)

                movie_info_file.write(
                    f"Summary: {summary}\n\n<---- Details for Download ---->\n\n")

                with open(f"{movie_directory_name}\\cover.jpg", 'wb') as image:
                    image.write(requests.get(
                        movie['large_cover_image']).content)

                for download in movie['torrents']:
                    with open(f"{movie_directory_name}\\{movie['title']} [{download['quality']}]  [{download['size']}]  S[{download['seeds']}]  P[{download['peers']}].torrent", 'wb') as torrent:
                        torrent.write(requests.get(
                            download['url']).content)
                    movie_info_file.write(
                        f"Quality: {download['quality']}\nType: {download['type']}\nSeeders: {download['seeds']}\nPeers: {download['peers']}\nSize: {download['size']}\nDownload Link: {download['url']}\n\n")

            written_movie_count += 1


def main():
    generate_movies()


if __name__ == "__main__":
    main()
