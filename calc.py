from tkinter import *
from MyMath import *
from tkinter import ttk
from tkinter import messagebox

# creating basic root window
root = Tk()
root.title('MyMath')
root.geometry("500x500")
root.configure(background="light blue")

# defining area function


def area():

    SelectedShape = shapes.get()

    if SelectedShape == "Rectangle":
        l = int(radius_entry.get())
        b = int(height_entry.get())
        area_rectangle = myArea(SelectedShape.lower(), l, b, 0, 0)
        messagebox.showinfo("Area Rectangle", area_rectangle)

    elif SelectedShape == "Square":
        r = int(radius_entry.get())
        area_square = myArea(SelectedShape.lower(), r, 0, 0, 0)
        messagebox.showinfo("Area Square", area_square)

    elif SelectedShape == "Triangle":
        b = int(radius_entry.get())
        h = int(height_entry.get())
        area_triangle = myArea(SelectedShape.lower(), 0, b, h, 0)
        messagebox.showinfo("Area Triangle", area_triangle)

    elif SelectedShape == "Circle":
        r = int(radius_entry.get())
        area_circle = myArea(SelectedShape.lower(), 0, 0, 0, r)
        messagebox.showinfo("Area Circle", area_circle)
    else:
        messagebox.showwarning("Invalid Input", "shape is not available")

# defining volume function


def volume():
    selected_solid_shape = solidshape.get()
    if selected_solid_shape == "Sphere":
        r = int(radius_entry2.get())
        vol_sphere = myvolume(selected_solid_shape.lower(), 0, 0, 0, r)
        messagebox.showinfo("Volume Sphere", vol_sphere)
    elif selected_solid_shape == "Cone":
        r = int(radius_entry2.get())
        h = int(height2.get())
        vol_cone = myvolume(selected_solid_shape.lower(), 0, 0, h, r)
        messagebox.showinfo("Volume Cone", vol_cone)

    elif selected_solid_shape == "Cube":
        l = int(radius_entry2.get())
        vol_cube = myvolume(selected_solid_shape.lower(), l, 0, 0, 0)
        messagebox.showinfo("Volume Cube", vol_cube)
    elif selected_solid_shape == "Cylinder":
        r = int(radius_entry2.get())
        h = int(height2.get())
        vol_cylinder = myvolume(selected_solid_shape.lower(), 0, 0, h, r)
        messagebox.showinfo("Volume Cylinder", vol_cylinder)

    elif selected_solid_shape == "Cuboid":
        l = int(radius_entry2.get())
        b = int(width_entry.get())
        h = int(height2.get())
        vol_cuboid = myvolume(selected_solid_shape.lower(), l, b, h, 0)
        messagebox.showinfo("Volume Cuboid", vol_cuboid)

    else:
        messagebox.showwarning("Invalid input", "shape is not available")


# defining condition_check function

def condition_check():
    tocheck = conditions.get()
    if tocheck == "Pythagorean Triplet Checker":
        a = int(side1_entry.get())
        b = int(side2_entry.get())
        c = int(side3_entry.get())
        py_check = mycondition(tocheck, a, b, c, 0)
        if py_check == 1:
            messagebox.showinfo("Check", "This is a Pythagorean Triplet.")
        else:
            messagebox.showinfo("Check", "This is not a Pythagorean Triplet.")

    elif tocheck == "Complimentary&Supplementary Angles":
        angle = int(angle_entry.get())
        comsup = mycondition(tocheck, 0, 0, 0, angle)


# creating tabs
note1 = ttk.Notebook(root)
note1.pack(pady=5)

# creating 3 frames
area_frame = Frame(note1, width=300, height=300,bg="Dark blue")
volume_frame = Frame(note1, width=300, height=300,bg="Dark blue")
condition_frame = Frame(note1, width=300, height=300,bg="Dark blue")
area_frame.pack(fill="both", expand=1)
volume_frame.pack(fill="both", expand=1)
condition_frame.pack(fill="both", expand=1)

