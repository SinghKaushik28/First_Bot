import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio
import re
import ast
from music import wishMe, play_random_spotify_track, sp, speak
import wikipedia
import webbrowser
import pyttsx3
import speech_recognition as sr
import threading
from discord.ext import commands



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KAUSH = os.getenv('KAUSH')
JATIN = os.getenv('DISCORD_JATIN')
ADI = os.getenv('DISCORD_ADI')
VEDAANT = os.getenv('DISCORD_VEDAANT')
ADARSH = os.getenv('DISCORD_ADARSH')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True  # For online status

bot = commands.Bot(command_prefix='*', intents=intents)


# ===== Configuration =====

secret_role_name = "Gamer"
kaush_user_id = KAUSH  # Replace with actual Kaush ID
CODE_CORRECTION_CHANNEL_ID = 123456789012345678  # Replace with your code correction channel ID

mention_user_ids = [
    KAUSH,  # Kaush
    JATIN,
    ADI,
    VEDAANT,
    ADARSH,
]

# Abuse words (English + Hindi + short forms)
abuse_words = ["suar ke kaali aand ke jhat ke baal", "kaali gand ke hijde", "shit", "fuck", "bhang bhosda", "gand", "bkl", "mc", "bc", "bsdk", "bhenchod", "madarchod", "lund", "chutiya", "gandu", "chut", "bhosdike", "randwe", "bhen ke lode", "maa ki chut", "bhosdike", "rand ke bacche ", "bhencho", "bsdk", "bhen ke lode", "randwe", "bhosdike", "chutiyapa", "gandu", "madarchod", "chutiyapa", "mkc", "bkl", "baklol", "mc", "madarchod", "madarchoddd", "madar", "madar ch*d", "madarch*d", "madarchod",
    "bc", "behenchod", "bhenchod", "bhenchoddd", "behench*d", "bhen ke lode", "bhenke", "bhen ke", "bhenkalode",
    "bsdk", "behen ke l*de", "behenkelode", "bhosdike", "bhosri", "bhosri ke", "bhosadi", "bhosadike", "bhosadikee",
    "chutiya", "chut", "chut ke", "chutiyapa", "chut ke baal", "chut ke lode", "chu*tiya", "chutiyah", "chutiyaa",
    "gaand", "gand", "gandu", "gand mara", "gandmara", "gandfat", "gandfaad", "gand faad", "gandu", "gaandfat",
    "harami", "haraami", "haramzada", "haramzade", "haram ki aulad", "haram ka", "harami ke", "haraam ke",
    "kutte", "kutti", "kuttiya", "kutte ka", "kutti ke", "kutti ki", "kutti kamini", "kutti kamina", "kutte kamine",
    "randi", "randwe", "randwa", "rand", "raand", "randwa ka", "randwe ke","raand ke",
    "saala", "sala", "saale", "saali", "saalon", "saale kamine", "saali kutti", "saali randi",
    "tatti", "tatte", "tatty", "tatte ke", "tatti ke", "tatti khana",
    "launde", "launda", "loda", "lodu", "lode", "lunde", "laundiya", "lund", "lund ke", "loda lassan",
    "moot", "mootna", "moot dena", "moot marna", "mut", "mutra",
    "suar", "suvar", "suar ke", "suar ki", "suvar ke bacche", "suar ke pille",
    "ullu", "ullu ka", "ullu ke", "ullu ke pathe", "ullu ka pattha", "ullu ka bacha",
    "talli", "talli ke", "talli ki",
    "chakka", "chhakka", "chhakka sale",
    "bawaseer", "bawaaseer",
    "jhantu", "jhant", "jhant ke", "jhant ka", "jhant ke baal",
    "kamine", "kamina", "kamini", "kamino", "kaminiyon",
    "kanjar", "kanjari", "kanjre", "kanjri", "kanjar ke",
    "paji", "pajji", "paji ke", "pajji ki",
    "lavde", "lavda", "lavde ke", "lavde ki", "lavda lassan",# English swears
    "fuck", "fucking", "fucker", "motherfucker", "mf", "mofo", "mother fucker",
    "shit", "bullshit", "piece of shit", "shitty", "shite",
    "ass", "asses", "asshole", "assholes", "jackass",
    "bitch", "bitches", "son of a bitch", "sonofabitch",
    "bastard", "bastards",
    "dick", "dicks", "dickhead", "dickheads",
    "cock", "cocks", "cocksucker", "cocksuckers",
    "pussy", "pussies", "dumbass", "retard", "retarded",
    "slut", "sluts", "whore", "whores", "hoe", "hoes",
    "cum", "cumshot", "cumslut", "wanker", "prick", "bollocks",
    "twat", "jerk", "jerking", "jerkoff"]  # Add more words as needed

