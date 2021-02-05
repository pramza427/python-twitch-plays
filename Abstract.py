from datetime import datetime
from tkinter import *
import socket
import re

# server and port that we will be connecting to in order to get twitch chat
server = 'irc.chat.twitch.tv'
port = 6667
# set the bots nickname
nickname = 'botfrank'
# requires user to retrieve their own stream token
token = 'oauth:'
# user must choose a twitch.tv channel that they want to take chat from
# channel name should be in the format '#name'
channel = '#'
# list of possible colors that python can display
COLORS = ['green', 'gainsboro', 'old lace',
          'linen', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
          'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
          'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
          'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
          'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
          'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
          'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
          'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
          'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
          'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
          'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red',
          'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
          'thistle', 'snow2', 'snow3',
          'snow4', 'seashell2', 'seashell3', 'seashell4', 'antiquewhite', 'antiquewhite2',
          'antiquewhite3', 'antiquewhite4', 'bisque2', 'bisque3', 'bisque4', 'peachpuff2',
          'peachpuff3', 'peachpuff4', 'navajowhite2', 'navajowhite3', 'navajowhite4',
          'lemonchiffon2', 'lemonchiffon3', 'lemonchiffon4', 'cornsilk2', 'cornsilk3',
          'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
          'lavenderblush2', 'lavenderblush3', 'lavenderblush4', 'mistyrose2', 'mistyrose3',
          'mistyrose4', 'azure2', 'azure3', 'azure4', 'slateblue', 'slateblue2', 'slateblue3',
          'slateblue4', 'royalblue', 'royalblue2', 'royalblue3', 'royalblue4', 'blue2', 'blue4',
          'dodgerblue2', 'dodgerblue3', 'dodgerblue4', 'steelblue', 'steelblue2',
          'steelblue3', 'steelblue4', 'deepskyblue2', 'deepskyblue3', 'deepskyblue4',
          'skyblue', 'skyblue2', 'skyblue3', 'skyblue4', 'lightskyblue', 'lightskyblue2',
          'lightskyblue3', 'lightskyblue4', 'slategray', 'slategray2', 'slategray3',
          'slategray4', 'lightsteelblue', 'lightsteelblue2', 'lightsteelblue3',
          'lightsteelblue4', 'lightblue', 'lightblue2', 'lightblue3', 'lightblue4',
          'lightcyan2', 'lightcyan3', 'lightcyan4', 'paleturquoise', 'paleturquoise2',
          'paleturquoise3', 'paleturquoise4', 'cadetblue', 'cadetblue2', 'cadetblue3',
          'cadetblue4', 'turquoise', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
          'cyan4', 'darkslategray', 'darkslategray2', 'darkslategray3', 'darkslategray4',
          'aquamarine2', 'aquamarine4', 'darkseagreen', 'darkseagreen2', 'darkseagreen3',
          'darkseagreen4', 'seagreen', 'seagreen2', 'seagreen3', 'palegreen', 'palegreen2',
          'palegreen3', 'palegreen4', 'springgreen2', 'springgreen3', 'springgreen4',
          'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
          'olivedrab', 'olivedrab2', 'olivedrab4', 'darkolivegreen', 'darkolivegreen2',
          'darkolivegreen3', 'darkolivegreen4', 'khaki', 'khaki2', 'khaki3', 'khaki4',
          'lightgoldenrod', 'lightgoldenrod2', 'lightgoldenrod3', 'lightgoldenrod4',
          'lightyellow2', 'lightyellow3', 'lightyellow4', 'yellow2', 'yellow3', 'yellow4',
          'gold2', 'gold3', 'gold4', 'goldenrod', 'goldenrod2', 'goldenrod3', 'goldenrod4',
          'darkgoldenrod', 'darkgoldenrod2', 'darkgoldenrod3', 'darkgoldenrod4',
          'rosybrown', 'rosybrown2', 'rosybrown3', 'rosybrown4', 'indianred', 'indianred2',
          'indianred3', 'indianred4', 'sienna', 'sienna2', 'sienna3', 'sienna4', 'burlywood',
          'burlywood2', 'burlywood3', 'burlywood4', 'wheat', 'wheat2', 'wheat3', 'wheat4', 'tan',
          'tan2', 'tan4', 'chocolate', 'chocolate2', 'chocolate3', 'firebrick', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown', 'brown2', 'brown3', 'brown4', 'salmon', 'salmon2',
          'salmon3', 'salmon4', 'lightsalmon2', 'lightsalmon3', 'lightsalmon4', 'orange2',
          'orange3', 'orange4', 'darkorange', 'darkorange2', 'darkorange3', 'darkorange4',
          'coral', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'orangered2',
          'orangered3', 'orangered4', 'red2', 'red3', 'red4', 'deeppink2', 'deeppink3', 'deeppink4',
          'hotpink', 'hotpink2', 'hotpink3', 'hotpink4', 'pink', 'pink2', 'pink3', 'pink4',
          'lightpink', 'lightpink2', 'lightpink3', 'lightpink4', 'palevioletred',
          'palevioletred2', 'palevioletred3', 'palevioletred4', 'maroon', 'maroon2',
          'maroon3', 'maroon4', 'violetred', 'violetred2', 'violetred3', 'violetred4',
          'magenta2', 'magenta3', 'magenta4', 'orchid', 'orchid2', 'orchid3', 'orchid4', 'plum',
          'plum2', 'plum3', 'plum4', 'mediumorchid', 'mediumorchid2', 'mediumorchid3',
          'mediumorchid4', 'darkorchid', 'darkorchid2', 'darkorchid3', 'darkorchid4',
          'purple', 'purple2', 'purple3', 'purple4', 'mediumpurple', 'mediumpurple2',
          'mediumpurple3', 'mediumpurple4', 'thistle', 'thistle2', 'thistle3', 'thistle4',
          'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
          'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
          'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
          'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
          'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
          'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
          'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
          'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
          'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
          'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
          'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

# create a socket, connect, and send our info
sock = socket.socket()

sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

# create a canvas using tkinter
master = Tk()

canvas_width = 1000
canvas_height = 1000
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()


# function for creating triangles, since it is a bit more complicated than the others
def draw_triangle(a, b, c, d, e):
    tri_points = [(a*42) % canvas_width, (b*73) % canvas_height,
              (c*94) % canvas_width, (len(d) * 62) % canvas_height,
              (len(e) * 83) % canvas_width, (len(e) * 38) % canvas_height]
    w.create_polygon(tri_points, outline=COLORS[a], fill=COLORS[a], width=1)


# while sock is not null collect the twitch chat one message at a time
while sock:
    resp = sock.recv(2048).decode('utf-8')
    # collect time metadata and append it to the message
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H:%M:%S - ")
    newresp = current_time + resp
    inArr = newresp.split(' - ')

    try:
        # extract the time, chatter name, chatter message, and channel name
        # from the formatted string we received
        hour, minute, second = re.search('20.*-.*-.*_(.*):(.*):(.*)', inArr[0]).groups()
        print(hour + minute + second)
        hour = int(hour)
        minute = int(minute)
        second = int(second)

        name, channel, message = re.search(":(.*)!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)", inArr[1]).groups()
        print(name + channel + message)

        # based on the second the message was sent, an arc, triangle, oval, or rectangle
        # will be drawn on screen. Color depends on message length.
        if second % 4 == 1:
            points = [(second*55) % canvas_width, (len(name)*77) % canvas_height,
                      (len(message)*33) % canvas_width, (minute*49) % canvas_height]
            w.create_arc(points, outline=COLORS[len(message)], fill=COLORS[len(message)])
        elif second % 4 == 2:
            draw_triangle(second, minute, hour, name, message)
        elif second % 4 == 3:
            w.create_oval((second*minute*23) % canvas_width, (second*hour*42) % canvas_height,  # x1, y1
                          (second*minute*23 + len(name)*len(channel)*12) % canvas_width,  # x2
                          (second*hour*42+len(message)*15) % canvas_height,  # y2
                          outline=COLORS[len(message)], fill=COLORS[len(message)])  # fill and outline
        elif second % 4 == 0:
            w.create_rectangle((second*hour*18) % canvas_width, (minute*len(name)*24) % canvas_height,
                               (len(name)*len(channel) + minute*24) % canvas_width,
                               (len(message)*second*57) % canvas_height,
                               outline=COLORS[len(message)], fill=COLORS[len(message)])
        # update the canvas
        master.update()

    except Exception:
        pass
