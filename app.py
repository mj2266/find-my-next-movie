# THIS IS OLD CODE
# IGNORE THIS FILE OR ONLY REFER TO FIND CODE
# BYW


from flask import Flask, render_template, flash, redirect, url_for, session
from neo4jrestclient.client import GraphDatabase


import http.client
import json

from forms import Registration, Login, SearchBar

app = Flask(__name__)

app.config['SECRET_KEY'] = 'panda'





@app.route('/login', methods =['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = form.username.data
        passw = form.password.data
        gdb = GraphDatabase("https://10.0.1.151-38922/", username="neo4j", password="possibilities-tug-sling")
        query = '''MATCH(m:users)WHERE m.username='%s' RETURN m.password''' % (user)
        result = gdb.query(query, data_contents=True)
        if result.rows[0][0] == passw:
            print('Successfully logged in')
            session['username'] = user
            query = '''MATCH((u:users)-[:VIEWED]->(m:Movie)) where u.username ="%s" RETURN m''' %(user)
            results = gdb.query(query, data_contents=True)
            if results.rows == None:
                print("right")
                return redirect(url_for('choose'))
            else:
                print("wrong")
                return redirect(url_for('index'))

        else:
            print('password does not match')

    return render_template('login.html',form =form)


@app.route('/dummy/<imdb>')
def addViewed(imdb):
    user = session.get('username')
    gdb = GraphDatabase("https://10.0.1.151-38922/", username="neo4j", password="possibilities-tug-sling")
    query = '''
    MATCH (m:Movie),(u:users) 
    where m.imdbId = '%s' and u.username = '%s'
    CREATE (u)-[:VIEWED]->(m) 
    return m.title
    '''  % (imdb ,user)
    results = gdb.query(query, data_contents=True)
    return redirect(url_for('index'))

@app.route('/registration',methods =['GET','POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        flash('Account successfully created')
        gdb = GraphDatabase("https://10.0.1.151-38922.neo4jsandbox.com/", username="neo4j", password="possibilities-tug-sling")
        query='''CREATE(:users{username:'%s', email:'%s', password:'%s'})''' %(form.username.data ,form.email.data ,form.password.data)
        gdb.query(query, data_contents=True)
        if (form.Animation.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Animation' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Adventure.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Adventure' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Comedy.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Comedy' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Children.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Children' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Action.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Action' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Crime.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Crime' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Romance.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Romance' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)

        if (form.Drama.data == True):
            query = '''MATCH (a:users),(g:Genre) where a.username= '%s' AND g.name='Drama' CREATE (a)-[:likes]->(g)''' % (
                form.username.data)
            gdb.query(query, data_contents=True)
        return redirect(url_for('login'))
    return render_template('registration.html',form = form)


@app.route('/choose',methods =['GET','POST'])
def choose():
    form = SearchBar()
    if form.validate_on_submit():
        search_val = form.search.data
        return redirect(url_for('search', var=search_val))
    return render_template('choose.html', form=form)



@app.route('/search/<var>')
def search(var):
    gdb = GraphDatabase("https://10.0.1.151-38922/", username="neo4j", password="possibilities-tug-sling")
    query = '''MATCH (m:Movie)
           WHERE toLower(m.title) contains '%s'
         RETURN m.title,m.imdbId''' %var
    results = gdb.query(query, data_contents=True)
    return render_template('search.html',results=results)


def imdbToMovieDetails(imdbID):
    imdbID = imdbID[0]
    print(imdbID)
    movie_id = 'tt{}'.format(imdbID)  # this will generate the imdb Movie ID
    # -----------------------------------------------------------------------------

    # ----------- HERE I WILL CONNECT WITH API AND SEND REQUEST -------------------
    # ----------- I WILL GET MY FINAL CLEANED DATA IN VARIABLE 'data' -------------
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"
    req_string = "/3/find/%s?external_source=imdb_id&language=en-US&api_key=55ae4e90966677050f53e4c93ae7b804" % movie_id
    conn.request("GET", req_string, payload)
    res = conn.getresponse()
    data = res.read()
    var = json.loads(data)
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
    return (data[0])


@app.route('/index',methods=['GET','POST'])
def index():
    username = session.get('username')
    if not username :
        return redirect(url_for('login'))
    gdb = GraphDatabase("https://10.0.1.151-38922/", username="neo4j", password="possibilities-tug-sling")

    form = SearchBar()
    if form.validate_on_submit():
        search_val = form.search.data
        return redirect(url_for('search', var=form.search.data))

    # ---------- THE FOLLOWING BLOCK WILL GENERATE IMDB MOVIE ID ------------------
    query = '''MATCH (u:users {username: '%s'})-->(m:Movie)<--(other:User)
    MATCH (other)-->(predict:Movie)
    WHERE not exists((u)-[:VIEWED]->(predict)) and exists(predict.imdbRating)
    with count(predict) as cnt , predict.imdbId as imdbId, predict.imdbRating as rating
    ORDER by cnt  desc
    RETURN distinct imdbId
    limit 5
    '''%username
    results = gdb.query(query, data_contents=True)
    # results = results.rows[0][0]
    data = []
    for res in results:
        data.append(imdbToMovieDetails(res))
    # link = 'https://image.tmdb.org/t/p/original/{}'.format(poster)
    # link2 = 'https://image.tmdb.org/t/p/original/{}'.format(back)
    #------------------------------------------------------------------
    genrelist=[]
    movielist=[]
    query = '''match p=(n:users)-[r:likes]->(m:Genre) where n.username="%s" return m''' %username
    results = gdb.query(query, data_contents=True)
    manjy_list = []
    for i in range(len(results)):
        appender = []
        result1 = results.rows[i][0]
        genrelist.append(result1['name'])
        # query2 = '''MATCH p=(m:Movie)-[r:IN_GENRE]->(n:Genre{name:'%s'}) where exists(m.imdbRating) RETURN p order by m.imdbRating DESC LIMIT 5''' % (
        #     result1['name'])

        query2 = '''
            MATCH (m:Movie)-[r:IN_GENRE]->(n:Genre)
            WHERE exists(m.imdbRating) and n.name ='%s'
            RETURN m.imdbId
            ORDER BY m.imdbRating DESC
            LIMIT 5
        ''' %result1['name']
        gresults = gdb.query(query2, data_contents=True)

        appender.append(result1['name'])
        for i in gresults:
            appender.append(imdbToMovieDetails(i))

        manjy_list.append(appender)

    query = '''
    match (m:Movie) where exists(m.imdbRating) return m.imdbId order by m.imdbRating DESC limit 2
    '''
    highrate = []
    results = gdb.query(query, data_contents=True)
    for res in results:
        highrate.append(imdbToMovieDetails(res))

    return render_template('index.html', data=data,form=form,list= manjy_list,highrate=highrate)

@app.route('/genres')
def genres():
    return render_template('genres.html')

@app.route('/product')
def product():
    return render_template('product.html')

if __name__ == '__main__':
    app.run()