abuse_pattern = re.compile(r'\b(' + '|'.join(abuse_words) + r')\b', re.IGNORECASE)

bad_abuse_responses_english = [
    "Shut your filthy mouth before I sew it shut, asshole!",
    "You brain-dead fuckstick, go drown yourself!",
    "You pathetic excuse for a human, fucking disappear!",
    "Go fuck yourself and don’t come back, you miserable cunt!",
    "You’re living proof that some people shouldn’t breed, wanker!",
    "Get the fuck out of my face before I lose it!",
    "You useless sack of shit, rot somewhere far away!",
    "You’d be more useful as roadkill, twat!",
    "You absolute waste of oxygen, choke on it!",
    "I’ve met dog shit with more value than you, bastard!",
    "You’re a cancer to everything you touch, prick!",
    "Get bent, you inbred fucking moron!",
    "May you trip and land face-first in your own shit!",
    "You worthless fuckbag, die tired!",
    "Eat a bag of dicks, loser!",
    "Bhosdike, tu zinda kyu hai ab tak?",
    "Madarchod, tera chehra hi gawahi deta hai ki tu fail hai.",
    "Behen ke laude, zyaada bakwas ki to muh tod dunga.",
    "Randi ke bacche, apni aukat mein reh!",
    "Chutiye, tera dimaag to ghaas khane gaya hai kya?",
    "Tere jaise gadhe ko dekhke Darwin bhi ro deta.",
    "Saale harami, teri maut bhi tujhe dekhke darr jaye.",
    "Bhadwe, tujhme insaaniyat ka ek percent bhi nahi hai.",
    "Teri shakal dekh ke lagta hai kisi ne curse kar diya ho.",
    "Kutte ke pille, tu attention ka bhuka hai na?",
    "Lund ke baal, apna muh bandh rakh.",
    "Tere mooh se badbu aise aati hai jaise kachre ka dabba khul gaya ho.",
    "Laude, tu galti ka bhi abortion hai.",
    "Chakka kahin ka, dusron ki zindagi mein mirch masala dalta hai.",
    "Tere jaise ko to gaali bhi sharam aake lage.",
    "Tere jaise chutiye ko dekhke to shaitan bhi job chhod de.",
    "Bhosdike, tera wajood hi ek galti ka product hai.",
    "Madarchod, tu insaan kam, kachra jyada lagta hai.",
    "Behenchod, tu ek walking disaster hai.",
    "Teri zubaan kaat ke museum mein rakh deni chahiye.",
    "Randi ke laal, teri soch nalli se bhi gandi hai.",
    "Chutiye, tera dimaag format karke dobara install karna chahiye.",
    "Gadhe ke tatte, apna muh band rakh warna hawa kharab ho jayegi.",
    "Bhadwe, tu ullu ka patha bhi insult lagta hai.",
    "Kutte ki jhaat, tu bolta kam aur bakwas zyada karta hai.",
    "Saale jhaantu, tujhme akal ka drop bhi nahi hai.",
    "Lode ke phool, tu fail hone ki dictionary definition hai.",
    "Harami ke bacche, tujhe dekhke depression bhi pakad le.",
    "Laude, teri harkatein dekhke to gutter ka paani bhi sharma jaaye.",
    "Bhosdike, tera naam stupidity ka brand ambassador hona chahiye."
]


tagged_replies_online = [
    "I will be late, please wait!",
    "Hold on, I'll be there soon.",
    "Busy now, will catch up later!",
]

tagged_replies_offline = [
    "I'm offline right now, please wait.",
    "Currently not available, try later.",
    "I'm away, will respond when back!",
]

teasing_triggers = ['kaush', 'noob', 'coder', 'bug', 'error','fail', 'crash', 'syntax', 'debug', 'lag', 'potato',
    'glitch', 'update', 'compile', 'nerd', 'geek', 'bot',
    'slowpoke', 'rookie', 'mess', 'load', 'timeout', 'retry','gay']

