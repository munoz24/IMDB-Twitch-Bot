import threading
import socket
from imdbbot import imdbFunc, RepresentsFloat

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "" #TODO
PASS = "" #TODO

BOTNICK = "" #TODO
BOTPASS = "" #TODO

valid_genres = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "family",
                "fantasy", "film-Noir", "game-Show", "history", "horror", "music", "musical", "mystery", "news",
                "reality-tv", "romance", "sci-fi", "sport", "talk-show", "thriller", "war", "western"]


def bot():
    def send_message(message):
        botSock = socket.socket()
        botSock.connect((HOST, PORT))
        botSock.send(bytes("PASS " + BOTPASS + "\r\n", "UTF-8"))
        botSock.send(bytes("NICK " + BOTNICK + "\r\n", "UTF-8"))
        botSock.send(bytes("JOIN #" + NICK + "\r\n", "UTF-8"))
        botSock.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))

    def imdb_cmd_thread(cmd, user):
        check = False

        index = 1
        if len(cmd) > 2:
            if RepresentsFloat(cmd[2]):
                index = 3
            else:
                index = 2

        if index == 1:
            return send_message(user + ": You need to enter a genre!")

        for item in range(index, len(cmd)):
            if cmd[item].lower() not in valid_genres:
                return send_message(user + ": One or more genre was not valid!")
            else:
                check = True

        if check:
            gen = ""
            y = None
            if len(cmd) > 2:
                if RepresentsFloat(cmd[2]):
                    y = cmd[2]
                else:
                    gen = cmd[2]
                if len(cmd) > 3:
                    for g in cmd[3:]:
                        gen = gen + " " + g

            rate = cmd[1]
            if len(cmd[1].split('.')) != 1 and not RepresentsFloat(cmd[1].split('.')[1]):
                if '*' in cmd[1]:
                    rate = str(float(cmd[1].split('.')[0])) + '*'
                else:
                    rate = str(float(cmd[1].split('.')[0]))

            send_message(user + ": " + str(imdbFunc(rating=rate, genres=gen, top_or_bottom=None, year=y)))
        else:
            return send_message(user + ": Incorrect format. Check !imdbcommands for available formats")

    def t_or_b(user, value):
        send_message(user + ": " + str(imdbFunc(genres=None, rating=None, top_or_bottom=value, year=None)))

    print("Bot is Running")

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    sock.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    sock.send(bytes("JOIN #" + NICK + "\r\n", "UTF-8"))

    while True:
        line = str(sock.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:
        for line in str(sock.recv(1024)).split('\\r\\n'):

            parts = line.split(':')
            if len(parts) < 3:
                continue

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                msg = parts[2][:len(parts[2])]

            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            print(username + ": " + msg)

            commands = msg.split()
            if len(commands) >= 1:
                if commands[0] == "!imdb":
                    message_thread = threading.Thread(target=imdb_cmd_thread(cmd=commands, user=username))
                    message_thread.start()
                if commands[0] == "!top" or commands[0] == "!bottom":
                    message_thread = threading.Thread(target=t_or_b(user=username, value=commands[0][1:]))
                    message_thread.start()
