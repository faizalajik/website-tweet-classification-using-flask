import re
import string
import numpy as np
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from app import app
def open_kamus_prepro(x):
	kamus={}
	with open(x,'r') as file :
		for line in file :
			slang=line.replace("'","").split(':')
			kamus[slang[0].strip()]=slang[1].rstrip('\n').lstrip()
	return kamus

def casefolding(ulasan):
	for i in range(len(ulasan)):
		ulasan = ulasan[i].lower()
	return ulasan

def casefolding_file(ulasan):
    ulasan = ulasan.lower()
    return ulasan

def remove_punct(text):
	punct = '!"$%&+'''+'()*+,-./:;<=>?@[\]^_`{|}~?'
	data = []
	data.append(str(text))
	tweet = []
	for i in range(len(data)):
		text_nopunct = ''
		text_nopunct = re.sub('['+punct+']', ' ', data[i])
		text_noulr = re.sub(r"#\S+", "", text_nopunct)
		tweet.append(text_noulr)
	return tweet

def remove_punct_file(text):
	text_nopunct = ''
	text_notag = re.sub(r'@\S+', ' ',text)
	text_notag1 = re.sub(r'rt@\S+', ' ',text_notag)
	text_notagar = re.sub(r'#\S+', ' ', text_notag1)
	text_noulr = re.sub(r"http\S+", " ", text_notagar)
	text_nopunct = re.sub('['+string.punctuation+']', ' ', text_noulr)
	text_nostip =re.sub(r"\n\S+", " ", text_nopunct)
	return text_nostip

def remove_punct_spam(text):
	punct = '!"$%&+'''+'()*+,-./:;<=>?@[\]^_`{|}~?'
	text_nopunct = ''
	text_notag = re.sub(r'@\S+', ' ',text)
	text_notag1 = re.sub(r'rt@\S+', ' ',text_notag)
	# text_notagar = re.sub(r'#\S+', '', text_notag1)
	text_noulr = re.sub(r":/\S+", " ", text_notag1)
	text_nopunct = re.sub('['+punct+']', ' ', text_noulr)
	text_notagar = re.sub(r"#\S+", " ", text_nopunct)
	text_nostip =re.sub(r"\n\S+", " ", text_notagar)
	return text_nostip

def remove_num(text):
	data_remove_num=[]
	for i in range(len(text)):
		text_nonum = ''
		text_nonum = re.sub(r'\d+','', text[i])
		data_remove_num.append(text_nonum)
	return data_remove_num

def remove_num_file(text):
	text_nonum = ''
	text_nonum = re.sub(r'\d+','', text)
	return text_nonum