teasing_replies = [
    "Tum haso toh lagta hai Wi‑Fi full signal, bas dil connect ho jata hai. 😉",
    "Waise tum over smart ho ya sirf mujhe impress karne ke liye? 😏",
    "Tumhe dekhke lagta hai Google ko bhi jealous ho gaya hoga. 📱",
    "Tum toh aise chadh ke baat karti ho jaise share market – kab upar, kab neeche. 📈",
    "Kya tum coffee ho? Kyunki tum pe addict ho jaane ka mann karta hai. ☕",
    "Waise tum itni khubsurat ho, Zoom meeting mein bhi spotlight tum pe hi rahe. 💡",
    "Tumne math padha hai? Kyunki tum meri har problem ka solution lagti ho. 🧮",
    "Tumhare saath baat karna mobile ka fast charge lagata hai – mood instantly full. ⚡",
    "Tum online aati ho toh lagta hai festival shuru ho gaya. 🎉",
    "Tum meri playlist jaisi ho – hamesha repeat pe. 🎵",
    "Waise tum single ho ya main sapne dekhna band kar du? 🤭",
    "Tum toh waise ho jaise kulfi – dekhte hi dil pighal jata hai. 🍦",
    "Tumhari smile toh OTP jaisi hai – ek hi baar kaam karti hai, lekin dil direct unlock kar deti hai. 🔓",
    "Tum mujhe padhi-likhi problems ki jagah padha-likh ke khushi deti ho. 📚",
    "Tumhare messages popcorn jaison hote hain – ek ka intezaar nahi rukta. 🍿",
    "Waise tum chef ho kya? Kyunki tum meri life me taste bhar deti ho. 🍲",
    "Tumhare bina din us aakhri biscuit jaisa lagta hai – adhoora. 🍪",
    "Tum toh notifications jaisi ho – bina tumhare din incomplete lagta hai. 📲",
    "Tum itni amazing ho, tumhe dekhke calories bhi melt ho jati hain. 🏃‍♂️",
    "Tumhare jokes bad ho sakte hain, par tum khud perfect ho. 😏",
    "Tumhare naam ka ringtone bana lu kya? Har baar sunne ka mann karega. 🎶",
    "Tum Instagram filter ho kya? Har cheez perfect bana deti ho. 📸",
    "Tum se baat karke lagta hai main unlimited recharge pe hoon. 🥳",
    "Tum meri charging cable ho – tumhare bina main dead ho jata hoon. 🔌",
    "Tumse milke lagta hai ki gaane ka woh line sach hai – 'Tujhme Rab Dikhta Hai'. 🎤",
    "Tum itni khubsurat ho ki traffic police tumhe dekh ke signal green kar de. 🚦",
    "Tum toh woh refresh button ho jo mood instantly better kar de. 🔄",
    "Tum cute ho ya knowingly kar rahi ho? 🤨",
    "Waise tum magician ho? Kyunki tumhe dekhte hi baaki sab gayab ho jata hai. 🎩",
    "Tum toh Wi-Fi password jaisi ho – sab tumhe paana chahte hain. 🔐"
]


