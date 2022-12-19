from tkinter import *
from tkinter.ttk import Style
from recherche import *

frame = Tk()
frame.title("donner une requête :")
frame.geometry('400x200')
frame.resizable(False, False)


def format_dict(data: dict):
    keys = list(data.keys())

    formatted_dict = ""

    for i in range(len(keys)):
        formatted_dict += f"{keys[i]} : {data[keys[i]]}"
        formatted_dict += "\n" if (i % 2 == 0 or i == 0) else " "

    return formatted_dict


def open_results_window():

    results_window = Toplevel(frame)

    results_window.title("Résultats")

    results_window.geometry("400x600")

    results_window.resizable(False, False)

    results_window.grid_columnconfigure(0, weight=1)
    results_window.grid_rowconfigure(0, weight=1)

    r = inputbox.get(
        1.0, "end-1c")
    array = []
    array.append("Requête : \n")
    array.append(r+"\n")

    traited_r = traitement_requete(r)
    array.append("Requête aprés l'appel de la fonction traitement_requete : \n\n {} \n".format(
        traited_r))

    vect_dict = vecteur_dictionnaire(dict_path)

    array.append("vecteur_dictionnaire : \n\n{}".format(
        format_dict(vect_dict)))

    vect_req = vecteur_requete(vect_dict, traited_r)

    array.append("\n\nvecteur_requete : \n\n{}".format(
        format_dict(vect_req)))

    sim_dict = sim_req_docs(inverse_file_path, docs_path, vect_req)

    array.append("\n\nsim_req_docs : \n\n{}".format(format_dict(sim_dict)))

    sorted_docs = trie_doc(sim_dict)

    array.append("\n\ntrie_doc :\n\n{}".format("\n".join(sorted_docs)))

    mylabel = Label(results_window)
    mylabel.grid()
    text = Text(mylabel, width=40, padx=20, pady=20)
    text.grid(row=0, column=1)
    scrollbar = Scrollbar(mylabel, command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=0, sticky=NSEW)
    text.insert(1.0, "\n".join(array))
    text.config(state=DISABLED)


style = Style()

style.configure('TButton', font=('calibri', 20, 'bold'),
                borderwidth='4')


inputbox = Text(frame, height=10, width=40)
inputbox.pack()


continue_btn = Button(frame, text='Continue!',
                      command=open_results_window, pady=10)
continue_btn.pack()

frame.mainloop()
