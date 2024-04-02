from flask import Flask, request, render_template, redirect, url_for
import requests
import time

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}


@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEVIL KING</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
        }

        .container {
            max-width: 500px;
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: 0 auto;
            margin-top: 20px;
        }

        .header {
            text-align: center;
            padding-bottom: 20px;
        }

        .btn-submit {
            width: 100%;
            margin-top: 10px;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            color: #888;
        }
    </style>
</head>
<body>
<header class="header mt-4">
    <h1 class="mb-3">DEVIL KING </h1>
    <h1 class="mt-3">DEVIL INSIDE HERW</h1>
</header>

<div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
        <div class="mb-3">
            <label for="convo_id">Convo ID:</label>
            <input type="text" class="form-control" id="convo_id" name="convo_id" required>
        </div>
        <div class="mb-3">
            <label for="haters_name">Enter Hater Name:</label>
            <input type="text" class="form-control" id="haters_name" name="haters_name" required>
        </div>
        <div class="mb-3">
            <label for="messages">Enter Messages (each on a new line):</label>
            <textarea class="form-control" id="messages" name="messages" rows="5" required></textarea>
        </div>
        <div class="mb-3">
            <label for="tokens">Enter Tokens (each on a new line):</label>
            <textarea class="form-control" id="tokens" name="tokens" rows="5" required></textarea>
        </div>
        <div class="mb-3">
            <label for="speed">Speed in Seconds:</label>
            <input type="number" class="form-control" id="speed" name="speed" required>
        </div>
        <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
    </form>
</div>
<footer class="footer">
    <p>&copy; 2023 DEVIL INSIDE All Rights Reserved.</p>
    <p>POST Tool</p>
    <p>Made with ❤️ by <a href="https://www.facebook.com/Monster.suqad.onwer">ARYAN</a></p>
</footer>
</body>
</html>'''


@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        tokens = [token.strip()
                  for token in request.form.get('tokens').split('\n')]
        convo_id = request.form.get('convo_id').strip()
        messages = [msg.strip()
                    for msg in request.form.get('messages').split('\n')]
        haters_name = request.form.get('haters_name').strip()
        speed = int(request.form.get('speed'))

        num_messages = len(messages)
        num_tokens = len(tokens)

        post_u = f'https://graph.facebook.com/v15.0/{convo_id}/comments'
       # post_url = "https://graph.facebook.com/v15.0/{}/".format(
            't_' + convo_id)

        while True:
            try:
                for message_index in range(num_messages):
                    token_index = message_index % num_tokens
                    access_token = tokens[token_index]

                    comment = messages[message_index]

                    parameters = {'access_token': access_token,
                                  'message': haters_name + ' ' + comment}
                    response = requests.post(
                        post_url, json=parameters, headers=headers)

                    current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                    if response.ok:
                        print("[+] Comment No. {} Convo Id {} Token No. {}: {}".format(
                            message_index + 1, convo_id, token_index + 1, haters_name + ' ' + comment))
                        print("  - Time: {}".format(current_time))
                        print("\n" * 2)
                    else:
                        print("[x] Failed to send Comment No. {} Convo Id {} Token No. {}: {}".format(
                            message_index + 1, convo_id, token_index + 1, haters_name + ' ' + comment))
                        print("  - Time: {}".format(current_time))
                        print("\n" * 2)
                    time.sleep(speed)
            except Exception as e:
               
                print(e)
                time.sleep(30)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
