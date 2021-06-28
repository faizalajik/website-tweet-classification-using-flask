import os
import pandas as pd 
import numpy as np 
import pickle
import string
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import flask as flask
import tensorflow as tf
from flask import Flask, render_template, request, flash, session, redirect, url_for, logging
from functools import wraps
import sys
from flask_mysqldb import MySQL
from proses import prepos as pre
from proses import ambil_gambar as gam
from proses import crawling as craw
from proses import crawling2 as craw2
from werkzeug import secure_filename
from nltk.tokenize import word_tokenize
import tweepy
from tweepy import Stream
import requests
import twint
import time

app=Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'skripsi'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_PATH'] = 'static/img'

mysql = MySQL(app)

@app.route('/tambah_kata/<string:id>',methods = ['GET','POST'])
def tambah_kata(id):
	if id == '1':
		msg = None
		if request.method == 'POST':
			kata = request.form['kata']
			kata_negasi = request.form['kata_negasi']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO negasi(id, kata_asli, kata_negasi) VALUES(%s, %s, %s)",('',kata,kata_negasi))
			mysql.connection.commit()
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM negasi")
			negasi = cur.fetchall()
			mysql.connection.commit()
			msg = 'Input Kata Berhasil'
			return flask.render_template('tambah_kata.html',msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM negasi")
		negasi = cur.fetchall()
		mysql.connection.commit()
		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))
	if id == '2':
		msg = None
		if request.method == 'POST':
			kata = request.form['kata']
			kata_negasi = request.form['kata_negasi']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO spelling(id, kata, kata_asli) VALUES(%s, %s, %s)",('',kata,kata_negasi))
			mysql.connection.commit()
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM spelling")
			negasi = cur.fetchall()
			mysql.connection.commit()
			msg = 'Input Kata Berhasil'
			return flask.render_template('tambah_kata.html',msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM spelling")
		negasi = cur.fetchall()
		mysql.connection.commit()
		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))
	if id == '3':
		msg = None
		if request.method == 'POST':
			kata = request.form['kata']
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO stopword(id, kata_stop) VALUES(%s, %s)",('',kata))
			mysql.connection.commit()
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM stopword")
			negasi = cur.fetchall()
			mysql.connection.commit()
			msg = 'Input Kata Berhasil'
			return flask.render_template('tambah_kata.html',msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM stopword")
		negasi = cur.fetchall()
		mysql.connection.commit()
		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))

@app.route('/cari_kata/<string:id>',methods = ['GET','POST'])
def cari_kata(id):
	if id == '1':
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM negasi")
		negasi = cur.fetchall()
		mysql.connection.commit()
		msg = None
		if request.method == 'POST':
			kata_cari = request.form['cari']
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM negasi where kata_asli = %s",[kata_cari])
			hsl = cur.fetchall()
			mysql.connection.commit()
			print(hsl)
			if hsl:	
				msg = 'Kata Ditemukan'
				return flask.render_template('tambah_kata.html',hasil = hsl,msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
			else:
				msg = 'Kata Tidak Ditemukan'
				return flask.render_template('tambah_kata.html', msg = msg,negasi=negasi,id=id,jmlh=len(negasi))

		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))
	if id == '2':
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM spelling")
		negasi = cur.fetchall()
		mysql.connection.commit()
		msg = None
		if request.method == 'POST':
			kata_cari = request.form['cari']
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM spelling where kata_asli = %s",[kata_cari])
			hsl = cur.fetchall()
			mysql.connection.commit()
			print(hsl)
			if hsl:	
				msg = 'Kata Ditemukan'
				return flask.render_template('tambah_kata.html',hasil = hsl,msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
			else:
				msg = 'Kata Tidak Ditemukan'
				return flask.render_template('tambah_kata.html', msg = msg,negasi=negasi,id=id,jmlh=len(negasi))

		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))
	if id == '3':
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM stopword")
		negasi = cur.fetchall()
		mysql.connection.commit()
		msg = None
		if request.method == 'POST':
			kata_cari = request.form['cari']
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM stopword where kata_stop = %s",[kata_cari])
			hsl = cur.fetchall()
			mysql.connection.commit()
			print(hsl)
			if hsl:	
				msg = 'Kata Ditemukan'
				return flask.render_template('tambah_kata.html',hasil = hsl,msg=msg,negasi=negasi,id=id,jmlh=len(negasi))
			else:
				msg = 'Kata Tidak Ditemukan'
				return flask.render_template('tambah_kata.html', msg = msg,negasi=negasi,id=id,jmlh=len(negasi))

		return flask.render_template('tambah_kata.html',negasi=negasi,id=id,jmlh=len(negasi))


