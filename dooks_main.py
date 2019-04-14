# Main file. Holds the bulk of the program.
import tkinter as tk
import outsource
import time_controls
from threading import Timer, Thread
from time import time as time_module



class app:
    # Main class responsible for GUI and most method calls
    def __init__(self):
        # Calling necessary starting method
        generic().verify()

        # Tkinter window configuration
        self.root = tk.Tk()
        root = self.root
        self.width = 600
        self.height = 300
        generic().center_window(root, self.width, self.height)   # Window size initialization
        root.configure(bg=bgc)
        root.title(outsource.pref('title'))

        # Variables
        self.timer = False
        self.first_run = True
        self.last_time = 0
        self.time_interval = 0.1
        self.thread = 0

        # Labels
        #           Time Display
        self.time_display = tk.Label(root, text="00:00:00:00", font=('times', 20), bg=butc, relief='sunken')
        self.time_display.place(x=self.width/2, y=self.height/4.35, anchor='center')
        #           Money earned display
        tk.Label(root, text="$", font=('times', 20), bg=bgc).place(y=self.height/4.35, x=420, anchor='center')
        self.earned_display = tk.Label(root, text='0.00', bg=butc, font=('times', 20), relief='sunken', anchor='w')
        self.earned_display.place(x=470, y=self.height/4.35, width=85, anchor='center')
        #           Border
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width/2, y=0, anchor='center', width=575, height=10)
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width/2, y=self.height, anchor='center',
            width=575, height=10)
        tk.Label(root, relief='sunken', bg=butc).place(x=0, y=self.height/2, anchor='center', width=10, height=320)
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width, y=self.height/2, anchor='center',
            width=10, height=320)
        #           Payrate label
        self.payrateL = tk.Label(root, text="Pay Rate: $%.2f" % float(wage), font=('times', 14, 'underline'), bg=bgc)
        self.payrateL.place(x=75, y=25, anchor='center')
        #           Other labels
        tk.Label(root, text="Session Time:", font=('times', 15, 'underline'), bg=bgc).place(x=self.width/2, y=30, anchor='center')
        tk.Label(root, text='Earned:', font=('times', 15, 'underline'), bg=bgc).place(x=470, y=33, anchor='center')

        # Buttons
        #           Quit
        quit = tk.Button(root, text='Exit', font=('times', 17, 'bold'), command=lambda: self.exit_program(), bg=butc)
        quit.place(x=self.width - 45, y=self.height - 40, anchor='center')
        #           Start/Pause Timer
        self.start_timer = tk.Button(root, text='Start', font=('times', 18), command=lambda:
            app.timer_boolean(self), bg=butc)
        self.start_timer.place(x=250, y=self.height/2.2, anchor='center')
        #           Stop and save time
        self.stop_timer = tk.Button(root, text='Stop', font=('times', 18), command=lambda:
            app.time_stop(self), bg=butc)
        self.stop_timer.place(x=350, y=self.height/2.2, anchor='center')
        #           Options button
        self.options = tk.Button(root, text='Options', font=('times', 16), command=lambda:
            options(root, self), bg=butc)
        self.options.place(x=60, y=250, anchor='center')
        #           Payrate options
        self.pay_button1 = tk.Button(root, text="Payrate 1: $%.2f" % float(outsource.return_value('preferences.txt', 'wage1')), bg=butc,
            font=('times', 12), command=lambda: self.set_pay(1))
        self.pay_button1.place(x=15, y=55)
        self.pay_button2 = tk.Button(root, text="Payrate 2: $%.2f" % float(outsource.return_value('preferences.txt', 'wage2')), bg=butc,
            font=('times', 12), command=lambda: self.set_pay(2))
        self.pay_button2.place(x=15, y=105)

        # Mainloop. End of __init__
        self.root.mainloop()

    def time_start(self):
        # Controls the main time display and earned display. Refreshes every second.
        if self.timer == False:
            return
        
        if self.first_run == True:
            self.first_run = False
            self.last_time = time_module() - 0.1
            

        # Formatting time for display
        temp_time = time_controls.time_up()
        formatted_time = time_controls.format_time(temp_time)

        # Calculating money earned based on users pay rate
        time_hours = temp_time / 36000
        money = time_hours * wage
        self.earned_display.configure(text="%.2f" % money)
        self.time_display.configure(text=formatted_time)

        self.adjust_time_interval()
        self.thread = Timer(self.time_interval, self.time_start)
        self.thread.start()

    def timer_boolean(self):
        # Starts and pauses time_start from boolean value
        if self.timer == False:
            self.timer = True
            self.first_run = True
            self.start_timer.configure(text="Pause")
            self.time_start()
        else:
            self.timer = False
            self.thread = 0
            self.start_timer.configure(text="Start")
            self.thread = Timer(self.time_interval, self.time_start)
        
    def adjust_time_interval(self):
        # Adjusts the time interval so the timer stays accurate despite the time taken to run
        difference = time_module() - self.last_time
        difference -= 0.1
        self.time_interval -= (difference)
        self.last_time = time_module()

    def time_stop(self):
        # Stops timer and saves current time
        self.timer = False
        session_time = time_controls.timestamp
        ftime = time_controls.format_time(session_time)
        self.time_display.configure(text=time_controls.format_time(0))

        outsource.enter_into_logs(ftime + "\nPay Rate : $%.2f" % wage + '\n' + 
            "Amount Earned : $%.2f" % ((session_time/36000) * wage))
        
        self.session_stats_display()
    
    def session_stats_display(self):
        window = tk.Tk()
        height = 200
        width = 300
        generic().center_window(window, width, height)
        window.configure(bg=butc)
        window.title("Session summary")
        tk.Label(window, text="Hourly Rate: $" + str(wage), font=('times', 14), bg=bgc, relief='sunken').place(x=width/2, y=50, anchor='center')
        tk.Label(window, text="Time Worked: " + time_controls.format_time(time_controls.timestamp), font=('times', 14), 
            bg=bgc, relief='sunken').place(x=width/2, y=100, anchor='center')
        earned = (time_controls.timestamp / 36000) * wage
        tk.Label(window, text="Earned: ${0:.3f}".format(earned), font=('times', 14), bg=bgc).place(x=width/2, y=150, anchor='center')
        time_controls.timestamp = 0

    def close_main(self):
        # Used to close main window from a different class e.g. 'options'
        self.root.destroy()
    
    def set_pay(self, num):
        # Sets the current value of 'wage' for monetary calculations
        global wage
        value = outsource.return_value('preferences.txt', 'wage' + str(num))
        wage = float(value)
        self.payrateL.configure(text="Pay Rate: $%.2f" % wage)

    def update_main(self):
        # Updates info in main window.
        self.pay_button1.configure(text="Payrate 1: $%.2f" % float(outsource.return_value('preferences.txt', 'wage1')))
        self.pay_button2.configure(text="Payrate 2: $%.2f" % float(outsource.return_value('preferences.txt', 'wage2')))
        self.root.title(outsource.return_value('preferences.txt', 'title'))
        self.payrateL.configure(text="Pay Rate: $%.2f" % wage)
    
    def exit_program(self):
        self.timer = False
        self.root.destroy()


