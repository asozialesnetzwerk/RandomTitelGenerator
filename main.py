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
    elif ", die" in title:
        return "die"
    elif ", das" in title:
        return "das"
    else:
        return None


def replace_umlauts(word_to_replace):
    return word_to_replace.lower() \
        .replace("ä", "ae") \
        .replace("ö", "oe") \
        .replace("ü", "ue") \
        .replace("ß", "ss") \
        .capitalize()


def search_duden(search, not_replaced_word):
    result = duden.search(search)
    if len(result) > 0:
        article = get_article(result[0].title)
        if article is not None:
            article = article.capitalize()
            articles[not_replaced_word.lower()] = article
            write_to_file("output.txt", article + " " + not_replaced_word + "\n")
            with open("article.json", "w") as article_json_file:
                article_json_file.write(str(articles))


def write_to_file(file_name, val):
    with open(file_name, "a") as f:
        f.write(val)


words = open("sorted_words").read().splitlines()

print(len(words))
# words = ["Test", "Schnelltest", "Pinguin", "Test", "Känguru"]

output = open("output.txt", "w")
output.write("")
output.close()

# read file
with open('article.json', 'r') as myfile:
    data = myfile.read().replace("'", "\"")

# parse file
articles = json.loads(data)

for j in range(0, len(words)):
    with open("status", "w") as f:
        f.write(str(j))
    word = words[j]
    found = False
    for i in range(len(word) - 2):
        w_lower = word.lower()
        art = articles.get(w_lower[i:], None)
        if art is not None:
            write_to_file("output.txt", art + " " + word + "\n")
            found = True
            break

    if not found:
        replaced_word = replace_umlauts(word)
        try:
            search_duden(replaced_word, word)
        except:
            try:
                search_duden(replaced_word.upper(), word.upper())
            except:
                print("error with: " + word)
                write_to_file("error.txt", word + "\n")
