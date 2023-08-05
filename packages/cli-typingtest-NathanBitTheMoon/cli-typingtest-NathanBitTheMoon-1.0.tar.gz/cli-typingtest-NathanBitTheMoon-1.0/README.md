# cli-typingtest
A command line typing test written using curses in Python 3

Works best on Linux, works on Windows but you must install "windows-curses" and at this time, the delete key code must be changed but this will be fixed in the future.

### Command line arguments
* **-rs --range-start** The start of the range where words will be chosen. Default is 0
* **-re --range-end** The end of the list of words. The default is 100
* **-l --length** The length of the test in words. The default is 100
* **-tf --text-file** The path to the file that the program will read the words from. The default is "texts/words.txt"
* **-dr --disable-random** Randomize the list. "yes" or "no". The default is "yes"
* **-sw --shortest-word** The shortest a word can be in chars. The default is 3
* **-rp --remove-punctuation** Remove all punctuation from the text
