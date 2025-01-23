import discord
from discord.ext import commands, tasks
from discord import app_commands,Interaction
import json
import os
from datetime import datetime, timezone, timedelta, time
import asyncio
from dotenv import load_dotenv
import random
import aiohttp


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#developers:
Naveen_User_ID = "776486456918540308" 
Aastha_User_ID = "1290696205491507260"


class Client (commands.Bot):
    async def on_ready(self):
        try:
            guild = discord.Object(id=1326112748379312138)
            synced = await self.tree.sync(guild=guild)
            print(f"synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands : {e}")
        
        reminder_check.start()
        daily_reminder.start()
        #start auto-profile updater on restart
        if not auto_change_pfp.is_running():
            auto_change_pfp.start()
        print (f'Logged on as {self.user}!')
    





Guild_ID = discord.Object(id=1326112748379312138)
intents = discord. Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)







#######################################################embed-messages##################################################
# Store temporary embed data
embed_data = {}
# Slash command to generate embed
@client.tree.command(name="generate_embed", description="Generate an interactive embed", guild=Guild_ID)
async def generate_embed(interaction: discord.Interaction):
    await interaction.response.send_message("Starting embed generation process... Please check your DMs.", ephemeral=True)

    user = interaction.user
    dm_channel = await user.create_dm()
    embed_data.clear()

    try:
        # Title
        await dm_channel.send("What's the title of the embed?")
        title_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        embed_data["title"] = title_msg.content

        # Description
        await dm_channel.send("What should the description be?")
        desc_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        embed_data["description"] = desc_msg.content

        # URL (Optional)
        await dm_channel.send("Do you want to add a URL? (Yes/No)")
        url_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if url_msg.content.lower() == "yes":
            await dm_channel.send("Enter the URL:")
            url_input = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            embed_data["url"] = url_input.content

        # Author (Optional)
        await dm_channel.send("Do you want to add an author name? (Yes/No)")
        author_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if author_msg.content.lower() == "yes":
            await dm_channel.send("Enter the author name:")
            author_name_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            embed_data["author"] = {"name": author_name_msg.content}

            await dm_channel.send("Do you want to add an author URL? (Yes/No)")
            author_url_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            if author_url_msg.content.lower() == "yes":
                await dm_channel.send("Enter the author URL:")
                author_url_input = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
                embed_data["author"]["url"] = author_url_input.content

        # Thumbnail URL (Optional)
        await dm_channel.send("Do you want to add a thumbnail URL? (Yes/No)")
        thumbnail_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if thumbnail_msg.content.lower() == "yes":
            await dm_channel.send("Enter the thumbnail URL:")
            thumbnail_input = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            embed_data["thumbnail"] = thumbnail_input.content

        # Image URL (Optional)
        await dm_channel.send("Do you want to add an image URL? (Yes/No)")
        image_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if image_msg.content.lower() == "yes":
            await dm_channel.send("Enter the image URL:")
            image_input = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            embed_data["image"] = image_input.content

        # Footer (Optional)
        await dm_channel.send("Do you want to add a footer? (Yes/No)")
        footer_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if footer_msg.content.lower() == "yes":
            await dm_channel.send("Enter the footer text:")
            footer_text_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            embed_data["footer"] = {"text": footer_text_msg.content}

            await dm_channel.send("Do you want to add a footer image URL? (Yes/No)")
            footer_img_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            if footer_img_msg.content.lower() == "yes":
                await dm_channel.send("Enter the footer image URL:")
                footer_img_input = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
                embed_data["footer"]["icon_url"] = footer_img_input.content

        # Fields (Optional)
        embed_data["fields"] = []
        await dm_channel.send("Do you want to add fields? (Yes/No)")
        add_fields_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        while add_fields_msg.content.lower() == "yes":
            await dm_channel.send("Enter the field name:")
            field_name_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            field_name = field_name_msg.content

            await dm_channel.send("Enter the field value:")
            field_value_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            field_value = field_value_msg.content

            embed_data["fields"].append({"name": field_name, "value": field_value, "inline": True})

            await dm_channel.send("Do you want to add another field? (Yes/No)")
            add_fields_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)

        # Color
        await dm_channel.send("Enter a color for the embed (e.g., #ff5733 or 'random'):")
        color_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        embed_data["color"] = color_msg.content.lower()

        # Build Embed Preview
        embed_preview = discord.Embed(
            title=embed_data["title"],
            description=embed_data["description"],
            color=discord.Color.random() if embed_data["color"] == "random" else discord.Color(int(embed_data["color"].strip("#"), 16))
        )

        if "url" in embed_data:
            embed_preview.url = embed_data["url"]

        if "author" in embed_data:
            embed_preview.set_author(name=embed_data["author"]["name"], url=embed_data["author"].get("url"))

        if "thumbnail" in embed_data:
            embed_preview.set_thumbnail(url=embed_data["thumbnail"])

        if "image" in embed_data:
            embed_preview.set_image(url=embed_data["image"])

        if "footer" in embed_data:
            embed_preview.set_footer(text=embed_data["footer"]["text"], icon_url=embed_data["footer"].get("icon_url"))

        for field in embed_data["fields"]:
            embed_preview.add_field(name=field["name"], value=field["value"], inline=field["inline"])

        # Show Final Preview
        await dm_channel.send("Here is the preview of your embed:", embed=embed_preview)

        await dm_channel.send("Do you want to post it? (Yes/No)")
        confirm_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
        if confirm_msg.content.lower() == "yes":
            await dm_channel.send("Mention the channel to post the embed (e.g., #channel-name):")
            channel_msg = await client.wait_for('message', check=lambda m: m.author == user and m.channel == dm_channel, timeout=60)
            channel_name = channel_msg.content.strip('#').lower()

            channel = discord.utils.get(interaction.guild.text_channels, name=channel_name)
            if channel:
                await channel.send(embed=embed_preview)
                await dm_channel.send(f"Embed has been posted in {channel.mention}.")
            else:
                await dm_channel.send("Invalid channel. Embed not posted.")
        else:
            await dm_channel.send("Embed generation cancelled.")

    except Exception as e:
        await dm_channel.send(f"An error occurred: {e}")