roasts = [
    "Teri shakal dekh ke to UPI fraud wale bhi dar jaate hain.",
    "Tere dimaag mein khali plot hai, rent dena shuru kar.",
    "Tu Google ka opposite hai — kuch bhi poochh lo, hamesha wrong answer.",
    "Teri akal ka factory default set hai — update kabhi hua hi nahi.",
    "Tere jokes sun ke to Majak bhi suicide kar le.",
    "Tu chalti-phirti buffering screen hai.",
    "Tere kapdon mein style utna hi hai jitna sarkari chai mein doodh.",
    "Tere dimaag ki speed — BSNL internet 2002 mode.",
    "Tere face se to Zoom ka “blur background” bhi sharma jaye.",
    "Tu chal phir dictionary ka bekaar wala page.",
    "Tere muh se zyada badbu to dustbin se aati hai.",
    "Tu wahi galti hai jo delete nahi hoti.",
    "Tere baare mein Wikipedia mein bhi “no data available” likha hoga.",
    "Tu sadak ke khadde ka insaan version hai.",
    "Tu WhatsApp forward ka human form hai — bekaar aur irritating.",
    "Tere pass manners utne hi hain jitne machine par default audio.",
    "Tere doston ke doston ko bhi tu pasand nahi.",
    "Tu toh asli “Do not disturb” board ka poster child hai.",
    "Tere pass logic utna hi hai jitna chappal mein horsepower.",
    "Teri baat sun ke to Alexa bhi apne aap shut down ho jaye.",
    "Tu guarantee wala disappointment hai.",
    "Tu chal phir “before” photo ad campaign ka model.",
    "Tu unhe bhi boring lagta hai jo boringness ke fan hain.",
    "Tu chal phir lagao “loading…” ka tattoo.",
    "Tere muh pe mask lagane se pollution kam ho jayega.",
    "Tere andar se positivity waise hi gayab hai jaise free Wi-Fi ka password.",
    "Tu Google Translate ka drunk mode result hai.",
    "Tu toh default ringtone ka insaan version hai.",
    "Tere ideas Mirzapur ke Munna Bhaiya ke plans se bhi bekaar hain.",
    "Tu toh Apne parents ka “oops” moment hai.",
    "Tere muh pe pimple bhi aane se pehle resign kar dete hain.",
    "Tu toh 90s ke TV ka vertical hold problem hai.",
    "Tu free trial jaisa hai, shuru mein thoda interest phir pura bekaar.",
    "Tu toh budget earphones ka sound quality hai.",
    "Tere baare mein hearing loss wale log bhi relax feel karte hain.",
    "Tu toh rickshaw ka puncture tyre hai.",
    "Tu toh kam budget ka horror scene hai — cheap aur irritating.",
    "Tere dreams utne hi fake hain jitne Instagram followers.",
    "Tu chal phir apne muh pe “404 error” likhwa le.",
    "Tu toh load-shedding ka human form hai.",
    "Tu toh chai mein namak jaisa hai — sab mood kharab.",
    "Tu talwaarein nahi chalata, sirf muh ka harami ban kar rehta hai.",
    "Tu fokat ka TED talk hai — knowledge zero, time waste 100%.",
    "Teri presence room ka AC off kar deti hai.",
    "Tu negative vibes ka brand ambassador hai.",
    "Tu toh aam ka beej hai — jab tak zinda, bas bekaar jagah le ke.",
    "Tu budget horror movie ka extra hai.",
    "Tere muh se truth comes out utna rare hai jitna IIT exam clear karna.",
    "Tu zero watt ka bulb hai — useless lekin mahanga bill karta hai.",
    "Tu toh asli “control-alt-delete” ka reason hai.",
    "You’re proof that birth control isn’t 100% effective.",
    "You’re the human version of spam mail.",
    "Even your shadow tries to avoid you.",
    "You have the personality of wet cardboard.",
    "You bring nothing to the table except crumbs.",
    "You’re a cloud — blocking out the sunshine for everyone.",
    "You look like a “before” picture that stayed that way.",
    "Your brain’s Wi-Fi signal has been disconnected since birth.",
    "You’re living proof that evolution can go in reverse.",
    "You have the charisma of a dial tone.",
    "Somewhere, a village is missing its idiot.",
    "You’re the diet version of a disappointment.",
    "You’re like a phone at 1% with no charger — anxiety in human form.",
    "You’re a glitch in the human system.",
    "Even autocorrect wouldn’t know what to do with you.",
    "You could ruin a wet dream.",
    "You’re a noise complaint waiting to happen.",
    "You’re an argument for selective breeding.",
    "Your face could make onions cry.",
    "You’re the “Skip Ad” button personified.",
    "You’re the prize in a box of disappointment.",
    "You’re the human form of a 404 error.",
    "Even GPS can’t locate your point.",
    "You’re a participation award nobody asked for.",
    "You could trip over a wireless connection.",
    "You’re a bad investment with no returns.",
    "You’re the human version of a typo.",
    "You’re like a Monday morning before coffee.",
    "Even your imaginary friends left you.",
    "You’re the sequel nobody wanted.",
    "You could be replaced by an empty chair and no one would notice.",
    "You’re a plot twist people saw coming — and still hated.",
    "You’re like expired milk — sour and unwanted.",
    "You’re the pothole everyone keeps hitting.",
    "You’re a playlist with only one terrible song.",
    "You’re proof that not all experiments work.",
    "You’re the human form of an ad popup.",
    "You’re the trailer for a terrible movie.",
    "You bring bad luck like a broken mirror.",
    "You’re the reason warning labels exist.",
    "You’re a cloud in a hurricane — useless and in the way.",
    "You’re the human buffering icon.",
    "You were an accident no one cleaned up.",
    "You’re the extra screw left after assembling IKEA furniture.",
    "You’re the cancellation email of human beings.",
    "You’re like Wi-Fi with no internet connection.",
    "You could get lost in your own driveway.",
    "You’re the awkward silence at a bad party.",
    "You’re the rerun of a terrible show.",
    "You’re the reason mute buttons exist."
]


# Pending mentions for Kaush reply wait logic
pending_mentions = {}

# Anti-spam tracking
user_message_times = {}
voice_clients = {}
jarvis_activated = False

engine_local = pyttsx3.init()

def speak_local(text):
    engine_local.say(text)
    engine_local.runAndWait()
    

# ===== Syntax check helpers =====
def check_python_syntax(code):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"SyntaxError: {e.msg} at line {e.lineno}, offset {e.offset}"

def check_java_syntax(code):
    if code.count('{') != code.count('}'):
        return "SyntaxError: Mismatched braces {}"
    if not re.search(r'\bclass\s+\w+', code):
        return "SyntaxWarning: No class declaration found"
    return None

