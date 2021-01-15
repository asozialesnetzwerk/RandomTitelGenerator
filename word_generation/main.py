#!/usr/bin/env python3
# pylint: disable=invalid-name
import json
import duden


def get_article(title):
    """
    Word article
    """
    if ", der" in title:
        return "der"
    if ", die" in title:
        return "die"
    if ", das" in title:
        return "das"

    return None


def replace_umlauts(word_to_replace):
    return word_to_replace.lower() \
        .replace("ä", "ae") \
        .replace("ö", "oe") \
        .replace("ü", "ue") \
        .replace("ß", "ss") \
        .capitalize()


def search_duden(search, not_replaced_word):
    result = duden.search(search, True, True, False)
    if len(result) > 0:
        article = get_article(result[0].title)
        if article is not None:
            article = article.capitalize()
            articles[not_replaced_word.lower()] = article
            write_to_file("output.txt", article + " " + not_replaced_word + "\n")
            with open("article.json", "w") as article_json_file:
                article_json_file.write(str(articles))


def write_to_file(file_name, val):
    with open(file_name, "a") as ffff:
        ffff.write(val)


words = open("sorted_words").read().splitlines()

print(len(words))
# words = ["Test", "Schnelltest", "Pinguin", "Test", "Känguru"]


# read file
with open('article.json', 'r') as myfile:
    data = myfile.read().replace("'", "\"")

# parse file
articles = json.loads(data)

# read file
with open('status', 'r') as myfile:
    start = int(myfile.read())

for j in range(start, len(words)):
    word = words[j]
    found = False
    w_lower = word.lower()
    art = articles.get(w_lower, None)
    if art is not None:
        write_to_file("output.txt", art + " " + word + "\n")
        found = True

    if len(word) > 5:
        for i in range(2, len(word) - 2):
            art = articles.get(w_lower[i:], None)
            if art is not None:
                write_to_file("output.txt", art + " " + word + "\n")
                found = True
                break

    if not found:
        replaced_word = replace_umlauts(word)
        try:
            search_duden(replaced_word, word)
        except Exception:
            try:
                search_duden(replaced_word.upper(), word.upper())
            except Exception as exc:
                print("error with: " + word)
                write_to_file("error.txt", word + " - " + str(exc) + "\n")

    with open("status", "w") as f:
        f.write(str(j + 1))
