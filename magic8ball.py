import random
import time
import os
import json
import datetime
import math

# ============================================================
#                    MAGIC 8 BALL
#                 THE ORACLE: ULTIMATE
# ============================================================

VERSION = "4.0.0"
GAME_NAME = "THE ORACLE"

SAVE_FILE = "oracle_save.json"

# ============================================================
#                         COLORS
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# ============================================================
#                       RESPONSES
# ============================================================

RESPONSES = {

    "positive": [
        "Absolutely.",
        "Without a doubt.",
        "The answer is clearly YES.",
        "You can count on it.",
        "The stars say yes.",
        "It is looking very promising.",
        "Most definitely.",
        "The Oracle approves.",
        "The future looks bright.",
        "All signs point toward YES.",
        "The answer has revealed itself.",
        "There is little doubt.",
        "The universe agrees.",
        "This looks extremely promising.",
        "YES. The Oracle has spoken."
    ],

    "negative": [
        "No.",
        "Definitely not.",
        "The answer is NO.",
        "Don't count on it.",
        "The stars say no.",
        "Very unlikely.",
        "I wouldn't bet on it.",
        "The Oracle rejects this.",
        "The signs point elsewhere.",
        "The future does not favor this.",
        "The answer is firmly NO.",
        "The Oracle sees trouble ahead.",
        "The universe disagrees.",
        "This path appears blocked.",
        "NO. The Oracle has spoken."
    ],

    "maybe": [
        "Maybe.",
        "The future is unclear.",
        "Ask again later.",
        "There is a possibility.",
        "The answer is hidden.",
        "Too uncertain to tell.",
        "The signs are mixed.",
        "The Oracle is undecided.",
        "The future remains uncertain.",
        "It could go either way.",
        "The answer lies somewhere between.",
        "The Oracle cannot see clearly.",
        "Time will reveal the answer.",
        "The possibility remains open.",
        "Not enough information."
    ],

    "chaotic": [
        "ERROR 404: FUTURE NOT FOUND.",
        "The universe has stopped responding.",
        "Bro, I have no idea.",
        "That question broke the Oracle.",
        "Ask the moon instead.",
        "The timeline is glitching.",
        "Absolutely... maybe... probably.",
        "The Oracle has chosen chaos.",
        "Reality.exe has stopped working.",
        "The future has disconnected.",
        "Critical prophecy failure.",
        "The universe refused to answer.",
        "Your question caused a timeline split.",
        "The Oracle requires a software update.",
        "UNKNOWN. VERY UNKNOWN."
    ],

    "mysterious": [
        "You already know the answer.",
        "The answer is closer than you think.",
        "Something is approaching.",
        "The truth is hidden beneath the question.",
        "The Oracle sees something... unusual.",
        "There are forces you cannot see.",
        "The answer will reveal itself soon.",
        "Not everything is meant to be known.",
        "The path ahead is covered in fog.",
        "Something has changed.",
        "The Oracle remembers.",
        "Look beyond the obvious.",
        "The answer is watching you.",
        "The future refuses to speak.",
        "Some questions should remain unanswered."
    ],

    "funny": [
        "Ask your Wi-Fi.",
        "Bro, that's above my pay grade.",
        "I asked the ball. It laughed.",
        "The Oracle says: probably not.",
        "I would tell you, but I forgot.",
        "My crystal ball needs charging.",
        "The answer is hiding under the couch.",
        "The Oracle has left the chat.",
        "Have you tried asking nicely?",
        "That question is crazy.",
        "I consulted the universe. It said 'idk'.",
        "The ball needs a snack.",
        "Come back after updating reality.",
        "The Oracle is currently AFK.",
        "No comment."
    ]
}

# ============================================================
#                         MOODS
# ============================================================

MOODS = {
    "calm": {
        "description": "The Oracle is peaceful.",
        "modifier": 0
    },

    "mysterious": {
        "description": "The Oracle is hiding something.",
        "modifier": 5
    },

    "chaotic": {
        "description": "Reality is unstable.",
        "modifier": 15
    },

    "angry": {
        "description": "The Oracle does not appreciate your questions.",
        "modifier": -5
    },

    "powerful": {
        "description": "The Oracle is extremely powerful.",
        "modifier": 10
    },

    "sleepy": {
        "description": "The Oracle would rather be sleeping.",
        "modifier": -10
    }
}