@app.route('/')
def index():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM movie")
	film = cur.fetchall()
	# judul = 'Rafathar'
	# cur = mysql.connection.cursor()
	# cur.execute("SELECT id_film FROM movie WHERE judul = %s", [judul])
	# # res = cur.execute("SELECT * FROM film JOIN detail ON film.id_film=detail.id_film WHERE detail.id_film= %s", [id])
	# fil = cur.fetchall()
	# print(fil[0]['id_film'])
	# kamus_negasi=pre.kamus_stop()
	# for i in kamus_negasi:
	# 	cur = mysql.connection.cursor()
	# 	cur.execute("INSERT INTO stopword(id, kata_stop) VALUES(%s, %s)",('',i))
	# 	mysql.connection.commit()


	if result > 0:
		return flask.render_template('index.html', film=film) 
	msg = 'Tidak ada Film yang ditemukan'
	return flask.render_template('index.html', msg=msg)
	cur.close()

def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Tidak sah terdaftar, Silahkan Log In', 'danger')
			return redirect(url_for('login.html'))
	return wrap

@app.route('/rekap')
def rekap():
	cur = mysql.connection.cursor()
	cu = mysql.connection.cursor()

	res = cur.execute("SELECT * FROM film")
	film = cur.fetchall()
	res = cur.execute("SELECT * FROM detail")
	detail = cur.fetchall()
	data = {'Task' : 'Film'}
	dataneg = {'Task' : 'Film'}
	datanet = {'Task' : 'Film'}
	for i in film:
		# print(i['id_film'])
		re = cu.execute("SELECT * FROM detail where id_film = %s and sentimen = 'POSITIF'",[i['id_film']])
		det = cu.fetchall()
		data[i['judul']] = len(det)
		re = cu.execute("SELECT * FROM detail where id_film = %s and sentimen = 'NEGATIF'",[i['id_film']])
		det = cu.fetchall()

		dataneg[i['judul']] = len(det)
		re = cu.execute("SELECT * FROM detail where id_film = %s and sentimen = 'NETRAL'",[i['id_film']])
		det = cu.fetchall()
		datanet[i['judul']] = len(det)

	cur.close()
	
	print(data)
	return render_template("rekap.html",detail=detail,data=data,dataneg=dataneg, datanet=datanet)


def ValuePredictor(text):
 json_file = open('model/model_cnn3class_kim_v7.json', 'r')
 model_json = json_file.read()
 json_file.close()
 model = model_from_json(model_json)

 # model = load_model('modelcnn_v1.h5')
 model.load_weights('model/model_cnn3class_kim_v7.h5')


 with open('model/tokenizer_model_cnn3class_kim_v7.pickle', 'rb') as handle:
 	tokenizer = pickle.load(handle)


 sequences = tokenizer.texts_to_sequences(text)

 word_index = tokenizer.word_index
 test_cnn_data = pad_sequences(sequences, maxlen=37)
 x_test = test_cnn_data

 print(x_test[0])

 res = model.predict(x_test,batch_size=1, verbose=1)

 return res

