![Printer output: Hello from the universe, HACKING TIME](https://cloud-13i9niifd-hack-club-bot.vercel.app/0printer.jpg)
The Cat printer has multiple aliases such as the mini thermal printer, kitty printer, portable thermal printer. These kinds of thermal printers are usually available on online shopping platforms (aliexpress, shopee) for about 20$ 

This project is a unified solution that helps developers create better applications for their own use cases. This project aims to fulfil most of the tasks that developers would need to do on these kinds of printers.

## Features

 1. Text printing
	- Font size selection
	- Text alignment [left (by default), center, right]
	- Font selection
 2. Image printing 
	- multiple image conversion methods
## Installation
	
 - Basic way
		
```bash
Download the code from github
Extract the code
Open a code editor from the folder
RUN>> pip  install  -r  requirements.txt
```
 - Linux way

```bash

# Clone the repository.

$  git  clone  git@github.com:eshangonemad/Catprinter-Python-API

$  cd  Catprinter-Python-API

# Create a virtualenv on venv/ and activate it.

$  virtualenv  --python=python3  venv

$  source  venv/bin/activate

# Install requirements from requirements.txt.

$  pip  install  -r  requirements.txt

```
## Commands
```objective-c
-t "{enter text here}" //This is to print text
--fontsize {number} //This is to specify the font size of the text
-darker  //Print text or image darker
--align {left/center/right} //Specify alignment of text
--strikethrough //Apply strikethrough effect on text (Doesn't work using align)
-s //show preview before printing (this requires user interaction to approve printing)

```
## Usage
```python
python print.py -t "Helliverse" --strikethrough --align left --font-size 60 -darker -s 
```