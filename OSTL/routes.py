from flask import render_template,url_for, flash, redirect, request
from OSTL.forms import RegistrationForm, LoginForm
from OSTL.models import User, Movies
from flask_login import login_user, current_user, logout_user, login_required
from OSTL import app, db, bcrypt
import random, string

movie_list = [
	{
		'title':'Gully Boy', 'des':'A coming-of-age story based on the lives of street rappers in Mumbai.','dir':' Zoya Akhtar','cast':' Ranveer Singh, Alia Bhatt','imdb':'8.5','per':'85','imgname':'gullyboy'
	},
	{
		'title':'Thackeray', 'des':'Biographical account of Shiv Sena Supremo, Balasaheb Thackeray.','dir':' Abhijit Panse','cast':' Nawazuddin Siddiqui, Amrita Rao','imdb':'5.6','per':'56','imgname':'thackeray'
	},
	{
		'title':'Luka Chuppi', 'des':'A television reporter in Mathura falls in love with a headstrong woman.','dir':' Laxman Utekar','cast':' Kartik Aaryan, Kriti Sanon','imdb':'7.2','per':'72','imgname':'lukkachuppi'
	},
	{
		'title':'Infinity War', 'des':'The Avengers team up to fight their biggest enemy, Thanos.','dir':'Russo Brothers','cast':' Robert Downey Jr., Mark Ruffalo','imdb':'8.5','per':'85','imgname':'infinitywar'
	}

]

malayalam_movie_list = [
	{
		'title':'Njan Prakashan', 'des':'A typical Malayali man who aspires to lead a luzurious life.','dir':' Sathyan Anthikad','cast':' Fahadh Faasil, Nikhila Vimal','imdb':'8.0','per':'80','imgname':'njanprakashan'
	},
	{
		'title':'Joseph', 'des':'A crime thriller revolving around Joseph and his family.','dir':' M. Padmakumar','cast':' Joju George, Aathmiya','imdb':'8.5','per':'85','imgname':'joseph'
	},
	{
		'title':'Odiyan', 'des':'Story of Odiyan clan, the shape-shifting black magicians.','dir':' V.A. Shrikumar Menon','cast':' Mohanlal, Manju Warrier','imdb':'6.1','per':'61','imgname':'odiyan'
	},
	{
		'title':'Kumbalangi Nights', 'des':'Story of four brothers who share a love-hate relationship.','dir':' Madhu C. Narayanan','cast':' Shane Nigam, Fahadh Faasil','imdb':'9.0','per':'90','imgname':'kumbalanginights'
	}

]

telugu_movie_list = [
	{
		'title':'Rangasthalam', 'des':'Two brothers in a quest to overthrow unlawful village president.','dir':' Sukumar','cast':' Ram Charan, Samantha Prabhu','imdb':'8.6','per':'86','imgname':'rangasthalam'
	},
	{
		'title':'Bharat Ane Nenu', 'des':'A university graduate becomes disillusioned by corruption. ','dir':' Koratala Shiva','cast':' Mahesh Babu, Kiara Advani','imdb':'8.0','per':'80','imgname':'bharatanenenu'
	},
	{
		'title':'Sarkar', 'des':'A successful businessman gets involved in a political battle in TN.','dir':' A.R. Murugadoss','cast':' Joseph Vijay, Keerthi Suresh','imdb':'7.2','per':'72','imgname':'sarkar'
	},
	{
		'title':'Gully Boy', 'des':'A coming-of-age story based on the lives of street rappers in Mumbai.','dir':' Zoya Akhtar','cast':' Ranveer Singh, Alia Bhatt','imdb':'8.5','per':'85','imgname':'gullyboy'
	},
	
]

movierows = [
{'Class':'D','rate':550},
{'Class':'C','rate':450},
{'Class':'B','rate':350},
{'Class':'A','rate':250}
]

final = {'date':'28 March','theatre':{'name':'INOX Raghuleela','time':{'slot':'9:30 AM','movie':{'name':'Thackeray','seats':['B-1','B-2','C-2']}}}}

movieseats = ['1','2','3','4','5','6','7']

moviedates = ['10 April','11 April','12 April']

mumbai_list = ['INOX Raghuleela', 'INOX RCity','Maratha Mandir','PVR Phoenix','Regal Cinema']

delhi_list = ['MovieTime Cinemas','PVR 3Cs','PVR Anupam Saket','Cinepolis','Carnival Cinemas']

trv_list = ['Ariesplex Cinemas','Sree Padmanabha Theatre','Dhanya and Remya Cinemas','Kalabhavan Theatre','Carnival Cinemas']

hyd_list = ['Miraj Cinema','Prasad Multiplex','INOX GVK One','PVR Cinemas','Miraj Cinema']

movietime = ['9:30 AM','10:30 AM','12:00 PM','3:30 PM','5:30 PM','9:30 PM']

pop_choice = [
{'Choice':'Pizza and Coke', 'rate':200},
{'Choice':'Burger and Coke','rate':300},
{'Choice': 'Waffles','rate':100},
{'Choice':'Popcorn','rate':100},
{'Choice':'None','rate':0}
]