def ValuePredictorSpam(text):
 json_file_spam = open('model/model_spam4_kim.json', 'r')
 model_json_spam = json_file_spam.read()
 json_file_spam.close()
 model_spam = model_from_json(model_json_spam)

 model_spam.load_weights('model/model_spam4_kim.h5')

 with open('model/tokenizer_model_spam4_kim.pickle', 'rb') as handle:
 	tokenizer_spam = pickle.load(handle)


 sequences = tokenizer_spam.texts_to_sequences(text) 

 word_index = tokenizer_spam.word_index
 test_cnn_data = pad_sequences(sequences, maxlen=37)
 x_test = test_cnn_data

 res = model_spam.predict(x_test,batch_size=1, verbose=1)

 return res

@app.route('/kategori',methods = ['GET','POST'])
def kategori():
	kategori1 =''
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		kategori = request.form['Kategori']
		if kategori == 'Horor':
			kategori1 = 'Kengerian'
			result = cur.execute("SELECT *, jenis.jenis FROM movie INNER JOIN jenis ON movie.id_film=jenis.id_film AND jenis.jenis = %s ORDER BY movie.rate DESC",[kategori1])
			# result = cur.execute("SELECT * FROM movie where jenis = %s ORDER BY rate DESC",[kategori1])
			film = cur.fetchall()
		else:
			result = cur.execute("SELECT *, jenis.jenis FROM movie INNER JOIN jenis ON movie.id_film=jenis.id_film AND jenis.jenis = %s ORDER BY movie.rate DESC",[kategori])
			film = cur.fetchall()
			id_film=[]
			total = []
		return render_template("kategori.html",film = film, kategori=kategori)

	return render_template("kategori.html")

@app.route('/uji_data',methods = ['GET','POST'])
def uji_data():
 data = {'Task' : 'Film','Akaurasi':72,'Presisi':68,'Recall':65}
 dataneg = {'Task' : 'Film'}
 datanet = {'Task' : 'Film'}
 if request.method == 'POST':
 	tweet=[]
 	tweet.append(request.form['tweet'])
 	# hasil=str(hasil.values())
 	# hasil = list(hasil)

 	# tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hasil).setSince("2016-05-01").setUntil("2017-09-30").setMaxTweets(10)
 	# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
 	# text_tweets = [[tweet.text] for tweet in tweets]
 	# df = pd.read_json (open('hasiltwint.json',encoding="utf8"))
 	# df[['id','date','tweet']].to_csv(r'hasiltwint.csv')
 	# d = pd.read_csv('dataUjiCobaKe1(hasilprepo)v2.csv', encoding='unicode_escape')
 	# d.columns = ['id', 'tweet', 'label']
 	text=[]
 	predik=[]
 	predik_spam=[]
 	daftar_negasi = {}
 	daftar_kata = {}
 	cur = mysql.connection.cursor()
 	cur.execute("SELECT * FROM negasi")
 	negasi = cur.fetchall()
 	mysql.connection.commit()
 	cur = mysql.connection.cursor()
 	cur.execute("SELECT * FROM spelling")
 	kata = cur.fetchall()
 	mysql.connection.commit()
 	for i in (negasi):
 		daftar_negasi[i['kata_asli']] = i['kata_negasi']
 	for i in (kata):
 		daftar_kata[i['kata']] = i['kata_asli']
 	cur = mysql.connection.cursor()
 	cur.execute("SELECT * FROM stopword")
 	stopword = cur.fetchall()
 	mysql.connection.commit()
 	stop = []
 	for i in (stopword):
 		stop.append(i['kata_stop'])
 	c =[]
 	text.append(pre.casefolding(tweet))
 	text.append(pre.slangwords(tweet[0],daftar_kata))
 	text.append(pre.remove_punct(text[1]))
 	text.append(pre.remove_num(text[2]))
 	text.append(pre.ganti_negasi(text[3],daftar_negasi))
 	text.append(pre.tokenizing(text[4]))
 	text.append(pre.stopword_file(text[5],stop))
 	b = [' '.join(text[6])]
 	text.append(pre.stemming(b))
 	print(text)

 	result = ValuePredictor(text[7])
 	class_sentimen = ['POSITIF','NEGATIF','NETRAL']
 	predik.append(class_sentimen[result.argmax()])

 	return render_template("uji_data.html",prediction=predik,hasil=text,result = result)
 return render_template("uji_data.html")

