import os
import subprocess

from tkinter import Tk, Label, Button
import tkinter as tk

from ponyge import mane
from algorithm.parameters import params, set_params
from utilities.stats import trackers
from GameInterpreter.Compiler import Compiler
from algorithm.parameters import params
from Lift import Lift
import Game.Board as Board
from GameOperations import GameOperations


class MyFirstGUI:
    def __init__(self, master):
        set_params(["--parameters", "cargobot.txt"])
        self.path = params['GAME_BOARD']
        self.master = master
        self.generated_board = []
        self.initial_board = Board.Board(self.path, "init")
        self.final_board = Board.Board(self.path, "end")
        self.lift = Lift(self.path)
        self.width = 800
        self.height = 500
        master.title("Cargobot automatic programmer")
        frame0 = tk.Frame(master=master, width=self.width, height=50)
        frame0.pack()

        frame0_1 = tk.Frame(master=frame0, width=self.width // 2, height=50)
        frame0_1.pack(side="left")

        label_in = Label(frame0_1, text="Initial board")
        label_in.pack(side="left")

        frame0_2 = tk.Frame(master=frame0, width=self.width // 2, height=50)
        frame0_2.pack(side="right")

        label_fi = Label(frame0_2, text="Final board")
        label_fi.pack(side="right")

        frame1 = tk.Frame(master=master, width=self.width,
                          height=self.height // 2)
        frame1.pack()

        frame1_1 = tk.Frame(master=frame1, width=self.width // 2,
                            height=self.height // 2)
        frame1_1.pack(side="left")

        self.print_board(self.initial_board, frame1_1)

        frame1_2 = tk.Frame(master=frame1, width=self.width // 2,
                            height=self.height // 2)
        frame1_2.pack(side="right")
        self.print_board(self.final_board, frame1_2)

        frame1_5_0 = tk.Frame(master=master, width=self.width, height=50)
        frame1_5_0.pack()

        label_in = Label(frame1_5_0, text="Generated result ")
        label_in.pack(side="left")

        frame2 = tk.Frame(master=master, width=self.width,
                          height=self.height // 2)
        frame2.pack()

        self.frame2_1 = tk.Frame(master=frame2, width=int(self.width),
                                 height=self.height // 2)
        self.frame2_1.pack(side="left")

        frame3 = tk.Frame(master=master, width=self.width, height=50)
        frame3.pack()

        greet_button = Button(frame3, text="Generate solution",
                              command=self.generate_solution)
        greet_button.pack()

        close_button = Button(frame3, text="Close", command=self.master.quit)
        close_button.pack()

    def generate_solution(self):
        mane()
        compiler = Compiler()
        program = compiler.compile(trackers.best_ever.phenotype)
        game = GameOperations(self.initial_board, self.final_board, program,
                              self.lift)
        game.runProgram()
        self.print_board(game.board)

    def print_board(self, board, frame=None):
        if not frame:
            frame = self.frame2_1
        border = 6
        game_board_shape = (
            self.width // 2 - border * 4, self.height // 2 - border * 4)
        one_disc_shape = (
            game_board_shape[0] // (len(board.boardState[0])) - border,
            game_board_shape[1] // (len(board.boardState)) + 1 - border)

        canvas = tk.Canvas(frame)
        canvas.create_rectangle(border, border, game_board_shape[0],
                                game_board_shape[1],
                                outline="MistyRose3", fill="MistyRose3")
        for column in range(1, len(board.boardState[0]) + 1):
            rod_x = (column - 1) * one_disc_shape[0] + one_disc_shape[0] // 2
            canvas.create_rectangle(rod_x, self.height // 2 - border * 3,
                                    rod_x + 3,
                                    one_disc_shape[1], fill="DarkOrange4")
        canvas.pack()
        self.print_discks(board, canvas, one_disc_shape)
        return

    def print_discks(self, board, canvas, one_disc_shape):
        colors = {1: "DarkOliveGreen3", 2: "VioletRed2", 3: "DarkSlategray3",
                  4: "goldenrod1"}
        for row, i in enumerate(board.boardState):
            for column, j in enumerate(i):
                if j == 0:
                    continue
                x = column * one_disc_shape[0] + (
                        one_disc_shape[0] - one_disc_shape[0] // 1.4) // 2
                y = (row + 1) * one_disc_shape[1] - 3
                canvas.create_rectangle(x, y, x + one_disc_shape[0] // 1.4,
                                        y + one_disc_shape[1],
                                        outline="black", fill=colors[j])
        return


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