def slangwords(ulasan,kamus):
	# kamus_spell=open_kamus_prepro('D:/Tugas/Skripsi/kamus_slang_word.txt')
	kamus_spell = kamus
	# APPOSTOPHES= {"aq":"aku","gw":"aku","gwe":"aku","we":"aku","gak":"tidak","ga":"tidak","ngga":"tidak"
	# ,"nggak":"tidak","hak":"tidak","yg":"yang","yng":"yang","blum":"belum","blm":"belum","tlng":"tolong"
	# ,"tlong":"tolong","tlg":"tolong","tlng":"tolong","dgn":"dengan", "smoga":"semoga","bngt":"banget","bgt":"banget"
	# ,"sma":"sama","bnyak":"banyak","tp":"tapi","jg":"juga","byk":"banyak","org":"orang","dwpan":"depan"
	# ,"sdh":"sudah","brani":"berani","smua":"semua","jgn2":"jangan-jangan","blom":"belum","msuk":"masuk"
	# ,"brp":"berapa","kalo":"kalau","bls":"balas", "gpp":"gapapa","wktu":"waktu","blon":"belum","gmn":"gimana"
	# ,"jwb":"jawab","yng":"yang","syng":"sayang","bgs":"bagus","bda":"beda","pke":"pakai","bw":"bawa","bs":"bisa"
	# ,"knpa":"kenapa","knp":"kenapa","idup":"hidup","lg":"lagi","ttp":"tetap","dr":"dari","tmn2":"teman-teman"
	# ,"dri":"dari","pd":"pada","skrg":"sekarang","pdhl":"padahal","lmyn":"lumayan","tmpt":"tempat","ok":"oke"
	# ,"mmair":"air","pedagan":"pedagang","untk":"untuk","sgt":"sangat","lait":"laut","tenamg":"tenang"
	# ,"stlh":"setelah","u":"kamu","td":"tadi","cm":"cuma","nntn":"nonton","nggak":"tidak","ngga":"tidak"
	# ,"gak":"tidak","ga":"tidak","g":"tidak","ngak":"tidak","enggak":"tidak","engga":"tidak","krng":"tidak"
	# ,"kurng":"tidak","kurang":"tidak","suka":"bagus","ska":"bagus","nggak":"tidak","ngga":"tidak","gak":"tidak"
	# ,"ga":"tidak","g":"tidak","ngak":"tidak","enggak":"tidak","engga":"tidak","tp":"tapi","gasuka":" tidak suka"
	# ,"tpi":"tapi","bgd":"banget","bgttt":"banget","bgtt":"banget","bgt":"banget","bgtttt":"banget"}
	sentence_list = ulasan.split()
	new_sentence = []
	
	for word in sentence_list:
		for candidate_replacement in kamus_spell:
			if candidate_replacement == word:
				word = word.replace(candidate_replacement, kamus_spell[candidate_replacement])
				
		new_sentence.append(word)
	hsl = " ".join(new_sentence)
	return hsl


def tokenizing(ulasan):
	token = ulasan
	for sen in ulasan:
		token = word_tokenize(str(sen))
	# tokens = [word_tokenize(sen) for sen in ulasan]
	# ulasan = word_tokenize(str(ulasan))
	return token

def stemming(text): 
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	text_stem = []
	for i in range(len(text)):
		text_stem.append(stemmer.stem(text[i]))
	return text_stem

def stemming_file(ulasan):
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	text_stem = ''
	text_stem = stemmer.stem(ulasan)
	return text_stem

def ganti_negasi(w,kamus_negasi):
	# kamus_negasi=open_kamus_prepro('D:/Tugas/Skripsi/Kamus_negation_word.txt')
	cobaneg = []
	for k in range(len(w)):
		w_splited = w[k].split(' ')
		if 'tidak' in w_splited:
			index_negasi = w_splited.index('tidak')
			for i,k in enumerate(w_splited):
				if k in kamus_negasi and w_splited[i-1] == 'tidak':
					w_splited[i] = kamus_negasi[k]
			cobaneg.append(' '.join(w_splited))
		if 'kurang' in w_splited:
			index_negasi = w_splited.index('kurang')
			for i,k in enumerate(w_splited):
				if k in kamus_negasi and w_splited[i-1] == 'kurang':
					w_splited[i] = kamus_negasi[k]
			cobaneg.append(' '.join(w_splited))
		if 'sedikit' in w_splited:
			index_negasi = w_splited.index('sedikit')
			for i,k in enumerate(w_splited):
				if k in kamus_negasi and w_splited[i-1] == 'sedikit':
					w_splited[i] = kamus_negasi[k]
			cobaneg.append(' '.join(w_splited))
		else:
			cobaneg.append(' '.join(w_splited))
	return cobaneg

def ganti_negasi_f(w, kamus_negasi):
	# kamus_negasi=open_kamus_prepro('D:/Tugas/Skripsi/Kamus_negation_word.txt')
	w_splited = w.split(' ')
	if 'tidak' in w_splited:
		index_negasi = w_splited.index('tidak')
		for i,k in enumerate(w_splited):
			if k in kamus_negasi and w_splited[i-1] == 'tidak':
				w_splited[i] = kamus_negasi[k]
	return ' '.join(w_splited)

def negasi_file (ulasan):
	hsl = ulasan.apply(lambda x: ganti_negasi_f(x))
	return hsl