# ============================================================
#                      ACHIEVEMENTS
# ============================================================

ACHIEVEMENTS = {

    "first_question": {
        "name": "First Contact",
        "description": "Ask your first question.",
        "xp": 25
    },

    "ten_questions": {
        "name": "Curious",
        "description": "Ask 10 questions.",
        "xp": 50
    },

    "fifty_questions": {
        "name": "Oracle Addict",
        "description": "Ask 50 questions.",
        "xp": 100
    },

    "hundred_questions": {
        "name": "Oracle Master",
        "description": "Ask 100 questions.",
        "xp": 250
    },

    "chaos": {
        "name": "Chaos Unleashed",
        "description": "Receive a chaotic response.",
        "xp": 50
    },

    "mystery": {
        "name": "Hidden Truth",
        "description": "Receive a mysterious response.",
        "xp": 50
    },

    "streak_5": {
        "name": "Five in a Row",
        "description": "Ask questions five times in a row.",
        "xp": 75
    },

    "streak_10": {
        "name": "Unstoppable",
        "description": "Ask questions ten times in a row.",
        "xp": 150
    },

    "secret": {
        "name": "Forbidden Knowledge",
        "description": "Discover the secret command.",
        "xp": 100
    },

    "level_10": {
        "name": "Oracle Apprentice",
        "description": "Reach level 10.",
        "xp": 100
    },

    "level_25": {
        "name": "Oracle Expert",
        "description": "Reach level 25.",
        "xp": 250
    },

    "level_50": {
        "name": "Oracle Legend",
        "description": "Reach level 50.",
        "xp": 500
    }
}

# ============================================================
#                         PLAYER
# ============================================================

player = {
    "name": "Player",
    "xp": 0,
    "level": 1,

    "total_questions": 0,

    "positive": 0,
    "negative": 0,
    "maybe": 0,
    "chaotic": 0,
    "mysterious": 0,
    "funny": 0,

    "streak": 0,
    "best_streak": 0,

    "achievements": [],

    "history": [],

    "custom_responses": [],

    "theme": "default",

    "oracle_mood": "calm",

    "created": str(datetime.datetime.now())
}

# ============================================================
#                       UTILITIES
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def slow_print(text, delay=0.015):
    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)

    print()


def line(character="=", length=70):
    print(character * length)


def title(text):
    clear()

    line()
    print(f"{BOLD}{CYAN}{text.center(70)}{RESET}")
    line()


# ============================================================
#                         SAVE SYSTEM
# ============================================================

def save_game():

    try:

        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(player, file, indent=4)

        print(f"{GREEN}Game saved successfully.{RESET}")

    except Exception as error:
        print(f"{RED}Could not save game: {error}{RESET}")


def load_game():

    global player

    if not os.path.exists(SAVE_FILE):
        return

    try:

        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        player.update(data)

        print(f"{GREEN}Save data loaded.{RESET}")

    except Exception:
        print(f"{RED}Save file could not be loaded.{RESET}")


# ============================================================
#                       LEVEL SYSTEM
# ============================================================

def xp_required(level):

    return int(100 * (level ** 1.35))


def check_level():

    while player["xp"] >= xp_required(player["level"]):

        required = xp_required(player["level"])

        player["xp"] -= required
        player["level"] += 1

        print()
        line("*")
        print(
            f"{YELLOW}{BOLD}"
            f"LEVEL UP! You are now level {player['level']}!"
            f"{RESET}"
        )
        line("*")

        unlock_achievement_for_level()


def add_xp(amount):

    player["xp"] += amount

    check_level()


# ============================================================
#                     ACHIEVEMENT SYSTEM
# ============================================================

