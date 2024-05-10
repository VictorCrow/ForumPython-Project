import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

class ForumApp:
    def __init__(self, master):
        self.master = master
        master.title("Fórum")

        self.topics = []

        self.topic_title_label = tk.Label(master, text="Título do Tópico:")
        self.topic_title_label.grid(row=0, column=0, sticky="w")

        self.topic_title_entry = tk.Entry(master, width=50)
        self.topic_title_entry.grid(row=0, column=1, columnspan=2)

        self.topic_content_label = tk.Label(master, text="Conteúdo do Tópico:")
        self.topic_content_label.grid(row=1, column=0, sticky="w")

        self.topic_content_entry = scrolledtext.ScrolledText(master, width=50, height=10)
        self.topic_content_entry.grid(row=1, column=1, columnspan=2)

        self.submit_button = tk.Button(master, text="Publicar Tópico", command=self.submit_topic)
        self.submit_button.grid(row=2, column=0)

        self.clear_button = tk.Button(master, text="Limpar", command=self.clear_fields)
        self.clear_button.grid(row=2, column=1)

        self.quit_button = tk.Button(master, text="Sair", command=master.quit)
        self.quit_button.grid(row=2, column=2)

        self.topic_frame = tk.Frame(master)
        self.topic_frame.grid(row=3, column=0, columnspan=3)

    def submit_topic(self):
        title = self.topic_title_entry.get()
        content = self.topic_content_entry.get("1.0", tk.END)
        if title and content:
            topic = {
                "title": title,
                "content": content,
                "author": "Usuário Anônimo",
                "created_at": datetime.now(),
                "comments": []
            }
            self.topics.append(topic)
            self.display_topics()
            self.clear_fields()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def display_topics(self):
        for widget in self.topic_frame.winfo_children():
            widget.destroy()

        for index, topic in enumerate(self.topics):
            title_label = tk.Label(self.topic_frame, text=f"{index+1}. {topic['title']}")
            title_label.grid(row=index, column=0, sticky="w")

            content_label = tk.Label(self.topic_frame, text=topic['content'][:50] + "...")
            content_label.grid(row=index, column=1, sticky="w")

            like_button = tk.Button(self.topic_frame, text="Like", command=lambda i=index: self.like_topic(i))
            like_button.grid(row=index, column=2)

            comment_button = tk.Button(self.topic_frame, text="Comentar", command=lambda i=index: self.open_comment_window(i))
            comment_button.grid(row=index, column=3)

            comments_label = tk.Label(self.topic_frame, text="Comentários:")
            comments_label.grid(row=index, column=4, sticky="w")
            for comment_index, comment in enumerate(topic["comments"]):
                comment_text = f"{comment['content']} ({comment['likes']} likes)"
                comment_label = tk.Label(self.topic_frame, text=comment_text, wraplength=300, justify="left")
                comment_label.grid(row=index+comment_index, column=4, sticky="w")
                like_comment_button = tk.Button(self.topic_frame, text="Like", command=lambda i=index, j=comment_index: self.like_comment(i, j))
                like_comment_button.grid(row=index+comment_index, column=5)

    def like_topic(self, topic_index):
        messagebox.showinfo("Like", f"Você deu like no tópico: {self.topics[topic_index]['title']}")

    def like_comment(self, topic_index, comment_index):
        self.topics[topic_index]["comments"][comment_index]["likes"] += 1
        self.display_topics()

    def open_comment_window(self, topic_index):
        comment_window = tk.Toplevel(self.master)
        comment_window.title("Comentar Tópico")

        tk.Label(comment_window, text="Comentário:").pack()
        comment_entry = scrolledtext.ScrolledText(comment_window, width=60, height=10)
        comment_entry.pack()

        submit_button = tk.Button(comment_window, text="Enviar Comentário", command=lambda: self.submit_comment(topic_index, comment_entry.get("1.0", tk.END)))
        submit_button.pack()

    def submit_comment(self, topic_index, comment_content):
        if comment_content.strip():
            comment = {
                "author": "Usuário Anônimo",
                "created_at": datetime.now(),
                "content": comment_content,
                "likes": 0
            }
            self.topics[topic_index]["comments"].append(comment)
            self.display_topics()
            messagebox.showinfo("Sucesso", "Comentário enviado com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, insira um comentário.")

    def clear_fields(self):
        self.topic_title_entry.delete(0, "end")
        self.topic_content_entry.delete("1.0", tk.END)

def main():
    root = tk.Tk()
    app = ForumApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()