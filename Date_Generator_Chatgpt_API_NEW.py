import openai
import os
import tkinter as tk
from tkinter import messagebox



class MyGUI:
    def __init__(self):
        #Create app
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.title("Date Idea Generator")

        #Age scale 1
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(anchor='nw', padx=10, pady=25)

        self.label1 = tk.Label(self.frame1, text="Select your age")
        self.label1.pack(side='left', padx = 23)

        self.age_scale1 = tk.Scale(self.frame1, from_=0, to=65, orient='horizontal', length=200, tickinterval=10, font=('Arial', 10))
        self.age_scale1.pack(side='left', padx=10)

        self.submit_button1 = tk.Button(self.frame1, text="Submit", font=('Arial', 12), command=self.set_age_one)
        self.submit_button1.pack(side='left', padx=10)

        #age scale 2
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(anchor='nw', padx=10, pady=25)

        self.label2 = tk.Label(self.frame2, text="Select your partners age")
        self.label2.pack(side='left')

        self.age_scale2 = tk.Scale(self.frame2, from_=0, to=65, orient='horizontal', length=200, tickinterval=10, font=('Arial', 10))
        self.age_scale2.pack(side='left', padx=10)

        self.submit_button2 = tk.Button(self.frame2, text="Submit", font=('Arial', 12), command=self.set_age_two)
        self.submit_button2.pack(side='left', padx=10)

        self.age_one = None
        self.age_two = None

        #Inside and Outside checkboxes
        self.check_state_outside = tk.IntVar()
        self.check_state_inside = tk.IntVar()

        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(anchor='nw', padx=10, pady=25)

        self.outside = tk.Checkbutton(self.frame3, text = "Outside?", font = ('Arial', 12,), variable = self.check_state_outside)
        self.outside.pack(side = 'left', padx=100, pady = 25)

        self.inside = tk.Checkbutton(self.frame3, text = "Inside?", font = ('Arial', 12,), variable = self.check_state_inside)
        self.inside.pack(side = 'left', padx=100, pady = 25)

        #Text box to input area
        self.frame4 = tk.Frame(self.root)
        self.frame4.pack(anchor='nw', padx=10, pady=5)

        self.area_label = tk.Label(self.frame4, text = "What area should this date take place in?", font = ('Arial', 14))
        self.area_label.pack(side = 'left', padx = 10)

        self.area_text = tk.Text(self.frame4, height = 1, font=('Arial', 12))
        self.area_text.pack(side = 'left', padx = 10)
        

        #Label and spinbox for selecting length of date
        self.frame5 = tk.Frame(self.root)
        self.frame5.pack(anchor='nw', padx=10, pady=5)

        self.hours_label = tk.Label(self.frame5, text = "How many hours do you want his date to take?", font = ('Arial', 14))
        self.hours_label.pack(side = 'left', padx = 10, pady = 10)
                                    
        self.hours_spinbox = tk.Spinbox(self.frame5, from_=0, to=24)
        self.hours_spinbox.pack(side = 'left', padx = 10, pady = 10)
        

        #Submit Button
        self.button = tk.Button(self.root, text="Generate Date Idea", font=('Arial', 16), command=self.generate_date)
        self.button.place(x = 200, y = 525)

        self.root.mainloop()

    def set_age_one(self):
        self.age_one = str(self.age_scale1.get())
        
    def set_age_two(self):
        self.age_two = str(self.age_scale2.get())
    
    def set_outside_inside(self):
        self.outside = False
        self.inside = False
        if self.check_state_outside.get() == 1:
            self.outside = True
        if self.check_state_inside.get() == 1:
            self.inside = True

    def set_area(self):
        self.area = self.area_text.get('1.0', tk.END)

    def set_hours(self):
        self.hours = self.hours_spinbox.get()

    def generate_date(self, event=None):
        api_key = os.getenv("OPENAI_API_KEY_DATE_GEN")
        if not api_key:
            print("API key not found. Please set the OPENAI_API_KEY_DATE_GEN environment variable.")
            return
        
        openai.api_key = api_key

        self.set_outside_inside()
        self.set_area()
        self.set_hours()

        prompt = f"Come up with date ideas using these criterion. Person 1 age: {self.age_one}. Person 2 age: {self.age_two} \
                Takes place outside: {self.outside}. Takes place inside {self.inside}. \
                Area the date will take place: {self.area}. Prefered length of the date: {self.hours}. Try to recommend something different each time." 
        

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an application that generates a date idea based on criterion"},
                    {"role": "user", "content": prompt}
                ]
            )
            messagebox.showinfo(title = "Date Idea", message = response['choices'][0]['message']['content'])
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    MyGUI()
