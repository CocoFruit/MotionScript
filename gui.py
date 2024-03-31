import tkinter as tk
from tkinter import ttk
import json
import pose_esti
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def check_challenge_number(team_id, json_data):
    for team in json_data['teams']:
        if team['teamID'] == team_id:
            return team.get('challenge_number')
    return None


def start_challenge(challenge_number):
    random = False
    diff = None
    minutes = 5000
    target = None

    challenge_number = int(challenge_number)
    if challenge_number == 1:
        minutes = 1.25
        target = "hack"
        m,h = None,None
    elif challenge_number == 2:
        minutes = 3.5
        target=""
        random = True
        diff = 3
        m,h = 5,25
    elif challenge_number == 3:
        minutes = 5 
        target = ""
        random = True
        diff = 3
        m,h = 30,42


    result = pose_esti.start_watching(pose,mpDraw,mpPose,minutes*60,target,random,diff,m,h)
    print(f"starting challenge {challenge_number}")
    if result:
        print(f"Challenge {challenge_number} completed")
        show_correct_screen(challenge_number)
    else:
        print(f"Challenge {challenge_number} failed")
        show_failed_screen()   

    # challenge = challenges[challenge_number]
    # minutes = challenge[0]
    # target = challenge[1]
    # result = pose_esti.start_watching(pose,mpDraw,mpPose,minutes*60,target)

    # print(f"starting challenge {challenge_number}")

    # if result:
    #     print(f"Challenge {challenge_number} completed")
    #     # send them the flag and update the challenge number in the json file
    #     with open("team_data.json","w") as f:
    #         data = json.load(f)
    #         for team in data['teams']:
    #             if team['teamID'] == team_number:
    #                 team['challenge_number'] +=1
    #                 json.dump(data,f)
    # else:
    #     print(f"Challenge {challenge_number} failed")
    #     show_failed_screen()

def show_erorr_screen(num):
    for i in range(3):
        time.sleep(.1)
        failed_screen = tk.Toplevel()
        failed_screen.attributes("-fullscreen", True)
        failed_screen.configure(bg='yellow')
        failed_label = ttk.Label(failed_screen, text=f"ERROR ERROR {num}", font=("Helvetica", 50), foreground='white', background='yellow')
        failed_label.pack(expand=True)
        failed_screen.after(4000, failed_screen.destroy)  # Flash every 500 milliseconds


def show_correct_screen(num):
    for i in range(3):
        time.sleep(.1)
        failed_screen = tk.Toplevel()
        failed_screen.attributes("-fullscreen", True)
        failed_screen.configure(bg='green')
        failed_label = ttk.Label(failed_screen, text=f"COMPLTED {num}", font=("Helvetica", 50), foreground='white', background='green')
        failed_label.pack(expand=True)
        failed_screen.after(5000, failed_screen.destroy)  # Flash every 500 milliseconds


def show_failed_screen():
    for i in range(3):
        time.sleep(.1)
        failed_screen = tk.Toplevel()
        failed_screen.attributes("-fullscreen", True)
        failed_screen.configure(bg='red')
        failed_label = ttk.Label(failed_screen, text="FAILED", font=("Helvetica", 50), foreground='white', background='red')
        failed_label.pack(expand=True)
        failed_screen.after(2000, failed_screen.destroy)  # Flash every 500 milliseconds

def start_game():
    challenge_num = challenge_id_entry.get()
    start_challenge(challenge_num)


    # team_number = team_number_entry.get()
    # with open("team_data.json", "r") as f:
    #     data = json.load(f)
    # challenge_number = check_challenge_number(team_number, data)
    # if challenge_number is not None:
    #     print(f"Starting challenge {challenge_number} for team {team_number}")
    #     # Start the game
    #     start_challenge(challenge_number, team_number)
    # else:
    #     print(f"Team {team_number} not found or challenge not set")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Get the geometry of the second monitor
    second_monitor_geometry = window.winfo_toplevel().geometry().split('+')
    second_monitor_x = int(second_monitor_geometry[1])
    second_monitor_y = int(second_monitor_geometry[2])

    # Calculate the coordinates to center the window on the second monitor
    x = second_monitor_x + (screen_width // 2) - (width // 2)
    y = second_monitor_y + (screen_height // 2) - (height // 2)

    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def make_gui():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Main Menu")

    # Center the window
    center_window(root)

    # Team Number Entry
    challenge_id_label = ttk.Label(root, text="Enter Challenge ID:", font=("Helvetica", 20))
    challenge_id_label.pack(pady=20)
    global challenge_id_entry
    challenge_id_entry = ttk.Entry(root, font=("Helvetica", 20), width=20)
    challenge_id_entry.pack(pady=10)

    # Start Button
    start_button = ttk.Button(root, text="Start", command=start_game, style='my.TButton')
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    make_gui()
