# Linked Translator

A Discord bot that automatically translates messages between multiple language channels using configurable translation groups.

## Features

* Multiple translation groups per server
* Unlimited channels per group
* Supports 100+ languages through Google Translate
* Slash-command administration
* Automatic translation between all channels in a group
* Attachment forwarding
* Low resource usage
* Works across multiple Discord servers

## Example

A server administrator can create a translation group called `diplomacy`:

```text
/creategroup name:diplomacy
```

Then add channels:

```text
/ addchannel group:diplomacy channel:#english language:en
/ addchannel group:diplomacy channel:#chinese language:zh-CN
/ addchannel group:diplomacy channel:#spanish language:es
/ addchannel group:diplomacy channel:#french language:fr
```

Messages sent in any channel will automatically be translated and forwarded to the others.

### Example Flow

English user posts:

```text
Hello everyone, we'd like to discuss a peace treaty.
```

Chinese channel receives:

```text
大家好，我们想讨论一项和平条约。
```

Spanish channel receives:

```text
Hola a todos, nos gustaría discutir un tratado de paz.
```

French channel receives:

```text
Bonjour à tous, nous aimerions discuter d'un traité de paix.
```

## Commands

### Create a Group

```text
/creategroup name:diplomacy
```

### Delete a Group

```text
/deletegroup name:diplomacy
```

### Add a Channel

```text
/addchannel group:diplomacy channel:#english language:en
```

### Remove a Channel

```text
/removechannel group:diplomacy channel:#english
```

### List Groups

```text
/listgroups
```

### List Channels in a Group

```text
/listchannels group:diplomacy
```

## Supported Languages

The bot uses Google Translate through the `deep-translator` package and supports most languages available through Google Translate.

Examples:

| Language              | Code  |
| --------------------- | ----- |
| English               | en    |
| Chinese (Simplified)  | zh-CN |
| Chinese (Traditional) | zh-TW |
| Spanish               | es    |
| French                | fr    |
| German                | de    |
| Japanese              | ja    |
| Korean                | ko    |
| Russian               | ru    |
| Portuguese            | pt    |
| Arabic                | ar    |
| Hindi                 | hi    |
| Tagalog (Filipino)    | tl    |

## Requirements

* Python 3.10+
* discord.py
* python-dotenv
* deep-translator

## Installation

Clone the repository:

```bash
git clone https://github.com/eric0486/linked_translator.git
cd linked_translator
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an environment file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN
```

Start the bot:

```bash
python bot.py
```

## Discord Developer Portal Setup

### Bot Settings

Enable:

* Public Bot
* Message Content Intent

### OAuth2 Scopes

* bot
* applications.commands

### Recommended Permissions

* View Channels
* Send Messages
* Read Message History
* Attach Files
* Embed Links

## Resource Usage

This bot was designed to run on low-resource systems.

Typical usage:

* RAM: ~50–70 MB
* CPU: Minimal under normal Discord traffic

Suitable for:

* Raspberry Pi
* Oracle Cloud Free Tier
* Small VPS instances
* Home servers

## License

MIT License