@app.route('/detail/<string:id>', methods=['GET','POST'])
def detail(id):
	
	#print(data)
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM ulasan WHERE id_film = %s", [id])
	# res = cur.execute("SELECT * FROM film JOIN detail ON film.id_film=detail.id_film WHERE detail.id_film= %s", [id])
	film = cur.fetchall()
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM movie WHERE id_film = %s", [id])
	fil = cur.fetchall()
	result_spam = cur.execute("SELECT * FROM spam WHERE id_film = %s", [id])
	# res = cur.execute("SELECT * FROM film JOIN detail ON film.id_film=detail.id_film WHERE detail.id_film= %s", [id])
	spam = cur.fetchall()
	result_jenis = cur.execute("SELECT * FROM jenis WHERE id_film = %s", [id])
	jenis = cur.fetchall()
	pos = 0
	neg = 0
	net = 0
	sp = 0
	kat = []
	for i in film:
		# print(i)
		if i['sentimen'] == 'POSITIF':
			pos = pos + 1
		elif i['sentimen'] == 'NEGATIF':
			neg = neg + 1
		else :
			net = net + 1
	for i in spam:
		# print(i)
		if i['klasifikasi'] == 'SPAM':
			sp = sp + 1
	for i in jenis:
		kat.append(i['jenis'])
	print(len(kat))
	for i in range(len(kat)):
		if len(kat) > 1 and i < len(kat)-1:
			kat [i] = kat[i]+','
	print(kat)

	# if net > pos or neg < net:
	# 	net = net - pos
	# 	netral = list(film[0]['sentimen'])
	# 	for i in film:
	# 		if i['sentimen'] == 'NETRAL':
			

	data = {'Task' : 'Hours per Day', 'Positif' : pos, 'Negatif' : neg, 'Netral' : net, 'Spam' : sp}
	return render_template("detail.html", detail = film, data=data, fil = fil, spam= spam, jenis=kat)