class generic:
    # Houses frequently used generic methods.

    def center_window(self, win, w, h):   
        # Window center/size
        win.update_idletasks()
        width = w
        height = h
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def preferences(self):  
        # Sets global variables at program start
        # Function calls 'outsource.py'
        global bgc, butc, wage
        bgc = outsource.pref('bgc')
        butc = outsource.pref('butc')
        wage = float(outsource.return_value('preferences.txt', 'wage1'))

    def verify(self):   
        # Initial method to verify necessary files
        try:
            file = open('preferences.txt', 'r')
            file.close()
        except FileNotFoundError:
            # File additions NEED to follow given format
            file = open('preferences.txt', 'w')
            file.write('bgc : #bbb\n')
            file.write('butc : #888\n')
            file.write('title : Work Timer\n')
            file.write('wage1 : 10\n')
            file.write('wage2 : 15\n')
            file.close()
        try:
            file = open('logs.txt', 'r')
            file.close()
        except FileNotFoundError:
            file = open('logs.txt', 'w')
            file.write('Format:    Date - Work_Time(hours:minutes:seconds)\n\n\n')
            file.close()

        # - Ended up not needing to use a text file for this. It's more efficient without it.
        # file = open('timelogs.txt', 'w')
        # file.write('timestamp : 0\n')
        # file.close()
        self.preferences()

    def update(self, root):
        # Updates global variables. Currently not used.
        self.preferences()
        root.title(outsource.pref('title'))


