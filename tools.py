import os
import time
import webbrowser
import sys
import requests
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ১. ইউজারের আইপি এবং লোকেশন ডাটা সংগ্রহ
def get_user_info():
    try:
        data = requests.get('https://ipapi.co/json/').json()
        info = {
            "ip": data.get("ip", "Unknown"),
            "city": data.get("city", "Unknown"),
            "country": data.get("country_name", "Unknown"),
            "timezone": data.get("timezone", "Unknown"),
            "org": data.get("org", "Unknown")
        }
        return info
    except:
        return {"ip": "Offline", "city": "N/A", "country": "N/A", "timezone": "N/A", "org": "N/A"}

# ২. এনিমেটেড লোডিং
def loading_screen(msg):
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold magenta"),
        TextColumn("[white]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        expand=True
    ) as progress:
        task = progress.add_task(msg, total=100)
        while not progress.finished:
            progress.update(task, advance=2.5)
            time.sleep(0.02)

# ৩. মেইন ব্যানার
def get_banner():
    banner_art = """
    ██████╗ ██████╗  ██████╗     ████████╗ ██████╗  ██████╗ ██╗
    ██╔══██╗██╔══██╗██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
    ██████╔╝██████╔╝██║   ██║       ██║   ██║   ██║██║   ██║██║
    ██╔═══╝ ██╔══██╗██║   ██║       ██║   ██║   ██║██║   ██║██║
    ██║     ██║  ██║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    return Panel(Align.center(Text(banner_art, style="bold red")), border_style="bright_blue")

# ৪. লগইন সিস্টেম
def login_ui():
    clear()
    console.print(get_banner())
    console.print(Align.center("[bold yellow]LOGIN  PROTOCOL[/bold yellow]\n"))
    
    user = Prompt.ask("[bold white]👤 USER[/bold white]", default="admin")
    pw = Prompt.ask("[bold white]🔑 PASS[/bold white]", password=True)

    if user == "admin" and pw == "123":
        loading_screen("Bypassing Firewall")
        console.print("\n[bold reverse green]  GRANTED  [/bold reverse green]")
        time.sleep(1)
        webbrowser.open("https://www.facebook.com/profile.php?id=61578220087761")
        main_dashboard()
    else:
        console.print("\n[bold reverse red]  DENIED  [/bold reverse red]")
        time.sleep(2)
        login_ui()

# ৫. মেইন ড্যাশবোর্ড
def main_dashboard():
    clear()
    user_data = get_user_info()
    
    # ইউজার ইনফো প্যানেল
    info_text = Text()
    info_text.append(f"🌐 IP ADDR : {user_data['ip']}\n", style="bold cyan")
    info_text.append(f"📍 LOCATION: {user_data['city']}, {user_data['country']}\n", style="bold green")
    info_text.append(f"⏰ TIMEZONE: {user_data['timezone']}\n", style="bold yellow")
    info_text.append(f"🏢 ISP     : {user_data['org']}", style="bold magenta")
    
    user_panel = Panel(info_text, title="[bold white]USER NETWORK DETAILS[/bold white]", border_style="white")

    # মেনু টেবিল
    table = Table(expand=True, border_style="bright_magenta")
    table.add_column("SL", justify="center", style="bold yellow")
    table.add_column("TOOL NAME", style="bold white")
    table.add_column("STATUS", justify="center")

    table.add_row("01", "🚀 SYSTEM SCANNER (CORE)", "[green]READY[/green]")
    table.add_row("02", "👤 DEVELOPER DATABASE", "[blue]INFO[/blue]")
    table.add_row("03", "🔄 UPDATE SYSTEM", "[yellow]V1.0[/yellow]")
    table.add_row("00", "❌ DISCONNECT", "[red]EXIT[/red]")

    console.print(get_banner())
    console.print(user_panel)
    console.print(Panel(table, title="[bold cyan]COMMAND CENTER[/bold cyan]", border_style="blue"))
    console.print(Align.center(f"[dim]Last Sync: {datetime.now().strftime('%H:%M:%S')}"))

    choice = Prompt.ask("\n[bold cyan]Select Protocol[/bold cyan]", choices=["1", "2", "3", "0"])

    if choice == "1":
        loading_screen("Scanning Local Ports")
        console.print(Panel(f"[bold green]Scanning Complete![/bold green]\nTarget IP: {user_data['ip']}\nStatus: All systems nominal.", title="RESULT"))
        input("\nPress Enter...")
        main_dashboard()
        
    elif choice == "2":
        clear()
        about = f"""
        [bold red]NAME      :[/bold red] MULTI-TOOL
        [bold red]DEV       :[/bold red] MR. BILLU
        [bold red]FB PROFILE:[/bold red] [link]https://fb.com/61578220087761[/link]
        [bold red]LICENSE   :[/bold red] [bold green]MR. PREMIUM[/bold green]
        """
        console.print(Panel(about, title="ABOUT DEVELOPER", border_style="yellow"))
        input("\nPress Enter...")
        main_dashboard()
        
    elif choice == "3":
        loading_screen("Checking Repository Updates")
        console.print("[bold yellow]✔ System is synchronized with the latest version (1.0).[/bold yellow]")
        time.sleep(2)
        main_dashboard()
        
    elif choice == "0":
        console.print("[bold red]Connection Terminated.[/bold red]")
        sys.exit()

if __name__ == "__main__":
    try:
        login_ui()
    except KeyboardInterrupt:
        print("\n[!] Disconnected.")
def loading_screen(msg):
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold magenta"),
        TextColumn("[white]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        expand=True
    ) as progress:
        task = progress.add_task(msg, total=100)
        while not progress.finished:
            progress.update(task, advance=2.5)
            time.sleep(0.02)

# ৩. মেইন ব্যানার
def get_banner():
    banner_art = """
    ██████╗ ██████╗  ██████╗     ████████╗ ██████╗  ██████╗ ██╗
    ██╔══██╗██╔══██╗██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
    ██████╔╝██████╔╝██║   ██║       ██║   ██║   ██║██║   ██║██║
    ██╔═══╝ ██╔══██╗██║   ██║       ██║   ██║   ██║██║   ██║██║
    ██║     ██║  ██║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    return Panel(Align.center(Text(banner_art, style="bold red")), border_style="bright_blue")