###############################################End##############################################################

###############################################Delete-Message#######################################################

@client.tree.command(name="delete", description="Deletes the specified number of messages", guild=Guild_ID)
async def delete(interaction: discord.Interaction, amount: int):
    # Ensure the user has permission to manage messages
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "You don't have permission to delete messages.", ephemeral=True
        )
        return

    # Defer the response to handle potential delays
    await interaction.response.defer(ephemeral=True)

    try:
        # Fetch and delete messages
        deleted = await interaction.channel.purge(limit=amount)
        deleted_count = len(deleted)

        # Notify the user about the actual number of messages deleted
        await interaction.followup.send(
            f"Requested to delete {amount} messages. Successfully deleted {deleted_count} messages.",
            ephemeral=True,
        )
    except Exception as e:
        # Handle any errors gracefully
        await interaction.followup.send(
            f"An error occurred: {e}", ephemeral=True
        )
#########################################################end####################################################

#############################################Banned-Words-Moderation############################################

JSON_FILE = "banned_slash_command_data.json"

# Function to load data from JSON file
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            return data
    else:
        return {"banned_words": ["breakup", "argument"], "allowed_role_list": ["Moderator", "Admin"]}

# Function to save data to JSON file
def save_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load data from the JSON file at the start
data = load_data()

# Extract banned words and allowed roles from loaded data
banned_words = set(data["banned_words"])
allowed_role_list = data["allowed_role_list"]

# Slash command to manage banned words
@client.tree.command(name="manage_banned_words", description="Manage banned words ('add', 'remove', 'view')", guild=Guild_ID)
@discord.app_commands.describe(
    action="Choose an action: add, remove, or view",
    word="The word to add or remove (not required for 'view')"
)
@discord.app_commands.choices(
    action=[
        discord.app_commands.Choice(name="Add a banned word", value="add"),
        discord.app_commands.Choice(name="Remove a banned word", value="remove"),
        discord.app_commands.Choice(name="View banned words", value="view"),
    ]
)
async def manage_banned_words(
    interaction: discord.Interaction,
    action: discord.app_commands.Choice[str],
    word: str = None
):
    action = action.value.lower()

    # Check if the user has permission to modify banned words
    if not interaction.user.guild_permissions.administrator and not any(role.name in allowed_role_list for role in interaction.user.roles):
        await interaction.response.send_message("You do not have permission to modify banned words.")
        return

    # Handle actions
    if action == "add":
        if not word:
            await interaction.response.send_message("Please provide a word to add.")
            return

        word = word.lower()
        if word not in banned_words:
            banned_words.add(word)
            data["banned_words"] = list(banned_words)
            save_data(data)  # Save the updated list
            await interaction.response.send_message(f"'{word}' added to banned words.")
        else:
            await interaction.response.send_message(f"'{word}' is already in the banned words list.")

    elif action == "remove":
        if not word:
            await interaction.response.send_message("Please provide a word to remove.")
            return

        word = word.lower()
        if word in banned_words:
            banned_words.remove(word)
            data["banned_words"] = list(banned_words)
            save_data(data)  # Save the updated list
            await interaction.response.send_message(f"'{word}' removed from banned words.")
        else:
            await interaction.response.send_message(f"'{word}' is not in the banned words list.")

    elif action == "view":
        banned_list = ", ".join(banned_words) if banned_words else "No banned words yet."
        await interaction.response.send_message(f"Banned words: {banned_list}")

    else:
        await interaction.response.send_message("Invalid action. Use 'add', 'remove', or 'view'.")

