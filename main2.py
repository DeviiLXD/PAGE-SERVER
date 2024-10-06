from flask import Flask, request, render_template_string
import requests
import re
import time
import threading
from requests.exceptions import RequestException

app = Flask(__name__)

class FacebookCommenter:
    def __init__(self):
        self.comment_count = 0

    def comment_on_post(self, cookie, post_id, comment, delay):
        try:
            with requests.Session() as r:
                r.headers.update({
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'sec-fetch-site': 'none',
                    'accept-language': 'id,en;q=0.9',
                    'Host': 'mbasic.facebook.com',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-encoding': 'gzip, deflate',
                    'sec-fetch-mode': 'navigate',
                    'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.166 Mobile Safari/537.36',
                    'connection': 'keep-alive',
                })

                response = r.get(f'https://mbasic.facebook.com/{post_id}', cookies={"cookie": cookie})

                next_action_match = re.search('method="post" action="([^"]+)"', response.text)
                if next_action_match:
                    next_action = next_action_match.group(1).replace('amp;', '')
                else:
                    print("<Error> Next action not found")
                    return

                fb_dtsg_match = re.search('name="fb_dtsg" value="([^"]+)"', response.text)
                if fb_dtsg_match:
                    fb_dtsg = fb_dtsg_match.group(1)
                else:
                    print("<Error> fb_dtsg not found")
                    return

                jazoest_match = re.search('name="jazoest" value="([^"]+)"', response.text)
                if jazoest_match:
                    jazoest = jazoest_match.group(1)
                else:
                    print("<Error> jazoest not found")
                    return

                data = {
                    'fb_dtsg': fb_dtsg,
                    'jazoest': jazoest,
                    'comment_text': comment,
                    'comment': 'Submit',
                }

                r.headers.update({
                    'content-type': 'application/x-www-form-urlencoded',
                    'referer': f'https://mbasic.facebook.com/{post_id}',
                    'origin': 'https://mbasic.facebook.com',
                })

                response2 = r.post(f'https://mbasic.facebook.com{next_action}', data=data, cookies={"cookie": cookie})

                if 'comment_success' in str(response2.url) and response2.status_code == 200:
                    self.comment_count += 1
                    print(f"[{self.comment_count}] Comment successfully posted: {comment}")
                else:
                    print(f"Failed to post comment: {comment}, URL: {response2.url}, Status Code: {response2.status_code}")

        except RequestException as e:
            print(f"<Error> RequestException: {str(e).lower()}")
        except Exception as e:
            print(f"<Error> Exception: {str(e).lower()}")
        except KeyboardInterrupt:
            print("<Error> Process interrupted by user")

    def handle_inputs(self, cookie_file, post_id, kidx_name, comment_file, delay):
        try:
            # Read cookies and comments as text
            your_cookies = cookie_file.read().decode('utf-8').splitlines()
            comments = comment_file.read().decode('utf-8').splitlines()

            if len(your_cookies) == 0:
                print("<Error> The cookies file is empty")
                return

            cookie_index = 0  # Start with the first cookie

            for comment in comments:
                comment = kidx_name + ' ' + comment.strip()
                if comment:
                    time.sleep(delay)
                    self.comment_on_post(your_cookies[cookie_index], post_id, comment, delay)
                    cookie_index = (cookie_index + 1) % len(your_cookies)  # Cycle through cookies
        except RequestException as e:
            print(f"<Error> RequestException: {str(e).lower()}")
        except Exception as e:
            print(f"<Error> Exception: {str(e).lower()}")
        except KeyboardInterrupt:
            print("<Error> Process interrupted by user")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cookies_file = request.files['cookies_file']
        post_id = request.form['post_id']
        kidx_name = request.form['kidx_name']
        comment_file = request.files['comment_file']
        delay = int(request.form['delay'])

        commenter = FacebookCommenter()
        threading.Thread(target=commenter.handle_inputs, args=(cookies_file, post_id, kidx_name, comment_file, delay)).start()

        return "Commenting started. Check the console for details."

    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>OffLiNe PosT SeRveR </title>
        </head>
        <body>
            <h1>OffLiNe PosT SeRveR </h1>
            <form method="POST" enctype="multipart/form-data">
                <label>Post ID:</label><br>
                <input type="text" name="post_id" required><br><br>

                <label>Kidx Name:</label><br>
                <input type="text" name="kidx_name" required><br><br>

                <label>Cookies File:</label><br>
                <input type="file" name="cookies_file" required><br><br>

                <label>Comments File:</label><br>
                <input type="file" name="comment_file" required><br><br>

                <label>Delay (in seconds):</label><br>
                <input type="text" name="delay" required><br><br>

                <input type="submit" value="Start Commenting">
            </form>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
