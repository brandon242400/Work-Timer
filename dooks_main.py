# Main file. Holds the bulk of the program.
import tkinter as tk
import outsource
import time_controls
global bgc, butc
bgc = ''
butc = ''


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

        # Labels
        #           Time Display
        self.time_display = tk.Label(root, text="00:00:00", font=('times', 20), bg=butc, relief='sunken')
        self.time_display.place(x=self.width/2, y=self.height/4.35, anchor='center')
        #           Money earned display
        tk.Label(root, text="$", font=('times', 20), bg=bgc).place(y=self.height/4.35, x=420, anchor='center')
        self.earned_display = tk.Label(root, text='0.00', bg=butc, font=('times', 20), relief='sunken', anchor='w')
        self.earned_display.place(x=470, y=self.height/4.35, width=75, anchor='center')
        #           Border
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width/2, y=0, anchor='center', width=575, height=10)
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width/2, y=self.height, anchor='center',
            width=575, height=10)
        tk.Label(root, relief='sunken', bg=butc).place(x=0, y=self.height/2, anchor='center', width=10, height=320)
        tk.Label(root, relief='sunken', bg=butc).place(x=self.width, y=self.height/2, anchor='center',
            width=10, height=320)

        # Buttons
        #           Quit
        quit = tk.Button(root, text='Exit', font=('times', 17, 'bold'), command=lambda: root.destroy(), bg=butc)
        quit.place(x=self.width - 45, y=self.height - 40, anchor='center')
        #           Start/Pause Timer
        self.start_timer = tk.Button(root, text='Start/Pause', font=('times', 14), command=lambda:
            app.timer_boolean(self), bg=butc)
        self.start_timer.place(x=268, y=self.height/2.5, anchor='center')
        #           Stop and save time
        self.stop_timer = tk.Button(root, text='Stop', font=('times', 14), command=lambda:
            app.time_stop(self), bg=butc)
        self.stop_timer.place(x=350, y=self.height/2.5, anchor='center')
        #           Options button
        self.options = tk.Button(root, text='Options', font=('times', 14), command=lambda:
            options(root), bg=butc)
        self.options.place(x=50, y=200, anchor='center')

        # Mainloop. End of __init__
        self.root.mainloop()

    def time_start(self):
        # Controls the main time display and earned display. Refreshes every second.
        if self.timer == False:
            return

        # Formatting time for display
        temp_time = time_controls.time_up()
        formatted_time = time_controls.format_time(temp_time)

        # Calculating money earned based on users pay rate

        self.time_display.configure(text=formatted_time)
        self.time_display.after(1000, self.time_start)

    def timer_boolean(self):
        # Starts and pauses time_start from boolean value
        if self.timer == False:
            self.timer = True
            app.time_start(self)
        else:
            self.timer = False

    def time_stop(self):
        # Stops timer and saves current time
        self.timer = False
        session_time = int(time_controls.timestamp)
        time_controls.timestamp = 0
        ftime = time_controls.format_time(session_time)
        self.time_display.configure(text=time_controls.format_time(0))

        outsource.enter_into_logs(ftime)

    def close_main(self):
        # Used to close main window from a different class e.g. 'options'
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
        global bgc, butc
        bgc = outsource.pref('bgc')
        butc = outsource.pref('butc')

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
            file.write('Format:    Date - Time(hours:minutes:seconds)\n\n')
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

    def __init__(self, mainApp):
        self.root = tk.Tk()
        generic().center_window(self.root, 300, 400)
        self.root.configure(bg=bgc)
        root = self.root
        root.title(outsource.return_value('preferences.txt', 'title') + ' options')
        self.main = mainApp

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
            bg=butc).place(x=100, y=360, anchor='center', height=40)
        tk.Button(root, text='Close', font=('times', 18, 'bold'), bg=butc, command=lambda: root.destroy()).place(
            x=240, y=360, anchor='center', height=40)

        # Misc
        tk.Label(root, bg=butc, relief='sunken').place(x=150, y=122, anchor='center', width=290, height=7)
        tk.Label(root, bg=butc, relief='sunken').place(x=150, y=227, anchor='center', width=290, height=7)
        tk.Label(root, bg=bgc, text='$', font=('times', 14)).place(x=180, y=155, anchor='center')
        tk.Label(root, bg=bgc, text='$', font=('times', 14)).place(x=180, y=195, anchor='center')

        # End of __init__
        self.root.mainloop()

    def set_all(self):
        old_bgc = bgc[1:]
        old_butc = butc[1:]
        outsource.replace_value('preferences.txt', 'bgc', '#' + self.bgc_var.get())
        outsource.replace_value('preferences.txt', 'butc', '#' + self.butc_var.get())
        outsource.replace_value('preferences.txt', 'wage1', self.wage1_var.get())
        outsource.replace_value('preferences.txt', 'wage2', self.wage2_var.get())
        outsource.replace_value('preferences.txt', 'title', self.title_var.get())
        self.main.title(self.title_var.get())
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
        message = '''Pay rate and title have been changed.\nFor color changes to take effect
the application must be restarted.\nYou will lose any ongoing timer progress.\nRestart now?'''
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


if __name__ == "__main__":
    app()
