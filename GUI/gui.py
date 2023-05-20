from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import img_to_array
from keras.models import load_model

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import re
import datetime
import math

from tkinter import *
from PIL import ImageTk, Image

#load our proposed model that we have trained before ******
model = load_model('C:/Users/nazir/Desktop/TB detection files/trainedModels/NazirTrained/final_model.h5py')
print(model)

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
win.geometry("970x590")
win.title("AI - Tuberculosis Detection System")
win.resizable(False, False)


# Create a label for the background image
bg_label = Label(win)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load the background image
bg_image = ImageTk.PhotoImage(Image.open("GUI/images/back.jpg"))

# Set the background image of the label
bg_label.config(image=bg_image)

#functions for buttons
#cancel button:

def cancel():
    win.destroy()
# take the information about patient window
def takeInfo():
    # Create an instance of tkinter top-level window
    patient_window = Toplevel()
    patient_window.title("Patient Info")
    #patient_window.geometry("800x500")
    patient_window.config(bg="black")
    patient_window.resizable(False, False)
    patient_window.grab_set()

    # Create a frame to hold the form
    form_frame = Frame(patient_window, bg="black")
    form_frame.pack(side="right", padx=10, pady=10)

    # Create labels and entry fields for patient info
    title_label = Label(form_frame, bg="black",fg="lightblue", text="Enter the patient information:", font=("arial", 20,"italic"))
    title_label.grid(row=0, columnspan=2, padx=5, pady=10,sticky="w")

    name_label = Label(form_frame, bg="black",fg="lightblue", text="Patient Name:", font=("arial",14),)
    name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = Entry(form_frame, bg="black",fg="lightblue", font=("arial",14),insertbackground="white")
    name_entry.grid(row=1, column=1, padx=5, pady=5,sticky="w")

    last_name_label = Label(form_frame,bg="black",fg="lightblue", text="Patient Surname:", font=("arial",14),)
    last_name_label.grid(row=2, column=0, padx=5, pady=5,sticky="w")
    last_name_entry = Entry(form_frame,bg="black",fg="lightblue", font=("arial",14),insertbackground="white")
    last_name_entry.grid(row=2, column=1, padx=5, pady=5,sticky="w")

    age_label = Label(form_frame,bg="black",fg="lightblue", text="Patient Age:", font=("arial",14),)
    age_label.grid(row=3, column=0, padx=5, pady=5,sticky="w")
    age_entry = Entry(form_frame,bg="black",fg="lightblue", font=("arial",14),insertbackground="white")
    age_entry.grid(row=3, column=1, padx=5, pady=5,sticky="w")

    gender_label = Label(form_frame,bg="black",fg="lightblue", text="Patient Sex:", font=("arial",14),)
    gender_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    gender_var = StringVar(value="Male")
    male_radio = Radiobutton(form_frame, bg="black", fg="lightblue", text="Male", variable=gender_var, value="Male",
                             font=("arial", 14),selectcolor="black")
    male_radio.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    female_radio = Radiobutton(form_frame, bg="black", fg="lightblue", text="Female", variable=gender_var,
                               value="Female", font=("arial", 14),selectcolor="black")
    female_radio.grid(row=4, column=1, padx=5, pady=5, sticky="e")

    # Create a button to submit the form
    submit_button = Button(form_frame, bg="black",fg="lightblue",text="Select X-ray", width=10,font=("arial",13,"bold"),)
    submit_button.config(
        command=lambda: run(name_entry, last_name_entry, age_entry, gender_var, patient_window))
    submit_button.grid(row=5, column=1, padx=5, pady=10,sticky="w")

    # create a cancel button
    cancel_button = Button(form_frame,bg="black",fg="lightblue",command=patient_window.destroy, text="Cancel",width=10,font=("arial",13,"bold"),)
    cancel_button.grid(row=5, column=1, padx=5, pady=10,sticky="e")

    patient_window.mainloop()

#regExp for the form
def regExpForm(name, last_name, age, gender,patient_window):
    name = name.strip()
    last_name = last_name.strip()
    age = age.strip()

    # Check if name is valid
    name_regex = r'^[a-zA-Z ]{3,}$'
    if not re.match(name_regex, name):
        messagebox.showerror("Invalid Name", "Name must have at least 3 letters. Digits and symbols are not allowed!")
        patient_window.grab_set()
        return False

    # Check if last name is valid
    last_name_regex = r'^[a-zA-Z ]{3,}$'
    if not re.match(last_name_regex, last_name):
        messagebox.showerror("Invalid Surname", "Surname must have at least 3 letters. Digits and symbols are not allowed!")
        return False

    # Check if age is valid
    if not age.isdigit() or not 1 <= int(age) <= 120:
        messagebox.showerror("Invalid Age", "Age must be a number between 1 and 120. Letters are not allowed!")
        return False

    #if user information are correct so go throughout our process
    return True