def unlock_achievement(key):

    if key not in ACHIEVEMENTS:
        return

    if key in player["achievements"]:
        return

    achievement = ACHIEVEMENTS[key]

    player["achievements"].append(key)

    print()
    line("*")
    print(
        f"{YELLOW}{BOLD}"
        f"ACHIEVEMENT UNLOCKED"
        f"{RESET}"
    )
    print(f"{CYAN}{achievement['name']}{RESET}")
    print(achievement["description"])
    print(f"+{achievement['xp']} XP")
    line("*")

    player["xp"] += achievement["xp"]

    check_level()


def unlock_achievement_for_level():

    if player["level"] >= 10:
        unlock_achievement("level_10")

    if player["level"] >= 25:
        unlock_achievement("level_25")

    if player["level"] >= 50:
        unlock_achievement("level_50")


def check_achievements():

    questions = player["total_questions"]

    if questions >= 1:
        unlock_achievement("first_question")

    if questions >= 10:
        unlock_achievement("ten_questions")

    if questions >= 50:
        unlock_achievement("fifty_questions")

    if questions >= 100:
        unlock_achievement("hundred_questions")

    if player["streak"] >= 5:
        unlock_achievement("streak_5")

    if player["streak"] >= 10:
        unlock_achievement("streak_10")


# ============================================================
#                      ORACLE MOOD
# ============================================================

def change_mood():

    player["oracle_mood"] = random.choice(list(MOODS.keys()))


def show_mood():

    mood = player["oracle_mood"]

    data = MOODS[mood]

    print(f"\nCurrent Oracle mood: {CYAN}{mood.upper()}{RESET}")
    print(data["description"])


# ============================================================
#                     RESPONSE ENGINE
# ============================================================

def determine_category():

    mood = player["oracle_mood"]

    roll = random.randint(1, 100)

    modifier = MOODS[mood]["modifier"]

    roll += modifier

    if roll <= 35:
        return "positive"

    elif roll <= 65:
        return "negative"

    elif roll <= 82:
        return "maybe"

    elif roll <= 90:
        return "mysterious"

    elif roll <= 96:
        return "funny"

    else:
        return "chaotic"


def get_answer(category):

    possible_answers = RESPONSES.get(category, [])

    if player["custom_responses"]:
        possible_answers += player["custom_responses"]

    if not possible_answers:
        return "The Oracle has no answer."

    return random.choice(possible_answers)


# ============================================================
#                       LOADING
# ============================================================

def oracle_loading():

    phrases = [
        "Consulting the Oracle",
        "Reading the timeline",
        "Searching the future",
        "Consulting the stars",
        "Scanning reality",
        "Calculating probability",
        "Opening the prophecy"
    ]

    phrase = random.choice(phrases)

    print(f"\n{CYAN}{phrase}{RESET}", end="")

    for _ in range(random.randint(3, 6)):

        time.sleep(0.35)

        print(".", end="", flush=True)

    print()


# ============================================================
#                         BALL
# ============================================================

def show_ball():

    print(f"""
{CYAN}
                 ███████████████████
             ███                     ███
          ███                             ███
        ██                                   ██
      ██                                       ██
     ██                                         ██
    ██                                           ██
    ██              ███████████                  ██
    ██             ██           ██                ██
    ██            ██             ██               ██
    ██            ██      8      ██               ██
    ██            ██             ██               ██
    ██             ██           ██                ██
    ██              █████████████                 ██
    ██                                           ██
     ██                                         ██
      ██                                       ██
        ██                                   ██
          ███                             ███
             ███                     ███
                 ███████████████████
{RESET}
""")


# ============================================================
#                       ASK QUESTION
# ============================================================

