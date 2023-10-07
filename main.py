import random
import string
from tkinter import *
from collections import Counter
from tkinter import filedialog
from tkinter.colorchooser import askcolor

def generate_word(n):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(n))

def generate_paragraph(num_of_words, include_numbers=False):
    data = ""
    for _ in range(num_of_words):
        if include_numbers:
            random_number = random.randint(1, 15)
            data += generate_word(random_number)
            data += " "
        else:
            random_number = random.randint(1, 10)
            if random_number != 10:  # 10% chance of including a number
                data += generate_word(random_number)
                data += " "
            else:
                random_num = random.randint(0, 999)
                data += str(random_num)
                data += " "
    return data.strip()

def generate_and_display_paragraph():
    num_of_words = int(input_entry.get())
    include_numbers = include_numbers_var.get()
    text_color = text_color_var.get()
    
    para_data = generate_paragraph(num_of_words, include_numbers)
    para_label = Label(container, text=para_data, padx=10, pady=10, bg="lightgray", fg=text_color)
    para_label.pack()
    generated_paragraphs.append(para_data)
    update_word_frequency()
    update_word_count()

def clear_generated_paragraphs():
    for widget in container.winfo_children():
        widget.destroy()
    generated_paragraphs.clear()
    update_word_frequency()
    update_word_count()

def save_paragraphs_to_file():
    with open("generated_paragraphs.txt", "w") as file:
        for para in generated_paragraphs:
            file.write(para + "\n")
    status_label.config(text="Paragraphs saved to generated_paragraphs.txt")

def load_paragraphs_from_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            paragraphs = file.read().splitlines()
            for para in paragraphs:
                para_label = Label(container, text=para, padx=10, pady=10, bg="lightgray", fg=text_color_var.get())
                para_label.pack()
                generated_paragraphs.append(para)
        status_label.config(text="Paragraphs loaded from file")
        update_word_count()

def update_word_frequency():
    word_frequency = Counter(' '.join(generated_paragraphs).split())
    word_freq_text.delete(1.0, END)
    for word, freq in word_frequency.items():
        word_freq_text.insert(END, f"{word}: {freq}\n")
    
    # Display a histogram of word frequencies
    histogram_text.config(state=NORMAL)
    histogram_text.delete(1.0, END)
    max_freq = max(word_frequency.values())
    for word, freq in word_frequency.items():
        histogram_text.insert(END, f"{word}: {'#' * (freq * 50 // max_freq)} ({freq})\n")
    histogram_text.config(state=DISABLED)

def update_word_count():
    word_count_text.config(state=NORMAL)
    word_count_text.delete(1.0, END)
    for para in generated_paragraphs:
        words = para.split()
        word_count_text.insert(END, f"Para {generated_paragraphs.index(para) + 1}: {len(words)} words\n")
    word_count_text.config(state=DISABLED)

def search_words():
    search_term = search_entry.get()
    if not search_term:
        return
    found_paragraphs = []
    for para in generated_paragraphs:
        if search_term in para:
            found_paragraphs.append(para)
    if found_paragraphs:
        search_result_text.config(state=NORMAL)
        search_result_text.delete(1.0, END)
        for para in found_paragraphs:
            search_result_text.insert(END, para + "\n")
        search_result_text.config(state=DISABLED)
    else:
        search_result_text.config(state=NORMAL)
        search_result_text.delete(1.0, END)
        search_result_text.insert(END, "No matches found.")
        search_result_text.config(state=DISABLED)

def remove_paragraph():
    selected_para = remove_para_var.get()
    if selected_para:
        generated_paragraphs.pop(int(selected_para) - 1)
        update_word_frequency()
        update_word_count()
        clear_generated_paragraphs()
        for para in generated_paragraphs:
            para_label = Label(container, text=para, padx=10, pady=10, bg="lightgray", fg=text_color_var.get())
            para_label.pack()

# Create a GUI window using Tkinter
root = Tk()
root.title("Random Paragraph Generator")

container = Frame(root, padx=10, pady=10)
container.pack()

input_label = Label(container, text="Number of Words:")
input_label.pack()
input_entry = Entry(container)
input_entry.pack()

include_numbers_var = BooleanVar()
include_numbers_var.set(False)
include_numbers_checkbox = Checkbutton(container, text="Include Numbers", variable=include_numbers_var)
include_numbers_checkbox.pack()

text_color_var = StringVar()
text_color_var.set("black")
text_color_button = Button(container, text="Choose Text Color", command=lambda: text_color_var.set(askcolor()[1]))
text_color_button.pack()

generate_button = Button(container, text="Generate Paragraph", command=generate_and_display_paragraph)
generate_button.pack()

clear_button = Button(container, text="Clear Paragraphs", command=clear_generated_paragraphs)
clear_button.pack()

save_button = Button(container, text="Save Paragraphs", command=save_paragraphs_to_file)
save_button.pack()

load_button = Button(container, text="Load Paragraphs", command=load_paragraphs_from_file)
load_button.pack()

status_label = Label(container, text="", fg="green")
status_label.pack()

word_freq_label = Label(container, text="Word Frequency Analysis:")
word_freq_label.pack()
word_freq_text = Text(container, height=10, width=40)
word_freq_text.pack()

histogram_label = Label(container, text="Word Frequency Histogram:")
histogram_label.pack()
histogram_text = Text(container, height=10, width=40, state=DISABLED)
histogram_text.pack()

word_count_label = Label(container, text="Word Count per Paragraph:")
word_count_label.pack()
word_count_text = Text(container, height=5, width=40, state=DISABLED)
word_count_text.pack()

search_label = Label(container, text="Search for Words:")
search_label.pack()
search_entry = Entry(container)
search_entry.pack()
search_button = Button(container, text="Search", command=search_words)
search_button.pack()
search_result_text = Text(container, height=5, width=40, state=DISABLED)
search_result_text.pack()

remove_para_label = Label(container, text="Remove Paragraph (by index):")
remove_para_label.pack()
remove_para_entry = Entry(container)
remove_para_entry.pack()
remove_para_button = Button(container, text="Remove", command=remove_paragraph)
remove_para_button.pack()
remove_para_var = StringVar()
remove_para_entry.config(textvariable=remove_para_var)

generated_paragraphs = []

root.mainloop()
