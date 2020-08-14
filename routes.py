from rvce_web_results import app,db
from flask import render_template, flash, redirect,session
from rvce_web_results.forms import *
from rvce_web_results.models import *
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import operator

#download data into shelf file using rvresult.py,(status, sd) = scrape_student_detail('1RV18CS' + roll_no_str) mmust be changed as per usn range desired, run update_sql.py(beware of shelf file name in both),this_student_row.sgpa2 = st['sgpa'] line must be changed as well as credits = [20,20]
#shellf_sql.py remain unchanged
#PROGRAM BELEIVES IN THE CONCEPT OF TIED RANKS


if __name__ == '__main__':
    app.debug = True
    app.run()

def remove_initials(a):
    b = a.copy()
    for elem in a:
        if len(elem) == 1:
            b.remove(elem)
    return b

def fuzz_compare(substr,st):
    st_list = st.split(' ')
    st_list = remove_initials(st_list)
    flist = []
    for s in st_list:
        flist.append(fuzz.WRatio(substr,s))
    return max(flist)



def fuzzy_search_database(st_name):
    
    st_name_dict = {}
    fuzzy_score_list = []
    
    student_list = db.session.query(Student).all()
    for st in student_list:
        st_name_dict[st.name] = fuzz_compare(st_name,st.name)
       
    fuzzy_score_list = sorted(st_name_dict.items(), key = operator.itemgetter(1),reverse=True)
    print(fuzzy_score_list[:10])
    return fuzzy_score_list[:10]



def select_choice(choice_list,item_no):
    item_no = int(item_no)
    single_tuple = choice_list[item_no-1]
    name = single_tuple[0]
    student_object = db.session.query(Student).filter(Student.name == name).one()
    return student_object




def find_rank(gpa,sem_no):
    gpa = float(gpa)
    sem_no = int(sem_no)
    if sem_no == 10:
        gpa_str = "cgpa"
    else:
        gpa_str = "sgpa" + str(sem_no)
    a = db.session.query(getattr(Student,gpa_str)).all()
    a = [r for (r,) in a]
    a = [x for x in a if x is not None]
    a.sort(reverse=True)
    rank = 1
    for element in a:
        if gpa >= element:
            break
        rank+=1
    return (rank,len(a))
    

def analyse(sem_no):
    '''sem_no = int(sem_no)
    if sem_no == 10:
        gpa_str = "cgpa"
    else:
        gpa_str = "sgpa" + str(sem_no)
    a = session.query(getattr(Student,gpa_str)).all()
    a = [r for (r,) in a]
    a.sort(reverse=True)'''
    analysis = ""
    for gpa_val_hi in range(100,79,-1):
        gpa_val = float(gpa_val_hi/10)
        (rank,l) = find_rank(gpa_val,sem_no)
        analysis = analysis+ ("The rank for sgpa = {} is {} out of {} students\n".format(gpa_val,rank,l))
    return analysis










#------------------------------------------------------------------------------------------------------------



    

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route('/name_results',methods=['GET', 'POST'])
def name_results():
    #print("starting")
    form=NameSearchForm()
    if form.validate_on_submit():
        print("Now redirecrtion")
        choices_list = fuzzy_search_database(form.name.data)   #returns a list of 9 dictionaries
        #choices_list = [{3:5,2:3},{1:1,2:2}]
        session['cl'] = choices_list
        
        return redirect('/confirm_name')
    else:
        print("not validated")
        print(form.errors)
    return render_template('name_search.html',form=form)
    

@app.route('/confirm_name',methods=['GET', 'POST'])
def confirm_name():
    form=ConfirmName()
    if form.validate_on_submit():
        choices_list=session['cl']
        choice = select_choice(choices_list,form.item_no.data)                   #function returns choice_list[item_no] of type orm object
        session['ch'] = str(choice.usn)
        return redirect('/results_page')
    else:
        print("not validated")
        print(form.errors)
    choices_list=session['cl']
    return render_template('confirm_name.html',form=form,my_list=choices_list)    #Appropriately prints the list with only the names- the required concise data is filtered in the template file




@app.route('/results_page',methods=['GET', 'POST'])
def results_page():
    choice_usn = session['ch']
    
    choice = db.session.query(Student).filter(Student.usn == choice_usn).one()
    return render_template('results_page.html', result=choice)




@app.route('/rank_checker',methods=['GET', 'POST'])
def rank_checker():
    form = RankCheckerForm()
    if form.validate_on_submit():
        (rank,l) = find_rank(form.gpa.data,form.sem_no.data)
        session['r'] = (rank,l)
        return redirect('/rank_result')
    else:
        print("not validated")
        print(form.errors)
    return render_template('rank_checker.html',form=form)



@app.route('/rank_result',methods=['GET', 'POST'])
def rank_result():
    (rank,l) = session['r']       
    return render_template('rank_result.html', rank=str(rank),l=str(l))



@app.route('/ranks_analyser',methods=['GET', 'POST'])
def ranks_analyser():
    form = AnalyserForm()
    if form.validate_on_submit():
        analysis_str = analyse(form.sem_no.data)
        session['a'] = analysis_str
        return redirect('/analysis')

    else:
        print("not validated")
        print(form.errors)

    return render_template('ranks_analyser.html',form=form)


@app.route('/analysis',methods=['GET', 'POST'])
def analysis():
    analysis_str = str(session['a'])
    analysis_list = analysis_str.split('\n')
    print(analysis_list)
    return render_template('analysis.html',al = analysis_list)































#-------------------------------------------------------
"""
user_dict = {"Sriram":"8055","Admin":"abcd","lmn":"pol"}
def authenticate(usr,pwd):
    if usr in user_dict:
        if user_dict[usr] == pwd:
            return True
    
    return False

@app.route('/index',  methods=['GET', 'POST'])
def index():
    user = {'username': 'Miguel'}
    this_student = db.session.query(Student).filter(Student.usn == '1RV18CS173').one()
    my_usn = this_student.usn
    my_name = this_student.name
    my_sgpa = this_student.sgpa1
    student = {'usn':my_usn,'name':my_name,'sgpa1':my_sgpa}
    #capitals_list = ['Paris',"tokyo"]
    #capitals_dict = {'France':'Paris','japan':'tokyo'}
    #return render_template('001.html', title='Home', user=user,capitals=capitals_list)
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts,student=student)



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        flash('Hello World')
        global a
        a = form.username.data
        if authenticate(form.username.data,form.password.data):
            return redirect('/post_login')
        else:
            return redirect('/index')
        
    #below statement is executed if form is not valid: ie the form is returned empty with required errors if a field is left empty
    return render_template('login.html', title='Sign In', form=form)

@app.route('/post_login')
def after_login():
    return render_template('003.html',un = a)
"""

