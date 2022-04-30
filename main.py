from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror
from datetime import datetime
import time


class App(Tk):
  def __init__(self):
    super().__init__()
    self.title('SnowFall - converter')
    self.iconbitmap('SFlogo.ico')

    #Prohibit resizing
    self.resizable(width=False, height=False)

    #Create a window in the center of the screen
    width_of_window = 500
    height_of_window = 200
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    self.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

    #Global variable to write to the table (row)
    self.tree_row = 0

    # Create NoteBook
    tab_control = ttk.Notebook(self)
    tab_control.pack(fill=BOTH, expand=True)
    # Create Frames
    tab_main = Frame(tab_control)
    tab_main.configure(background='#249794')
    tab_history = ttk.Frame(tab_control)
    tab_control.add(tab_main, text='main')
    tab_control.add(tab_history, text='history')
    # Create Treeview
    self.my_tree = ttk.Treeview(tab_history)
    # Create vertical scrollbar
    tree_scroll = Scrollbar(tab_history,orient='vertical')
    tree_scroll.pack(side=RIGHT, fill=Y)
    self.my_tree = ttk.Treeview(tab_history, yscrollcommand=tree_scroll.set, selectmode='extended')
    self.my_tree.pack()
    tree_scroll.config(command=self.my_tree.yview)
    # Define our columns
    self.my_tree['columns'] = ('Input','Output','Task')
    #Formate our columns
    self.my_tree.column('#0', width=0, stretch=NO)
    self.my_tree.column('Input', anchor=W, width=150)
    self.my_tree.column('Output', anchor=W, width=150)
    self.my_tree.column('Task', anchor=W, width=200)
    #Create heading
    self.my_tree.heading('#0', text='')
    self.my_tree.heading('Input', text='Input',anchor=N)
    self.my_tree.heading('Output', text='Output',anchor=N)
    self.my_tree.heading('Task', text='Task',anchor=N)
    #Pack to the screen
    self.my_tree.pack(pady=20)

    #User input field
    entry = Entry(tab_main,justify=CENTER,foreground='#249794')
    entry.place(x=50,y=10)
    entry.focus()

    conv_menu = StringVar()
    conv_cb = ttk.Combobox(tab_main, textvariable=conv_menu)
    conv_cb['values'] = ('sec to time','unixtime to time','fahrenheit to celsius','celsius to fahrenheit')
    conv_cb['state'] = 'readonly'
    conv_cb.current(0)
    conv_cb.place(x=190,y=9)

    conv_button = Button(tab_main,text='Convert',command=lambda: self.conv([conv_menu.get(),entry.get()]))
    conv_button.place(x=350,y=8,width=100)

    #info label
    self.label = Label(tab_main,text=f'',fg='white',bg='#249794')
    self.label.config(font=('Calibri (Body)',10))
    self.label.place(x=175,y=55)

    #my labels :)
    l1=Label(tab_main,text='SnowFall',fg='powderblue',bg='#249794')
    lst1=('Calibri (Body)',18,'bold')
    l1.config(font=lst1)
    l1.place(x=110,y=100)

    l2=Label(tab_main,text='production',fg='powderblue',bg='#249794')
    lst2=('Calibri (Body)',18)
    l2.config(font=lst2)
    l2.place(x=222,y=102)

    self.my_tree.bind('<Double-1>', self.edit_cell)

  def edit_cell(self,e):
    column = self.my_tree.identify_column(e.x)
    item = self.my_tree.identify_row(e.y)
    try:
      x,y,width,height = self.my_tree.bbox(item,column)
    except ValueError:
      return
    value = self.my_tree.set(item,column)
    entry = ttk.Entry(self.my_tree)
    entry.place(x=x,y=y,width=width,height=height,anchor='nw')
    entry.insert(0,value)
    entry.bind('<FocusOut>',lambda e: entry.destroy())

  def conv(self,val):
    try:
      data = float(val[1])
    except ValueError:
      showerror(
        title='Error',
        message='Data entry error. Please check the correctness (numbers only)')
      return()
    self.label['text'] = ''
    header = val[0]
    if header == 'sec to time':
      try:
        ty_res = time.gmtime(data)
      except (OSError,OverflowError):
        showerror(
          title='Error',
          message='Data entry error. Please check the correctness')
        return()
      res = time.strftime('%H:%M:%S',ty_res)
    elif header == 'unixtime to time':
      res = datetime.utcfromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S')
    elif header == 'fahrenheit to celsius':
      res = round((data - 32) * 5/9, 1)
    elif header == 'celsius to fahrenheit':
      res = round(data * 9/5 + 32, 1)
    showinfo(
      title='Info',
      message=f'output: {res}')
    self.label['text'] = f'{val[1]} = {res}'
    self.my_tree.insert(parent='',index='end',iid=self.tree_row,text='',values=(val[1],res,header))
    self.tree_row+=1

if __name__ == "__main__":
  app = App()
  app.mainloop()