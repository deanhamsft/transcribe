import whisper
import os
import re
from pathlib import Path
from datetime import datetime
from bcolors import bcolors

success = False
files_list = []
book = ""
chapter = ""
link_prototype_blueletter = f"[FULLNAME](https://www.blueletterbible.org/kjv/BOOK)"
markdown_link_regex = r'\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)'
directory_path = "H:\\Trimmed"
book_list = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "New Testament Books", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
book_dic = {
            "Genesis": "gen",
            "Exodus": "exo",
            "Leviticus": "lev",
            "Numbers": "num",
            "Deuteronomy": "deu",
            "Joshua": "jos",
            "Judges": "jdg",
            "Ruth": "rth",
            "1 Samuel": "1sa",
            "2 Samuel": "2sa",
            "1 Kings": "1ki",
            "2 Kings": "2ki",
            "1 Chronicles": "1ch",
            "2 Chronicles": "2ch",
            "first Samuel": "1sa",
            "second Samuel": "2sa",
            "first Kings": "1ki",
            "second Kings": "2ki",
            "first Chronicles": "1ch",
            "second Chronicles": "2ch",
            "Ezra": "ezr",
            "Nehemiah": "neh",
            "Esther": "est",
            "Job": "job",
            "Psalms": "psa",
            "Proverbs": "pro",
            "Ecclesiastes": "ecc",
            "Song of Solomon": "sng",
            "Isaiah": "isa",
            "Jeremiah": "jer",
            "Lamentations": "lam",
            "Ezekiel": "eze",
            "Daniel": "dan",
            "Hosea": "hos",
            "Joel": "joe",
            "Amos": "amo",
            "Obadiah": "oba",
            "Jonah": "jon",
            "Micah": "mic",
            "Nahum": "nah",
            "Habakkuk": "hab",
            "Zephaniah": "zep",
            "Haggai": "hag",
            "Zechariah": "zec",
            "Malachi": "mal",
            "Matthew": "mat",
            "Mark": "mar",
            "Luke": "luk",
            "John": "jhn",
            "Acts": "act",
            "Romans": "rom",
            "1 Corinthians": "1co",
            "2 Corinthians": "2co",
            "first Corinthians": "1co",
            "second Corinthians": "2co",
            "Galatians": "gal",
            "Ephesians": "eph",
            "Philippians": "phl",
            "Colossians": "col",
            "1 Thessalonians": "1th",
            "2 Thessalonians": "2th",
            "first Thessalonians": "1th",
            "second Thessalonians": "2th",
            "1 Timothy": "1ti",
            "2 Timothy": "2ti",
            "first Timothy": "1ti",
            "second Timothy": "2ti",
            "Titus": "tit",
            "Philemon": "phm",
            "Hebrews": "heb",
            "James": "jas",
            "1 Peter": "1pe",
            "2 Peter": "2pe",
            "first John": "1jo",
            "second John": "2jo",
            "third John": "3jo",
            "first Peter": "1pe",
            "second Peter": "2pe",
            "1 John": "1jo",
            "2 John": "2jo",
            "3 John": "3jo",
            "Jude": "jde",
            "Revelation": "rev"
            }


def list_files_walk(start_path='.'):
    """
    Method to enumerate all underlaying files and add to a list of all files to be processed

        :param start_path: A path to walk, default of '.' for the current working directory
    """
    for root, dirs, files in os.walk(start_path):
        for file in files:
            files_list.append(os.path.join(root, file))

def is_file_older_than(file_path, date):
    """
    Method to check if the specified file is older than the provided date.

        :param file_path: path to specified file
        :param date: date format is YYYY-MM-DD

        :return: bool
    """
    # Get the last modification time of the file
    file_time = os.path.getmtime(file_path)
    # Convert the modification time to a datetime object
    file_datetime = datetime.fromtimestamp(file_time)
    
    # Convert the given date to a datetime object if it's not already
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%Y-%m-%d")  # Assuming date format is YYYY-MM-DD
    
    # Compare the file's modification time with the given date
    return file_datetime < date

def find_whole_word(text, word):
    """
    This method returns true if the whole word is matched in the submitted text
    
        :param text: Whole text to be searched
        :param word: Word to be found exact match

        :return: bool
    """
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, text))
          
def split_into_paragraphs(transcript, max_sentences=3):
    """
    Method to split text into managable reading paragraphs.

        :param text: Whole text to be split
        :param max_sentences: number of maximmum sentences per paragraph

        :return: split text
    """
    # Step 1: Split the transcript into sentences
    sentence_endings = re.compile(r'([.!?])\s+')
    sentences = sentence_endings.split(transcript)

    # Recombine the sentence endings with sentences
    sentences = ["".join(x) for x in zip(sentences[0::2], sentences[1::2])]

    # Step 2: Group sentences into paragraphs
    paragraphs = []
    paragraph = []
    
    for sentence in sentences:
        paragraph.append(sentence)
        if len(paragraph) >= max_sentences:
            paragraphs.append(" ".join(paragraph).strip())
            paragraph = []

    # Add any leftover sentences as the last paragraph
    if paragraph:
        paragraphs.append(" ".join(paragraph).strip())

    return "\n\n\n".join(paragraphs)

def process_file(file_path):
    """
    Process the file. Checks for file type and dates, processes and transcribes file accodingly

        :param file_path path to file to process
        
        :returns: bool
    """
    if file_path.endswith(".mp4"):
        filename = os.path.basename(filefullpath)
        print(f"{bcolors.OKGREEN}found audio file: {filename}{bcolors.ENDC}")
        out_path = Path(filename).stem
        out_path = "H:\\Transcripts\\" + out_path + ".md"
        if os.path.exists(out_path):
            check_date = "2025-01-13"
            print(f"{bcolors.OKGREEN}File found checking date for: {out_path}{bcolors.ENDC}")
            if is_file_older_than(out_path, check_date):
                print(f"{bcolors.WARNING}File already processed by older version, removing to fix links{bcolors.ENDC}")
                os.remove(out_path)
            else:
                return True
            
        # Load the model
        model = whisper.load_model('base')

        # Transcribe the audio file
        result = model.transcribe(filefullpath, verbose=False, fp16=False)
        result_proto = result["text"]
        
        for key, value in book_dic.items():
            if find_whole_word(result_proto.lower(), key.lower()):
                print(f'{bcolors.OKCYAN}Found {key} in text{bcolors.ENDC}')
                result_title = re.sub('FULLNAME', key, link_prototype_blueletter, flags=re.IGNORECASE)
                result_link = re.sub('BOOK', value, result_title, flags=re.IGNORECASE)
                # link = link_prototype_blueletter.replace("FULLNAME", key).replace("BOOK", value)
                result_proto = re.sub(key, result_link, result_proto, flags=re.IGNORECASE)

            # Create the output text file and write the text
            result_text = split_into_paragraphs(result_proto, max_sentences=4)
            with open(out_path, 'w') as f:
                f.write(result_text)
    return True

list_files_walk(directory_path)

for filefullpath in files_list:
    attempts = 0

    while attempts < 1 and not success:
        try: 
            attempts += 1
            print(f"{bcolors.OKBLUE}Attempt {attempts} for file {filefullpath} {bcolors.ENDC}")
            success = process_file(filefullpath)
        except Exception as e:
            print(f"{bcolors.FAIL}Attempt {attempts} Failed for file {filefullpath}\r\n{e}{bcolors.ENDC}")
    
    if success:
        success = False
        print(f"{bcolors.OKGREEN}Sucessuflly processed file {filefullpath}{bcolors.ENDC}")