def check_html_syntax(code):
    if code.count('<') != code.count('>'):
        return "SyntaxError: Mismatched < or > in HTML tags"
    open_tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>', code)
    close_tags = re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)>', code)
    self_closing = {"br", "hr", "img", "input", "meta", "link"}
    unclosed = {tag for tag in open_tags if tag not in close_tags and tag.lower() not in self_closing}
    if unclosed:
        return f"SyntaxWarning: Possible unclosed tags: {', '.join(unclosed)}"
    return None

def check_sql_syntax(code):
    if not code.strip().endswith(';'):
        return "SyntaxWarning: SQL statement should end with ';'"
    if not re.search(r'\b(select|insert|update|delete|create|drop|alter)\b', code, re.I):
        return "SyntaxWarning: No common SQL keywords found"
    return None

def check_css_syntax(code):
    if code.count('{') != code.count('}'):
        return "SyntaxError: Mismatched braces {} in CSS"
    for line in code.split('\n'):
        line = line.strip()
        if line and not line.startswith('@') and '{' not in line and '}' not in line:
            if ';' in line and ':' not in line:
                return "SyntaxWarning: Possible missing colon in CSS declaration"
    return None

def check_js_syntax(code):
    if code.count('{') != code.count('}'):
        return "SyntaxError: Mismatched braces {}"
    lines = code.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            continue
        if (not stripped.endswith(';') and
            not stripped.endswith('{') and
            not stripped.endswith('}') and
            not stripped.endswith(',') and
            not stripped.endswith(':') and
            not stripped.endswith(')') and
            not re.match(r'^(if|for|while|else|switch|try|catch)\b', stripped)):
            return f"SyntaxWarning: Missing semicolon on line {i+1}"
    return None

@bot.command(name="h")
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 Bot Commands & Events",
        description="Here is a list of commands you can use:",
        color=discord.Color.blue()
    )

    # Commands
    embed.add_field(
        name="**Syntax & Code Commands**",
        value=(
            "`*check` - Check syntax of Python, Java, HTML, SQL, CSS, JavaScript.\n"
            "`*roll [NdM+K]` - Roll dice using the format NdM+K (e.g., 2d6+3). Defaults to 1d6 if no input is given.\n"
            "`*poll <duration_in_seconds> <question>;<option1>;<option2>;...` - Create a timed poll with multiple options. Reactions will be added automatically for voting."
        ),
        inline=False
    )

    embed.add_field(
        name="**Voice & Jarvis Commands**",
        value=(
            "`*join [channel]` - Make bot join a voice channel.\n"
            "`*leave` - Make bot leave the voice channel.\n"
            "`*j` - Activate Jarvis voice assistant for commands.\n"
        ),
        inline=False
    )

    embed.add_field(
        name="**Fun & Social Commands**",
        value=(
            "`*roast [member]` - Roast a member or yourself.\n"
            "`*tease [text]` - Send a fun teasing message.\n"
            "`*friends` - Ping the configured users.\n"
        ),
        inline=False
    )

    embed.add_field(
        name="**Events / Features**",
        value=(
            "- Auto-abuse filter: Deletes messages with bad words.\n"
            "- Auto-teasing: Replies if message contains triggers like 'kaush', 'bug', etc.\n"
            "- Pending Kaush mentions: Sends a reply if Kaush doesn't respond in 4 minutes.\n"
            "- Random compliments: ~10% chance to compliment users.\n"
        ),
        inline=False
    )

    embed.set_footer(text="Use the commands responsibly! 😎")

    await ctx.send(embed=embed)


