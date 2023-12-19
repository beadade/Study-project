from typing import Optional
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk

# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark

from a3_support import *


# Write your classes here
class Model:
    def __init__(self) -> None:
        self._list = []
        for i in range(4):
            self._list.append([None, None, None, None])
        self.add_tile()
        self.add_tile()
        self._score = 0
        self._undos = MAX_UNDOS
        self.old_boards = []

    def replace_list(self, new_list: list[list[Optional[int]]]):
        self._list = new_list
        ''''''''''
        Call the stored list data
        '''''

    def replace_score(self, new_score: int):
        self._score = new_score
        '''''
        call the stored score data
        '''''

    def replace_undos(self, new_undos: int):
        self._undos = new_undos
        '''''''''
        call the stored undos data
        '''''

    def replace_undos_board(self, undos_board: list[list[Optional[int]]], undos_score:list):
        self.old_boards = undos_score + undos_board
        '''''''''
        call the stored old_boards data
        '''''

    def add_old_board(self,Board:list[list[Optional[int]]]):
        self.old_boards.append(Board)

    def add_old_score(self,Score:int):
        self.old_boards.append(Score)

    def new_game(self) -> None:
        self._list = []
        for i in range(4):
            self._list.append([None, None, None, None])
        self.add_tile()
        self.add_tile()
        self._score = 0
        self._undos = MAX_UNDOS
        self.old_boards = []
        '''''''''
        start new game and recovery the function
        '''

    def get_tiles(self) -> list[list[Optional[int]]]:

        return self._list
    ''''''''''
    get list 
    '''''

    def add_tile(self) -> None:
        board_full = True
        for row in self._list:
            for tile in row:
                if tile == None:
                    board_full = False
        if board_full is False:
            res = generate_tile(self.get_tiles())
            self.get_tiles()[res[0][0]][res[0][1]] = res[1]
    '''''''''
    generate  random number from empty list position
    '''''

    def move_left(self) -> None:
        self._list = stack_left(self.get_tiles())
        self._list, score_added = combine_left(self._list)
        self._list = stack_left(self._list)
        self._score = score_added + self._score
    '''''''''
    move left and stack tiles from list, when board move the old_board append old score 
    accumulate score when move
    '''''

    def move_right(self) -> None:
        self._list = reverse(self.get_tiles())
        self.move_left()
        self._list = reverse(self.get_tiles())
    '''''''''
    Moves all tiles to their right extreme
    '''''

    def move_up(self) -> None:
        self._list = transpose(self.get_tiles())
        self.move_left()
        self._list = transpose(self.get_tiles())
    '''''''''
       Moves all tiles to their up extreme
    '''''

    def move_down(self) -> None:
        self._list = transpose(self.get_tiles())
        self.move_right()
        self._list = transpose(self.get_tiles())
    '''''''''
           Moves all tiles to their down extreme
        '''''

    def attempt_move(self, move: str) -> bool:
        new_list = self._list[:]
        if move == UP:
            self.move_up()
        elif move == DOWN:
            self.move_down()
        elif move == LEFT:
            self.move_left()
        elif move == RIGHT:
            self.move_right()

        return self._list != new_list
    '''''''''
    Call the move function
    '''''

    def has_won(self) -> bool:
        for row in self._list:
            for tile in row:
                return tile == 2048
    '''''
    one of tiles equall 2048 the game will be win
    '''

    def has_lost(self) -> bool:
        new_board = self._list[:]
        old_score = self._score
        for row in self._list:
            for tile in row:
                if tile is None:
                    return False
        if self.attempt_move('d') or self.attempt_move('a')\
                or self.attempt_move('s') or self.attempt_move('w') :
            self._list = new_board
            self._score = old_score
            return False
        else:
            return True
    '''''''''
    judge the game will be lost if every move function equal False
    '''
    def get_score(self) -> int:

        return self._score

    def get_undos_remaining(self):

        return self._undos

    def use_undo(self) -> None:
        if self._undos == 0:
            return
        if self.old_boards == []:
            return
        if self._undos > 0 :
            self._list = self.old_boards.pop()
            self._score =self.old_boards.pop()
        self._undos = self._undos - 1
    '''''
    pop will return value ,first value is old_boards and second remain old_score
    '''

