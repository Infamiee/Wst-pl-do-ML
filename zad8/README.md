### JSON

#### Prosta serializacja

```python
data = {
    "postId": 5,
    "id": 23,
    "name": "quis tempora quidem nihil iste",
    "email": "Sophia@arianna.co.uk",
    "body": "voluptates provident repellendus iusto perspiciatis ex fugiat ut\nut dolor nam aliquid et expedita voluptate\nsunt vitae illo rerum in quos\nvel eligendi enim quae fugiat est"
}

with open('files/data_file.json','w') as f:
	json.dump(data,f)

json_string = json.dumps(data)
```

Dzięki wbudowanej bibliotece json możliwa jest konwersja klas i typów serializowanych na string json. Metoda dump zapisuje od razu do pliku a dumps zwraca serializowanego stringa w formacie json

[Zapisany plik json](files/data_file_kowalczyk.json)

#### Deserializacja

```python
blackjack_hand = (8, "Q")
encoded_hand = json.dumps(blackjack_hand)
decoded_hand = json.loads(encoded_hand)
print(type(blackjack_hand)) -> <class 'tuple'> 
print(type(decoded_hand)) -> <class 'list'>
```

Deserializacje możemy wykonać przy pomocy metody loads, zwraca jednak ona domyślne typy pythonowe dla typów json i w tym przypadku tuple jest zamieniany na listę

#### Deserializacja z pliku

[plik json](files/data_file_kowalczyk.json)

```python
with open('files/data_file.json','r') as f:
	data = json.load(f)
```

metoda load przyjmuje plik jako argument i zwraca zdeserializowany plik json. Typem wyjściowym jest zazwyczaj słownik lub lista



#### Deserializacja ze stringa

```python
data = '''{"widget": {
    "debug": "on",
    "window": {
        "title": "Sample Konfabulator Widget",
        "name": "main_window",
        "width": 500,
        "height": 500
    },
    "image": {
        "src": "Images/Sun.png",
        "name": "sun1",
        "hOffset": 250,
        "vOffset": 250,
        "alignment": "center"
    },
    "text": {
        "data": "Click Here",
        "size": 36,
        "style": "bold",
        "name": "text1",
        "hOffset": 250,
        "vOffset": 100,
        "alignment": "center",
        "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
    }
}} '''

deserialized = json.loads(data)
```

metoda loads przyjmuje string json i konwertuje go na pythonowe typy danych



#### Przykład na "prawdziwych" danych - Znalezienie najdłuższych komentarzy

##### Pobranie danych

```python
url = 'https://jsonplaceholder.typicode.com/comments'
data = requests.get(url).json()
```

z biblioteki requests używamy metody get do pobrania danych z url i metody json do deserializacji na typy pythonowe

##### Znajdowanie najdłuższych komentarzy

```python
def max_len_comments(data,count=1):
	sorted_data = sorted(data,key=lambda x: len(x['body']),reverse=True)
	return sorted_data[:count]
```

Wyszukiwanie najdłuższych komentarzy i zwracanie wyznaczonej ilości największych wyników

##### Zapisywanie do pliku

```
with open('files/longest_comments_kowalczyk.json','w') as f:
	json.dump(max_len_comments(data,10),f)
```

Zapisanie 10 najdłuższych komentarzy

#### Enkodowanie i Dekodowanie klas

##### Tworzenie metody do enkodowania liczb zespolonych

```python
def encode_complex(z):
	if isinstance(z, complex):
		return (z.real, z.imag)
	else:
		type_name = z.__class__.__name__
		raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

json.dumps(2+1j,default=encode_complex)
```

Dla klas które nie są serializowane możemy stworzyć metodę, która zamieni obiekt na serializowalne zamienniki w tym przypadku tuple

##### Tworzenie własnego enkodera do liczb zespolonych

```python
class ComplexEncoder(json.JSONEncoder):
	def default(self, z):
		if isinstance(z, complex):
			return (z.real, z.imag)
		else:
			return super().default(z)

json.dumps(4+5j,cls=ComplexEncoder)
ComplexEncoder().encode(5+2j)
```

Własny enkoder tworzy się poprzez stworzenie klasy dziedziczącej z json.JSONEncoder i nadpisaniu metody default. Zamiana na stringa może się również odbyć przez wywołanie metody encode z klasy enkodera

