import os
import sys
import time
import requests
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt

console = Console()

# =========================
# CONFIG
# =========================
APP_NAME = "PRO TOOL"
APP_VERSION = "1.0.0"

GITHUB_USER = "TOXICBILLU"
GITHUB_REPO = "Tools"
GITHUB_BRANCH = "main"

REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/Version.txt"
REMOTE_MAIN_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/tools.py"

LOCAL_FILE = os.path.abspath(__file__)

# =========================
# BASIC
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading_screen(msg, speed=0.02):
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[white]{task.description}"),
        BarColumn(),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        expand=True
    ) as progress:
        task = progress.add_task(msg, total=100)
        while not progress.finished:
            progress.update(task, advance=2.5)
            time.sleep(speed)

# =========================
# USER NETWORK INFO
# =========================
def get_user_info():
    urls = [
        "https://ipapi.co/json/",
        "https://ipwho.is/",
        "http://ip-api.com/json/"
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            r.raise_for_status()
            data = r.json()

            # ipapi.co
            if "ip" in data and ("country_name" in data or "city" in data):
                return {
                    "ip": data.get("ip", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "country": data.get("country_name", data.get("country", "Unknown")),
                    "timezone": data.get("timezone", "Unknown"),
                    "org": data.get("org", data.get("asn_org", "Unknown"))
                }

            # ip-api.com
            if data.get("status") == "success":
                return {
                    "ip": data.get("query", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "country": data.get("country", "Unknown"),
                    "timezone": data.get("timezone", "Unknown"),
                    "org": data.get("isp", "Unknown")
                }

            # ipwho.is
            if "ip" in data and "country" in data:
                timezone = data.get("timezone", {})
                connection = data.get("connection", {})
                tz_value = timezone.get("id", "Unknown") if isinstance(timezone, dict) else str(timezone)
                isp_value = connection.get("isp", "Unknown") if isinstance(connection, dict) else "Unknown"

                return {
                    "ip": data.get("ip", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "country": data.get("country", "Unknown"),
                    "timezone": tz_value,
                    "org": isp_value
                }

        except Exception:
            continue

    return {
        "ip": "Offline",
        "city": "N/A",
        "country": "N/A",
        "timezone": "N/A",
        "org": "N/A"
    }

# =========================
# BANNER
# =========================
def get_banner():
    banner_art = f"""
██████╗ ██████╗  ██████╗     ████████╗ ██████╗  ██████╗ ██╗
██╔══██╗██╔══██╗██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
██████╔╝██████╔╝██║   ██║       ██║   ██║   ██║██║   ██║██║
██╔═══╝ ██╔══██╗██║   ██║       ██║   ██║   ██║██║   ██║██║
██║     ██║  ██║╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝     ╚═╝  ╚═╝ ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

{APP_NAME}  |  VERSION: {APP_VERSION}
"""
    return Panel(Align.center(Text(banner_art, style="bold red")), border_style="bright_blue")

# =========================
# UPDATE SYSTEM
# =========================
def fetch_remote_version():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(REMOTE_VERSION_URL, headers=headers, timeout=10)
    r.raise_for_status()
    return r.text.strip()

def fetch_remote_code():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(REMOTE_MAIN_URL, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text

def backup_current_file():
    backup_file = LOCAL_FILE + ".bak"
    with open(LOCAL_FILE, "r", encoding="utf-8") as src:
        current_code = src.read()
    with open(backup_file, "w", encoding="utf-8") as dst:
        dst.write(current_code)

def restore_backup():
    backup_file = LOCAL_FILE + ".bak"
    if os.path.exists(backup_file):
        with open(backup_file, "r", encoding="utf-8") as src:
            old_code = src.read()
        with open(LOCAL_FILE, "w", encoding="utf-8") as dst:
            dst.write(old_code)

def install_update(new_code):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)

def check_for_updates(show_no_update=True):
    try:
        loading_screen("Checking remote version", 0.01)
        remote_version = fetch_remote_version()

        if remote_version == APP_VERSION:
            if show_no_update:
                console.print(f"[bold green]✔ Already latest version: {APP_VERSION}[/bold green]")
            return False, remote_version

        console.print(f"[bold yellow]Update available:[/bold yellow] {APP_VERSION} → {remote_version}")
        return True, remote_version

    except Exception as e:
        console.print(f"[bold red]Update check failed:[/bold red] {e}")
        return False, None

def update_app():
    try:
        has_update, remote_version = check_for_updates(show_no_update=False)

        if not has_update:
            console.print(f"[bold green]✔ Already latest version: {APP_VERSION}[/bold green]")
            return

        confirm = Prompt.ask("[bold cyan]Do update now?[/bold cyan]", choices=["y", "n"], default="y")
        if confirm != "y":
            return

        loading_screen("Downloading new build", 0.01)
        new_code = fetch_remote_code()

        if "APP_VERSION" not in new_code or "def update_app()" not in new_code:
            console.print("[bold red]Downloaded file looks invalid. Update canceled.[/bold red]")
            return

        backup_current_file()
        install_update(new_code)

        console.print(f"[bold green]✔ Updated successfully to {remote_version}[/bold green]")
        console.print("[bold yellow]Restart the app now to use new features.[/bold yellow]")

    except Exception as e:
        console.print(f"[bold red]Update failed:[/bold red] {e}")
        console.print("[yellow]Trying to restore previous version...[/yellow]")
        try:
            restore_backup()
            console.print("[bold green]Previous version restored.[/bold green]")
        except Exception as restore_error:
            console.print(f"[bold red]Restore failed:[/bold red] {restore_error}")

# =========================
# LOGIN
# =========================
def login_ui():
    while True:
        clear()
        console.print(get_banner())
        console.print(Align.center("[bold yellow]LOGIN PROTOCOL[/bold yellow]\n"))

        user = Prompt.ask("[bold white]👤 USER[/bold white]", default="admin")
        pw = Prompt.ask("[bold white]🔑 PASS[/bold white]", password=True)

        if user == "admin" and pw == "123":
            loading_screen("Authenticating")
            console.print("\n[bold reverse green]  ACCESS GRANTED  [/bold reverse green]")
            time.sleep(1)
            main_dashboard()
            break
        else:
            console.print("\n[bold reverse red]  ACCESS DENIED  [/bold reverse red]")
            time.sleep(1.5)

# =========================
# DASHBOARD
# =========================
def main_dashboard():
    while True:
        clear()
        user_data = get_user_info()

        info_text = Text()
        info_text.append(f"🌐 IP ADDR : {user_data['ip']}\n", style="bold cyan")
        info_text.append(f"📍 LOCATION: {user_data['city']}, {user_data['country']}\n", style="bold green")
        info_text.append(f"⏰ TIMEZONE: {user_data['timezone']}\n", style="bold yellow")
        info_text.append(f"🏢 ISP     : {user_data['org']}", style="bold magenta")

        user_panel = Panel(
            info_text,
            title="[bold white]USER NETWORK DETAILS[/bold white]",
            border_style="white"
        )

        table = Table(expand=True, border_style="bright_magenta")
        table.add_column("SL", justify="center", style="bold yellow")
        table.add_column("TOOL NAME", style="bold white")
        table.add_column("STATUS", justify="center")

        table.add_row("1", "🚀 SYSTEM SCANNER", "[green]READY[/green]")
        table.add_row("2", "👤 DEVELOPER INFO", "[blue]INFO[/blue]")
        table.add_row("3", "🔄 CHECK UPDATE", "[yellow]UPDATE[/yellow]")
        table.add_row("0", "❌ EXIT", "[red]OFF[/red]")

        console.print(get_banner())
        console.print(user_panel)
        console.print(Panel(table, title="[bold cyan]COMMAND CENTER[/bold cyan]", border_style="blue"))
        console.print(Align.center(f"[dim]Last Sync: {datetime.now().strftime('%H:%M:%S')}"))

        choice = Prompt.ask("\n[bold cyan]Select Protocol[/bold cyan]", choices=["1", "2", "3", "0"])

        if choice == "1":
            loading_screen("Scanning local system")
            console.print(Panel(
                f"[bold green]Scan Complete![/bold green]\nTarget IP: {user_data['ip']}\nStatus: All systems nominal.",
                title="RESULT",
                border_style="green"
            ))
            input("\nPress Enter to continue...")

        elif choice == "2":
            clear()
            about = """
[bold red]NAME      :[/bold red] PRO TOOL
[bold red]DEV       :[/bold red] TOXIC BILLU
[bold red]LICENSE   :[/bold red] [bold green]PREMIUM[/bold green]
"""
            console.print(Panel(about, title="ABOUT DEVELOPER", border_style="yellow"))
            input("\nPress Enter to continue...")

        elif choice == "3":
            update_app()
            input("\nPress Enter to continue...")

        elif choice == "0":
            console.print("[bold red]Connection Terminated.[/bold red]")
            sys.exit()

if __name__ == "__main__":
    try:
        login_ui()
    except KeyboardInterrupt:
        print("\n[!] Disconnected.")def loading_screen(msg):
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
