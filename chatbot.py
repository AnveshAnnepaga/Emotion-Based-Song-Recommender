import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emotion_analyzer import analyze_emotion
from song_recommender import get_song_recommender
from user_logger import log_user_interaction
from clerk_service import create_user, find_user_by_email

console = Console()

def display_song_recommendation(song):
    """Prints the song details in a clean, professional format using rich."""
    table = Table(show_header=False, box=None, padding=0)
    table.add_column(style="bold")
    table.add_column(style="dim")

    table.add_row(Text("🎶 Title: ", style="bold green"), Text(song['song_title'], style="green"))
    table.add_row(Text("🎤 Artist:", style="bold blue"), Text(song['artists'], style="blue"))
    table.add_row(Text("🔗 Link:  ", style="bold cyan"), Text(song['link'], style="cyan"))

    panel = Panel(
        table,
        title="✨ Your Song Recommendation",
        title_align="left",
        border_style="dim",
        padding=(1, 2)
    )
    console.print(panel)


def run_chatbot():
    console.print(Panel(
        Text("🎶 Emotion-Based Song Recommender", style="bold white"),
        title_align="center",
        border_style="bold magenta",
        padding=(1, 4)
    ))
    console.print("\n[bold]Please log in or sign up to continue.[/bold]")

    # --- Authentication Flow ---
    user_id = None
    while not user_id:
        action = console.input("[bold yellow]> Type 'login' or 'signup': [/bold yellow]").lower()

        if action == 'login':
            email = console.input("Enter your email: ")
            password = console.input("Enter your password: ")
            # You would need a more robust login function here that also checks password
            user_id = find_user_by_email(email)
            if not user_id:
                console.print("[bold red]❌ Login failed. User not found. Please try again.[/bold red]")
        elif action == 'signup':
            email = console.input("Enter your email: ")
            password = console.input("Enter your password: ")
            user_id = create_user(email, password)
            if user_id:
                console.print("[bold green]✅ Sign-up successful! You can now log in.[/bold green]")
            else:
                console.print("[bold red]❌ Sign-up failed. Please try again.[/bold red]")
        else:
            console.print("[bold yellow]❗ Invalid option. Please choose 'login' or 'signup'.[/bold yellow]")

    # --- Main Chatbot Loop ---
    console.print("\n" + "-"*50)
    console.print("[bold blue]🟢 Login successful![/bold blue]")
    console.print(f"Welcome back! Your user ID is {user_id}.")
    console.print("\nFeel free to tell me how you're feeling.")
    console.print("[dim]Type 'quit' or 'exit' to end the conversation.[/dim]")
    console.print("-"*50)

    while True:
        user_input = console.input("[bold magenta]You:[/bold magenta] ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            console.print("\n[dim]👋 Chatbot: Goodbye! Hope you feel better.[/dim]")
            break

        if not user_input.strip():
            console.print("[dim]🤖 Chatbot: Please tell me something so I can help.[/dim]")
            continue

        try:
            console.print("\n[dim]🤖 Chatbot: Analyzing your mood...[/dim]")
            detected_mood = analyze_emotion(user_input)
            console.print(f"[bold]🤖 Chatbot: I detect you're feeling {detected_mood.upper()}...[/bold]")

            recommended_song = get_song_recommender(detected_mood)

            if recommended_song:
                display_song_recommendation(recommended_song)
                log_user_interaction(user_id, user_input, detected_mood, recommended_song['id'])
            else:
                console.print("[dim]🤖 Chatbot: Sorry, I couldn't find a song for that mood.[/dim]")

        except Exception as e:
           console.print(f"[dim]🤖 Chatbot: An error occurred: {e}[/dim]")
            
        console.print("-"*50)

if __name__ == "__main__":
    run_chatbot()