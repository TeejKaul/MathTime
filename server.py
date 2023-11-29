from flask import Flask, render_template, request, redirect
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.debug = True

# Get the absolute path to the directory containing the Flask application script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the absolute path to the userdata.txt file
userdata_file_path = os.path.join(base_dir, 'userdata.txt')

@app.route("/login")
def my_login():
    return redirect('login.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get("emailForm")
            password = request.form.get("passwordForm")

            # Perform validation against the userdata.txt file
            with open(userdata_file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("Email:") and email in line:
                        next_line = next(file).strip()
                        if next_line.startswith("Password:") and password in next_line:
                            return redirect('/thankyou')

            # If email and password do not match, show an error message
            error_message = "Invalid email or password"
            return render_template('login.html', error_message=error_message)

        except Exception as e:
            error_message = str(e)
            print(f"Error: {error_message}")
            return f'Could not process the request. Error: {error_message}'

    else:
        return render_template('login.html', error_message="")

def scrape_hacker_news():
    res = requests.get('https://news.ycombinator.com/news')
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titleline > a')
    subtext = soup.select('.subtext')
    hn = create_custom_hn(links, subtext)

    res2 = requests.get('https://news.ycombinator.com/news?p=2')
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    links2 = soup2.select('.titleline > a')
    subtext2 = soup2.select('.subtext')
    hn2 = create_custom_hn(links2, subtext2)

    return hn, hn2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'links': href, 'votes': points})
    return sort_stories_by_votes(hn)

@app.route('/shop.html')
def shop():
    hn, hn2 = scrape_hacker_news()
    return render_template('shop.html', hn=hn, hn2=hn2)

@app.route("/")
def my_home():
    return render_template('login.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    try:
        return render_template(page_name)
    except:
        return render_template('404.html')

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get("emailForm")
            password = request.form.get("passwordForm")

            # Write email and password to the userdata.txt file
            with open(userdata_file_path, 'a') as file:
                file.write(f"Email: {email}\n")
                file.write(f"Password: {password}\n")

            return redirect('/thankyou')

        except Exception as e:
            error_message = str(e)
            print(f"Error: {error_message}")
            return f'Could not process the request. Error: {error_message}'

    else:
        return 'Error: Method not allowed'

@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run()