@app.route('/tambah_film',methods=['GET','POST'])
def tambah():
	if request.method == 'POST':
		# id_film = request.form['id']
		judul = request.form['judul']
		# keterangan = request.form['keterangan']
		# tahun = request.form['tahun']
		# uploaded_file = request.files['myfile']
		# uploaded_file.save(secure_filename(uploaded_file.filename))
		# photo = request.files['myphoto']
		# photo.save(os.path.join(app.config['UPLOAD_PATH'],secure_filename(photo.filename)))

		response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=7fd843b47a88b5d34635d7a0dd54e431&language=in-ID&query='+judul+'&page=1&include_adult=false')
		print (type(response.json()))
		film = response.json()
		time.sleep(3)
		if film['total_results'] != 0 :
			print(film)
			id_fil = film['results'][0]['id']
			tahun = film['results'][0]['release_date']
			sinopsis = film['results'][0]['overview']
			rate_film = film['results'][0]['vote_average']
			rate_film = rate_film*10
			print(film['results'][0])
			cur = mysql.connection.cursor()
			cur.execute("SELECT id_film FROM movie WHERE id_film = %s", [id_fil])
			# res = cur.execute("SELECT * FROM film JOIN detail ON film.id_film=detail.id_film WHERE detail.id_film= %s", [id])
			mov = cur.fetchall()
			# value = mov[0]['id_film']
			if (not mov):

				response = requests.get("https://api.themoviedb.org/3/movie/"+str(id_fil)+"?api_key=7fd843b47a88b5d34635d7a0dd54e431&language=id-ID")
				detail = response.json()
				time.sleep(3)

				kategori = []
				for i in range (len(detail['genres'])):
					kategori.append(detail['genres'][i]['name'])
				gambar = gam.tmdb_posters(id_fil,judul)
				# gambar = ''

				th = int(tahun[:4])
				th1 = tahun[4:10]
				th = th +1
				year = str(th)+th1
				print(year)

				# text = []
				# access_token="2607105624-E7Cclz6iRePPyj9tCDz7arO0yKFKZgHvjPfO10V"
				# access_token_secret="gZXK8nQqb1h1W2CnjCtSNV5uLhP6wJq2oH3udFQqV20HB"
				# consumer_key="baOzDDRm8SlPDYuVOCdM3Fueq"
				# consumer_secret="9clkfSq5JF3t0f00UkD8FoVC4WM7vOdMBTOc1QOyPhnXCzRXfa"

				# auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
				# auth.set_access_token(access_token,access_token_secret)
				# api = tweepy.API(auth,wait_on_rate_limit=True)

				# for tweet in tweepy.Cursor(api.search,q="Film "+judul,lang="id").items(50):
				# 	# d['text'] = tweet.text
				# 	text.append(tweet.text)
				# c = twint.Config()
				# c.Search = 'Film '+judul #search keyword
				# c.Since = '2015-08-5'
				# c.Store_csv = False
				# c.Hide_output =True
				# c.Count = True
				# c.Stats = True
				# twint.run.Search(c)
				# text = twint.output.tweet_objects
				tweet1 = craw.getTweetByKeyword(judul, 100, tahun, year)
				# if len(tweet1) > 0:  
				tweet2 = craw.getTweet2(judul, 100, tahun, year)
				text = tweet2+tweet1
				# import csv
				# with open('Film '+judul+'.csv', 'w', encoding='utf-8') as myfile:
				# 	wr = csv.writer(myfile)
				# 	wr.writerow(text)
				print(len(text))
				daftar_negasi = {}
				daftar_kata = {}
				cur = mysql.connection.cursor()
				cur.execute("SELECT * FROM negasi")
				negasi = cur.fetchall()
				mysql.connection.commit()
				cur = mysql.connection.cursor()
				cur.execute("SELECT * FROM spelling")
				kata = cur.fetchall()
				mysql.connection.commit()
				for i in (negasi):
					daftar_negasi[i['kata_asli']] = i['kata_negasi']
				for i in (kata):
					daftar_kata[i['kata']] = i['kata_asli']
				# print(text)
				cur = mysql.connection.cursor()
				cur.execute("SELECT * FROM stopword")
				stopword = cur.fetchall()
				mysql.connection.commit()
				stop = []
				for i in (stopword):
					stop.append(i['kata_stop'])
				if (len(text) != 0 ):
					d = pd.DataFrame(data=text, columns=["text"])

					# d = pd.read_csv(secure_filename(uploaded_file.filename),encoding='unicode_escape')
					# d.columns = ['id', 'text']
					predik = []
					predik_spam = []
					prediksi_spam = []
					ulasan = []
					ulasan_spam = []
					ulasan_asli = []
					d['case'] = d['text'].apply(lambda x: pre.casefolding_file(x))
					d['spelling'] = d['case'].apply(lambda x: pre.slangwords(x, daftar_kata))
					d['punc'] = d['spelling'].apply(lambda x: pre.remove_punct_spam(x))
					d['num'] = d['punc'].apply(lambda x: pre.remove_num_file(x))
					d['negasi'] =  d['num'].apply(lambda x: pre.ganti_negasi_f(x,daftar_negasi))
					d['tokens'] = [word_tokenize(sen) for sen in d.negasi]
					dataToken = d['tokens'].apply(pre.removeDoublecharWordList).reset_index()['tokens']
					stops = [pre.stopword_file(sen,stop) for sen in dataToken] 
					d['stop'] = [' '.join(sen) for sen in stops]
					d['stemming'] = d['stop'].apply(lambda x: pre.stemming_file(x))
					# d['tweet'] = d['stemming']
					# print(d.spelling[0])
					# print(d.punc[0])
					# print(d.num[0])
					# print(d.negasi[0])

					# print(d.stop[0])
					# print(d.stemming[0])
					result_spam = ValuePredictorSpam(d['stemming'])
					class_spam = ['SPAM','BUKAN SPAM']
					for i in range(len(result_spam)):
						predik_spam.append(class_spam[result_spam[i].argmax()])
						if predik_spam[i] == 'BUKAN SPAM':
							ulasan_asli.append(d.text[i])
							ulasan.append(d.stemming[i])
						else:
							prediksi_spam.append(predik_spam[i])
							ulasan_spam.append(d.text[i])
					data = pd.DataFrame(data=ulasan, columns=["text"])
					# d['case'] = d['text'].apply(lambda x: pre.casefolding_file(x))
					# d['spelling'] = d['case'].apply(lambda x: pre.slangwords(x))
					# data['text'] = d['stemming']
					data['punc'] = data['text'].apply(lambda x: pre.remove_punct_file(x))
					data['num'] = data['punc'].apply(lambda x: pre.remove_num_file(x))
					# data['negasi'] =  data['num'].apply(lambda x: pre.ganti_negasi_f(x))
					# d['tokens'] = [word_tokenize(sen) for sen in d.negasi]
					# dataToken = d['tokens'].apply(pre.removeDoublecharWordList).reset_index()['tokens']
					# stops = [pre.stopword_file(sen) for sen in dataToken] 
					# d['stop'] = [' '.join(sen) for sen in stops]
					# d['stemming'] = d['stop'].apply(lambda x: pre.stemming_file(x))
					result = ValuePredictor(data['num'])
					class_sentimen = ['POSITIF','NEGATIF','NETRAL']

					pos = 0
					neg = 0
					net = 0
					for i in range(len(result)):
						# dat = np.array(ulasan)
						predik.append(class_sentimen[result[i].argmax()])
						if predik[i] == 'POSITIF':
							pos = pos + 1
						elif predik[i] == 'NEGATIF':
							neg = neg + 1
						else :
							net = net + 1
					print(pos)
					print(neg)
					print(net)

					rate = 0
					rate = (pos*100)/(pos+neg)

					cur = mysql.connection.cursor()
					cur.execute("INSERT INTO movie(id_film, judul, sinopsis, tahun, gambar,rate,rate_movie) VALUES(%s, %s, %s,%s,%s,%s,%s)",(id_fil, judul,sinopsis, tahun,gambar,rate,rate_film))
					mysql.connection.commit()
					for i in kategori:
						cur = mysql.connection.cursor()
						cur.execute("INSERT INTO jenis(id, id_film, jenis) VALUES(%s, %s, %s)",('',id_fil,i))
						mysql.connection.commit()

					cur = mysql.connection.cursor()
					cur.execute("SELECT id_film FROM movie WHERE judul = %s", [judul])
				# res = cur.execute("SELECT * FROM film JOIN detail ON film.id_film=detail.id_film WHERE detail.id_film= %s", [id])
					fil = cur.fetchall()
					value = fil[0]['id_film']
					print(value)
					for i in range(len(prediksi_spam)):
						cur = mysql.connection.cursor()
						cur.execute("INSERT INTO spam(id,id_film, ulasan, klasifikasi) VALUES(%s,%s, %s, %s)",('',id_fil, str(ulasan_spam[i]), str(prediksi_spam[i])))
						mysql.connection.commit()
					cur.close()
					for i in range(len(result)):
						cur = mysql.connection.cursor()
						cur.execute("INSERT INTO ulasan(id,id_film, ulasan, sentimen) VALUES(%s,%s, %s, %s)",('',id_fil, str(ulasan[i]), str(predik[i])))
						mysql.connection.commit()
					cur.close()
					return redirect(url_for('index'))

				# return redirect(url_for('detail/'+str(id_fil)))
				else :
					msg = 'Tidak ada ulasan film yang ditemukan'
					return flask.render_template('tambah_film.html', msg=msg)
			else:
				msg = 'Film Sudah Ada'
				return flask.render_template('tambah_film.html', msg=msg)
		else :
			msg = 'Tidak ada ulasan film yang ditemukan'
			return flask.render_template('tambah_film.html', msg=msg)
			
	return render_template('tambah_film.html')	