# Event triggered when a message is sent
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Detect if banned word is used
    detected_words = [word for word in banned_words if word in message.content.lower()]
    if detected_words:
        # Delete the message
        await message.delete()

        # Prepare the response message with "****" replacing the banned words
        modified_content = message.content
        for word in detected_words:
            modified_content = modified_content.replace(word, "******")

        # Send a message in the same channel
        await message.channel.send(f"{message.author.name} used a banned word! Please stay mindful. You said: \"{modified_content}\"")

        # Log the banned word(s) usage
        print(f"Banned word(s) used: {', '.join(detected_words)} by {message.author.name} in: '{message.content}'")
        
        # Optionally, DM the user
        try:
            await message.author.send(f"Your message contained a banned word: {', '.join(detected_words)}. Message is deleted.")
        except discord.errors.Forbidden:
            pass  # No DM if user has them closed

    await client.process_commands(message)  # Allow commands to work
#####################################################End#########################################################

###################################################Reminders#####################################################

REMINDER_JSON_FILE = "reminder_data.json"

# Functions to handle reminders
def load_reminders():
    """Load reminders from the JSON file."""
    if os.path.exists(REMINDER_JSON_FILE):
        try:
            with open(REMINDER_JSON_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading reminders JSON: {e}")
    return {}

def save_reminders(reminders):
    """Save reminders to the JSON file."""
    try:
        with open(REMINDER_JSON_FILE, "w") as f:
            json.dump(reminders, f, indent=4)
    except Exception as e:
        print(f"Error saving reminders JSON: {e}")

reminders = load_reminders()  # Load reminders at start

# Slash command to set a reminder
@client.tree.command(name="reminder", description="Set a reminder", guild=Guild_ID)
@app_commands.describe(
    date="Enter 'today', 'tomorrow', 'day after tomorrow', or 'dd/mm/yyyy'",
    time="Time in hh:mm format",
    am_pm="'am' or 'pm'",
    content="Reminder description"
)
async def set_reminder(
    interaction: discord.Interaction,
    date: str,
    time: str,
    am_pm: str,
    content: str
):
    try:
        # Calculate the reminder date and time
        if date.lower() == "today":
            reminder_date = datetime.now()
        elif date.lower() == "tomorrow":
            reminder_date = datetime.now() + timedelta(days=1)
        elif date.lower() == "day after tomorrow":
            reminder_date = datetime.now() + timedelta(days=2)
        else:
            reminder_date = datetime.strptime(date, "%d/%m/%Y")

        hour, minute = map(int, time.split(":"))
        if am_pm.lower() == "pm" and hour != 12:
            hour += 12
        elif am_pm.lower() == "am" and hour == 12:
            hour = 0

        reminder_datetime = datetime(
            reminder_date.year, reminder_date.month, reminder_date.day, hour, minute
        )

        if reminder_datetime <= datetime.now():
            await interaction.response.send_message("You can't set a reminder in the past.")
            return

        reminder_key = f"{interaction.user.id}-{reminder_datetime.timestamp()}"
        reminders[reminder_key] = {
            "datetime": reminder_datetime.strftime("%d/%m/%Y %H:%M"),
            "user_id": interaction.user.id,
            "channel_id": interaction.channel.id,
            "content": content,
        }
        save_reminders(reminders)

        formatted_datetime = reminder_datetime.strftime("%d/%m/%Y at %I:%M %p")
        await interaction.response.send_message(f"Reminder set for {formatted_datetime}.")

    except Exception as e:
        await interaction.response.send_message(f"Error: {str(e)}. Please check your input format.")

# Slash command to view reminders
@client.tree.command(name="view-reminder", description="View all reminders", guild=Guild_ID)
async def view_calendar(interaction: discord.Interaction):
    user_reminders = [
        rem for rem in reminders.values() if rem["user_id"] == interaction.user.id
    ]

    if not user_reminders:
        await interaction.response.send_message("No reminders set.")
        return

    reminder_list = [
        f"{datetime.strptime(rem['datetime'], '%d/%m/%Y %H:%M').strftime('%d/%m/%Y at %I:%M %p')} - {rem['content']}"
        for rem in user_reminders
    ]
    reminder_list.sort()
    calendar_view = "\n".join(reminder_list)
    await interaction.response.send_message(f"**Reminders:**\n{calendar_view}")

# Background task to check reminders
@tasks.loop(seconds=1)  # Check every second
async def reminder_check():
    now = datetime.now()
    reminders_to_remove = []
#update- 24jan 2025 -> removed while true
    for key, rem in reminders.items():
        reminder_time = datetime.strptime(rem["datetime"], "%d/%m/%Y %H:%M")
        if now >= reminder_time:  # Trigger reminder
            user_id = rem["user_id"]
            channel_id = rem.get("channel_id")
            content = rem["content"]

            try:
                # Send DM to the user
                user = await client.fetch_user(user_id)
                if user:
                    await user.send(
                        f"🔔 Reminder: **{content}** (set for {reminder_time.strftime('%d/%m/%Y at %I:%M %p')})"
                    )
            except discord.NotFound:
                print(f"User with ID {user_id} not found. Removing reminder.")
                reminders_to_remove.append(key)
                continue
            except discord.HTTPException as e:
                print(f"Failed to fetch user {user_id} due to an API error: {e}")
                continue

            # Send reminder in the server channel
            if channel_id:
                channel = client.get_channel(channel_id)
                if channel:
                    await channel.send(
                        f"🔔 <@{user_id}> Reminder: **{content}** (set for {reminder_time.strftime('%d/%m/%Y at %I:%M %p')})"
                    )

            reminders_to_remove.append(key)

    # Remove processed reminders
    for key in reminders_to_remove:
        del reminders[key]
    save_reminders(reminders)

#####################################################End#########################################################

##################################################Daily journal###########################

#loop

@tasks.loop(time=time(22, 0))  # Run at 10:00 PM daily
async def daily_reminder():
    # Reminder message
    reminder_message = "Hey, <@{naveen}> & <@{aastha}>, use /journal and log your journal entry now!".format(
        naveen=Naveen_User_ID, aastha=Aastha_User_ID
    )

    # Send message to each user's DM
    for user_id in [Naveen_User_ID, Aastha_User_ID]:
        try:
            user = await client.fetch_user(user_id)
            await user.send(reminder_message)
        except Exception as e:
            print(f"Failed to send DM to user with ID {user_id}: {e}")

@daily_reminder.before_loop
async def before_daily_reminder():
    await client.wait_until_ready()


#loop end


@client.tree.command(name="journal", description="Log your journal entry for the day.", guild=Guild_ID)
async def journal(interaction: discord.Interaction):
    try:
        # Respond immediately in the server to confirm the process has started
        await interaction.response.send_message(
            "I’ve sent you a DM to log your journal. Please check your DMs.",
            ephemeral=True
        )

        # Send initial DM message
        dm_channel = await interaction.user.create_dm()
        await dm_channel.send("Start Journaling now. Write about your day.")
        
        def check(msg):
            return msg.author == interaction.user and msg.channel == dm_channel

        # Wait for the user's journal content
        journal_entry_msg = await client.wait_for('message', check=check, timeout=300.0)
        journal_entry = journal_entry_msg.content

        await dm_channel.send("Rate your mood out of 10.")
        mood_msg = await client.wait_for('message', check=check, timeout=300.0)
        mood_rating = mood_msg.content

        await dm_channel.send("Did you exercise today?")
        exercise_msg = await client.wait_for('message', check=check, timeout=300.0)
        exercised = exercise_msg.content

        await dm_channel.send("Did you eat junk food today?")
        junk_food_msg = await client.wait_for('message', check=check, timeout=300.0)
        ate_junk_food = junk_food_msg.content

        await dm_channel.send("Did you bath today?")
        bath_msg = await client.wait_for('message', check=check, timeout=300.0)
        bathed = bath_msg.content

        await dm_channel.send("Did you work hard today?")
        work_msg = await client.wait_for('message', check=check, timeout=300.0)
        worked_hard = work_msg.content

        await dm_channel.send("Learnt something new today? if yes, whats it?")
        learnt_today_msg = await client.wait_for('message', check=check, timeout=300.0)
        Learnt_today = learnt_today_msg.content

        await dm_channel.send("What are things that you are grateful for? what made you smile today?")
        smile_today_msg = await client.wait_for('message', check=check, timeout=300.0)
        smile_today = smile_today_msg.content

        await dm_channel.send("What You Accomplished Today: Write down what you accomplished today, no matter how big or small it may seem.")
        accomplishment_today_msg = await client.wait_for('message', check=check, timeout=300.0)
        accomplishment_today = accomplishment_today_msg.content

        # Determine embed color and GIF based on user ID
        if str(interaction.user.id) == Naveen_User_ID:  # Naveen_User_ID
            embed_color = discord.Color.blue()
            gif_url = "https://i.ibb.co/XZS19GG/dudu-writing-naveen.gif"  # GIF for Naveen
        elif str(interaction.user.id) == Aastha_User_ID:  # Aastha_User_ID
            embed_color = discord.Color.from_rgb(255, 182, 193)  # Baby Pink
            gif_url = "https://i.ibb.co/TtG2vsr/bubu-aastha.gif"  # GIF for Aastha
        else:
            embed_color = discord.Color.default()  # Default color for other users
            gif_url = None

        # Create an embed with author's profile picture and GIF as image
        today_date = datetime.now().strftime("%d/%m/%Y")
        embed = discord.Embed(
            title=f"{interaction.user.name}'s journal entry of {today_date}",
            description=journal_entry,
            color=embed_color
        )

        # Check if avatar is not None
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)  # Author's profile picture
        else:
            embed.set_thumbnail(url="https://via.placeholder.com/150")  # Fallback placeholder

        if gif_url:  # Add the GIF only if defined for the user
            embed.set_image(url=gif_url)

        embed.add_field(name="Rate your mood out of 10", value=mood_rating, inline=False)
        embed.add_field(name="Did you exercise today?", value=exercised, inline=False)
        embed.add_field(name="Did you eat junk food today?", value=ate_junk_food, inline=False)
        embed.add_field(name="Did you bath today?", value=bathed, inline=False)
        embed.add_field(name="Did you work hard today?", value=worked_hard, inline=False)
        embed.add_field(name="Learnt something new today? if yes, whats it?", value=Learnt_today, inline=False)
        embed.add_field(name="What are things that you are grateful for? what made you smile today?", value=smile_today, inline=False)
        embed.add_field(name="What You Accomplished Today: Write down what you accomplished today, no matter how big or small it may seem.", value=accomplishment_today, inline=False)
        embed.set_footer(text=f"{today_date} {interaction.user.name}")

        # Send the embed to the journal channel
        journal_channel = discord.utils.get(interaction.guild.text_channels, name="journal")
        if journal_channel:
            await journal_channel.send(embed=embed)
            await dm_channel.send(
                f"Your journal entry has been successfully logged in {journal_channel.mention}!"
            )
        else:
            await dm_channel.send(
                "Journal channel not found. Please create a channel named 'journal'."
            )
    
    except asyncio.TimeoutError:
        await dm_channel.send("You took too long to respond. Please try again later.")
    except discord.Forbidden:
        await interaction.followup.send(
            "I couldn't send you a DM. Please enable DMs from server members and try again.", ephemeral=True
        )