def ask_question():

    question = input("\nAsk the Oracle: ").strip()

    if not question:

        print(f"{RED}You need to ask a question.{RESET}")
        return

    player["total_questions"] += 1
    player["streak"] += 1

    if player["streak"] > player["best_streak"]:
        player["best_streak"] = player["streak"]

    change_mood()

    oracle_loading()

    category = determine_category()

    answer = get_answer(category)

    player[category] += 1

    history_entry = {
        "question": question,
        "answer": answer,
        "category": category,
        "mood": player["oracle_mood"],
        "time": str(datetime.datetime.now())
    }

    player["history"].append(history_entry)

    add_xp(random.randint(10, 25))

    if category == "chaotic":
        unlock_achievement("chaos")

    if category == "mysterious":
        unlock_achievement("mystery")

    check_achievements()

    print()

    line()

    print(f"{BOLD}{CYAN}THE ORACLE SPEAKS{RESET}".center(80))

    line("-")

    print(f"Question:")
    print(f"{WHITE}{question}{RESET}")

    print()

    print(f"Mood: {MAGENTA}{player['oracle_mood'].upper()}{RESET}")
    print(f"Category: {YELLOW}{category.upper()}{RESET}")

    print()

    print(
        f"{BOLD}{GREEN}"
        f"{answer}"
        f"{RESET}"
    )

    line()

    print(
        f"XP: {player['xp']} / "
        f"{xp_required(player['level'])}"
    )

    print(
        f"Level: {player['level']} | "
        f"Streak: {player['streak']}"
    )


# ============================================================
#                        HISTORY
# ============================================================

def show_history():

    title("ORACLE HISTORY")

    if not player["history"]:

        print("No questions have been asked yet.")
        pause()
        return

    for index, entry in enumerate(
        reversed(player["history"]),
        start=1
    ):

        print(f"\n#{index}")
        print("-" * 50)

        print("Question:", entry["question"])
        print("Answer:", entry["answer"])
        print("Category:", entry["category"])
        print("Mood:", entry["mood"])
        print("Time:", entry["time"])

    pause()


# ============================================================
#                       STATISTICS
# ============================================================

def show_statistics():

    title("ORACLE STATISTICS")

    total = player["total_questions"]

    print(f"Player: {player['name']}")
    print(f"Level: {player['level']}")
    print(f"XP: {player['xp']}")

    print()

    print(f"Total questions: {total}")
    print(f"Current streak: {player['streak']}")
    print(f"Best streak: {player['best_streak']}")

    print()

    categories = [
        "positive",
        "negative",
        "maybe",
        "mysterious",
        "funny",
        "chaotic"
    ]

    for category in categories:

        amount = player[category]

        if total > 0:
            percentage = (amount / total) * 100
        else:
            percentage = 0

        bar_length = int(percentage / 5)

        bar = "█" * bar_length

        print(
            f"{category.capitalize():12}"
            f"{bar:<20}"
            f"{percentage:5.1f}%"
        )

    pause()


# ============================================================
#                    ACHIEVEMENTS MENU
# ============================================================

def show_achievements():

    title("ACHIEVEMENTS")

    for key, achievement in ACHIEVEMENTS.items():

        if key in player["achievements"]:

            status = f"{GREEN}UNLOCKED{RESET}"

        else:

            status = f"{DIM}LOCKED{RESET}"

        print(
            f"\n{achievement['name']}"
            f" — {status}"
        )

        print(
            f"  {achievement['description']}"
        )

        print(
            f"  Reward: {achievement['xp']} XP"
        )

    pause()


# ============================================================
#                         PROFILE
# ============================================================

def show_profile():

    title("PLAYER PROFILE")

    print(f"Name: {player['name']}")
    print(f"Level: {player['level']}")
    print(f"XP: {player['xp']}")
    print(
        f"XP required: "
        f"{xp_required(player['level'])}"
    )

    print()

    print(
        f"Questions asked: "
        f"{player['total_questions']}"
    )

    print(
        f"Current streak: "
        f"{player['streak']}"
    )

    print(
        f"Best streak: "
        f"{player['best_streak']}"
    )

    print()

    print(
        f"Achievements: "
        f"{len(player['achievements'])}"
        f"/{len(ACHIEVEMENTS)}"
    )

    print(
        f"Oracle mood: "
        f"{player['oracle_mood']}"
    )

    print(
        f"Theme: "
        f"{player['theme']}"
    )

    print()

    print("Created:", player["created"])

    pause()


# ============================================================
#                      CHANGE NAME
# ============================================================

def change_name():

    name = input("\nEnter your new Oracle name: ").strip()

    if not name:

        print("Name cannot be empty.")
        return

    if len(name) > 30:

        print("Name is too long.")
        return

    player["name"] = name

    print(f"\nName changed to {name}.")