##### Dekodowanie customowych klas

```python
def decode_complex(dct):
	if "__complex__" in dct:
		return complex(dct["real"], dct["imag"])
	return dct
data = '''{
    "__complex__": true,
    "real": 42,
    "imag": 36
}'''
decoded_data = json.loads(data,object_hook=decode_complex)
print(type(decoded_data))
```

dekodowanie do nieserializowanych klas można uzyskać tworząc metodę obsługującą podstawowe typy i zamieniając je na klasy



### CSV

#### Otwieranie pliku csv

[Używany plik](files/bollywood_movies_kowalczyk.csv)

##### Wczytywanie pliku csv

```python

with open('files/bollywood_movies_kowalczyk.csv','r') as f:
 csv_reader = csv.reader(f, delimiter=',')
 column_names = next(csv_reader)
 print("Nazwy kolumn: " + str(column_names))
 for row in csv_reader:
  print(f"Film {row[0]} premierę miał {row[3].split('|')[0]} i trwa {row[3].split('|')[1]}, średnia ocen użytkowników wynosi {row[4]}" )
```

metoda reader z biblioteki csv zwraca iterator zwracający wiersz w postaci listy

##### Wczytywanie pliku do słownika

```python
with open('files/bollywood_movies_kowalczyk.csv','r') as f:
	csv_reader = csv.DictReader(f)
	for row in csv_reader:
		print(f"Film {row['Movie_name']} premierę miał {row['Release date & duration'].split('|')[0]} i trwa {row['Release date & duration'].split('|')[1]}, średnia ocen użytkowników wynosi {row['User_ratings']}" )

```

metoda DictReader zwraca iterator z wierszami w formie słownika gdzie kluczami są nazwy kolumn a wartościami wartości z wiersza

#### Zapisywanie do pliku

##### Zapisywanie używając list

```python
with open('files/album_file_kowalczyk.csv', mode='w') as albums_file:
 album_writer = csv.writer(albums_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 album_writer.writerow(['Author','Name','Release Date'])
 album_writer.writerow(['The Doors', 'Strange Days', '1967'])
 album_writer.writerow(['David Bowie', 'The Man Who Sold the World', '1970'])
 album_writer.writerow(['Pink Floyd', 'Meddle', '1971'])
```

Do pliku można zapisać wiersze w formie listy używając metody writerow

[Plik wyjściowy](files/album_file_kowalczyk.csv)

##### Zapisywanie używając słownika

```python
with open('files/album_file2_kowalczyk.csv', mode='w') as albums_file:
 fieldnames = ['Author','Name','Release Date']
 album_writer = csv.DictWriter(albums_file, fieldnames)
 album_writer.writeheader()
 album_writer.writerow({"Author":'The Doors',"Name":"Strange Days", "Release Date":"1967"})
 album_writer.writerow({"Author":'David Bowie',"Name":"The Man Who Sold the World", "Release Date":"1970"})
 album_writer.writerow({"Author":'Pink Floyd',"Name":"Meddle", "Release Date":"1971"})
```

W przypadku DictWriter w metodzie writerow trzeba podać słownik z kluczami odpowiadającymi tym w nagłówku

[Plik wyjściowy](files/album_file2_kowalczyk.csv)

### Pandas

#### Wczytywanie pliku używając pandas

[Używany plik](files/bollywood_movies_kowalczyk.csv)

```pandas
df = pandas.read_csv('files/bollywood_movies_kowalczyk.csv')
```

Pandas ma wbudowaną metodę read_csv, która wczytuje plik csv i zamienia go na obiekt klasy DataFrame

##### Tworzenie indexu i parsowanie daty

[Używany plik](files/album_file2_kowalczyk.csv)

```python
import pandas
df = pandas.read_csv('files/album_file2_kowalczyk.csv', index_col='Author', parse_dates=['Release Date'])
```

metoda read_csv pozwala także na wskazanie kolumny indeksowej a także na wskazanie kolumny do parsowania na poprawny typ daty 

#### Zapisywanie do pliku 

```python
df.to_csv('files/album_file2_mod_kowalczyk.csv')
```

Zapisać możemy używając metody to_csv

[Plik wyjściowy](files/album_file2_mod_kowalczyk.csv)

