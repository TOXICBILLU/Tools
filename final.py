import os
import re
import sys
import time
import random
import shutil
import subprocess
import requests
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn,
)
from rich.prompt import Prompt

console = Console()

# =========================================================
# MAIN APP CONFIG
# =========================================================
APP_NAME = "PRO TOOL"
APP_VERSION = "1.0.1"

GITHUB_USER = "TOXICBILLU"
GITHUB_REPO = "Tools"
GITHUB_BRANCH = "main"

REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/Version.txt"
REMOTE_MAIN_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/tools.py"

LOCAL_FILE = os.path.abspath(__file__)

# =========================================================
# TIKTOK DOWNLOADER CONFIG
# =========================================================
TT_APP_NAME = "TIKTOK DOWNLOADER"
TT_VERSION = "7.0 STABLE"
DOWNLOAD_FOLDER = "/sdcard/Download"
API_URL = "https://tikwm.com/api/"

# Static colors
C_BORDER = "bright_cyan"
C_TITLE = "bold bright_green"
C_TEXT = "white"
C_INFO = "bold bright_cyan"
C_WARN = "bold bright_yellow"
C_ERR = "bold bright_red"
C_OK = "bold bright_green"
C_MENU = "bold bright_magenta"


# =========================================================
# BASIC HELPERS
# =========================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg="\nPress Enter to continue..."):
    input(msg)


def loading_screen(msg, speed=0.02):
    clear()
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold magenta"),
        TextColumn("[white]{task.description}"),
        BarColumn(),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        expand=True,
        console=console,
    ) as progress:
        task = progress.add_task(msg, total=100)
        while not progress.finished:
            progress.update(task, advance=2.5)
            time.sleep(speed)


def slow_print(text, style=C_INFO, delay=0.01, end="\n"):
    for ch in text:
        console.print(ch, style=style, end="")
        time.sleep(delay)
    console.print(end=end)


