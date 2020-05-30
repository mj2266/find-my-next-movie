import gunicorn
from flask import Flask, render_template, flash, redirect, url_for, session
from neo4j import GraphDatabase, basic_auth
import requests

from forms import Registration, Login, SearchBar
app = Flask(__name__)

app.config['SECRET_KEY'] = 'panda'

bolt_url = "bolt://hobby-gfahodcaabamgbkegkdpbbel.dbs.graphenedb.com:24787"
usr_nm_db = 'developer'
pswrd_db = 'b.rEb0aDuWDSh6.MJh3xAHL51pltkfC'

# bolt_url = "bolt://54.82.3.194:37481"
# usr_nm_db = 'neo4j'
# pswrd_db = 'addressees-attitude-game'

# bolt_url = "bolt://107.22.147.78:33503"
# usr_nm_db = 'neo4j'
# pswrd_db = 'wiggles-dates-laps'



@app.route('/logout')
def logout():
    if session.get('username'):
        # prevent flashing automatically logged out message
        del session['username']
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = form.username.data
        passw = form.password.data
        gdb1 = GraphDatabase.driver(bolt_url, auth=basic_auth(usr_nm_db, pswrd_db))
        gdb = gdb1.session()
        query = '''MATCH(m:users)WHERE m.username='%s' RETURN m.password AS pass''' % (user)
        result = gdb.run(query, parameters={})
        result = result.value()
        print(result)
        if result[0] == passw:
            print('Successfully logged in')
            session['username'] = user
            query = '''MATCH((u:users)-[:VIEWED]->(m:Movie)) where u.username ="%s" RETURN m''' % (user)
            results = gdb.run(query)
            results = results.value()
            print("haba", results)
            if len(results) == 0:
                print("right")
                return redirect(url_for('choose'))
            else:
                print("wrong")
                return redirect(url_for('index'))

        else:
            print('password does not match')

    return render_template('login.html', form=form)


