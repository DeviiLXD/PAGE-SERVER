from flask import Flask, render_template, request, redirect, url_for
import requests
import re
import time
import os

app = Flask(__name__)

def make_request(url, headers, cookies):
    try:
        response = requests.get(url, headers=headers, cookies=cookies).text
        return response
    except requests.RequestException as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        if password == "Devil 789":
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error="Incorrect Password! Try again.")
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        cookies = request.form['cookie']
        id_post = request.form['post_id']
        commenter_name = request.form['commenter_name']
        delay = int(request.form['delay'])
        comment_file = request.files['comment_file']
        comment_file_path = os.path.join('uploads', comment_file.filename)
        comment_file.save(comment_file_path)

        response = make_request('https://business.facebook.com/business_locations', headers={
            'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'
        }, cookies={'Cookie': cookies})

        if response is None:
            return render_template('dashboard.html', error="Error making initial request")

        try:
            token_eaag = re.search('(EAAG\w+)', str(response)).group(1)
        except AttributeError:
            return render_template('dashboard.html', error="Token not found in response")

        with open(comment_file_path, 'r') as file:
            comments = file.readlines()

        x, y = 0, 0
        results = []

        while True:
            try:
                time.sleep(delay)
                teks = comments[x].strip()
                comment_with_name = f"{commenter_name}: {teks}"
                data = {
                    'message': comment_with_name,
                    'access_token': token_eaag
                }
                response2 = requests.post(f'https://graph.facebook.com/{id_post}/comments/', data=data, cookies={'Cookie': cookies}).json()
                if 'id' in response2:
                    results.append({
                        'post_id': id_post,
                        'datetime': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'comment': comment_with_name,
                        'status': 'Success'
                    })
                    x = (x + 1) % len(comments)
                else:
                    y += 1
                    results.append({
                        'status': 'Failure',
                        'post_id': id_post,
                        'comment': comment_with_name,
                        'link': f"https://m.basic.facebook.com//{id_post}"
                    })
            except requests.RequestException as e:
                results.append({'status': 'Error', 'message': str(e)})
                time.sleep(5.5)
                continue

        return render_template('dashboard.html', results=results)

    return render_template('dashboard.html')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
