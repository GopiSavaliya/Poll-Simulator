from flask import *
import operator, itertools

app = Flask(__name__)

db = {}
voter = {}
error = None
count = {}


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/Home')
def home():
    global error
    return render_template("Home.html", error=error)


@app.route('/AddCandidate', methods=['GET', 'POST'])
def addCandidate():
    global error
    error = None
    global db
    global count
    if request.method == 'POST':
        if 'id' in request.form and 'Name' in request.form:
            id = request.form['id']
            Name = request.form['Name']
            if id in db.keys():
                error = "Already Registered"
            else:
                db[id] = Name
                count[Name] = 0
                error = "Registration Successful"
                return redirect(url_for('home'))
    return render_template("AddCandidate.html", error=error)


@app.route('/Vote', methods=['GET', 'POST'])
def vote():
    global error
    error = None
    global voter
    global count
    if request.method == 'POST':
        if 'voterID' in request.form and 'Candidate' in request.form:
            voterID = request.form['voterID']
            Candidate = request.form['Candidate']
            if voterID in voter.keys():
                error = "Already Voted"
            else:
                voter[voterID] = Candidate
                count[Candidate] += 1
                error = "Successfully Voted"
                return redirect(url_for('home'))
    global db
    return render_template("Vote.html", db=db, error=error)


@app.route('/PollResult')
def pollResult():
    global error
    error = None
    global count
    sorted_count = dict(sorted(count.items(), key=operator.itemgetter(1), reverse=True))
    winners = dict(itertools.islice(sorted_count.items(), 2))
    first = None
    if len(sorted_count) > 0:
        first = dict(itertools.islice(sorted_count.items(), 1))
    return render_template("PollResult.html", winners=winners, first=first)


@app.route('/ReportResult')
def reportResult():
    global error
    error = None
    global count
    return render_template("ReportResult.html", report=count)


if __name__ == '__main__':
    app.run(debug=True)