@app.route('/update_film/<string:id>')
def update_film(id):
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM movie WHERE id_film = %s", [id])
	fil = cur.fetchall()
	mysql.connection.commit()
	tahun = fil[0]['tahun']
	judul = fil[0]['judul']

	ulasan = craw.getTweetUpdate(judul, 100, tahun)
	if (len(ulasan) != 0 ):

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM ulasan WHERE id_film = %s", [id])
		ul = cur.fetchall()
		mysql.connection.commit()
		ulasan_lama = []
		tweet = []
		for i,k in enumerate(ul):
			ulasan_lama.append(k['ulasan'])
		# update_ulasan = ulasan+ulasan_lama
		# seen = set()
		# result = []
		# for item in update_ulasan:
		# 	if item not in seen:
		# 		seen.add(item)
		# 	else:  
		# 		result.append(item)
		# print(len(ulasan))
		# print(len(result))

		# xc = []
		# for u in ulasan:
		# 	for j in result:
		# 		if u == j:
		# 			xc.append(u)
		# for x in xc:
		# 	ulasan.remove(x)
		# print(ulasan)
		# print(len(ulasan))
		temp = list(set(ulasan) ^ set(ulasan_lama))
		ul_baru = list(set(ulasan)&set(temp))
		print(len(ul_baru))
		daftar_negasi = {}
		daftar_kata = {}
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM negasi")
		negasi = cur.fetchall()
		mysql.connection.commit()
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM spelling")
		kata = cur.fetchall()
		mysql.connection.commit()
		for i in (negasi):
			daftar_negasi[i['kata_asli']] = i['kata_negasi']
		for i in (kata):
			daftar_kata[i['kata']] = i['kata_asli']
		# print(text)
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM stopword")
		stopword = cur.fetchall()
		mysql.connection.commit()
		stop = []
		for i in (stopword):
			stop.append(i['kata_stop'])

		d = pd.DataFrame(data=ul_baru, columns=["text"])

		d['case'] = d['text'].apply(lambda x: pre.casefolding_file(x))
		d['spelling'] = d['case'].apply(lambda x: pre.slangwords(x, daftar_kata))
		d['punc'] = d['spelling'].apply(lambda x: pre.remove_punct_spam(x))
		d['num'] = d['punc'].apply(lambda x: pre.remove_num_file(x))
		d['negasi'] =  d['num'].apply(lambda x: pre.ganti_negasi_f(x,daftar_negasi))
		d['tokens'] = [word_tokenize(sen) for sen in d.negasi]
		dataToken = d['tokens'].apply(pre.removeDoublecharWordList).reset_index()['tokens']
		stops = [pre.stopword_file(sen,stop) for sen in dataToken] 
		d['stop'] = [' '.join(sen) for sen in stops]
		d['stemming'] = d['stop'].apply(lambda x: pre.stemming_file(x))

		result_spam = ValuePredictorSpam(d['stemming'])
		class_spam = ['SPAM','BUKAN SPAM']
		bukan_spam = []
		ulasan_asli = []
		predik_spam = []
		ulasan_spam = []
		prediksi_spam = []
		print(len(result_spam))
		print(result_spam)
		for i in range(len(result_spam)):
			predik_spam.append(class_spam[result_spam[i].argmax()])
			if predik_spam[i] == 'BUKAN SPAM':
				ulasan_asli.append(d.text[i])
				bukan_spam.append(d.stemming[i])
			else:
				prediksi_spam.append(predik_spam[i])
				ulasan_spam.append(d.text[i])

		result = ValuePredictor(bukan_spam)
		class_sentimen = ['POSITIF','NEGATIF','NETRAL']

		pos = 0
		neg = 0
		net = 0
		predik = []
		for i in range(len(prediksi_spam)):
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO spam(id,id_film, ulasan, klasifikasi) VALUES(%s,%s, %s, %s)",('',id, str(ulasan_spam[i]), str(prediksi_spam[i])))
			mysql.connection.commit()
		cur.close()
		for i in range(len(result)):
			predik.append(class_sentimen[result[i].argmax()])
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO ulasan(id,id_film, ulasan, sentimen) VALUES(%s,%s, %s, %s)",('',id, str(ulasan_asli[i]), str(predik[i])))
			mysql.connection.commit()
			cur.close()

		for i in ul:
			# print(i)
			if i['sentimen'] == 'POSITIF':
				pos = pos + 1
			elif i['sentimen'] == 'NEGATIF':
				neg = neg + 1
			else :
				net = net + 1

		rate = 0
		rate = (pos*100)/(pos+neg)
		cur = mysql.connection.cursor()
		cur.execute("UPDATE movie SET rate = %s WHERE id_film = %s", [rate,id])
		mysql.connection.commit()

		cur.close()

		return detail(id)
	else :
		return detail(id)
	