@bot.command(name="check")
async def check_command(ctx):
    """Ask for language and code, then check syntax"""
    r = sr.Recognizer()

    await ctx.send(f"{ctx.author.mention} Which language? (Python, Java, HTML, SQL, CSS, JavaScript)")
    speak_local("Which language would you like to check?")

    lang = None

    # Try speech recognition first
    try:
        with sr.Microphone() as source:
            await ctx.send("Say a command...")
            speak_local("Say the language now.")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            spoken_text = r.recognize_google(audio).lower()
            await ctx.send(f"You said: `{spoken_text}`")
            lang = spoken_text.strip()
    except Exception as e:
        await ctx.send(f"(Speech failed: {e}) Please type the language instead.")

    # If speech failed or unrecognized, wait for typed message
    if not lang:
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        lang = msg.content.strip().lower()

    # Normalize JS
    if "javascript" in lang or lang == "js":
        lang = "javascript"

    # Check if supported
    if lang not in ["python", "java", "html", "sql", "css", "javascript"]:
        speak_local("Unsupported language.")
        await ctx.send(f"Sorry, {ctx.author.mention}, I only support Python, Java, HTML, SQL, CSS, or JavaScript.")
        return

    # Ask for code
    speak_local(f"Please paste your {lang} code. Type 'done' when finished.")
    await ctx.send(f"Paste your `{lang}` code here, {ctx.author.mention}. Type `done` when finished.")

    code_lines = []
    while True:
        msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        if msg.content.strip().lower() == "done":
            break
        code_lines.append(msg.content)

    code = "\n".join(code_lines)

    # Run syntax check
    check_func = {
        "python": check_python_syntax,
        "java": check_java_syntax,
        "html": check_html_syntax,
        "sql": check_sql_syntax,
        "css": check_css_syntax,
        "javascript": check_js_syntax
    }[lang]

    error = check_func(code)
    if error:
        speak_local(f"Error found: {error}")
        await ctx.send(f"**Error in your `{lang}` code:**\n```{error}```")
    else:
        speak_local(f"No syntax errors detected in your {lang} code.")
        await ctx.send(f"✅ No syntax issues detected in your `{lang}` code, {ctx.author.mention}.")

# ===== Voice channel helpers =====
@bot.command()
async def join(ctx, *, channel_name: str = None):
    """Join a voice channel by name or the user's current voice channel if not specified"""
    
    # Optional: Restrict to your Discord ID
    if ctx.author.id != 772331428385390633:
        await ctx.send("You are not allowed to use this command.")
        return

    # Determine target channel
    if channel_name:
        # Case-insensitive search for the channel name
        channel = discord.utils.find(lambda c: c.name.lower() == channel_name.lower(), ctx.guild.voice_channels)
        if not channel:
            await ctx.send(f"Could not find a voice channel named '{channel_name}'.")
            return
    else:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not in a voice channel. Please join one first or specify the channel name.")
            return

    # Connect or move
    vc = voice_clients.get(ctx.guild.id)
    if vc and vc.is_connected():
        # Move bot if already connected
        await vc.move_to(channel)
        await ctx.send(f"Moved to voice channel: {channel.name}")
        speak(f"Moved to voice channel {channel.name}")
    else:
        # Connect bot
        vc = await channel.connect()
        voice_clients[ctx.guild.id] = vc
        await ctx.send(f"Joined voice channel: {channel.name}")
        speak(f"Joined voice channel {channel.name}")


