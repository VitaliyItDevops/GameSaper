import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    0: 'white',
    1: 'blue',
    2: 'green',
    3: 'Red',
    4: 'Yellow',
    5: 'Orange',
    6: 'Purple',
    7: 'gray',
    8: 'Azure',
}

class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='calibri 15 bold')
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}'


class Saper:
    window = tk.Tk()
    window.title("Saper")
    photo = tk.PhotoImage(file='logo.png')
    window.iconphoto(False, photo)
    window.config(bg='Yellow')
    right = 7
    down = 10
    mines = 13
    is_game_over = False
    is_first_click = True

    def __init__(self):
        self.buttons = []
        for i in range(Saper.right + 2):
            temp = []
            for j in range(Saper.down + 2):
                btn = MyButton(Saper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        if Saper.is_game_over:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):

        if Saper.is_game_over:
            return

        if Saper.is_first_click:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            Saper.is_first_click = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            Saper.is_game_over = True
            showinfo('Game Over', 'Вы проиграли')
            for i in range(1, Saper.right + 1):
                for j in range(1, Saper.down + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground='black')
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    # if not abs(dx - dy) == 1:
                    #     continue

                    next_btn = self.buttons[x + dx][y + dy]
                    if not next_btn.is_open and 1 <= next_btn.x <= Saper.right and \
                            1 <= next_btn.y <= Saper.down and next_btn not in queue:
                        queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        Saper.is_first_click = True
        Saper.is_game_over = False

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0, padx=10)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, Saper.right)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество колоннок').grid(row=1, column=0, padx=10)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, Saper.down)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0, padx=10)
        mine_entry = tk.Entry(win_settings)
        mine_entry.insert(0, Saper.mines)
        mine_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mine_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mine: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mine.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неправильное значение')
            return

        Saper.right = int(row.get())
        Saper.down = int(column.get())
        Saper.mines = int(mine.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Меню', menu=settings_menu)

        count = 1
        for i in range(1, Saper.right + 1):
            for j in range(1, Saper.down + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, sticky='NWES')
                count += 1

        for i in range(1, Saper.right + 1):
            Saper.window.rowconfigure(i, weight=1)
        for j in range(1, Saper.down + 1):
            Saper.window.columnconfigure(j, weight=1)

    def open_all_buttons(self):
        for i in range(Saper.right + 2):
            for j in range(Saper.down + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        Saper.window.mainloop()

    def print_buttons(self):
        for i in range(1, Saper.right + 1):
            for j in range(1, Saper.down + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)

        for i in range(1, Saper.right + 1):
            for j in range(1, Saper.down + 1):
                btn = self.buttons[i][j]

                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(1, Saper.right + 1):
            for j in range(1, Saper.down + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, Saper.down * Saper.right + 1))
        print(f'Исключаем кнопку {exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:Saper.mines]



game = Saper()
game.start()
