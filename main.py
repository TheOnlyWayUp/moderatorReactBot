# A bot that'll awaurd users a role if a moderator reacts to their message based on the settings in config.yaml
import discord, yaml
from discord.ext import commands
from rich import console, print

with open("config.yaml", "r") as handler:
    config = yaml.load(handler, Loader=yaml.FullLoader)
    print(config)

# Empty config =
# {
#     'general': {'token': None, 'onlyOneChannel': [True, {'channelId': None}], 'emoji': None},
#     'roles': {'moderatorRoleId': None, 'verifiedRoleId': None}
# }
# general
# - token = Bot Token
# - onlyOneChannel = [Boolean Value, {'channelId': Channel ID to check if messages were sent in}]
# - emoji - The emoji a moderator must react with
# roles
# - moderatorRoleId = Role ID of the moderator role
# - verifiedRoleId = Role ID of the verified role

if config["general"]["token"] is None:
    print(
        "[red]No token found![/red][yellow] Please add a token to config.yaml[/yellow]."
    )
    exit()
if config["general"]["token"] is None:
    print(
        '[yellow]No prefix configured, using default prefix of[/yellow][cyan] "!"[/cyan].'
    )
    config["general"]["prefix"] = "!"
if config["general"]["onlyOneChannel"][0]:
    if config["general"]["onlyOneChannel"][1] is None:
        print(
            "[red]No channel configured for onlyOneChannel![/red][yellow] Please add a channel to config.yaml[/yellow]."
        )
        exit()
if config["general"]["emoji"] is None:
    print(
        "[red]No emoji configured![/red][yellow] Please add an emoji to config.yaml[/yellow]."
    )
    exit()
if config["roles"]["moderatorRoleId"] is None:
    print(
        "[red]No moderator role configured![/red][yellow] Please add a role ID to config.yaml[/yellow]."
    )
    exit()
if config["roles"]["verifiedRoleId"] is None:
    print(
        "[red]No verified role configured![/red][yellow] Please add a role ID to config.yaml[/yellow]."
    )
    exit()

bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description="Bot made by TheOnlyWayUp#1231 for www.reddit.com/r/Discord_Bots/comments/sc34l8/need_verification_bot/",
    intents=discord.Intents.all(),
)
console = console.Console()


@bot.event
async def on_ready():
    console.log(
        f"Connected to Discord Socket as {bot.user} (ID: {bot.user.id}) and in {len(bot.guilds)} guilds.\n\nGuilds - \n- "
        + "\n- ".join(
            [
                f"{guild.name} ({guild.id}) - {guild.member_count} Members"
                for guild in bot.guilds
            ]
        )
        + "\n---\n"
    )
    print(
        f"Connected as {bot.user} and in {len(bot.guilds)} {'guild' if len(bot.guilds) == 1 else 'guilds'}."
    )


@bot.event
async def on_raw_reaction_add(payload):
    console.log(
        f"{payload.emoji} was added to {payload.message_id} by {payload.user_id} in {payload.channel_id}."
    )
    # check if the message channel is the same as the onlyOneChannel
    if config["general"]["onlyOneChannel"][0]:
        console.log(f"{payload.message_id} - Only one channel is enabled.")

        if payload.channel_id == config["general"]["onlyOneChannel"][1]["channelId"]:
            console.log(f"{payload.message_id} - Reaction is in onlyOneChannel.")

            # Check if the person adding the reaction has the moderator role
            if config["roles"]["moderatorRoleId"] in [
                role.id for role in payload.member.roles
            ]:
                console.log(f"{payload.message_id} - Reaction is from a moderator.")
                if str(payload.emoji) == str(config["general"]["emoji"]):
                    console.log(f"{payload.message_id} - Reaction is correct.")
                    channel = await bot.fetch_channel(
                        config["general"]["onlyOneChannel"][1]["channelId"]
                    )
                    msg = await channel.fetch_message(payload.message_id)
                    await msg.author.add_roles(
                        msg.guild.get_role(config["roles"]["verifiedRoleId"]),
                        reason=f"Verified by {bot.get_user(payload.user_id).name}.",
                    )
                    console.log(f"{payload.message_id} - Added role to user.")


bot.run(config["general"]["token"])
