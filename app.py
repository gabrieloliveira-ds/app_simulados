import tkinter as tk
import random
import json
from tkinter import font
from queue import Queue

class Sessao:
    def __init__(self, root):
        self.root = root
        self.question_queue = Queue()
        self.load_questions()

        self.pergunta = Pergunta(root, "")
        self.opcoes = Opcoes(root)
        self.resposta = Resposta(root)
        self.submit = Submit(root, self.on_submit)

        self.total_questions = len(self.questions)
        self.current_question_count = 0

        self.next_question()

    def load_questions(self):
        with open("database.json", "r") as f:
            self.questions = json.load(f)
            random.shuffle(self.questions)
            for question in self.questions:
                self.question_queue.put(question)

    def on_submit(self):
        self.next_question()

    def next_question(self):
        if not self.question_queue.empty():
            self.current_question = self.question_queue.get()
            print(self.current_question)
            self.pergunta.update(self.current_question["question"])
            self.opcoes.update(self.current_question["options"])
            self.resposta.update(self.current_question["answer"])
            self.resposta.hide()
            self.submit.update_result("")
            self.current_question_count += 1
        else:
            self.show_result()

    def show_result(self):
        self.root.destroy()
        result_window = tk.Tk()
        result_window.title("Resultado")

        resultado = Resultado(result_window, self.total_questions, self.current_question_count)
        resultado.show()

class Pergunta:
    def __init__(self, root, question):
        frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.label = tk.Label(frame, text=question,font=font.Font(family="Montserrat", size=13, weight="bold"))
        self.label.pack(padx=20, pady=10)

    def update(self, question):
        self.label.config(text=question)

class Opcoes:
    def __init__(self, root):
        self.option_buttons = []
        self.option_selected = tk.StringVar()
        frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        options = {"A": "", "B": "", "C": "", "D": "","E":""}
        for option_key, option_text in options.items():
            button = tk.Radiobutton(frame, text=f"{option_key}) {option_text}", variable=self.option_selected, value=option_key, font=font.Font(family="Montserrat", size=11))
            button.option = option_key
            button.pack(anchor="w", padx=10, pady=5)
            self.option_buttons.append(button)

    def update(self, options):
        for button, option_key in zip(self.option_buttons, options):
            button.config(text=f"{option_key}) {options[option_key]}")




class Submit:
    def __init__(self, root, on_submit):
        self.submit_button = tk.Button(root, text="Próxima Pergunta", command=on_submit)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def update_result(self, result):
        self.result_label.config(text=result)

class Resultado:
    def __init__(self, root, total_questions, current_question_count):
        self.root = root
        self.total_questions = total_questions
        self.current_question_count = current_question_count

    def show(self):
        tk.Label(self.root, text=f"Você respondeu {self.current_question_count} de {self.total_questions} perguntas.").pack(padx=20, pady=20)
        tk.Button(self.root, text="Fechar", command=self.root.destroy).pack()

class Resposta:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="", fg="red")
        self.label.pack()

        self.mostrar_button = tk.Button(root, text="Mostrar Alternativa Correta", command=self.show)
        self.mostrar_button.pack()

    def update(self, answer):
        self.label.config(text=f"Alternativa correta: {answer.upper()}")

    def hide(self):
        self.label.pack_forget()

    def show(self):
        self.label.pack()

    def show_correct_answer(self):
        if hasattr(self.opcoes, 'show_correct_option'):
            if hasattr(self.root.master, 'current_question'):
                correct_answer = self.root.master.current_question["answer"]
                self.opcoes.show_correct_option(correct_answer)

# Cria a janela principal


root = tk.Tk()
root.title("Pergunta de Múltipla Escolha")

# Cria a sessão do jogo
sessao = Sessao(root)

# Inicia o loop principal da interface gráfica
root.mainloop()