# ============================================================
#                    CUSTOM RESPONSES
# ============================================================

def add_custom_response():

    response = input(
        "\nEnter a custom Oracle response: "
    ).strip()

    if not response:
        print("Response cannot be empty.")
        return

    if len(response) > 150:
        print("Response is too long.")
        return

    player["custom_responses"].append(response)

    print("Custom response added.")


def remove_custom_response():

    if not player["custom_responses"]:

        print("\nYou have no custom responses.")
        return

    print("\nCustom responses:")

    for index, response in enumerate(
        player["custom_responses"],
        start=1
    ):

        print(f"{index}. {response}")

    try:

        choice = int(
            input("\nChoose one to remove: ")
        )

        if 1 <= choice <= len(
            player["custom_responses"]
        ):

            removed = player[
                "custom_responses"
            ].pop(choice - 1)

            print(
                f"Removed: {removed}"
            )

        else:

            print("Invalid choice.")

    except ValueError:

        print("Enter a number.")


def custom_response_menu():

    while True:

        title("CUSTOM RESPONSES")

        print("1. Add response")
        print("2. Remove response")
        print("3. View responses")
        print("4. Back")

        choice = input("\nChoice: ")

        if choice == "1":

            add_custom_response()

        elif choice == "2":

            remove_custom_response()

        elif choice == "3":

            if player["custom_responses"]:

                for response in player[
                    "custom_responses"
                ]:

                    print("-", response)

            else:

                print("No custom responses.")

            pause()

        elif choice == "4":

            break

        else:

            print("Invalid choice.")


# ============================================================
#                         THEMES
# ============================================================

THEMES = {
    "default": CYAN,
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "purple": MAGENTA,
    "yellow": YELLOW
}


def change_theme():

    title("THEMES")

    names = list(THEMES.keys())

    for index, theme in enumerate(names, start=1):

        print(f"{index}. {theme}")

    try:

        choice = int(
            input("\nChoose theme: ")
        )

        if 1 <= choice <= len(names):

            player["theme"] = names[choice - 1]

            print(
                f"Theme changed to "
                f"{player['theme']}."
            )

        else:

            print("Invalid choice.")

    except ValueError:

        print("Enter a number.")


# ============================================================
#                      SETTINGS MENU
# ============================================================

def settings():

    while True:

        title("SETTINGS")

        print("1. Change name")
        print("2. Change theme")
        print("3. Custom responses")
        print("4. Show Oracle mood")
        print("5. Save game")
        print("6. Back")

        choice = input("\nChoice: ")

        if choice == "1":

            change_name()

        elif choice == "2":

            change_theme()

        elif choice == "3":

            custom_response_menu()

        elif choice == "4":

            show_mood()
            pause()

        elif choice == "5":

            save_game()
            pause()

        elif choice == "6":

            break

        else:

            print("Invalid choice.")


# ============================================================
#                     RESET STREAK
# ============================================================

def reset_streak():

    player["streak"] = 0

    print("Streak reset.")


# ============================================================
#                       SECRET MODE
# ============================================================

def secret_mode():

    unlock_achievement("secret")

    title("████ SECRET MODE ████")

    print(f"""
{RED}
The Oracle has revealed a hidden layer.

You were never supposed to find this.

Reality is only pretending to be stable.

There is something behind the answers.

Something watching.

Something waiting.

{RESET}
""")

    time.sleep(2)

    number = random.randint(1, 999999)

    print(
        f"SECRET TIMELINE NUMBER: {number}"
    )

    print()

    if number % 2 == 0:

        print(
            "The timeline is currently stable."
        )

    else:

        print(
            "The timeline is currently unstable."
        )

    pause()


# ============================================================
#                     EXPORT HISTORY
# ============================================================