# =========================================================
# USER NETWORK INFO
# =========================================================
def get_user_info():
    urls = [
        "https://ipwho.is/",
        "https://ipapi.co/json/",
        "http://ip-api.com/json/",
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=5)
            r.raise_for_status()
            data = r.json()

            if "ip" in data and "country" in data:
                return {
                    "ip": data.get("ip", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("region", "Unknown"),
                    "country": data.get("country", "Unknown"),
                }

            if "ip" in data and ("country_name" in data or "city" in data):
                return {
                    "ip": data.get("ip", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("region", "Unknown"),
                    "country": data.get("country_name", "Unknown"),
                }

            if data.get("status") == "success":
                return {
                    "ip": data.get("query", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "country": data.get("country", "Unknown"),
                }

        except Exception:
            continue

    return {
        "ip": "Offline",
        "city": "N/A",
        "region": "N/A",
        "country": "N/A",
    }


# =========================================================
# MAIN BANNER / UI
# =========================================================
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


def splash():
    clear()
    console.print(get_banner())
    console.print(
        Panel(
            Align.center(
                "[bold bright_green]WELCOME TO PRO TOOL[/bold bright_green]\n"
                "[bright_cyan]Optimized UI • GitHub Update • Multi Tool System[/bright_cyan]"
            ),
            border_style="bright_magenta",
            title="[bold yellow]BOOT[/bold yellow]",
        )
    )
    time.sleep(1.8)


def draw_main_screen():
    clear()
    user_data = get_user_info()

    info_text = Text()
    info_text.append(f"🌐 IP       : {user_data['ip']}\n", style="bold cyan")
    info_text.append(f"🏙️ CITY     : {user_data['city']}\n", style="bold green")
    info_text.append(f"🗺️ REGION   : {user_data['region']}\n", style="bold yellow")
    info_text.append(f"🌍 COUNTRY  : {user_data['country']}", style="bold magenta")

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
    table.add_row("4", "🎬 TIKTOK DOWNLOADER", "[cyan]ACTIVE[/cyan]")
    table.add_row("5", "😈 FUNNY HACK MODE", "[magenta]FUN[/magenta]")
    table.add_row("0", "❌ EXIT", "[red]OFF[/red]")

    console.print(get_banner())
    console.print(user_panel)
    console.print(Panel(table, title="[bold cyan]COMMAND CENTER[/bold cyan]", border_style="blue"))
    console.print(Align.center(f"[dim]Last Sync: {datetime.now().strftime('%H:%M:%S')}"))


# =========================================================
# UPDATE SYSTEM
# =========================================================
def fetch_remote_version():
    r = requests.get(REMOTE_VERSION_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    r.raise_for_status()
    return r.text.strip()


def fetch_remote_code():
    r = requests.get(REMOTE_MAIN_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    return r.text


def backup_current_file():
    backup_file = LOCAL_FILE + ".bak"
    with open(LOCAL_FILE, "r", encoding="utf-8") as src:
        with open(backup_file, "w", encoding="utf-8") as dst:
            dst.write(src.read())


def restore_backup():
    backup_file = LOCAL_FILE + ".bak"
    if os.path.exists(backup_file):
        with open(backup_file, "r", encoding="utf-8") as src:
            with open(LOCAL_FILE, "w", encoding="utf-8") as dst:
                dst.write(src.read())


def install_update(new_code):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)


def check_for_updates(show_no_update=True):
    try:
        loading_screen("Checking remote version", 0.01)
        remote_version = fetch_remote_version()

        if remote_version == APP_VERSION:
            if show_no_update:
                clear()
                console.print(get_banner())
                console.print(f"[bold green]✔ Already latest version: {APP_VERSION}[/bold green]")
            return False, remote_version

        clear()
        console.print(get_banner())
        console.print(f"[bold yellow]Update available:[/bold yellow] {APP_VERSION} → {remote_version}")
        return True, remote_version

    except Exception as e:
        clear()
        console.print(get_banner())
        console.print(f"[bold red]Update check failed:[/bold red] {e}")
        return False, None


def update_app():
    try:
        has_update, remote_version = check_for_updates(show_no_update=False)

        if not has_update:
            return

        confirm = Prompt.ask("[bold cyan]Do update now?[/bold cyan]", choices=["y", "n"], default="y")
        if confirm != "y":
            return

        loading_screen("Downloading new build", 0.01)
        new_code = fetch_remote_code()

        if "APP_VERSION" not in new_code or "def update_app()" not in new_code:
            clear()
            console.print(get_banner())
            console.print("[bold red]Downloaded file looks invalid. Update canceled.[/bold red]")
            return

        backup_current_file()
        install_update(new_code)

        clear()
        console.print(get_banner())
        console.print(f"[bold green]✔ Updated successfully to {remote_version}[/bold green]")
        console.print("[bold yellow]Restart the app now to use new features.[/bold yellow]")

    except Exception as e:
        clear()
        console.print(get_banner())
        console.print(f"[bold red]Update failed:[/bold red] {e}")
        console.print("[yellow]Trying to restore previous version...[/yellow]")
        try:
            restore_backup()
            console.print("[bold green]Previous version restored.[/bold green]")
        except Exception as restore_error:
            console.print(f"[bold red]Restore failed:[/bold red] {restore_error}")


# =========================================================
# LOGIN
# =========================================================
def login_ui():
    while True:
        clear()
        console.print(get_banner())
        console.print(Align.center("[bold yellow]LOGIN PROTOCOL[/bold yellow]\n"))

        user = Prompt.ask("[bold white]👤 USER[/bold white]", default="admin")
        pw = Prompt.ask("[bold white]🔑 PASS[/bold white]", password=True)

        if user == "admin" and pw == "123":
            loading_screen("Authenticating")
            clear()
            console.print(get_banner())
            console.print("\n[bold reverse green]  ACCESS GRANTED  [/bold reverse green]")
            time.sleep(1)
            return
        else:
            console.print("\n[bold reverse red]  ACCESS DENIED  [/bold reverse red]")
            time.sleep(1.5)


# =========================================================
# SCANNER / ABOUT
# =========================================================
def system_scanner():
    loading_screen("Scanning local system")

    user_data = get_user_info()

    clear()
    console.print(get_banner())
    console.print(Panel(
        f"[bold green]Scan Complete![/bold green]\n\n"
        f"Target IP: {user_data['ip']}\n"
        f"City     : {user_data['city']}\n"
        f"Region   : {user_data['region']}\n"
        f"Country  : {user_data['country']}\n"
        f"Status   : All systems nominal.",
        title="RESULT",
        border_style="green"
    ))
    pause()


def developer_info():
    clear()
    console.print(get_banner())

    about = """
[bold red]NAME      :[/bold red] PRO TOOL
[bold red]DEV       :[/bold red] TOXIC BILLU
[bold red]LICENSE   :[/bold red] [bold green]PREMIUM[/bold green]
[bold red]REPO      :[/bold red] TOXICBILLU/Tools
"""
    console.print(Panel(about, title="ABOUT DEVELOPER", border_style="yellow"))
    pause()


# =========================================================
# FUNNY HACK MODE (FAKE / SAFE)
# =========================================================
def fake_matrix_line():
    chars = "01ABCDEF#$%@*&"
    return "".join(random.choice(chars) for _ in range(58))


def funny_hack_mode():
    clear()
    console.print(get_banner())
    console.print(
        Panel(
            Align.center(
                "[bold bright_red]FUNNY HACK MODE[/bold bright_red]\n"
                "[bright_yellow]This is only a fake cinematic simulation[/bright_yellow]"
            ),
            border_style="red",
            title="[bold white]WARNING[/bold white]",
        )
    )
    time.sleep(1.2)

    stages = [
        "Injecting meme packets...",
        "Locating secret potato server...",
        "Bypassing nani firewall...",
        "Decrypting cat database...",
        "Syncing cyber tea protocol...",
        "Accessing moonlight kernel...",
        "Recovering hidden biryani.exe...",
    ]

    for stage in stages:
        clear()
        console.print(get_banner())
        console.print(Panel(Align.center(f"[bold bright_cyan]{stage}[/bold bright_cyan]"),
                            border_style="bright_magenta",
                            title="[bold yellow]SIMULATION[/bold yellow]"))
        console.print(f"[green]{fake_matrix_line()}[/green]")
        console.print(f"[green]{fake_matrix_line()}[/green]")
        console.print(f"[green]{fake_matrix_line()}[/green]")
        time.sleep(0.9)

    loading_screen("Finalizing ultra secret operation", 0.015)

    results = [
        "WiFi password found: [bold yellow]password123[/bold yellow]  😹",
        "NASA mainframe replaced with [bold green]RickRoll.mp4[/bold green]",
        "Root access granted to [bold cyan]Tea-Stall Server[/bold cyan]",
        "Classified file unlocked: [bold magenta]homework_final_final2.pdf[/bold magenta]",
        "Target compromised with [bold red]unlimited memes[/bold red]",
    ]

    clear()
    console.print(get_banner())
    console.print(
        Panel(
            Align.center(
                "[bold bright_green]MISSION COMPLETE ✔[/bold bright_green]\n\n"
                + random.choice(results)
                + "\n\n[bold bright_yellow]Status:[/bold bright_yellow] 100% Fake / Just For Fun"
            ),
            border_style="green",
            title="[bold white]FUN RESULT[/bold white]",
        )
    )
    pause()


# =========================================================
# TIKTOK DOWNLOADER SECTION
# =========================================================
def tt_banner():
    clear()
    logo = Text(r"""
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
""", style="bold bright_green")

    console.print(Align.center(logo))
    console.print(
        Panel(
            Align.center(
                "[bold bright_green]HD[/bold bright_green] • "
                "[bold bright_cyan]Stable[/bold bright_cyan] • "
                "[bold bright_magenta]No Auto Color Change[/bold bright_magenta] • "
                "[bold bright_yellow]Better Video Compatibility[/bold bright_yellow]"
            ),
            border_style=C_BORDER,
            title="[bold bright_yellow]TIKTOK PANEL[/bold bright_yellow]",
        )
    )


def tt_footer():
    console.print(
        Align.center(
            f"[bright_white]{TT_APP_NAME}[/bright_white] [bright_cyan]|[/bright_cyan] [bright_yellow]Version {TT_VERSION}[/bright_yellow]"
        )
    )


def safe_name(name: str, max_len: int = 60) -> str:
    name = (name or "tiktok_video").strip()
    name = re.sub(r'[\\/:*?"<>|]+', "", name)
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._")
    return name[:max_len] if name else "tiktok_video"


def ensure_folder():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def fetch_info(tiktok_url: str):
    try:
        r = requests.get(
            API_URL,
            params={"url": tiktok_url, "hd": 1},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=25,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        console.print(
            Panel(
                f"[{C_ERR}]API Error[/{C_ERR}]\n[white]{e}[/white]",
                border_style="red",
                title="[bold white]ERROR[/bold white]",
            )
        )
        return None


def get_stream_candidates(info: dict):
    d = (info or {}).get("data") or {}
    candidates = []

    if d.get("hdplay") and isinstance(d.get("hdplay"), str):
        candidates.append(("HD", d["hdplay"]))
    if d.get("play") and isinstance(d.get("play"), str):
        candidates.append(("Normal", d["play"]))
    if d.get("wmplay") and isinstance(d.get("wmplay"), str):
        candidates.append(("Watermark", d["wmplay"]))

    return [(label, url) for label, url in candidates if url.startswith("http")]


def show_video_info(title: str, quality: str):
    table = Table(
        title="[bold bright_magenta]VIDEO INFO[/bold bright_magenta]",
        show_lines=True,
        border_style=C_BORDER,
    )
    table.add_column("Field", style="bold bright_green", justify="center")
    table.add_column("Value", style="bold bright_yellow")

    table.add_row("[bright_cyan]Title[/bright_cyan]", f"[white]{title}[/white]")
    table.add_row("[bright_magenta]Quality[/bright_magenta]", f"[bright_green]{quality}[/bright_green]")
    console.print(table)


def prep_animation():
    frames = [
        "[bright_cyan]Preparing download engine...[/bright_cyan]",
        "[bright_magenta]Checking best stream...[/bright_magenta]",
        "[bright_yellow]Building stable save pipeline...[/bright_yellow]",
        "[bright_green]Ready to download...[/bright_green]",
    ]

    for text in frames:
        tt_banner()
        console.print(
            Panel(
                Align.center(text),
                border_style=C_BORDER,
                title="[bold bright_yellow]PLEASE WAIT[/bold bright_yellow]",
            )
        )
        time.sleep(0.35)


def download_stream(url: str, filepath: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tiktok.com/",
    }

    resp = requests.get(url, stream=True, timeout=60, headers=headers)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    temp_path = filepath + ".part"

    with Progress(
        SpinnerColumn(style="bold bright_magenta"),
        TextColumn("[bold bright_cyan]Downloading[/bold bright_cyan]"),
        BarColumn(complete_style="bright_green", finished_style="bright_green"),
        DownloadColumn(),
        TransferSpeedColumn(),
        TextColumn("[bold bright_yellow]{task.percentage:>3.0f}%[/bold bright_yellow]"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("download", total=total if total > 0 else None)

        with open(temp_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
                    if total > 0:
                        progress.update(task, advance=len(chunk))

    os.replace(temp_path, filepath)


def ffprobe_ok(path: str) -> bool:
    if not shutil.which("ffprobe"):
        return os.path.exists(path) and os.path.getsize(path) > 1024

    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_name,width,height",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return bool(out)
    except Exception:
        return False


def ffprobe_resolution(path: str) -> str:
    if not shutil.which("ffprobe"):
        return ""

    try:
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "csv=p=0:s=x",
                path,
            ],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return out
    except Exception:
        return ""


def optimize_with_ffmpeg(src_path: str) -> str:
    if not shutil.which("ffmpeg"):
        return src_path

    tmp_out = src_path + ".fixed.mp4"

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", src_path,
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "18",
                "-c:a", "aac",
                "-b:a", "192k",
                "-movflags", "+faststart",
                tmp_out,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        if ffprobe_ok(tmp_out) and os.path.getsize(tmp_out) > 1024:
            os.replace(tmp_out, src_path)
            return src_path

    except Exception:
        pass

    if os.path.exists(tmp_out):
        try:
            os.remove(tmp_out)
        except Exception:
            pass

    return src_path


def scan_to_gallery(filepath: str) -> bool:
    try:
        subprocess.run(
            ["termux-media-scan", filepath],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        pass

    try:
        subprocess.run(
            [
                "am", "broadcast",
                "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d", f"file://{filepath}",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def try_download_best_stream(info: dict, filepath: str):
    candidates = get_stream_candidates(info)

    if not candidates:
        raise RuntimeError("No downloadable stream found")

    last_error = None

    for label, url in candidates:
        try:
            download_stream(url, filepath)

            if not ffprobe_ok(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
                raise RuntimeError(f"{label} stream downloaded but failed validation")

            optimize_with_ffmpeg(filepath)

            if not ffprobe_ok(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
                raise RuntimeError(f"{label} stream failed after compatibility fix")

            return label
        except Exception as e:
            last_error = e
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass

    raise RuntimeError(str(last_error) if last_error else "Download failed")


def download_video(tiktok_url: str):
    tt_banner()
    slow_print("Fetching video info...", style=C_WARN, delay=0.02)

    info = fetch_info(tiktok_url)
    if not info:
        pause()
        return

    if info.get("code") != 0:
        console.print(
            Panel(
                Align.center("[bold bright_red]Invalid TikTok URL or API failed[/bold bright_red]"),
                border_style="red",
                title="[bold white]ERROR[/bold white]",
            )
        )
        pause()
        return

    title = (info.get("data") or {}).get("title") or "tiktok_video"

    ensure_folder()
    filename = safe_name(title) + ".mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    base, ext = os.path.splitext(filepath)
    i = 1
    while os.path.exists(filepath):
        filepath = f"{base}_{i}{ext}"
        i += 1

    show_video_info(title, "HD / Auto Fallback")
    prep_animation()

    tt_banner()
    show_video_info(title, "HD / Auto Fallback")

    try:
        final_quality = try_download_best_stream(info, filepath)
        time.sleep(0.4)
        scan_to_gallery(filepath)

        resolution = ffprobe_resolution(filepath)
        if resolution:
            msg = (
                f"[bold bright_green]DOWNLOAD COMPLETE ✔[/bold bright_green]\n"
                f"[bold bright_cyan]Saved Successfully[/bold bright_cyan]\n"
                f"[bold bright_yellow]Final Quality:[/bold bright_yellow] {final_quality}\n"
                f"[bold bright_yellow]Resolution:[/bold bright_yellow] {resolution}"
            )
        else:
            msg = (
                f"[bold bright_green]DOWNLOAD COMPLETE ✔[/bold bright_green]\n"
                f"[bold bright_cyan]Saved Successfully[/bold bright_cyan]\n"
                f"[bold bright_yellow]Final Quality:[/bold bright_yellow] {final_quality}"
            )

        console.print(
            Panel(
                Align.center(msg),
                border_style="green",
                title="[bold bright_yellow]SUCCESS[/bold bright_yellow]",
            )
        )

    except Exception as e:
        console.print(
            Panel(
                Align.center(f"[bold bright_red]Download Failed[/bold bright_red]\n[white]{e}[/white]"),
                border_style="red",
                title="[bold white]FAILED[/bold white]",
            )
        )

    pause()


def multiple_download():
    tt_banner()
    console.print(
        Panel(
            Align.center(
                "[bold bright_cyan]Paste TikTok links one by one[/bold bright_cyan]\n"
                "[bold bright_yellow]Type done to start[/bold bright_yellow]"
            ),
            border_style=C_BORDER,
            title="[bold bright_green]MULTI DOWNLOAD[/bold bright_green]",
        )
    )

    links = []
    while True:
        link = input("URL : ").strip()
        if link.lower() == "done":
            break
        if link:
            links.append(link)

    if not links:
        console.print(
            Panel(
                Align.center("[bold bright_red]No links added[/bold bright_red]"),
                border_style="red",
            )
        )
        pause()
        return

    for idx, link in enumerate(links, 1):
        tt_banner()
        console.print(
            Panel(
                Align.center(f"[bold bright_yellow]Processing {idx}/{len(links)}[/bold bright_yellow]"),
                border_style=C_BORDER,
                title="[bold bright_magenta]QUEUE[/bold bright_magenta]",
            )
        )
        time.sleep(0.6)
        download_video(link)


def tiktok_downloader_menu():
    while True:
        tt_banner()

        menu = Panel(
            Align.center(
                "[bold bright_green]1[/bold bright_green] [white]Download Single Video[/white]\n\n"
                "[bold bright_cyan]2[/bold bright_cyan] [white]Download Multiple Videos[/white]\n\n"
                "[bold bright_yellow]0[/bold bright_yellow] [white]Back To Main Menu[/white]"
            ),
            border_style=C_BORDER,
            title="[bold bright_yellow]TIKTOK MENU[/bold bright_yellow]",
        )

        console.print(menu)
        tt_footer()

        choice = Prompt.ask("\n[bold bright_magenta]Select Option[/bold bright_magenta]", default="1").strip()

        if choice == "1":
            url = Prompt.ask("[bold bright_cyan]Enter TikTok URL[/bold bright_cyan]").strip()
            if url:
                download_video(url)

        elif choice == "2":
            multiple_download()

        elif choice == "0":
            return

        else:
            console.print(
                Panel(
                    Align.center("[bold bright_red]Invalid Option[/bold bright_red]"),
                    border_style="red",
                )
            )
            time.sleep(1.1)


# =========================================================
# MAIN LOOP
# =========================================================
def main_dashboard():
    while True:
        draw_main_screen()
        choice = Prompt.ask("\n[bold cyan]Select Protocol[/bold cyan]", choices=["1", "2", "3", "4", "5", "0"])

        if choice == "1":
            system_scanner()

        elif choice == "2":
            developer_info()

        elif choice == "3":
            update_app()
            pause()

        elif choice == "4":
            tiktok_downloader_menu()

        elif choice == "5":
            funny_hack_mode()

        elif choice == "0":
            clear()
            console.print(
                Panel(
                    Align.center("[bold bright_red]Connection Terminated.[/bold bright_red]"),
                    border_style="red",
                    title="[bold white]EXIT[/bold white]",
                )
            )
            sys.exit()


if __name__ == "__main__":
    try:
        splash()
        login_ui()
        main_dashboard()
    except KeyboardInterrupt:
        clear()
        print("\n[!] Disconnected.")