@app.route('/dummy/<imdb>')
def addViewed(imdb):
    print(imdb)
    user = session.get('username')
    gdb1 = GraphDatabase.driver(bolt_url, auth=basic_auth(usr_nm_db, pswrd_db))
    gdb = gdb1.session()
    query = '''
    MATCH (m:Movie),(u:users)
    where m.imdbId = '%s' and u.username = '%s'
    CREATE (u)-[:VIEWED]->(m) 
    return m.title
    ''' % (imdb, user)
    results = gdb.run(query, data_contents=True)

    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        flash('Account successfully created')
        gdb1 = GraphDatabase.driver(bolt_url, auth=basic_auth(usr_nm_db, pswrd_db))
        gdb = gdb1.session()
        
        query = '''CREATE(:users{username:'%s', email:'%s', password:'%s'})''' % (
        form.username.data, form.email.data, form.password.data)
        gdb.run(query)
        if (form.Animation.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Animation' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())
        if (form.Adventure.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Adventure' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Comedy.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Comedy' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Children.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Children' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Action.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Action' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Crime.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Crime' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Romance.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Romance' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())

        if (form.Drama.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Drama' CREATE (a)-[:likes]->(g)
            return g.name''' % (
                form.username.data)
            result = gdb.run(query)
            print(result.values())
        print(form.username.data)
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    form = SearchBar()
    if form.validate_on_submit():
        search_val = form.search.data
        return redirect(url_for('search', var=search_val))
    return render_template('choose.html', form=form)


@app.route('/search/<var>')
def search(var):
    gdb1 = GraphDatabase.driver(bolt_url, auth=basic_auth(usr_nm_db, pswrd_db))
    gdb = gdb1.session()
    query = '''MATCH (m:Movie)
           WHERE toLower(m.title) contains '%s'
         RETURN m.title,m.imdbId''' % var
    results = gdb.run(query)
    results = results.values()
    return render_template('search.html', results=results)


def imdbToMovieDetails(imdbId):
    imdbId = imdbId[0]
    print(imdbId)
    movie_id = '{}'.format(imdbId)  # this will generate the imdb Movie ID
    # -----------------------------------------------------------------------------

    # ----------- HERE I WILL CONNECT WITH API AND SEND REQUEST -------------------
    # ----------- I WILL GET MY FINAL CLEANED DATA IN VARIABLE 'data' -------------
    # conn = http.client.HTTPSConnection("api.themoviedb.org")
    req_string = "https://api.themoviedb.org/3/find/%s?external_source=imdb_id&language=en-US&api_key=55ae4e90966677050f53e4c93ae7b804" % movie_id
    response = requests.get(req_string)

    var = response.json()

    data = var.get('movie_results')
    if not data:
        data = var.get('tv_results')
    # ----------------------------------------------------------------------------

    # --------- 'data' can be used to extract anything you want ---------------
    # ------ execute print(data) to find out what is available in data
    # data1 = data[0]['poster_path']
    # data2 = data[0]['backdrop_path']
    # print(data)
    # poster = data1
    # back = data2

    # This is the format to generate link
    # every image link should be of following format
    # https://image.tmdb.org/t/p/original/(here goes ur link)
    # link = 'https://image.tmdb.org/t/p/original/{}'.format(poster)
    # link2 = 'https://image.tmdb.org/t/p/original/{}'.format(back)
    # ------------------------------------------------------------------
    print("hey",data)
    return (data[0])


@app.route('/index', methods=['GET', 'POST'])
def index():
    username = session.get('username')
    print(username)
    if not username:
        return redirect(url_for('login'))
    gdb1 = GraphDatabase.driver(bolt_url, auth=basic_auth(usr_nm_db, pswrd_db))
    gdb = gdb1.session()

    form = SearchBar()
    if form.validate_on_submit():
        search_val = form.search.data
        return redirect(url_for('search', var=form.search.data))

    # ---------- THE FOLLOWING BLOCK WILL GENERATE IMDB MOVIE ID ------------------
    query = '''MATCH (u:users {username: '%s'})-->(m:Movie)<--(other:users)
    MATCH (other)-->(predict:Movie)
    WHERE not exists((u)-[:VIEWED]->(predict)) and exists(predict.imdbRating)
    with count(predict) as cnt , predict.imdbId as imdbId, predict.imdbRating as rating
    ORDER by cnt  desc
    RETURN distinct imdbId
    limit 5
    ''' % username
    results = gdb.run(query, data_contents=True)
    # results = results.rows[0][0]
    data = []
    results = results.values()
    for res in results:
        print(res)
        data.append(imdbToMovieDetails(res))
    # link = 'https://image.tmdb.org/t/p/original/{}'.format(poster)
    # link2 = 'https://image.tmdb.org/t/p/original/{}'.format(back)
    # ------------------------------------------------------------------
    genrelist = []
    movielist = []
    query = '''match p=(n:users)-[r:likes]->(m:Genre) where n.username="%s" return m.name''' % username
    results = gdb.run(query, data_contents=True)
    manjy_list = []
    results = results.value()
    print(results)
    for i in range(len(results)):
        print(i)

        appender = []
        result1 = results[i]
        print(result1)
        genrelist.append(result1)
        # query2 = '''MATCH p=(m:Movie)-[r:IN_GENRE]->(n:Genre{name:'%s'}) where exists(m.imdbRating) RETURN p order by m.imdbRating DESC LIMIT 5''' % (
        #     result1['name'])

        query2 = '''
            MATCH (m:Movie)-[r:IN_GENRE]->(n:Genre)
            WHERE exists(m.imdbRating) and n.name ='%s'
            RETURN m.imdbId
            ORDER BY m.imdbRating DESC
            LIMIT 5
        ''' % result1
        gresults = gdb.run(query2, data_contents=True)

        appender.append(result1)
        for i in gresults:
            appender.append(imdbToMovieDetails(i))

        manjy_list.append(appender)

    query = '''
    match (m:Movie) where exists(m.imdbRating) return m.imdbId order by m.imdbRating DESC limit 2
    '''
    highrate = []
    results = gdb.run(query, data_contents=True)
    results = results.values()
    for res in results:
        highrate.append(imdbToMovieDetails(res))

    return render_template('index.html', data=data, form=form, list=manjy_list, highrate=highrate)


@app.route('/genres')
def genres():
    return render_template('genres.html')


@app.route('/product')
def product():
    return render_template('product.html')


if __name__ == '__main__':
    app.run()