def kamus_stop():
	x=('D:/Tugas/Skripsi/stopword.txt')
	kamus_stopword=[]
	with open(x,'r') as file :
		for line in file :
			kamus_stopword.append(line.replace("\n","").split(','))
			# kamus[slang[0].strip()]=slang[1].rstrip('\n').lstrip()
	# kamus_stopword=['tidak','a','ada','adalah','adanya','adapun','agak','agaknya','agar','akan','akankah','akhir',
 #        'akhiri','akhirnya','aku','akulah','amat','amatlah','anda','andalah','antar','antara',
 #        'antaranya','apa','apaan','apabila','apakah','apalagi','apatah','arti','artinya','asal',
 #        'asalkan','atas','atau','ataukah','ataupun','awal','awalnya','b','bagai','bagaikan',
 #        'bagaimana','bagaimanakah','bagaimanapun','bagainamakah','bagi','bagian','bahkan','bahwa',
 #        'bahwasannya','bahwasanya','baiklah','bakal','bakalan','balik','banyak','bapak',
 #        'baru','bawah','beberapa','begini','beginian','beginikah','beginilah','begitu','begitukah',
 #        'begitulah','begitupun','bekerja','belakang','belakangan','belumlah','benar',
 #        'benarkah','benarlah','berada','berakhir','berakhirlah','berakhirnya','berapa','berapakah',
 #        'berapalah','berapapun','berarti','berawal','berbagai','berdatangan','beri','berikan',
 #        'berikut','berikutnya','berjumlah','berkali-kali','berkata','berkehendak','berkeinginan',
 #        'berkenaan','berlainan','berlalu','berlangsung','berlebihan','bermacam','bermacam-macam',
 #        'bermaksud','bermula','bersama','bersama-sama','bersiap','bersiap-siap','bertanya',
 #        'bertanya-tanya','berturut','berturut-turut','bertutur','berujar','berupa','besar',
 #        'betul','betulkah','biasa','biasanya','bila','bilakah','bisa','bisakah','boleh','bolehkah',
 #        'bolehlah','buat','bukan','bukankah','bukanlah','bukannya','bulan','bung','c','cara',
 #        'caranya','cukup','cukupkah','cukuplah','cuma','d','dahulu','dalam','dan','dapat','dari',
 #        'daripada','datang','demi','demikian','demikianlah','dengan','depan','di','dia',
 #        'diakhiri','diakhirinya','dialah','diantara','diantaranya','diberi','diberikan','diberikannya',
 #        'dibuat','dibuatnya','didapat','didatangkan','digunakan','diibaratkan','diibaratkannya',
 #        'diingat','diingatkan','diinginkan','dijawab','dijelaskan','dijelaskannya','dikarenakan',
 #        'dikatakan','dikatakannya','dikerjakan','diketahui','diketahuinya','dikira','dilakukan',
 #        'dilalui','dilihat','dimaksud','dimaksudkan','dimaksudkannya','dimaksudnya','diminta',
 #        'dimintai','dimisalkan','dimulai','dimulailah','dimulainya','dimungkinkan','dini','dipastikan',
 #        'diperbuat','diperbuatnya','dipergunakan','diperkirakan','diperlihatkan','diperlukan',
 #        'diperlukannya','dipersoalkan','dipertanyakan','dipunyai','diri','dirinya','disampaikan',
 #        'disebut','disebutkan','disebutkannya','disini','disinilah','ditambahkan','ditandaskan',
 #        'ditanya','ditanyai','ditanyakan','ditegaskan','ditujukan','ditunjuk','ditunjuki','ditunjukkan',
 #        'ditunjukkannya','ditunjuknya','dituturkan','dituturkannya','diucapkan','diucapkannya',
 #        'diungkapkan','dong','dua','dulu','e','empat','enggak','enggaknya','entah','entahlah',
 #        'f','g','guna','gunakan','h','hadap','hai','hal','halo','hallo','hampir','hanya','hanyalah',
 #        'hari','harus','haruslah','harusnya','helo','hello','hendak','hendaklah','hendaknya','hingga',
 #        'i','ia','ialah','ibarat','ibaratkan','ibaratnya','ibu','ikut','ingat','ingat-ingat','ingin',
 #        'inginkah','inginkan','inikah','inilah','itu','itukah','itulah','j','jadi','jadilah',
 #        'jadinya','jawab','jawaban','jawabnya','jelas','jelaskan','jelaslah','jelasnya','jika','jikalau','juga','jumlah','jumlahnya','justru',
 #        'k','kadar','kala','kalau','kalaulah','kalaupun','kali','kalian','kami','kamilah','kamu',
 #        'kamulah','kan','kapan','kapankah','kapanpun','karena','karenanya','kasus','kata','katakan',
 #        'katakanlah','katanya','ke','keadaan','kebetulan','kecil','kedua','keduanya','keinginan',
 #        'kelamaan','kelihatan','kelihatannya','kelima','keluar','kembali','kemudian','kemungkinan',
 #        'kemungkinannya','kena','kenapa','kepada','kepadanya','kerja','kesampaian','keseluruhan',
 #        'keseluruhannya','keterlaluan','ketika','khusus','khususnya','kini','kinilah','kira',
 #        'kira-kira','kiranya','kita','kitalah','kok','l','lagi','lagian','lah','lain',
 #        'lainnya','lalu','lama','lamanya','langsung','lanjut','lanjutnya','lebih','lewat',
 #        'lihat','lima','luar','m','macam','maka','makanya','makin','maksud','malah','malahan',
 #        'mampu','mampukah','mana','manakala','manalagi','masa','masalah','masalahnya','masih',
 #        'masihkah','masing','masing-masing','masuk','mata','mau','maupun','melainkan','melakukan',
 #        'melalui','melihat','melihatnya','memang','memastikan','memberi','memberikan','membuat',
 #        'memerlukan','memihak','meminta','memintakan','memisalkan','memperbuat','mempergunakan',
 #        'memperkirakan','memperlihatkan','mempersiapkan','mempersoalkan','mempertanyakan','mempunyai',
 #        'memulai','memungkinkan','menaiki','menambahkan','menandaskan','menanti','menanti-nanti',
 #        'menantikan','menanya','menanyai','menanyakan','mendapat','mendapatkan','mendatang','mendatangi',
 #        'mendatangkan','menegaskan','mengakhiri','mengapa','mengatakan','mengatakannya','mengenai',
 #        'mengerjakan','mengetahui','menggunakan','menghendaki','mengibaratkan','mengibaratkannya',
 #        'mengingat','mengingatkan','menginginkan','mengira','mengucapkan','mengucapkannya','mengungkapkan',
 #        'menjadi','menjawab','menjelaskan','menuju','menunjuk','menunjuki','menunjukkan','menunjuknya',
 #        'menurut','menuturkan','menyampaikan','menyangkut','menyatakan','menyebutkan','menyeluruh',
 #        'menyiapkan','merasa','mereka','merekalah','merupakan','meski','meskipun','meyakini','meyakinkan',
 #        'minta','mirip','misal','misalkan','misalnya','mohon','mula','mulai','mulailah','mulanya','mungkin',
 #        'mungkinkah','n','nah','naik','namun','nanti','nantinya','nya','nyaris','nyata','nyatanya',
 #        'o','oleh','olehnya','orang','p','pada','padahal','padanya','pak','paling','panjang','pantas',
 #        'para','pasti','pastilah','penting','pentingnya','per','percuma','perlu','perlukah','perlunya',
 #        'pernah','persoalan','pertama','pertama-tama','pertanyaan','pertanyakan','pihak','pihaknya',
 #        'pukul','pula','pun','punya','q','r','rasa','rasanya','rupa','rupanya','s','saat','saatnya','saja',
 #        'sajalah','salam','saling','sama','sama-sama','sambil','sampai','sampai-sampai','sampaikan','sana',
 #        'sangat','sangatlah','sangkut','satu','saya','sayalah','se','sebab','sebabnya','sebagai',
 #        'sebagaimana','sebagainya','sebagian','sebaik','sebaik-baiknya','sebaiknya','sebaliknya',
 #        'sebanyak','sebegini','sebegitu','sebelum','sebelumnya','sebenarnya','seberapa','sebesar',
 #        'sebetulnya','sebisanya','sebuah','sebut','sebutlah','sebutnya','secara','secukupnya','sedang',
 #        'sedangkan','sedemikian','sedikit','sedikitnya','seenaknya','segala','segalanya','segera',
 #        'seharusnya','sehingga','seingat','sejak','sejenak','sejumlah','sekadar','sekadarnya',
 #        'sekali','sekali-kali','sekalian','sekaligus','sekalipun','sekarang','sekaranglah','sekecil',
 #        'seketika','sekiranya','sekitar','sekitarnya','sekurang-kurangnya','sekurangnya','sela','selain',
 #        'selaku','selalu','selama','selama-lamanya','selamanya','selanjutnya','seluruh','seluruhnya',
 #        'semacam','semakin','semampu','semampunya','semasa','semasih','semata','semata-mata','semaunya',
 #        'sementara','semisal','semisalnya','sempat','semua','semuanya','semula','sendiri','sendirian',
 #        'sendirinya','seolah','seolah-olah','seorang','sepanjang','sepantasnya','sepantasnyalah',
 #        'seperlunya','seperti','sepertinya','sepihak','sering','seringnya','serta','serupa','sesaat',
 #        'sesama','sesampai','sesegera','sesekali','seseorang','sesuatu','sesuatunya','sesudah',
 #        'sesudahnya','setelah','setempat','setengah','seterusnya','setiap','setiba','setibanya',
 #        'setidak-tidaknya','setidaknya','setinggi','seusai','sewaktu','siap','siapa','siapakah',
 #        'siapapun','sini','sinilah','soal','soalnya','suatu','sudah','sudahkah','sudahlah','supaya',
 #        't','tadi','tadinya','tahu','tak','tambah','tambahnya','tampak','tampaknya','tandas','tandasnya',
 #        'tanpa','tanya','tanyakan','tanyanya','tapi','tegas','tegasnya','telah','tempat','tentang','tentu',
 #        'tentulah','tentunya','tepat','terakhir','terasa','terbanyak','terdahulu','terdapat','terdiri',
 #        'terhadap','terhadapnya','teringat','teringat-ingat','terjadi','terjadilah','terjadinya','terkira',
 #        'terlalu','terlebih','terlihat','termasuk','ternyata','tersampaikan','tersebut','tersebutlah',
 #        'tertentu','tertuju','terus','terutama','tetap','tetapi','tiap','tiba','tiba-tiba',
 #        'tidakkah','tidaklah','tiga','toh','tuju','tunjuk','turut','tutur','tuturnya','u','ucap','ucapnya',
 #        'ujar','ujarnya','umumnya','ungkap','ungkapnya','untuk','usah','usai','v','w','waduh','wah','wahai',
 #        'waktunya','walau','walaupun','wong','x','y','ya','yaitu','yakin','yakni','yang','z']
	return kamus_stopword

def remove_stop_words(tokens,kamus_stop):
	ulasan = []
	kamus = kamus_stop
	a = [j for sub in kamus for j in sub]
	for k in tokens:
		if k not in a:
			ulasan.append(k)
	return ulasan

def stopword_file (ulasan,kamus_stop):
	kamus = kamus_stop
	return [word for word in ulasan if word not in kamus]

def removeDoublecharWordList(word_list):
  return [removeDoublechar(word) for word in word_list]

def removeDoublechar(word):
 	newWord = list(word)
 	charsList = enumerate(list(word))
 	for i,c in charsList:
 		if i > len(newWord) -2:
 			break
 		if newWord[i+1] == c:
 			newWord[i+1] = ''
 	return ''.join(newWord)