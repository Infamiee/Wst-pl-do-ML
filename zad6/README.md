#### Otwieranie i zamykanie plików

[files/first_file_kowalczyk.txt](Plik tekst)

##### Otwieranie za pomocą metody open

```python
file = open('files/first_file_kowalczyk.txt')
```

##### Otwarcie i zamknięcie używając try finally

```python
file = open('files/first_file_kowalczyk.txt')
try:
	data = file.read()
finally:
	file.close()
```

##### Otwarcie i zamknięcie używając with

```python
with open('files/first_file_kowalczyk.txt') as file:
	data = file.read()
```

używając with operacja file.close() jest wykonywana automatycznie przy wyjściu z with

##### Wykorzystanie trybów otwierania plików

do otworzenia można wykorzystać jeden z wielu trybów, najpopularniejszymi są

- 'r' - tryb tylko do odczytu
- 'w' - tryb tylko do zapisu
- 'rb' odczyt w formie binarnej
- 'wb' zapis w formie binarnej



##### Typy plików tekstowych

```python
with open('files/first_file_kowalczyk.txt','r') as file:
	file.read()
<class '_io.TextIOWrapper'>
```

Pliki tekstowe domyślnie używają klasy TextIOWrapper



##### Typy plików binarnych

```python
with open('files/first_file_kowalczyk.txt','rb') as file:
	print(type(file))
<class '_io.BufferedReader'>
```

Do odczytu plików w trybie binarnym wykorzystuje się klasę BufferedReader

```python
with open('files/first_file_kowalczyk.txt','wb') as file:
	print(type(file))
<class '_io.BufferedWriter'>
```

A do pisania do plików binarnych używa się klasy BufferedWriter

##### Typy plików raw

```python
with open('files/first_file_kowalczyk.txt','rb',buffering=0) as file:
	print(type(file))
<class '_io.FileIO'>
```

W tym przypadku zwracany jest obiekt klasy FileIO



#### Pisanie i czytanie otwartych plików

[Wykorzystywany plik tekstowy](files/read_file_kowalczyk.txt)

##### Wczytanie całego pliku

```
with open('files/read_file_kowalczyk.txt','r') as file:
	print(file.read())
```

Metoda read zwraca wszystkie dane z pliku

##### Wczytanie po kilka znaków

```python
with open('files/read_file_kowalczyk.txt','r') as file:
	print(file.readline(3))
	print(file.readline(3))
	print(file.readline(3))
```

metoda readline z parametrem determinującym ilość znaków lini pobiera te znaki i dodaje znak końca linii

##### Wczytywanie całego pliku metodą readlines

```python
with open('files/read_file_kowalczyk.txt','r') as file:
	print(file.readlines())
```

readlines zwraca listę wszystkich linii w tekście

##### Iteracja po liniach

```python
with open('files/read_file_kowalczyk.txt','r') as file:
	for line in file:
		print(line)
```

Klasa TextIOWrapper jest generatorem przez co możemy przez obiekt tej klasy iterować lub zamienić na listę używając metody list

#### Zapisywanie do pliku

```python
with open('files/read_file_kowalczyk.txt', 'rw') as file:
	lines = list(file)
	file.writelines(reversed(lines))
```

Do zapisywania do pliku można użyć trybu 'w' lub dodać + do trybu 'r'. Metoda writelines przyjmuje listę linii które chcemy zapisać i dodaje je do końca 

#### Praca z bajtami

[Wykorzystywany obraz](files/cyberpunk_kowalczyk.png)

##### Otwieranie pliku jpg w trybie binarnym

```python
with open('files/cyberpunk_kowalczyk.png','rb') as file:
 for i in range(5):
  print(file.read(i))
```



#### Dos2Unix

Systemy Unixowe i Dosowe używają innego zakończenia końca linii w unixie jest to \n a w dosie \r\n. Aby zamienić znak końca linii wystarczy użyć metody replace

```python
def str2unix(input_str: str) -> str:
    r_str = input_str.replace('\r\n', '\n')
    return r_str


def dos2unix(source_file: str, dest_file: str):
    with open(source_file, 'r') as reader:
        dos_content = reader.read()
    unix_content = str2unix(dos_content)
    with open(dest_file, 'w') as writer:
        writer.write(unix_content)

dos2unix('files/dos2unix_text_kowalczyk.txt','files/dos2unix_text_unix_kowalczyk.txt')

```

[Plik źródłowy](files/dos2unix_text_kowalczyk.txt)

[Plik docelowy](files/dos2unix_text_unix_kowalczyk.txt)



#### Dołączanie do pliku

[Wykorzystywany plik tekstowy](files/read_file_kowalczyk.txt)

Aby dodawać kolejne dane do pliku, a nie go napisać należy użyć trybu 'a'.

W przeciwieństwie do trybów 'r' i 'w' tryb 'a' ustawia pointer na końcu pliku

```python
with open('files/read_file_kowalczyk.txt','a') as file:
	file.write('\npikachu')
```



#### Praca z wieloma plikami

```python
d_path = 'files/read_file_kowalczyk.txt'
d_r_path = 'files/read_file_reversed_kowalczyk.txt'
with open(d_path, 'r') as reader, open(d_r_path, 'w') as writer:
    pokemons = reader.readlines()
    writer.writelines(reversed(pokemons))
```

Używając with można otworzyć wiele plików



#### Tworzenie własnego menadżera treści

```python
class my_file_reader():
	def __init__(self, file_path):
		self.__path = file_path
		self.__file_object = None
	def __enter__(self):
		self.__file_object = open(self.__path)
		return self

	def __exit__(self, type, val, tb):
		self.__file_object.close()
```

Możemy stworzyć własną klasę obsługującą pliki



#### Używanie własnej klasy do parsowania pliku png

[Wykorzystywany obraz](files/cyberpunk_kowalczyk.png)

```python
class PngReader():
    # Every .png file contains this in the header.  Use it to verify
    # the file is indeed a .png.
    _expected_magic = b'\x89PNG\r\n\x1a\n'

    def __init__(self, file_path):
        # Ensure the file has the right extension
        if not file_path.endswith('.png'):
            raise NameError("File must be a '.png' extension")
        self.__path = file_path
        self.__file_object = None

    def __enter__(self):
        self.__file_object = open(self.__path, 'rb')

        magic = self.__file_object.read(8)
        if magic != self._expected_magic:
            raise TypeError("The File is not a properly formatted .png file!")

        return self

    def __exit__(self, type, val, tb):
        self.__file_object.close()

    def __iter__(self):
        # This and __next__() are used to create a custom iterator
        # See https://dbader.org/blog/python-iterators
        return self

    def __next__(self):
        # Read the file in "Chunks"
        # See https://en.wikipedia.org/wiki/Portable_Network_Graphics#%22Chunks%22_within_the_file

        initial_data = self.__file_object.read(4)

        # The file hasn't been opened or reached EOF.  This means we
        # can't go any further so stop the iteration by raising the
        # StopIteration.
        if self.__file_object is None or initial_data == b'':
            raise StopIteration
        else:
            # Each chunk has a len, type, data (based on len) and crc
            # Grab these values and return them as a tuple
            chunk_len = int.from_bytes(initial_data, byteorder='big')
            chunk_type = self.__file_object.read(4)
            chunk_data = self.__file_object.read(chunk_len)
            chunk_crc = self.__file_object.read(4)
            return chunk_len, chunk_type, chunk_data, chunk_crc
```