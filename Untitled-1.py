from tkinter import *
import sqlite3

root = Tk()
root.title("login")
root.geometry("230x200")
#tallenetaan ikkunan korkeus muuttujaan jottai voidaan muuttaa sitä helposti
root.taskheight = "265"

#luodaan ikkuna johon päästään sisään kirjautumalla
def taskScreen():
    global taskSC
    taskSC = Tk()
    taskSC.title("Task screen")
    taskSC.geometry("270x" + root.taskheight)

    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("Drop table if exists tasks")

    sql='''CREATE TABLE tasks (
        task VARCHAR(255)
    )'''

    c.execute(sql)
    conn.commit()
    conn.close()

    task_label = Label(taskSC, text="Tehtävä")
    task_label.grid(row=0, column=0, pady=(10,0))

    taskScreen.task = Entry(taskSC, width=30)
    taskScreen.task.grid(row=0, column=1, padx=20, pady=(10,0))

    submit_btn = Button(taskSC, text="Lisää tehtävä tietokantaan", command=lambda:[submit(), query()])
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    select_label = Label(taskSC, text="Valitse ID")
    select_label.grid(row=4, column=0, pady=5)

    taskScreen.delete_box = Entry(taskSC, width=30)
    taskScreen.delete_box.grid(row=5, column=1, pady=5)

    delete_btn = Button(taskSC, text="Poista tehtävä", command=lambda:[delete(), query()])
    delete_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    edit_btn = Button(taskSC, text="Muokkaa tehtävää", command=edit)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

def query():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    c.execute("SELECT task, oid FROM tasks")
    records = c.fetchall()
    print_records = " "

    for record in records:
        print_records += str(record[0]) + " \t " + str(record[1]) + "\n"

    heading_label = Label(taskSC, text="Helvetica", font=("Helvetica", 16))

    heading_label['text'] = "Tehtävä \t ID"
    heading_label.grid(row=8, column=0, columnspan=2) 

    #sain tämän kohdan allulta
    if hasattr(taskSC, 'query_label'):
        taskSC.query_label['text'] = print_records
    else:
        taskSC.query_label = Label(taskSC, text=print_records)
        taskSC.query_label.grid(row=9, column=0, columnspan=2)

    conn.commit()
    conn.close()


def submit():
    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    if taskScreen.task.get() != "":
        c.execute("INSERT INTO tasks VALUES (:task)",
            {
                'task' : taskScreen.task.get()
            })
        #aina kun submitti tapahtuu niin ja teksti kenttä ei ole tyhjä niin lisää 15 pixeliä ruudun korkeuteen
        root.taskheight = int(root.taskheight) + 15
        taskSC.geometry("270x" + str(root.taskheight))
    
    conn.commit()
    conn.close()
    
    taskScreen.task.delete(0, END)
    

def delete():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()

    if taskScreen.delete_box.get() != "":
        c.execute("DELETE FROM tasks WHERE oid=" + taskScreen.delete_box.get())
        taskScreen.delete_box.delete(0, END)

    conn.commit()
    conn.close()
    #deleten kohdalla lähtee 15 pixeliä ruudun korkeudesta
    root.taskheight = int(root.taskheight) - 15
    taskSC.geometry("270x" + str(root.taskheight))

def update():
    conn = sqlite3.connect("tasklist.db")
    c = conn.cursor()
    record_id = taskScreen.delete_box.get()

    c.execute("""UPDATE tasks SET
        task = :task
              
        WHERE oid = :oid""",
        {
            'task': task_editor.get(),
            'oid': record_id
        })

    conn.commit()
    conn.close()
    editor.destroy()
    query()

def edit():
    global editor
    editor = Tk()
    editor.title("Päivitä")
    editor.geometry("300x100")

    conn = sqlite3.connect("tasklist.db")

    c = conn.cursor()

    record_id = taskScreen.delete_box.get()
    c.execute("SELECT * FROM tasks WHERE oid = " + record_id)
    records=c.fetchall()

    global task_editor

    task_label = Label(editor, text="Tehtävä")
    task_label.grid(row=0, column=0, pady=(10,0))

    task_editor = Entry(editor, width=30)
    task_editor.grid(row=0, column=1, padx=20, pady=(10,0))

    for record in records:
        task_editor.insert(0, record[0])

    save_btn = Button(editor, text="Tallenna", command=update)
    save_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

def login():
    login.user = username.get()
    login.password = password.get()

    #Tämä kohta kertoo jos käyttäjänimi tai salasana on virheellinen
    if login.password == "admin" and login.user == "admin":
        taskScreen()
        root.destroy()
    else:
        error_label.config(text="Käyttäjänimi tai salasana on virheellinen")



username_label = Label(root, text="Käyttäjänimi")
username_label.grid(row=0, column=1, pady=(10,0))

username = Entry(root, width=30)
username.grid(row=1, column=1, padx=20, pady=(10,0))

password_label = Label(root, text="Salasana")
password_label.grid(row=2, column=1, pady=(10,0))

password = Entry(root, width=30, show="*")
password.grid(row=3, column=1, padx=20, pady=(10,0))

login_btn = Button(root, text="Kirjaudu", command=login)
login_btn.grid(row=4, column=1, columnspan=2, pady=10, padx=10)

error_label = Label(root, text="")
error_label.grid(row=5, column=1, pady=(10,0))

root.mainloop()
