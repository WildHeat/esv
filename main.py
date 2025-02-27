import re
import json


file = open("ESV Bible 2001.txt", 'r')
full = file.read()
short_names = re.findall(r"...\s1:1\s", full)

name_index = {}
prev = -1
next_start = -1

for index in range(len(short_names)):
    if prev == -1:
        prev = re.search(short_names[index], full).span()[0]
    if index == len(short_names)-1:
        next_start = len(full)
    else:
        next_start = re.search(short_names[index+1], full).span()[0]

    # filename = f"chapter/{index + 1}-{short_names[index][:3]}"
    filename = short_names[index][:3]
    name_index[filename] = (prev, next_start - 1)
    # write full books to individual files
    with open(f"books txt/{filename}.txt", 'w') as file:
        file.write(full[prev: next_start - 1])

    prev = next_start

separated = {}

for index in range(len(short_names)):
    coords = name_index[short_names[index][:3]]
    book_text = full[coords[0]:coords[1]]
    chapters = {}
    prev = -1
    next_start = -1
    all_chapter_starts = re.findall(short_names[index][:3] + r"\s\d{1,2}:1\s", book_text)
    for start_of_chapter_index in range(len(all_chapter_starts)):
        chapter_start = all_chapter_starts[start_of_chapter_index]
        if prev == -1:
            prev = re.search(chapter_start, book_text).span()[0]
        if start_of_chapter_index < len(all_chapter_starts)-1:
            next_start = re.search(all_chapter_starts[start_of_chapter_index + 1], book_text).span()[0]
        else:
            next_start = len(book_text)-1

        chapter_text = book_text[prev:next_start]
        verses = {}
        prev_verse_index = -1
        next_verse_index = -1
        all_verses_starts = re.findall(short_names[index][:3] + r"\s\d{1,2}:\d{1,2}\s", chapter_text)
        for start_of_verse_index in range(len(all_verses_starts)):
            verse_start = all_verses_starts[start_of_verse_index]
            if prev_verse_index == -1:
                prev_verse_index = re.search(verse_start, chapter_text).span()[0]
            if start_of_verse_index < len(all_verses_starts) - 1:
                next_verse_index = re.search(all_verses_starts[start_of_verse_index+ 1], chapter_text).span()[0]
            else:
                next_verse_index = len(chapter_text) - 1
            verses[start_of_verse_index + 1] = chapter_text[prev_verse_index:next_verse_index]
            prev_verse_index = next_verse_index
        chapters[int(chapter_start[4:-3])] = verses
        prev = next_start

    separated[short_names[index][:3]] = chapters
    filename = f"books json/{short_names[index][:3]}.json"
    with open(filename, 'w') as file:
        file.write(json.dumps(chapters))

# write full book to one JSON file
filename = "full ESV.json"
with open(filename, 'w') as file:
    file.write(json.dumps(separated))