@app.route('/') #Home Root
def main():
	return render_template("index.html")

@app.route('/Place/<place>')
def places(place):
	if place == 'Mumbai':
		return render_template("Mumbai.html", movie_list=movie_list,region='Mumbai')
	elif place == 'Delhi':
		return render_template("Delhi.html", movie_list=movie_list,region='Delhi')
	elif place == 'Hyderabad':
		return render_template("Hyd.html", movie_list=telugu_movie_list,region='Hyderabad')
	elif place == 'Trivandrum':
		return render_template("Trv.html", malayalam_movie_list=malayalam_movie_list,region='Trivandrum')


@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = RegistrationForm()
	if form.validate_on_submit():
		passw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(name = form.name.data, email = form.email.data, password = passw)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for { form.name.data }!','success')
		return redirect(url_for('login'))
	return render_template('Register.html',form = form)


@app.route('/Trial')
def trial():
	return render_template("Trial.html")


@app.route('/Login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember = False)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main'))
		else:
			flash('Unsuccessful Login','danger')
	return render_template('Login.html',form = form)


@app.route('/Logout')
def logout():
	logout_user()
	return redirect(url_for('main'))

@app.route('/account')
@login_required
def account():
	moviesData = Movies.query.filter_by(email=current_user.email).all()
	return render_template("Account.html",moviesData=moviesData)

@app.route('/plan/<movie>/<region>',methods=['GET','POST'])
@login_required
def plan(movie,region,methods=['GET','POST']):
	x = ""
	check_string = []
	check = False
	list_region = []
	if request.method == 'POST':
		seat_no = request.form.getlist('seats')
		date = request.form.get('date')
		time = request.form.get('time')
		theatre = request.form.get('theatre')
		movie_name = movie
		meal = request.form.get('eat')
		region_book = region
		seatString = ""
		trans_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
		movie_seat_check = Movies.query.filter_by(moviename=movie).all()
		for seat in movie_seat_check:
			if seat.moviedate==date and seat.movietheatre==theatre and seat.movietime==time:
				seat_list = list(seat.movieseat.split(","))
				del seat_list[-1]
				check_string = check_string + seat_list
				seat_list.clear()
		print(check_string)
		check = any(elem in seat_no for elem in check_string)
		print(check)
		if check:
			x = ["Seats are already booked."]
		else:
			for x in seat_no:
				seatString += x + ','
			movie_entry = Movies(id=trans_id,email=current_user.email,moviename=movie,moviedate=date,movietime=time,movietheatre=theatre,movieseat=seatString,eatable=meal)
			db.session.add(movie_entry)
			db.session.commit()
			print("Entry Successful in database.")
			return redirect(url_for('payment'))
	else:

		if region == 'Mumbai':
				list_region = mumbai_list
		elif region == 'Delhi':
				list_region = delhi_list
		elif region == 'Trivandrum':
				list_region = trv_list
		elif region == 'Hyderabad':
				list_region = hyd_list
	return render_template("Plan.html",movie=movie,movierows=movierows,movieseats=movieseats,moviedates=moviedates,movietime=movietime,list_reg=list_region,pop_choice=pop_choice,x=x,check=check,check_string=check_string)

@app.route('/payment',methods=['POST','GET'])
@login_required
def payment():
	data = Movies.query.filter_by(email=current_user.email).all()
	required_data = data[-1]
	print(required_data)
	seatlist = list(required_data.movieseat.split(","))
	del seatlist[-1]
	total = 0
	totalseats = len(seatlist)
	for x in seatlist:
		for y in movierows:
			if x[0][0] == y['Class']:
				total = total + y['rate']
	for x in pop_choice:
		if x['Choice'] == required_data.eatable:
			total = total + x['rate']
	if request.method == 'POST':
		return redirect(url_for('done'))
	return render_template("Payment.html",required_data=required_data,movierows=movierows,pop_choice=pop_choice,total=total,seatlist=seatlist,totalseats=totalseats)


@app.route('/done')
@login_required
def done():
	data = Movies.query.filter_by(email=current_user.email).all()
	required_data = data[-1]
	seatlist = list(required_data.movieseat.split(","))
	del seatlist[-1]
	total = 0
	totalseats = len(seatlist)
	for x in seatlist:
		for y in movierows:
			if x[0][0] == y['Class']:
				total = total + y['rate']
	for x in pop_choice:
		if x['Choice'] == required_data.eatable:
			total = total + x['rate']
	barcode_info = ""
	barcode_info = "Transaction ID: "+ required_data.id + "\nMovie Name: " + required_data.moviename + "\nMovie Date: " + required_data.moviedate + "\nMovie Show Time: " + required_data.movietime + "\nMovie Theatre: " + required_data.movietheatre + "\nTotal: " + str(total)
	print(barcode_info)
	return render_template("Done.html",required_data=required_data,barcode_info=barcode_info)

