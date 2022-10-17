# ZakupkiHack 2.0
Данный репозиторий появился после участия в zakupkiHack2.0 
Для запуска проекта требуется загрузить модели:
  
  dictionary - https://drive.google.com/file/d/1-mBUITUW7q6Ttwo9RmDlZyFahj6WdrlQ/view?usp=sharing
      
			dictionary = corpora.Dictionary(full_table['name_char_okpd'])

  
  tfidf - https://drive.google.com/file/d/1sACIBhThNVnn97LPxW9eUtLk6qhIwOtk/view?usp=sharing
      
			corpus = [dictionary.doc2bow(text) for text in full_table['name_char_okpd']]
      			tfidf = models.TfidfModel(corpus)
      

  index - https://drive.google.com/file/d/1Q3Y1tiAbtgKrYriK3IEgcE8uBk134r9O/view?usp=sharing
      
			feature_cnt = len(dictionary.token2id)
      			index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)  
  
	
датасет: https://drive.google.com/file/d/18FnSuiJw0NTFNp9c4hiftdiDhc7czG2C/view?usp=sharing

Для запуска проекта достаточно запустить файл main.py
результатом выполнения будет являться окно поиска, который может найти предмет по его характеристикам

Изначальные данные и пояснения можно найти по ссылке: https://disk.yandex.ru/d/GejytvocAPUAKQ
