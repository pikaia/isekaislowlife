import tkinter as tk

from slowlife.bot.game import do_collect_gold, do_banquet, do_roaming, do_fountain, do_kitchen, do_school, do_stage, \
    do_magic_farm, do_farmstead, register_locations, do_storage

window = tk.Tk()


class Control:
    # ====> Replace __init__ by a method you can call without creating a new instance
    def command(self, x):
        if x == 0:
            register_locations()
            return

        if x == 1:
            do_collect_gold(3000, 1)
            return
        if x == 2:
            do_banquet()
            return
        if x == 3:
            do_roaming()
            return
        if x == 4:
            while True:
                do_fountain()
            return
        if x == 5:
            do_kitchen()
            return
        if x == 6:
            do_school()
            return

        if x == 7:
            do_stage(0)
            return
        if x == 8:
            do_magic_farm()
            return
        if x == 9:
            do_farmstead()
            return
        if x == 10:
            do_storage()
            return
        if x == 11:
            do_mine_clearance()
            return


CtrlButtonsText = ["Register Locations", "Collect Gold", "Banquet", "Roaming", "Fountain", "Kitchen", "School",
                   "Stage", "Magic Farm", "Farmstead", "Storage"]

# ====> Creates a unique instance of the class and uses it below
control = Control()

for i in range(len(CtrlButtonsText)):
    ControlButtons = tk.Button(window, width=10, height=5, text=CtrlButtonsText[i],
                               command=lambda x=i: control.command(x))
    ControlButtons.grid(row=i, column=0)

window.mainloop()