@bot.command()
async def leave(ctx):
    """Leave the current voice channel"""
    vc = voice_clients.get(ctx.guild.id)
    if vc and vc.is_connected():
        await vc.disconnect()
        del voice_clients[ctx.guild.id]
        await ctx.send("Left the voice channel.")
        speak("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

# ===== Modify *j to work only if user is in the same voice channel as bot =====
@bot.command()
async def j(ctx):
    import speech_recognition as sr
    import webbrowser
    import re
    global jarvis_activated
    r = sr.Recognizer()

    if not jarvis_activated:
        greet_text = "Hello! Jarvis activated!"
        jarvis_activated = True
    else:
        greet_text = "Hello! I am Jarvis. You can tell me to open Google, YouTube, or play music (specific or random)."

    speak(greet_text)
    await ctx.send(greet_text)
    
    try:
        # Listen for main command
        with sr.Microphone() as source:
            await ctx.send("Say a command...")
            speak("Say a command...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=10)

        query = r.recognize_google(audio).lower()
        await ctx.send(f"You said: {query}")
        speak(f"You said: {query}")

        # Open YouTube
        if 'youtube' in query:
            channel_search = re.search(r'channel (\w+)', query)
            search_term = re.search(r'for (.+)', query)
            url = "https://youtube.com"
            if channel_search:
                url = f"https://www.youtube.com/c/{channel_search.group(1)}"
            elif search_term:
                url = f"https://www.youtube.com/results?search_query={search_term.group(1).replace(' ', '+')}"
            webbrowser.open(url)
            await ctx.send(f"Opening YouTube: {url}")
            speak(f"Opening YouTube: {url}")

        # Open Google
        elif 'google' in query:
            search_term = re.search(r'google (?:search |for |open )?(.+)', query)
            url = "https://google.com"
            if search_term:
                keyword = search_term.group(1).strip()
                websites = {
                    "geeks for geeks": "https://www.geeksforgeeks.org",
                    "youtube": "https://www.youtube.com",
                    "stackoverflow": "https://stackoverflow.com",
                }
                site_url = websites.get(keyword.lower())
                if site_url:
                    url = site_url
                else:
                    url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
            webbrowser.open(url)
            await ctx.send(f"Opening Google/search: {url}")
            speak(f"Opening Google/search: {url}")

        # Open any other website
        elif 'open' in query:
            website_match = re.search(r'open (.+)', query)
            if website_match:
                site = website_match.group(1).strip()
                if not site.startswith("http"):
                    site = "https://" + site
                webbrowser.open(site)
                await ctx.send(f"Opening {site}")
                speak(f"Opening {site}")

        # Music handling
        elif 'music' in query:
            await ctx.send("Do you want me to play a random track or a specific one? Say random or specific.")
            speak("Do you want me to play a random track or a specific one? Say random or specific.")

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio_choice = r.listen(source, timeout=10, phrase_time_limit=10)

            try:
                choice = r.recognize_google(audio_choice).lower()
                await ctx.send(f"You chose: {choice}")

                if 'random' in choice:
                    play_random_spotify_track()
                    await ctx.send("Playing a random track on Spotify!")
                    speak("Playing a random track on Spotify!")

                elif 'pacific' in choice:
                    await ctx.send("Please say the track, artist, or playlist you want me to play:")
                    speak("Please say the track, artist, or playlist you want me to play:")

                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio_search = r.listen(source, timeout=10, phrase_time_limit=10)

                    # Listen for specific track
                    search_query = r.recognize_google(audio_search).lower()
                    await ctx.send(f"Searching for: {search_query}")

                    # Search Spotify
                    results = sp.search(q=f"track:{search_query}", limit=1, type='track')
                    if results['tracks']['items']:
                        track = results['tracks']['items'][0]
                        url = track['external_urls']['spotify']
                        webbrowser.open(url)
                        await ctx.send(f"Playing track: {track['name']} by {track['artists'][0]['name']}\n{url}")
                        speak(f"Playing track {track['name']} by {track['artists'][0]['name']}")
                    else:
                        await ctx.send(f"Sorry, I couldn't find anything for '{search_query}' on Spotify.")
                        speak(f"Sorry, I couldn't find anything for {search_query} on Spotify.")

                else:
                    await ctx.send("Invalid choice, playing a random track instead.")
                    speak("Invalid choice, playing a random track instead.")
                    play_random_spotify_track()

            except sr.UnknownValueError:
                await ctx.send("Sorry, I couldn't understand your choice. Playing a random track instead.")
                speak("Sorry, I couldn't understand your choice. Playing a random track instead.")
                play_random_spotify_track()

        # Stop command
        elif 'stop' in query:
            await ctx.send("Stopping Jarvis.")
            speak("Stopping Jarvis.")
            return

        else:
            await ctx.send("Command not recognized.")
            speak("Command not recognized.")

    except sr.UnknownValueError:
        await ctx.send("Sorry, I couldn't understand your voice.")
        speak("Sorry, I couldn't understand your voice.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        speak(f"Error: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Anti-spam
    now = asyncio.get_event_loop().time()
    uid = message.author.id
    user_message_times.setdefault(uid, [])
    user_message_times[uid] = [t for t in user_message_times[uid] if now - t < 10]
    user_message_times[uid].append(now)
    if len(user_message_times[uid]) > 5:
        await message.channel.send(f"{message.author.mention}, slow down! You're sending too many messages.")
        user_message_times[uid].clear()
        return

    content_lower = message.content.lower()
    mentions_kaush = any(u.id == KAUSH for u in message.mentions)

    # If Kaush replies, cancel pending timer
    if message.author.id == KAUSH:
        ch_id = message.channel.id
        if ch_id in pending_mentions:
            del pending_mentions[ch_id]
        await bot.process_commands(message)
        return

    # === Case A & B: Kaush tagged ===
    if mentions_kaush:
        if abuse_pattern.search(content_lower):
            # Case A – Abusive mention → abuse back
            await message.channel.send(f"{message.author.mention} {random.choice(bad_abuse_responses_english)}")
        else:
            # Case B – Non-abusive mention → set pending "I will be late" or offline msg
            guild = message.guild
            kaush_member = guild.get_member(KAUSH)
            if kaush_member:
                if kaush_member.status != discord.Status.offline:
                    ch_id = message.channel.id
                    pending_mentions[ch_id] = message.author.mention
                    async def wait_for_kaush():
                        await asyncio.sleep(240)  # 4 minutes
                        if ch_id in pending_mentions:
                            await message.channel.send(f"{pending_mentions[ch_id]} I will be late, please wait!")
                            del pending_mentions[ch_id]
                    bot.loop.create_task(wait_for_kaush())
                else:
                    await message.channel.send(random.choice(tagged_replies_offline))
            else:
                await message.channel.send("Can't find Kaush in this server.")
        await bot.process_commands(message)
        return

    # === Case C: General abuse anywhere else (no tag) ===
    if abuse_pattern.search(content_lower):
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")
        return

    # Teasing triggers
    if any(trigger in content_lower for trigger in teasing_triggers):
        tease = random.choice(teasing_replies).format(user=message.author.mention)
        await message.channel.send(tease)

    # Random compliments (~10% chance)
    if not message.author.bot and random.random() < 0.1:
        comp = random.choice(compliments)
        await message.channel.send(f"{message.author.mention}, {comp}")

    await bot.process_commands(message)

# ===== Commands =====

@bot.command()
async def roast(ctx, member: discord.Member = None):
    member = member or ctx.author
    msg = random.choice(roasts).format(user=member.mention)
    await ctx.send(msg)

@bot.command()
async def tease(ctx, member: discord.Member = None):
    """
    If member is given, tease that member, otherwise tease the command user.
    Picks a random teasing line from teasing_replies.
    """
    target = member.mention if member else ctx.author.mention
    tease_line = random.choice(teasing_replies).format(user=target)
    await ctx.send(tease_line)

import re
import random
from discord.ext import commands

@bot.command()
async def roll(ctx, *, dice: str = "1d6"):
    """
    Roll dice.
    Usage examples:
    !roll 1d6       -> roll one 6-sided dice
    !roll 3d20+5    -> roll three 20-sided dice and add 5
    """

    try:
        # Parse dice string like "2d6+3" or "d20"
        pattern = r'(\d*)d(\d+)([+-]\d+)?'
        match = re.fullmatch(pattern, dice.replace(" ", ""))
        if not match:
            await ctx.send("Invalid dice format! Use NdM+K, e.g., 2d6+3")
            return

        num_dice = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        if num_dice > 20:
            await ctx.send("You can roll a maximum of 20 dice at once!")
            return
        if sides < 2:
            await ctx.send("Dice must have at least 2 sides!")
            return

        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        # Visual for d6
        dice_visual = ""
        if sides == 6:
            dice_faces = ["🎲", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            dice_visual = " ".join(dice_faces[r] for r in rolls)

        await ctx.send(
            f"{ctx.author.mention} rolled: {rolls}\n"
            + (f"Visual: {dice_visual}\n" if dice_visual else "")
            + (f"Modifier: {modifier}\n" if modifier else "")
            + f"Total: {total}"
        )

    except Exception as e:
        await ctx.send(f"Error rolling dice: {e}")


@bot.command()
async def friends(ctx):
    # Remove any None values from the list
    valid_mentions = [uid for uid in mention_user_ids if uid is not None]
    
    # Format mentions
    mentions = ' '.join(f"<@{uid}>" for uid in valid_mentions)
    
    if mentions:
        await ctx.send(f"🚨 Hey {mentions}! When are you all going to come online and join the fun on Discord? 😎")
    else:
        await ctx.send("No valid users to mention!")


import discord
from discord.ext import commands, tasks
import asyncio

@bot.command()
async def poll(ctx, duration: int, *, question_and_options):
    """
    Create a poll with custom options and duration.
    Usage: !poll 60 What's your favorite color?;Red;Blue;Green
    """
    try:
        parts = question_and_options.split(";")
        question = parts[0]
        options = parts[1:]

        if len(options) < 2:
            await ctx.send("You need to provide at least 2 options separated by `;`.")
            return

        # Emojis for up to 10 options
        emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        if len(options) > len(emojis):
            await ctx.send("Maximum 10 options allowed.")
            return

        description = ""
        for i, option in enumerate(options):
            description += f"{emojis[i]} {option}\n"

        embed = discord.Embed(title=f"Poll: {question}", description=description, color=0x00ff00)
        embed.set_footer(text=f"Poll ends in {duration} seconds")
        message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await message.add_reaction(emojis[i])

        # Wait for the duration
        await asyncio.sleep(duration)

        # Refresh message to get updated reactions
        message = await ctx.channel.fetch_message(message.id)

        results = {}
        for i in range(len(options)):
            reaction = discord.utils.get(message.reactions, emoji=emojis[i])
            if reaction:
                results[options[i]] = reaction.count - 1  # exclude bot's own reaction

        # Create result message
        result_msg = "Poll Results:\n"
        for option, count in results.items():
            result_msg += f"{option}: {count} votes\n"

        await ctx.send(result_msg)

    except Exception as e:
        await ctx.send(f"Error creating poll: {e}")


# Run the bot
bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
