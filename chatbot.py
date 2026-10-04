"""
Task 1: Rule-Based Chatbot
--------------------------
A simple chatbot that uses if-else logic and regex pattern matching
to understand user input and reply with predefined responses.

Run:  python chatbot.py
Exit: type 'bye', 'exit' or 'quit'
"""

import random
import re
from datetime import datetime


class RuleBasedChatbot:
    def __init__(self, bot_name="Buddy"):
        self.bot_name = bot_name
        self.user_name = None
        self.last_topic = None  # simple conversation memory

    # ---------- Helpers ----------
    @staticmethod
    def clean(text):
        """Lowercase, trim, and strip punctuation so matching is easier."""
        text = text.lower().strip()
        return re.sub(r"[^\w\s']", "", text)

    @staticmethod
    def has(pattern, text):
        """True if the regex pattern appears as whole word(s) in text."""
        return re.search(rf"\b(?:{pattern})\b", text) is not None

    # ---------- Core rule engine ----------
    def respond(self, raw_input):
        text = self.clean(raw_input)

        if not text:
            return "Please type something, I'm listening!"

        # 1. Exit
        if self.has(r"bye|goodbye|exit|quit|see you|cya", text):
            name = f", {self.user_name}" if self.user_name else ""
            return f"Goodbye{name}! Have a great day!"

        # 2. Capture the user's name (pattern with a capture group)
        match = re.search(r"\b(?:my name is|i am called|call me)\s+([a-z]+)", text)
        if match:
            self.user_name = match.group(1).capitalize()
            self.last_topic = "name"
            return f"Nice to meet you, {self.user_name}! How can I help you today?"

        # 3. Greetings
        if self.has(r"hi|hello|hey|hola|namaste|good morning|good afternoon|good evening", text):
            self.last_topic = "greeting"
            greeting = random.choice(["Hello", "Hi there", "Hey"])
            if self.user_name:
                return f"{greeting}, {self.user_name}! What can I do for you?"
            return f"{greeting}! I'm {self.bot_name}. What's your name?"

        # 4. Asking the bot's name
        if re.search(r"\b(your name|who are you)\b", text):
            return f"I'm {self.bot_name}, a simple rule-based chatbot."

        # 5. Asking the user's name back
        if re.search(r"\b(my name|do you know me|who am i)\b", text):
            if self.user_name:
                return f"Of course, you're {self.user_name}!"
            return "I don't know your name yet. Tell me with 'My name is ...'"

        # 6. How are you
        if re.search(r"\bhow are you\b|\bhow r u\b|\bhow('s| is) it going\b", text):
            self.last_topic = "feeling"
            return "I'm doing great, thanks for asking! How about you?"

        # 7. Follow-up to 'how are you' (uses conversation context)
        if self.last_topic == "feeling" and self.has(r"good|fine|great|well|awesome|okay|ok", text):
            self.last_topic = None
            return "Glad to hear that!"
        if self.last_topic == "feeling" and self.has(r"bad|sad|tired|sick|not good|terrible", text):
            self.last_topic = None
            return "Sorry to hear that. I hope things get better soon!"

        # 8. Time and date
        if self.has(r"time", text) and not self.has(r"sometimes|timetable", text):
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."
        if self.has(r"date|today|day", text) and re.search(r"\b(date|today|what day)\b", text):
            return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

        # 9. Capabilities / help
        if self.has(r"help|what can you do|capabilities|features", text):
            return ("I can greet you, remember your name, tell the time and date, "
                    "tell a joke, do simple maths (e.g. 'calculate 5 + 3'), "
                    "and chat a little. Try me!")

        # 10. Jokes
        if self.has(r"joke|funny|make me laugh", text):
            return random.choice([
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why was the computer cold? It left its Windows open!",
                "There are 10 types of people: those who understand binary and those who don't.",
            ])

        # 11. Simple calculator: "calculate 12 * 4", "what is 7 plus 3"
        calc = re.search(r"(-?\d+(?:\.\d+)?)\s*(\+|-|\*|x|/|plus|minus|times|divided by)\s*(-?\d+(?:\.\d+)?)", raw_input.lower())
        if calc:
            a, op, b = float(calc.group(1)), calc.group(2), float(calc.group(3))
            if op in ("+", "plus"):
                result = a + b
            elif op in ("-", "minus"):
                result = a - b
            elif op in ("*", "x", "times"):
                result = a * b
            else:
                if b == 0:
                    return "I can't divide by zero!"
                result = a / b
            return f"The answer is {result:g}."

        # 12. Thanks
        if self.has(r"thanks|thank you|thx|ty", text):
            return random.choice(["You're welcome!", "Happy to help!", "Anytime!"])

        # 13. Weather (cannot do live data - polite rule)
        if self.has(r"weather|temperature|rain", text):
            return "I can't check live weather, but a weather app will help you out."

        # 14. Compliments / small talk
        if self.has(r"love you|you are great|you are awesome|nice bot|good bot", text):
            return "Aww, thank you! You're awesome too."
        if self.has(r"age|old are you", text) and "you" in text:
            return "I'm just a few lines of Python, so I have no age!"

        # 15. Default fallback
        return random.choice([
            "Sorry, I didn't understand that. Could you rephrase it?",
            "Hmm, I'm not sure how to answer that. Type 'help' to see what I can do.",
            "I'm still learning! Try asking something else.",
        ])


def main():
    bot = RuleBasedChatbot("Buddy")
    print("=" * 50)
    print(f" {bot.bot_name} - Rule-Based Chatbot")
    print(" Type 'help' for options, 'bye' to quit")
    print("=" * 50)
    print(f"{bot.bot_name}: Hi! I'm {bot.bot_name}. How can I help you?")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.bot_name}: Goodbye!")
            break

        reply = bot.respond(user_input)
        print(f"{bot.bot_name}: {reply}")

        if re.search(r"\b(bye|goodbye|exit|quit|see you|cya)\b", user_input.lower()):
            break


if __name__ == "__main__":
    main()