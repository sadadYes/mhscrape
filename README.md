# MHScrape

Discord bot for scraping publicly available student information in Indonesia.


## Running Locally (Linux)

Clone the project

```bash
  git clone https://github.com/sadadYes/mhscrape.git
```

Go to the project directory

```bash
  cd mhscrape
```

Install dependencies

```bash
  pip install discord.py requests python-dotenv
```

Replacing the discord token
```bash
  cp example.env .env && sed -i 's/DISCORD_TOKEN=/DISCORD_TOKEN=your_discord_token_here/' .env

```

Running the bot

```bash
  python3 main.py
```


## Appendix

This project is only made possible because of the information provided by my good friend 'paran'.