@app.route('/hapus/<string:id>',methods=['GET','POST'])
def hapus(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM ulasan WHERE id_film = %s", [id])
	mysql.connection.commit()
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM spam WHERE id_film = %s", [id])
	mysql.connection.commit()
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM jenis WHERE id_film = %s", [id])
	mysql.connection.commit()
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM movie WHERE id_film = %s", [id])
	mysql.connection.commit()

	return redirect(url_for('index'))

@app.route('/cari_kata/hapus_kata/<string:id>/<string:id_kata>')
@app.route('/tambah_kata/hapus_kata/<string:id>/<string:id_kata>')
def hapus_kata(id,id_kata):
	if id == '1':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM negasi WHERE id = %s", [id_kata])
		mysql.connection.commit()
		cur = mysql.connection.cursor()
		# cur.execute("SELECT * FROM negasi")
		# negasi = cur.fetchall()
		# mysql.connection.commit()
		msg = 'Hapus Kata Berhasil'
		# jmlh = len(negasi)
		return redirect(url_for('tambah_kata',msg=msg,id=id))
	if id == '2':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM spelling WHERE id = %s", [id_kata])
		mysql.connection.commit()
		# cur = mysql.connection.cursor()
		# cur.execute("SELECT * FROM spelling")
		# negasi = cur.fetchall()
		# mysql.connection.commit()
		msg = 'Hapus Kata Berhasil'
		# jmlh = len(negasi)
		return redirect(url_for('tambah_kata',msg=msg,id=id))
	if id == '3':
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM stopword WHERE id = %s", [id_kata])
		mysql.connection.commit()
		# cur = mysql.connection.cursor()
		# cur.execute("SELECT * FROM stopword")
		# negasi = cur.fetchall()
		# mysql.connection.commit()
		msg = 'Hapus Kata Berhasil'
		# jmlh = len(negasi)
		return redirect(url_for('tambah_kata',msg=msg,id=id))
	return redirect(url_for('tambah_kata',id=id))


@app.route('/login', methods=['GET','POST'])
def login():
		if request.method == 'POST':

			username = request.form['username']
			password_candidate = request.form['password']

			cur = mysql.connection.cursor()

			result = cur.execute("SELECT * FROM account WHERE username = %s", [username])

			if result > 0:
				data = cur.fetchone()
				password = data['password']

				if password == data['password']:
					session['logged_in'] = True
					session['username'] = username

					flash('Kamu sekarang sudah Log In', 'success')
					return redirect(url_for('index'))
				else:
					error = 'Log In tidak Valid'
					return render_template('login.html', error=error)

				cur.close()
			else:
				error = 'Username tidak ditemukan'
				return render_template('login.html', error=error)
		return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('Kamu sekarang sudah Log Out', 'success')
	return redirect(url_for('index'))

if __name__ == "__main__":
 app.secret_key='secret123'
 app.debug = True
 app.run(use_reloader = True, threaded=True)