########################################################End################################################





############################################custom########################################

###say
@client.tree.command(name="say", description="says whatever you want to say", guild=Guild_ID)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

#removed reaction feature. //Causing 2nd time definition of even on_message, which made banned word feature useless.

#####Change_pfp#############################
pfp_urls = {
    "naveen": "https://i.ibb.co/cxyP8tm/Slash-Naveen-pfp.gif", #on naveen using /change_pfp
    "aastha": "https://i.ibb.co/tKHjGdj/slash-aastha-pfp.gif", #on aastha using /change_pfp
    "daytime": "https://i.ibb.co/cDccgcC/daytime-6am.gif",     #at 6am
    "nighttime": "https://i.ibb.co/S3D5FmR/nighttime-11pm.gif" #at 11pm
}


# Command to manually change the bot's PFP
@client.tree.command(name="change-pfp", description="Change the bot's profile picture.", guild=Guild_ID)
async def change_pfp(interaction: Interaction, user: str):
    """
    Slash command to change the bot's profile picture based on user ('naveen' or 'aastha').
    """
    # Acknowledge the command immediately to prevent timeout
    await interaction.response.defer(ephemeral=True)

    user = user.lower()
    if user == "naveen" and str(interaction.user.id) == Naveen_User_ID:
        pfp_url = pfp_urls["naveen"]
    elif user == "aastha" and str(interaction.user.id) == Aastha_User_ID:
        pfp_url = pfp_urls["aastha"]
    else:
        await interaction.followup.send("Sorry, you do not have permission to change the bot's PFP!")
        return

    try:
        # Fetch the image as binary data
        async with aiohttp.ClientSession() as session:
            async with session.get(pfp_url) as response:
                if response.status == 200:
                    pfp_bytes = await response.read()
                    await client.user.edit(avatar=pfp_bytes)
                    await interaction.followup.send("Profile picture updated successfully!")
                else:
                    await interaction.followup.send(f"Failed to fetch the image: HTTP {response.status}")
    except Exception as e:
        await interaction.followup.send(f"Failed to change the PFP: {e}")