def export_history():

    filename = input(
        "\nEnter filename "
        "(example: history.txt): "
    ).strip()

    if not filename:

        print("Invalid filename.")
        return

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            for number, entry in enumerate(
                player["history"],
                start=1
            ):

                file.write(
                    f"QUESTION #{number}\n"
                )

                file.write(
                    f"Question: "
                    f"{entry['question']}\n"
                )

                file.write(
                    f"Answer: "
                    f"{entry['answer']}\n"
                )

                file.write(
                    f"Category: "
                    f"{entry['category']}\n"
                )

                file.write(
                    f"Mood: "
                    f"{entry['mood']}\n"
                )

                file.write(
                    f"Time: "
                    f"{entry['time']}\n"
                )

                file.write("\n")

        print(
            f"\nHistory exported to {filename}"
        )

    except Exception as error:

        print(
            f"Could not export history: "
            f"{error}"
        )


# ============================================================
#                       COMMAND MENU
# ============================================================

def show_help():

    title("COMMAND CENTER")

    commands = {

        "ask":
            "Ask the Oracle a question.",

        "history":
            "View your question history.",

        "stats":
            "View detailed statistics.",

        "profile":
            "View your player profile.",

        "achievements":
            "View achievements.",

        "ball":
            "Display the Magic 8 Ball.",

        "mood":
            "View the current Oracle mood.",

        "settings":
            "Open settings.",

        "save":
            "Save your progress.",

        "export":
            "Export question history.",

        "secret":
            "Enter secret mode.",

        "help":
            "Display this command list.",

        "exit":
            "Exit the Oracle."
    }

    for command, description in commands.items():

        print(
            f"{CYAN}{command:<15}{RESET}"
            f"{description}"
        )

    pause()


# ============================================================
#                      MAIN MENU
# ============================================================

def main_menu():

    while True:

        title("THE ORACLE")

        print(
            f"Welcome, "
            f"{BOLD}{player['name']}{RESET}."
        )

        print()

        print(
            f"Level: {player['level']}    "
            f"XP: {player['xp']}    "
            f"Questions: {player['total_questions']}"
        )

        print()

        print("1. Ask the Oracle")
        print("2. History")
        print("3. Statistics")
        print("4. Profile")
        print("5. Achievements")
        print("6. Oracle Ball")
        print("7. Settings")
        print("8. Command Center")
        print("9. Save Game")
        print("0. Exit")

        choice = input("\nChoose: ").strip()

        if choice == "1":

            ask_question()
            pause()

        elif choice == "2":

            show_history()

        elif choice == "3":

            show_statistics()

        elif choice == "4":

            show_profile()

        elif choice == "5":

            show_achievements()

        elif choice == "6":

            title("THE ORACLE")
            show_ball()
            pause()

        elif choice == "7":

            settings()

        elif choice == "8":

            show_help()

        elif choice == "9":

            save_game()
            pause()

        elif choice == "0":

            save_game()

            print(
                f"\n{CYAN}"
                f"The Oracle has gone silent."
                f"{RESET}"
            )

            print("Goodbye.")

            break

        else:

            print(
                f"{RED}"
                f"Invalid selection."
                f"{RESET}"
            )

            time.sleep(1)


# ============================================================
#                         STARTUP
# ============================================================

def startup():

    clear()

    print(
        f"{CYAN}{BOLD}"
        r"""
     ████████╗██╗  ██╗███████╗
     ╚══██╔══╝██║  ██║██╔════╝
        ██║   ███████║█████╗
        ██║   ██╔══██║██╔══╝
        ██║   ██║  ██║███████╗
        ╚═╝   ╚═╝  ╚═╝╚══════╝

        ██████╗ ██████╗  █████╗ ██╗     
       ██╔═══██╗██╔══██╗██╔══██╗██║     
       ██║   ██║██████╔╝███████║██║     
       ██║   ██║██╔══██╗██╔══██║██║     
       ╚██████╔╝██║  ██║██║  ██║███████╗
        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
        """
        f"{RESET}"
    )

    print(
        f"\n{MAGENTA}"
        f"THE ORACLE — ULTIMATE EDITION"
        f"{RESET}"
    )

    print(
        f"Version {VERSION}"
    )

    print()

    load_game()

    time.sleep(1)

    main_menu()


# ============================================================
#                         RUN
# ============================================================

if __name__ == "__main__":
    startup()