import math
import os
from tkinter import *
from PIL import ImageGrab

WIN = Tk()
WIN.geometry("1400x1050")
WIN.title("Tree fractal")


Options = LabelFrame(height=400, width=190, text="Options")
Options.grid(row=1, column=0, padx=10, pady=10)
frame = Frame(Options, height=1, width=190)
frame.grid(row=0, column=0)

label_iterations = Label(Options, text="Iterations")
label_iterations.grid(row=2, column=0, sticky=W)
entry_iterations = Entry(Options)
entry_iterations.insert(0, "6")
entry_iterations.grid(row=2, column=1, sticky=E)

label_inheritance = Label(Options, text="Angle inheritance")
label_inheritance.grid(row=3, column=0, sticky=W)
entry_inheritance = Entry(Options)
entry_inheritance.grid(row=3, column=1, sticky=E)
entry_inheritance.insert(0, "0.9")

label_wind = Label(Options, text="Wind")
label_wind.grid(row=4, column=0, sticky=W)
entry_wind = Entry(Options)
entry_wind.grid(row=4, column=1, sticky=E)
entry_wind.insert(0, "0")

label_geo = Label(Options, text="Geometric length")
label_geo.grid(row=5, column=0, sticky=W)
entry_geo = Entry(Options)
entry_geo.grid(row=5, column=1, sticky=E)
entry_geo.insert(0, "0.5")

label_sca = Label(Options, text="Scalar length")
label_sca.grid(row=6, column=0, sticky=W)
entry_sca = Entry(Options)
entry_sca.grid(row=6, column=1, sticky=E)
entry_sca.insert(0, "0")

label_mirror = Label(Options, text="Angle scaling")
label_mirror.grid(row=7, column=0, sticky=W)
entry_mirror = Entry(Options)
entry_mirror.grid(row=7, column=1, sticky=E)
entry_mirror.insert(0, "1")

cv = Canvas(WIN, height=1000, width=1000)
cv.grid(row=0, column=1, rowspan=5, sticky=E)

AngleOptions = LabelFrame(height=400, width=190, text="Angles")
AngleOptions.grid(row=0, column=0, padx=10, pady=10)
AngleEntryList = [Entry(AngleOptions), Entry(AngleOptions)]
AngleEntryList[0].insert(0, "1")
AngleEntryList[1].insert(0, "-1")
AngleEntryList[0].grid(row=1, column=1)
AngleEntryList[1].grid(row=2, column=1)


def add_angle():
    if AngleEntryList.__len__() != 10:
        AngleEntryList.append(Entry(AngleOptions))
        AngleEntryList[AngleEntryList.__len__()-1].insert(0, "0")
        AngleEntryList[AngleEntryList.__len__() - 1].grid(row=AngleEntryList.__len__(), column=1)
        AngleOptions.update()


def delete_angle():
    if AngleEntryList.__len__() != 2:
        AngleEntryList[AngleEntryList.__len__()-1].destroy()
        AngleEntryList.pop(AngleEntryList.__len__()-1)
        print(AngleEntryList.__len__())
        AngleOptions.update()


AddAngle = Button(AngleOptions, text="Add angle", command=add_angle)
AddAngle.grid(row=0, column=1)
DeleteAngle = Button(AngleOptions, text="Delete Angle", command=delete_angle)
DeleteAngle.grid(row=0, column=0)


# calculate points for drawing
def calculate():
    
    winh = WIN.winfo_height()

    if winh < 1000:
        cv.config(height=winh, width=winh)
    else:
        cv.config(height=1000, width=1000)

    WIN.update()

    t_length = cv.winfo_height() / 2

    print(t_length)

    angles = []
    for a in range(AngleEntryList.__len__()):
        angles.append(float(AngleEntryList[a].get()))

    angle_relativity = float(entry_inheritance.get())  # How much the branch's new angle is based off the old.
    steps = float(entry_iterations.get())    # Total number of iterations.
    wind = float(entry_wind.get())  # How much the branches are skewed by in a horizontal direction. Almost useless.
    geometric_length = float(entry_geo.get())
    scalar_length = float(entry_sca.get())
    mirror = float(entry_mirror.get())

    vertex_list = [[[0.0, 0.0, 0.0]]]

    iteration = 0
    while iteration != steps:
        if geometric_length != 1:
            length = t_length * (scalar_length * (1 / steps) + (1 - scalar_length)
                                 * math.pow(geometric_length, iteration)
                                 * (1 - geometric_length) / (1 - math.pow(geometric_length, steps)))
        else:
            length = t_length / steps

        vertex_list.append([])
        for point in vertex_list[iteration]:
            for ang in angles:
                new_angle = angle_relativity * point[2] + ang
                vertex_list[iteration + 1].append([point[0] + length * (wind + math.sin(new_angle)), point[1]
                                                   + length * math.cos(new_angle), new_angle])

        iteration += 1
        for a in range(angles.__len__()):
            angles[a] = mirror * angles[a]

    cv.delete("all")
    iteration = 0
    cv.create_line(t_length, (t_length * 2), vertex_list[0][0][0] + t_length, t_length - vertex_list[0][0][1])

    while iteration != steps:
        for i in range(vertex_list[iteration].__len__()):
            for j in range(angles.__len__()):
                cv.create_line(vertex_list[iteration][i][0]+t_length,
                               t_length - vertex_list[iteration][i][1],
                               vertex_list[iteration + 1][angles.__len__()*i + j][0]+t_length,
                               t_length - vertex_list[iteration + 1][angles.__len__() * i + j][1])

        iteration += 1


#  bake to image
def save_image():
    if not os.path.isdir("Images"):
        os.mkdir("Images")

    number = os.listdir("Images").__len__()
    ssx = cv.winfo_rootx() + 1
    ssw = cv.winfo_width()
    ssy = cv.winfo_rooty() + 1
    ssh = cv.winfo_height()
    save = ImageGrab.grab(bbox=(ssx, ssy, ssx+ssw, ssy+ssh))
    save = save.convert("L")
    save.save(os.path.join("Images", "image"+str(number)+".png"), optimise=True)


create_button = Button(Options, text="Create tree", command=calculate)
create_button.grid(row=10, column=0, sticky=W)
save_button = Button(Options, text="Save to image", command=save_image)
save_button.grid(row=10, column=1, sticky=E)

calculate()

WIN.mainloop()
