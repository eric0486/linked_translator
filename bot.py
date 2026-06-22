import os
import json
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GROUPS_FILE = "translation_groups.json"


def load_groups():
    if not os.path.exists(GROUPS_FILE):
        return {}

    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_groups(groups):
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)


async def translate_text(text: str, target_language: str) -> str:
    if not text.strip():
        return ""

    return GoogleTranslator(source="auto", target=target_language).translate(text)


def user_can_manage_channels(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.manage_channels


def find_channel_group(groups, guild_id: str, channel_id: str):
    guild_groups = groups.get(guild_id, {})

    for group_name, channels in guild_groups.items():
        if channel_id in channels:
            return group_name, channels

    return None, None


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Translation group bot is ready.")


@bot.tree.command(
    name="creategroup",
    description="Create a translation group."
)
@app_commands.describe(
    name="Group name, example: diplomacy"
)
async def creategroup(interaction: discord.Interaction, name: str):
    if not user_can_manage_channels(interaction):
        await interaction.response.send_message(
            "You need Manage Channels permission to create translation groups.",
            ephemeral=True
        )
        return

    groups = load_groups()
    guild_id = str(interaction.guild.id)
    group_name = name.lower().strip()

    groups.setdefault(guild_id, {})

    if group_name in groups[guild_id]:
        await interaction.response.send_message(
            f"Group `{group_name}` already exists.",
            ephemeral=True
        )
        return

    groups[guild_id][group_name] = {}
    save_groups(groups)

    await interaction.response.send_message(
        f"Created translation group `{group_name}`.",
        ephemeral=True
    )


@bot.tree.command(
    name="deletegroup",
    description="Delete a translation group."
)
@app_commands.describe(
    name="Group name to delete"
)
async def deletegroup(interaction: discord.Interaction, name: str):
    if not user_can_manage_channels(interaction):
        await interaction.response.send_message(
            "You need Manage Channels permission to delete translation groups.",
            ephemeral=True
        )
        return

    groups = load_groups()
    guild_id = str(interaction.guild.id)
    group_name = name.lower().strip()

    if guild_id not in groups or group_name not in groups[guild_id]:
        await interaction.response.send_message(
            f"Group `{group_name}` does not exist.",
            ephemeral=True
        )
        return

    del groups[guild_id][group_name]
    save_groups(groups)

    await interaction.response.send_message(
        f"Deleted translation group `{group_name}`.",
        ephemeral=True
    )


@bot.tree.command(
    name="addchannel",
    description="Add a channel to a translation group."
)
@app_commands.describe(
    group="Translation group name",
    channel="Channel to add",
    language="Target language for this channel, example: en, zh-CN, es, fr"
)
async def addchannel(
    interaction: discord.Interaction,
    group: str,
    channel: discord.TextChannel,
    language: str
):
    if not user_can_manage_channels(interaction):
        await interaction.response.send_message(
            "You need Manage Channels permission to add channels.",
            ephemeral=True
        )
        return

    groups = load_groups()
    guild_id = str(interaction.guild.id)
    group_name = group.lower().strip()
    channel_id = str(channel.id)
    lang = language.strip()

    groups.setdefault(guild_id, {})
    groups[guild_id].setdefault(group_name, {})

    groups[guild_id][group_name][channel_id] = lang
    save_groups(groups)

    await interaction.response.send_message(
        f"Added {channel.mention} to `{group_name}` with language `{lang}`.",
        ephemeral=True
    )


@bot.tree.command(
    name="removechannel",
    description="Remove a channel from a translation group."
)
@app_commands.describe(
    group="Translation group name",
    channel="Channel to remove"
)
async def removechannel(
    interaction: discord.Interaction,
    group: str,
    channel: discord.TextChannel
):
    if not user_can_manage_channels(interaction):
        await interaction.response.send_message(
            "You need Manage Channels permission to remove channels.",
            ephemeral=True
        )
        return

    groups = load_groups()
    guild_id = str(interaction.guild.id)
    group_name = group.lower().strip()
    channel_id = str(channel.id)

    if (
        guild_id not in groups
        or group_name not in groups[guild_id]
        or channel_id not in groups[guild_id][group_name]
    ):
        await interaction.response.send_message(
            f"{channel.mention} is not in group `{group_name}`.",
            ephemeral=True
        )
        return

    del groups[guild_id][group_name][channel_id]
    save_groups(groups)

    await interaction.response.send_message(
        f"Removed {channel.mention} from `{group_name}`.",
        ephemeral=True
    )


@bot.tree.command(
    name="listgroups",
    description="List translation groups in this server."
)
async def listgroups(interaction: discord.Interaction):
    groups = load_groups()
    guild_id = str(interaction.guild.id)

    if guild_id not in groups or not groups[guild_id]:
        await interaction.response.send_message(
            "No translation groups are configured.",
            ephemeral=True
        )
        return

    lines = []

    for group_name, channels in groups[guild_id].items():
        lines.append(f"`{group_name}` — {len(channels)} channel(s)")

    await interaction.response.send_message(
        "\n".join(lines),
        ephemeral=True
    )


@bot.tree.command(
    name="listchannels",
    description="List channels in a translation group."
)
@app_commands.describe(
    group="Translation group name"
)
async def listchannels(interaction: discord.Interaction, group: str):
    groups = load_groups()
    guild_id = str(interaction.guild.id)
    group_name = group.lower().strip()

    if guild_id not in groups or group_name not in groups[guild_id]:
        await interaction.response.send_message(
            f"Group `{group_name}` does not exist.",
            ephemeral=True
        )
        return

    channels = groups[guild_id][group_name]

    if not channels:
        await interaction.response.send_message(
            f"Group `{group_name}` has no channels.",
            ephemeral=True
        )
        return

    lines = []

    for channel_id, language in channels.items():
        channel = interaction.guild.get_channel(int(channel_id))

        if channel:
            lines.append(f"{channel.mention} → `{language}`")
        else:
            lines.append(f"Unknown channel `{channel_id}` → `{language}`")

    await interaction.response.send_message(
        "\n".join(lines),
        ephemeral=True
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    if not message.content and not message.attachments:
        return

    groups = load_groups()
    guild_id = str(message.guild.id)
    source_channel_id = str(message.channel.id)

    group_name, channels = find_channel_group(groups, guild_id, source_channel_id)

    if not group_name or not channels:
        return

    for target_channel_id, target_language in channels.items():
        if target_channel_id == source_channel_id:
            continue

        target_channel = message.guild.get_channel(int(target_channel_id))

        if target_channel is None:
            print(f"Could not find target channel ID: {target_channel_id}")
            continue

        translated = ""

        if message.content:
            try:
                translated = await translate_text(message.content, target_language)
            except Exception as e:
                print(f"Translation failed for {target_language}: {e}")
                translated = "[Translation failed]"

        files = []

        for attachment in message.attachments:
            try:
                files.append(await attachment.to_file())
            except Exception as e:
                print(f"Attachment failed: {attachment.filename} - {e}")

        if translated:
            outgoing_message = f"**{message.author.display_name}:** {translated}"
        elif files:
            outgoing_message = f"**{message.author.display_name}:**"
        else:
            continue

        try:
            await target_channel.send(content=outgoing_message, files=files)
        except Exception as e:
            print(f"Sending message failed to {target_channel.name}: {e}")


bot.run(TOKEN)