#enter app button:
def run(name_entry, last_name_entry, age_entry, gender_var,patientWindow):
    # Retrieve patient information
    name = name_entry.get()
    last_name = last_name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    #after the get the data so we should do regExp
    validInfo = regExpForm(name, last_name, age, gender,patientWindow)
    #if user entered invalid information
    if not validInfo:
        return
    # if user entered valid information so continue the process
    # Open a file dialog and allow the user to select an image file
    try:
        filepath = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")]
        )
        # Print the absolute path of the selected file
        print(filepath)
        img = image.load_img(filepath, target_size=(512, 512))
        print(img)
        img = img_to_array(img)
        img = img / 255
        img = img.reshape(1, 512, 512, 3)

        result = model.predict(img)
        #show = result[0][1]
        Positivity = str(float(result[0]))[:5]
        # print(str(Positivity)[:5])
        posPercent = round((float(Positivity) * 100), 1)
        Negativity = round((1.0 - float(Positivity)), 3)
        negPercent = round((float(Negativity) * 100), 1)

        print("this is result")
        print(result)
        print("The Positivity: " + str(Positivity) + " - " + str(posPercent))
        print("The Negativity: " + str(Negativity))

        if result:
            # Create a new window to display the results
            resultWin = Toplevel()
            patientWindow.grab_release()
            resultWin.title("Test Results")
            #resultWin.geometry("880x400")
            resultWin.config(bg="black")
            resultWin.resizable(False, False)
            #calculation the result => True means, its affected, False means it is not affected
            print("this is show: ")
            print(result)
            AFFECTED = False
            if result < 0.5:
                print('you are not affected')
                AFFECTED = False
            else:
                print('you are affected')
                AFFECTED = True

            # Display the window
            resultFrame = Frame(resultWin,bg="black")
            resultFrame.grid(row=0, column=0, padx = 15, pady=17)

            # Display the patient name in the window title
            titleLable = Label(resultFrame, bg="black",fg="lightblue", text="The Results of " + name + " " + last_name + "'s test, are as follows: ",
                               font=("arial", 20, "italic"), )
            titleLable.grid(row=0, columnspan=4, padx=5, pady=20)

            lblDate = Label(resultFrame, bg="black",fg="lightblue",text="Test Date:", font=("arial", 16,), )
            lblDate .grid(row=1, column=0, pady=5, sticky="w")
            DateItSelf = Label(resultFrame, bg="black",fg="lightblue",text=str(datetime.datetime.now())[:16], font=("arial", 16, "italic"), )
            DateItSelf.grid(row=1, column=1, pady=5, sticky="w")

            lblName = Label(resultFrame, bg="black",fg="lightblue",text="Patient Name:", font=("arial",16,),)
            lblName.grid(row=2, column=0,pady=5,sticky="w")
            nameItSelf = Label(resultFrame, bg="black",fg="lightblue",text=name, font=("arial",16,"italic"),)
            nameItSelf.grid(row=2, column=1,pady=5,sticky="w")

            lblLastName = Label(resultFrame, bg="black",fg="lightblue",text="Patient Surname:", font=("arial", 16,), )
            lblLastName.grid(row=3, column=0, pady=5,sticky="w")
            lastnameItSelf = Label(resultFrame, bg="black",fg="lightblue",text=last_name, font=("arial", 16, "italic"), )
            lastnameItSelf.grid(row=3, column=1, pady=5,sticky="w")

            lblAge= Label(resultFrame, bg="black",fg="lightblue",text="Patient Age:", font=("arial", 16,), )
            lblAge.grid(row=4, column=0, pady=5, sticky="w")
            AgeItSelf = Label(resultFrame,bg="black",fg="lightblue", text=str(age) + " years", font=("arial", 16, "italic"), )
            AgeItSelf.grid(row=4, column=1, pady=5, sticky="w")

            lblGender= Label(resultFrame, bg="black",fg="lightblue",text="Patient Sex:", font=("arial", 16,), )
            lblGender.grid(row=5, column=0, pady=5, sticky="w")
            genderItSelf = Label(resultFrame,bg="black",fg="lightblue", text=gender, font=("arial", 16, "italic"), )
            genderItSelf.grid(row=5, column=1, pady=5, sticky="w")

            #result show section on result window
            if AFFECTED: # if the patient affected into illness display red background in result
                lblTotalResult = Label(resultFrame, bg="black",fg="lightblue",text="Test Result:", font=("arial", 16,), )
                lblTotalResult.grid(row=1, column=2, padx=10, pady=5, sticky="w")
                TotalResultItSelf = Label(resultFrame, text="Positive", font=("arial", 16, "italic"), bg="red",fg="black")
                TotalResultItSelf.grid(row=1, column=3, padx=5, pady=5, sticky="w")
            else:
                lblTotalResult= Label(resultFrame, bg="black",fg="lightblue",text="Test Result:", font=("arial", 16,), )
                lblTotalResult.grid(row=1, column=2, padx = 10, pady=5, sticky="w")
                TotalResultItSelf = Label(resultFrame, text="Negative", font=("arial", 16, "italic"),bg = "green",fg="lightgray")
                TotalResultItSelf.grid(row=1, column=3,padx = 5, pady=5, sticky="w")


            lblNegativityResult = Label(resultFrame,bg="black",fg="lightblue", text="Negativity:", font=("arial", 16,), )
            lblNegativityResult.grid(row=2, column=2, padx=10, pady=5, sticky="w")
            NegativityItSelf = Label(resultFrame,bg="black",fg="lightblue", text=str(Negativity) + " ("+str(negPercent)+"%)", font=("arial", 16, "italic"), )
            NegativityItSelf.grid(row=2, column=3, padx=5, pady=5, sticky="w")

            lblPositivityResult = Label(resultFrame,bg="black",fg="lightblue", text="Positivity:", font=("arial", 16,), )
            lblPositivityResult.grid(row=3, column=2, padx=10, pady=5, sticky="w")
            PositivityItSelf = Label(resultFrame,bg="black",fg="lightblue", text=str(Positivity) + " ("+str(posPercent)+"%)", font=("arial", 16, "italic"), )
            PositivityItSelf.grid(row=3, column=3, padx=5, pady=5, sticky="w")

            if AFFECTED: # if the patient affected into illness display red background in final note
                lblfinalNote = Label(resultFrame, text="The Patient Affected", font=("arial", 16,), bg="red", fg="black" )
                lblfinalNote.grid(row=4, column=2, rowspan=2, columnspan=2, padx=10, pady=5, sticky="nsew")
            else:
                lblfinalNote = Label(resultFrame, text="The Patient NOT Affected", font=("arial", 16,), bg="green", fg="lightgray")
                lblfinalNote .grid(row =4,column=2, rowspan=2, columnspan=2, padx=10, pady=5, sticky="nsew")

            #show the proposed x-ray image on the screen
            lblxRay = Label(resultFrame,bg="gray",width=200,height=230)
            lblxRay.grid(row=1,rowspan=4,column=4,padx= 10, sticky="s")
            # Load the image
            img1 = Image.open(filepath)
            # Resize the image to 150x170
            img1 = img1.resize((200, 230))
            # Convert the image to a PhotoImage object
            photo = ImageTk.PhotoImage(img1)
            lblxRay.config(image=photo)

            #CLOSE BUTTON
            btnClose = Button(resultFrame,command=resultWin.destroy,text="Close", fg="lightblue",bg="black",font=("arial",), width=18)
            btnClose.grid(row=5,column=4,pady=4,)


            #Copyright label
            lblCopyright = Label(resultWin,bg="black",font=("arial",8,"bold"),fg="lightgray",text="2023 Copyrighted by M.Nazir Akbari")
            lblCopyright.grid(sticky="s")



            resultWin.mainloop()

    except Exception as e:
        print(e)
        patientWindow.grab_set()
        messagebox.showinfo("Select the image", "Please select an x-ray image.")

bodyframe = Frame(win, bg="black")
bodyframe.grid(padx = 420, pady =0)


buttonFrame = Frame(bodyframe, bg="lightgray")
buttonFrame.grid(row=1, column=0, pady = 1, sticky="e")

lblTitle = Label(bodyframe, text="Tuberculosis Detection System", font=("arial", 25), bg="black", fg="lightblue")
lblTitle.grid(row=0, columnspan=2, pady=50)
btnEnter = Button(buttonFrame, command=takeInfo, text="Test a Case",font=("arial",20), width=10,relief=GROOVE,bd=1,bg="black",fg="lightblue")
btnEnter.grid(row=1, column=0)

btnCancel = Button(buttonFrame, command=cancel, text="Close",font=("arial",20), width=10,relief=GROOVE,bd=1,bg="black",fg="lightblue")
btnCancel.grid(row=1, column=1)

footerFrame= Frame(win,bg="black")
footerFrame.grid(sticky="s",padx = 2,)
labelFooter = Label(footerFrame,bg="black",fg="gray",text="2023 Copyrighted by: M.Nazir Akbari")
labelFooter.grid(sticky="s",pady=15)

win.mainloop()
