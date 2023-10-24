# profanity_multilang.py

def load_banned_words():
    banned_words = set()  # Initialize an empty set

    # Load banned words for each language and add them to the set
    # with open('static/spanish.txt', 'r') as english_file:
    #     banned_words.update(english_file.read().splitlines())

    with open('static/plang/italian.txt', 'r') as italian_file:
        banned_words.update(italian_file.read().splitlines())

    # with open('static/french.txt', 'r') as french_file:
    #     banned_words.update(french_file.read().splitlines())

    # Add more languages as needed

    return banned_words

def is_profane(text):
    words = text.split()
    banned_set = load_banned_words()

    for word in words:
        if word.lower() in banned_set:
            return True

    return False