class options:
    ''' Options tab to change settings for App '''

    def __init__(self, mainApp, mainInstance):
        self.root = tk.Tk()
        generic().center_window(self.root, 300, 440)
        self.root.configure(bg=bgc)
        root = self.root
        root.title(outsource.return_value('preferences.txt', 'title') + ' options')
        self.main = mainApp
        self.mainInstance = mainInstance

        # Background color setting
        tk.Label(root, text='Background color (hex):', font=('times', 12), bg=bgc, relief='sunken').place(
            x=10, y=35, height=30)
        self.bgc_var = tk.StringVar(root, outsource.return_value('preferences.txt', 'bgc')[1:])
        self.entry_bgc = tk.Entry(root, textvariable=self.bgc_var, font=('times', 14))
        self.entry_bgc.place(x=225, y=50, anchor='center', width=75)
        # Accent color setting
        tk.Label(root, text='Accent color (hex):', font=('times', 12), bg=bgc, relief='sunken').place(
            x=10, y=75, height=30)
        self.butc_var = tk.StringVar(root, outsource.return_value('preferences.txt', 'butc')[1:])
        self.entry_butc = tk.Entry(root, textvariable=self.butc_var, font=('times', 14), relief='raised')
        self.entry_butc.place(x=225, y=90, anchor='center', width=75)
        # Wage 1 setting
        tk.Label(root, text='Pay Rate 1:', font=('times', 12), bg=bgc, relief='sunken').place(
            x=10, y=140, height=30)
        self.wage1_var = tk.StringVar(root, outsource.return_value('preferences.txt', 'wage1'))
        self.entry_wage1 = tk.Entry(root, textvariable=self.wage1_var, font=('times', 14))
        self.entry_wage1.place(x=225, y=155, anchor='center', width=75)
        # Wage 2 setting
        tk.Label(root, text='Pay Rate 2:', font=('times', 12), bg=bgc, relief='sunken').place(
            x=10, y=180, height=30)
        self.wage2_var = tk.StringVar(root, outsource.return_value('preferences.txt', 'wage2'))
        self.entry_wage2 = tk.Entry(root, textvariable=self.wage2_var, font=('times', 14))
        self.entry_wage2.place(x=225, y=195, anchor='center', width=75)
        # Title
        tk.Label(root, text='Title:', font=('times', 12), bg=bgc, relief='sunken').place(
            x=10, y=245, height=30)
        self.title_var = tk.StringVar(root, outsource.return_value('preferences.txt', 'title'))
        self.entry_title = tk.Entry(root, textvariable=self.title_var, font=('times', 12))
        self.entry_title.place(x=188, y=260, anchor='center', width=150)

        # Buttons
        tk.Button(root, text='Apply and Close', font=('times', 16, 'bold'), command=lambda: options.set_all(self),
            bg=butc).place(x=100, y=400, anchor='center', height=40)
        tk.Button(root, text='Close', font=('times', 18, 'bold'), bg=butc, command=lambda: root.destroy()).place(
            x=240, y=400, anchor='center', height=40)
        tk.Button(root, text="Clear Logs", font=('times', 12), bg=butc, command=lambda: self.clear_logs()).place(
            x=20, y=290)
        tk.Button(root, text="Clear Preferences", font=('times', 12), bg=butc, command=lambda: self.confirm_preferences()).place(
            x=20, y=330)

        # Misc
        tk.Label(root, bg=butc, relief='sunken').place(x=150, y=122, anchor='center', width=290, height=7)
        tk.Label(root, bg=butc, relief='sunken').place(x=150, y=227, anchor='center', width=290, height=7)
        tk.Label(root, bg=bgc, text='$', font=('times', 14)).place(x=180, y=155, anchor='center')
        tk.Label(root, bg=bgc, text='$', font=('times', 14)).place(x=180, y=195, anchor='center')

        # End of __init__
        self.root.mainloop()

    def set_all(self):
        global wage
        if wage == float(outsource.return_value('preferences.txt', 'wage1')):
            wage = float(self.wage1_var.get())
        else:
            wage = float(self.wage2_var.get())
        
        old_bgc = bgc[1:]
        old_butc = butc[1:]
        outsource.replace_value('preferences.txt', 'bgc', '#' + self.bgc_var.get())
        outsource.replace_value('preferences.txt', 'butc', '#' + self.butc_var.get())
        outsource.replace_value('preferences.txt', 'wage1', self.wage1_var.get())
        outsource.replace_value('preferences.txt', 'wage2', self.wage2_var.get())
        outsource.replace_value('preferences.txt', 'title', self.title_var.get())
        self.mainInstance.update_main()
        self.root.title(self.title_var.get() + ' options')
        
        if self.bgc_var.get() != old_bgc:
            self.confirm()
        elif self.butc_var.get() != old_butc:
            self.confirm()
        else:
            self.root.destroy()

    def confirm(self):
        self.window = tk.Tk()
        window = self.window
        window.title('Restart now?')
        generic().center_window(window, 250, 175)
        window.configure(bg=bgc)
        message = '''Pay rate and title have been changed.\nFor color changes to take effect\n'''
        message += '''the application must be restarted.\nYou will lose any ongoing timer progress.\nRestart now?'''
        tk.Label(window, text=message, font=('times', 12), bg=bgc, justify='center').place(x=125, y=50, anchor='center')
        tk.Button(window, text='Yes', bg=butc, font=('times', 18), command=lambda: self.confirm_yes()).place(
            x=75, y=130, anchor='center')
        tk.Button(window, text='No', bg=butc, font=('times', 18), command=lambda: self.confirm_no()).place(
            x=175, y=130, anchor='center')

    def confirm_yes(self):
        global bgc, butc
        bgc = outsource.return_value('preferences.txt', 'bgc')
        butc = outsource.return_value('preferences.txt', 'butc')
        self.window.destroy()
        self.root.destroy()
        self.main.destroy()
        app()

    def confirm_no(self):
        self.window.destroy()
        self.root.destroy()
    
    def clear_logs(self):
        from os import remove
        remove("logs.txt")
        generic().verify()
    
    def confirm_preferences(self):
        window = tk.Tk()
        window.title('Confirm')
        window.configure(bg=bgc)
        generic().center_window(window, 225, 180)
        tk.Label(window, text="Clearing preferences will\nrestart the program. Are you\nsure you want to do that?",
            bg=bgc, font=('times', 13)).place(x=225/2, y=40, anchor='center')
        tk.Button(window, text='Yes', bg=butc, font=('times', 15, 'bold'), command=lambda: self.clear_preferences(window)).place(
            x=225/3, y=130, anchor='center')
        tk.Button(window, text='No', bg=butc, font=('times', 15, 'bold'), command=lambda: window.destroy()).place(
            x=(225*2)/3, y=130, anchor='center')
    
    def clear_preferences(self, win):
        from os import remove
        win.destroy()
        remove("preferences.txt")
        self.root.destroy()
        self.main.destroy()
        generic().verify()
        app()


# Running application from here.
if __name__ == "__main__":
    app()
    