# Task to automatically change PFP at specific times (IST)
@tasks.loop(minutes=1)
async def auto_change_pfp():
    """
    Automatically change the bot's profile picture at 6 AM and 11 PM IST.
    """
    now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)  # Convert UTC to IST
    current_time = now.strftime("%H:%M")

    if current_time == "06:00":  # 6 AM IST || 06:00
        pfp_url = pfp_urls["daytime"]
    elif current_time == "23:00":  # 11 PM IST || 23:00
        pfp_url = pfp_urls["nighttime"]
    else:
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(pfp_url) as response:
                if response.status == 200:
                    pfp_bytes = await response.read()
                    await client.user.edit(avatar=pfp_bytes)
                    print(f"Profile picture changed successfully at {current_time} IST.")
                else:
                    print(f"Failed to fetch the image: HTTP {response.status}")
    except Exception as e:
        print(f"Failed to change the PFP: {e}")

class PFPChangeView(discord.ui.View):
    """Custom view for selecting PFP change options."""

    def __init__(self):
        super().__init__()
        self.add_item(PFPChangeSelect())

class PFPChangeSelect(discord.ui.Select):
    """Dropdown menu for PFP change options."""

    def __init__(self):
        options = [
            discord.SelectOption(label="Change via URL", description="Provide a URL to update the PFP.", value="url"),
            discord.SelectOption(label="Enable Auto Updates", description="Automatically update PFP at set times.", value="auto"),
            discord.SelectOption(label="Disable Auto Updates", description="Stop automatic PFP updates.", value="disable")
        ]
        super().__init__(placeholder="Select an option to change the PFP...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "url":
            await interaction.response.send_message("Please provide a URL to update the PFP.", ephemeral=True)
        elif self.values[0] == "auto":
            if not auto_change_pfp.is_running():
                auto_change_pfp.start()
                await interaction.response.send_message("Automatic profile picture updates enabled.", ephemeral=True)
            else:
                await interaction.response.send_message("Automatic profile picture updates are already running.", ephemeral=True)
        elif self.values[0] == "disable":
            if auto_change_pfp.is_running():
                auto_change_pfp.cancel()
                await interaction.response.send_message("Automatic profile picture updates disabled.", ephemeral=True)
            else:
                await interaction.response.send_message("Automatic profile picture updates are not running.", ephemeral=True)

@client.tree.command(name="pfp-updater", description="Change the bot's profile picture.", guild=Guild_ID)
async def change_pfp(interaction: discord.Interaction):
    """
    Slash command to change the bot's profile picture with a dropdown menu.
    """
    view = PFPChangeView()
    await interaction.response.send_message("Select an option to change the profile picture:", view=view, ephemeral=True)




###############################################End#############################################

########Help######

about_bot_msg = f"This bot is made by with <3 by <@{Naveen_User_ID}> and <@{Aastha_User_ID}>. Please contact them via <@{Naveen_User_ID}> or <@{Aastha_User_ID}> if you have any questions." 

@client.tree.command(name="about-bot", description="List of commands", guild=Guild_ID)
async def about_bot(interaction: discord.Interaction):
    await interaction.response.send_message(about_bot_msg, ephemeral=False)




client.run(TOKEN)