class GameGrid(tk.Canvas):

    def __init__(self, master: tk.Tk, **kwargs) -> None:

        super().__init__(master, width=BOARD_WIDTH, height=BOARD_HEIGHT,
                         bg=BACKGROUND_COLOUR, **kwargs)

    def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
        x, y = position
        x_min = BUFFER + x * 100
        y_min = BUFFER + y * 100
        x_max = x_min + 100 - BUFFER
        y_max = y_min + 100 - BUFFER
        return x_min, y_min, x_max, y_max
    '''''''''
    get 4 position by 2 point in the canvas 
    '''

    def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
        x_min, y_min, x_max, y_max = self._get_bbox(position)
        x_mid = int((x_min + x_max) / 2)
        y_mid = int((y_min + y_max) / 2)
        return x_mid, y_mid

    '''''''''
       get midpoint in the canvas 
       '''

    def clear(self) -> None:

        self.delete(tk.ALL)

    def redraw(self, tiles: list[list[Optional[int]]]) -> None:
        self.clear()
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                self.create_rectangle(self._get_bbox((x, y)), outline=BACKGROUND_COLOUR, fill=COLOURS[tile])
                if tile is not None:
                    self.create_text(self._get_midpoint((x, y)), text=tile, font=TILE_FONT, fill=FG_COLOURS[tile])
    '''''''''
    get every rectangle position and get every tiles in the list
    '''

class Game:
    def __init__(self, master: tk.Tk) -> None:
        self.model = Model()
        self.gameGrid = GameGrid(master)
        self.gameGrid.redraw(self.model.get_tiles())
        self._master = master
        master.title('CSSE1001/7030 2022 Semester 2 A3')
        textLable = tk.Label(master, text='2048', font=TITLE_FONT, bg=COLOURS[2048], width=10, fg=FG_COLOURS[2048])
        textLable.pack(side=tk.TOP)
        self.gameGrid.pack()
        self.statusBar = StatusBar(master)
        self.statusBar.pack()
        master.bind('<Key>', self.attempt_move)
        self.statusBar.set_callbacks(self.start_new_game,self.undo_previous_move)
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save game",command=self.save_file)
        filemenu.add_command(label="Load game",command=self.load_file)
        filemenu.add_command(label="New game", command=self.start_new_game)
        filemenu.add_command(label="Quit",command=self.quit)
        self._filename = ''

    def draw(self) -> None:
        self.gameGrid.redraw(self.model.get_tiles())
        self.statusBar.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
    '''''''''
    display tiles and core ,remaining undos
    '''

    def attempt_move(self, event: tk.Event) -> None:
        if (event.char.upper() not in ['A', 'W', 'S', 'D']):
            return
        copied_score = self.model.get_score()
        copied_list = []
        for i in self.model.get_tiles():
            copied_list.append(i[:])
        has_changed = self.model.attempt_move(event.char)
        self.draw()
        if self.model.has_won():
            reply = messagebox.askquestion(type=messagebox.YESNO,
                                           title="WIN",
                                           message=WIN_MESSAGE)
            if reply == messagebox.YES:
                self.start_new_game()
            elif reply == messagebox.NO:
                self._master.destroy()
        elif has_changed:
            self.model.add_old_score(copied_score)
            self.model.add_old_board(copied_list)
            self._master.after(150, self.new_tile)
        '''''''''''
        ues keyboards to call move function and if has won will be show askquestion
        and not won will generate new tile
        '''''

    def new_tile(self) -> None:
        self.model.add_tile()
        self.draw()
        if self.model.has_lost():
            reply = messagebox.askquestion(type=messagebox.YESNO,
                                           title="Lost",
                                           message=LOSS_MESSAGE)
            if reply == messagebox.YES:
                self.start_new_game()
            elif reply == messagebox.NO:
                self._master.destroy()
        '''''''''
        call add tile function,if the game has lost the askquestion will show 
        '''

    def undo_previous_move(self) -> None:
        self.model.use_undo()
        self.draw()
        '''''''''
        call move function
        '''

    def start_new_game(self) -> None:
        self.model.new_game()
        self.draw()
    '''''''''
    call move function
    '''''

    def quit(self) -> None:
        reply = messagebox.askquestion(type=messagebox.YESNOCANCEL,
                               title="Quit",
                               message="Would you like to quit this file?")
        if reply == messagebox.YES:
            self._master.destroy()
    '''''''''
    game quit and exit
    '''''

    def save_file(self) -> None:
        s_tiles = str(self.model.get_tiles())
        s_score= str(self.model.get_score())
        s_undos = str(self.model.get_undos_remaining())
        if self.model.old_boards!= []:
            s_old_board = str(self.model.old_boards.pop())
            s_old_score = str(self.model.old_boards.pop())
            with filedialog.asksaveasfile() as f:
                f.writelines([s_tiles, '*', s_score, '*', s_undos, '*', s_old_board, '*', s_old_score])
        else:
            with filedialog.asksaveasfile() as f:
                f.writelines([s_tiles,'*',s_score, '*', s_undos,'*'])
        '''''''''
        Store old data in a file, use pop methods to find data
        '''''

    def load_file(self):
        list = ""
        score = ''
        undos = ''
        undos_board = ''
        undos_score = ''
        '''''''''
        Since you are storing strings, you need to remove some useless strings
        '''''
        with filedialog.askopenfile() as file:
            file_line = file.readline()
            file_line = file_line.split("*")
            for line in file_line[0]:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    line = line.replace(" ", "")
                    list += line

            for line in file_line[1]:
                line = line.replace(" ", "")
                score += line

            for line in file_line[2]:
                line = line.replace(" ", "")
                undos += line

            for line in file_line[3]:
                line = line.replace("[", "")
                line = line.replace("]", "")
                line = line.replace(" ", "")
                undos_board += line

            for line in file_line[4]:
                line = line.replace(" ", "")
                undos_score += line

        list = list.split(",")
        undos_board = undos_board.split(',')
        score = int(score)
        undos = int(undos)
        undos_score = [int(undos_score)]

        board = []  # Create a new board and add something to it
        count = 0
        for i in range(4):
            row = []
            for j in range(4):
                character = list[count]
                count += 1
                if character == "None":
                    row.append(None)
                else:
                    row.append(int(character))
            board.append(row)
        count1 = 0
        undos_board1 = []
        for i in range(4):
            row1 = []
            for j in range(4):
                character = undos_board[count1]
                if character == "None":
                    row1.append(None)
                else:
                    row1.append(int(character))
                count1 += 1
            undos_board1.append(row1)
        undos_board1 = [undos_board1]
        self.model.replace_list(board)
        self.model.replace_score(score)
        self.model.replace_undos(undos)
        self.draw()
        self.model.replace_undos_board(undos_board1,undos_score)