# adding tabs
note1.add(area_frame, text="Area Calculator",)
note1.add(volume_frame, text="Volume Calculator")
note1.add(condition_frame, text="Condition Checker")

# defining shapes and show
shapes = StringVar()
shapes.set("Select")
solidshape = StringVar()
solidshape.set("Select")
conditions = StringVar()
conditions.set("Select")


def show1():
    mylabel = Label(area_frame, text=shapes.get()).pack()


def show2():
    mylabel2 = Label(volume_frame, text=solidshape.get()).pack()


def show3():
    mylabel3 = Label(condition_frame, text=conditions.get()).pack()


# area frame option
shape_options = OptionMenu(
    area_frame, shapes, "Circle", "Square", "Triangle", "Rectangle").pack()
mybutton1 = Button(area_frame, text="Select shape", command=show1,bg="light blue").pack()

radius_side = Label(area_frame, text="Enter radius or side in m",bg="light blue").pack()

radius_entry = Entry(area_frame, font=("Helvetica", 20),bg="orange")
radius_entry.pack()

height = Label(
    area_frame, text="Enter height or width in m if applicable else enter 0",bg="light blue").pack()
height_entry = Entry(area_frame, font=("Helvetica", 20),bg="orange")
height_entry.pack()


# volume frame option
volume_options = OptionMenu(
    volume_frame, solidshape, "Cone", "Sphere", "Cylinder", "Cube", "Cuboid").pack()
mybutton2 = Button(volume_frame, text="Select shape", command=show2,bg="light blue").pack()
radius_side2 = Label(volume_frame, text="Enter radius or side in m",bg="light blue").pack()
radius_entry2 = Entry(volume_frame, font=("Helvetica", 20),bg="orange")
radius_entry2.pack()
height2 = Label(
    volume_frame, text="Enter height in m if applicable else enter 0",bg="light blue").pack()
height2 = Entry(volume_frame, font=("Helvetica", 20),bg="orange")
height2.pack()
width = Label(
    volume_frame, text="Enter breadth in m if applicable else enter 0",bg="light blue").pack()
width_entry = Entry(volume_frame, font=("Helvetica", 20),bg="orange")
width_entry.pack()

# condition frame
condition_options = OptionMenu(condition_frame, conditions,
                               "Pythagorean Triplet Checker", "Complimentary&Supplementary Angles").pack()
mybutton3 = Button(condition_frame, text="Select condition",
                   command=show3,bg="light blue").pack()
side1_label = Label(condition_frame, text="Enter first number",bg="light blue").pack()
side1_entry = Entry(condition_frame, font=("Helvetica", 20),bg="orange")
side1_entry.pack()
side2_label = Label(condition_frame, text="Enter second number",bg="light blue").pack()
side2_entry = Entry(condition_frame, font=("Helvetica", 20),bg="orange")
side2_entry.pack()
side3_label = Label(condition_frame, text="Enter third number",bg="light blue").pack()
side3_entry = Entry(condition_frame, font=("Helvetica", 20),bg="orange")
side3_entry.pack()
angle_label = Label(condition_frame, text="Enter angle in degrees",bg="light blue").pack()
angle_entry = Entry(condition_frame, font=("Helvetica", 20),bg="orange")
angle_entry.pack()

# button frame
button_frame1 = Frame(area_frame)
button_frame1.pack()
button_frame2 = Frame(volume_frame)
button_frame2.pack()
button_frame3 = Frame(condition_frame)
button_frame3.pack()

# creating buttons
button1 = Button(button_frame1, text="Calculate", command=area,bg="red")
button1.grid(row=0, column=0, padx=10)
button2 = Button(button_frame2, text="Calculate", command=volume,bg="red")
button2.grid(row=0, column=0, padx=10)
button3 = Button(button_frame3, text="Calculate", command=condition_check,bg="red")
button3.grid(row=0, column=0, padx=10)

root.mainloop()