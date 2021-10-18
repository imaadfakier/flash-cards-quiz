import tkinter
import pandas
# import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"


def word_is_known():
    known_word = canvas.itemcget(canvas_language_word, 'text')
    for same_dict in language_data_dict:
        if known_word != same_dict[language_data.columns[0]]:
            continue
        language_data_dict.remove(same_dict)  # <--- learned something new
        break

    words_to_learn_df = pandas.DataFrame(data=language_data_dict)
    words_to_learn_df.to_csv(path_or_buf='./data./words_to_learn.csv', index=False)  # to avoid bug of duplicate sets of
                                                                                     # indices being saved/written to
                                                                                     # csv file
    new_random_word()


def new_random_word():
    global timer
    window.after_cancel(id=timer)

    random_language_word = random.choice(language_data_dict)[language_data.columns[0]]
    # canvas.itemconfig(tagOrId=canvas, bg=BACKGROUND_COLOR)  # applicable only for canvas widgets
                                                              # - not the canvas itself!
    canvas.itemconfig(tagOrId=current_card_image, image=french_card_image)
    canvas.itemconfig(tagOrId=canvas_language_name, text=language_data.columns[0], fill='black')
    canvas.itemconfig(tagOrId=canvas_language_word, text=random_language_word, fill='black')

    timer = start_timer()


# ---------------------------- UI SETUP ------------------------------- #
# window
window = tkinter.Tk()
window.title(string='Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(ms=3000, func=new_random_word)

# canvas widget
canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# canvas widget image
french_card_image = tkinter.PhotoImage(file='./images/card_front.png')
english_card_image = tkinter.PhotoImage(file='./images/card_back.png')
current_card_image = canvas.create_image(400, 263, image=french_card_image)
canvas.grid(row=0, column=0, columnspan=2)

# canvas widget text
canvas_language_name = canvas.create_text(400, 150, text='', fill='black', font=('Ariel', 40, 'italic'))
canvas_language_word = canvas.create_text(400, 263, text='', fill='black', font=('Ariel', 60, 'bold'))

# buttons
error_image = tkinter.PhotoImage(file='./images/wrong.png')
error_button = tkinter.Button(image=error_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=new_random_word)
error_button.grid(row=1, column=0)
success_image = tkinter.PhotoImage(file='./images/right.png')
success_button = tkinter.Button(image=success_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=word_is_known)
success_button.grid(row=1, column=1)


# ---------------------------- FLASH CARDS MECHANISM ------------------------------- #
def display_english_translation():
    english_word = ''

    for the_dict in language_data_dict:
        if canvas.itemcget(canvas_language_word, 'text') not in the_dict[language_data.columns[0]]:
            continue
        english_word = the_dict[language_data.columns[1]]
        break

    canvas.itemconfig(tagOrId=current_card_image, image=english_card_image)
    canvas.itemconfig(tagOrId=canvas_language_name, text=language_data.columns[1], fill='white')
    canvas.itemconfig(tagOrId=canvas_language_word, text=english_word, fill='white')


def start_timer():
    global timer
    timer = window.after(ms=3000, func=display_english_translation)
    return timer


language_data = ''
try:
    language_data = pandas.read_csv(filepath_or_buffer='./data/words_to_learn.csv')
except FileNotFoundError:
    language_data = pandas.read_csv(filepath_or_buffer='./data/french_words.csv')
    # language_data_dict = language_data.to_dict(orient='records')
# else:
    # language_data_dict = language_data.to_dict(orient='records')
finally:
    language_data_dict = language_data.to_dict(orient='records')
    new_random_word()

# -------------- KEEP WINDOW FROM AUTOMATICALLY CLOSING --------------- #
window.mainloop(n=0)