def play_game(root):
    game = Game(root)


# Add a docstring and type hints to this function
# Then write your code here


class StatusBar(tk.Frame):
    def __init__(self, master: tk.Tk, **kwargs):
        super().__init__(master, **kwargs)
        score_frame = tk.Frame(self, bg=BACKGROUND_COLOUR)
        score_frame.pack(side=tk.LEFT, padx=15, pady=10,expand=True)
        undos_frame = tk.Frame(self, bg=BACKGROUND_COLOUR)
        undos_frame.pack(side=tk.LEFT, padx=20, pady=10,expand=True)
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.RIGHT,padx=15, pady=5,expand=True)
        score_label = tk.Label(score_frame, text="SCORE", font=('Arial bold', 20),
                               bg=BACKGROUND_COLOUR, fg='#ccc0b3')
        score_label.pack(expand=True)
        undos_label = tk.Label(undos_frame, text="UNDOS", font=('Arial bold', 20),
                               fg='#ccc0b3', bg=BACKGROUND_COLOUR)
        undos_label.pack()
        self._score_label1 = tk.Label(score_frame, text='0', font=('Arial bold', 20),
                                      fg='#f5ebe4',bg=BACKGROUND_COLOUR)
        self._score_label1.pack()
        self._undos_label1 = tk.Label(undos_frame, text='3', font=('Arial bold', 20),
                                      fg='#f5ebe4',bg=BACKGROUND_COLOUR)
        self._undos_label1.pack()
        self._btn01 = tk.Button(button_frame, text="New Game")
        self._btn01.pack(side=tk.TOP, anchor='e', padx=5, pady=5)
        self._btn02 = tk.Button(button_frame, text='Undo Move', )
        self._btn02.pack(side=tk.BOTTOM, anchor='se', padx=5, pady=5)

    def redraw_infos(self, score: int, undos: int) -> None:
        self._score_label1.config(text=score)
        self._undos_label1.config(text=undos)

    def set_callbacks(self, new_game_command: callable, undo_command: callable) -> None:
        self._btn01.config(command=new_game_command)
        self._btn02.config(command=undo_command)







if __name__ == '__main__':
    root = tk.Tk()
    random.seed(10017030)
    play_game(root)
    root.mainloop()