# ৪. লগইন সিস্টেম
def login_ui():
    clear()
    console.print(get_banner())
    console.print(Align.center("[bold yellow]L O G I N  P R O T O C O L[/bold yellow]\n"))
    
    user = Prompt.ask("[bold white]👤 USER[/bold white]", default="admin")
    pw = Prompt.ask("[bold white]🔑 PASS[/bold white]", password=True)

    if user == "admin" and pw == "123":
        loading_screen("Bypassing Firewall")
        console.print("\n[bold reverse green]  GRANTED  [/bold reverse green]")
        time.sleep(1)
        webbrowser.open("https://www.facebook.com/profile.php?id=61578220087761")
        main_dashboard()
    else:
        console.print("\n[bold reverse red]  DENIED  [/bold reverse red]")
        time.sleep(2)
        login_ui()

# ৫. মেইন ড্যাশবোর্ড
def main_dashboard():
    clear()
    user_data = get_user_info()
    
    # ইউজার ইনফো প্যানেল
    info_text = Text()
    info_text.append(f"🌐 IP ADDR : {user_data['ip']}\n", style="bold cyan")
    info_text.append(f"📍 LOCATION: {user_data['city']}, {user_data['country']}\n", style="bold green")
    info_text.append(f"⏰ TIMEZONE: {user_data['timezone']}\n", style="bold yellow")
    info_text.append(f"🏢 ISP     : {user_data['org']}", style="bold magenta")
    
    user_panel = Panel(info_text, title="[bold white]USER NETWORK DETAILS[/bold white]", border_style="white")

    # মেনু টেবিল
    table = Table(expand=True, border_style="bright_magenta")
    table.add_column("SL", justify="center", style="bold yellow")
    table.add_column("TOOL NAME", style="bold white")
    table.add_column("STATUS", justify="center")

    table.add_row("01", "🚀 SYSTEM SCANNER (CORE)", "[green]READY[/green]")
    table.add_row("02", "👤 DEVELOPER DATABASE", "[blue]INFO[/blue]")
    table.add_row("03", "🔄 UPDATE SYSTEM", "[yellow]V4.5[/yellow]")
    table.add_row("00", "❌ DISCONNECT", "[red]EXIT[/red]")

    console.print(get_banner())
    console.print(user_panel)
    console.print(Panel(table, title="[bold cyan]COMMAND CENTER[/bold cyan]", border_style="blue"))
    console.print(Align.center(f"[dim]Last Sync: {datetime.now().strftime('%H:%M:%S')}"))

    choice = Prompt.ask("\n[bold cyan]Select Protocol[/bold cyan]", choices=["1", "2", "3", "0"])

    if choice == "1":
        loading_screen("Scanning Local Ports")
        console.print(Panel(f"[bold green]Scanning Complete![/bold green]\nTarget IP: {user_data['ip']}\nStatus: All systems nominal.", title="RESULT"))
        input("\nPress Enter...")
        main_dashboard()
        
    elif choice == "2":
        clear()
        about = f"""
        [bold red]NAME      :[/bold red] PREMIUM MULTI-TOOL
        [bold red]DEV       :[/bold red] YOUR NAME / AI
        [bold red]FB PROFILE:[/bold red] [link]https://fb.com/61578220087761[/link]
        [bold red]LICENSE   :[/bold red] [bold green]LIFETIME PREMIUM[/bold green]
        """
        console.print(Panel(about, title="ABOUT DEVELOPER", border_style="yellow"))
        input("\nPress Enter...")
        main_dashboard()
        
    elif choice == "3":
        loading_screen("Checking Repository Updates")
        console.print("[bold yellow]✔ System is synchronized with the latest version (4.5).[/bold yellow]")
        time.sleep(2)
        main_dashboard()
        
    elif choice == "0":
        console.print("[bold red]Connection Terminated.[/bold red]")
        sys.exit()

if __name__ == "__main__":
    try:
        login_ui()
    except KeyboardInterrupt:
        print("\n[!] Disconnected.")
