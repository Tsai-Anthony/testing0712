  import discord
import asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = YOUR_CHANNEL_ID_TO_SEND_MESSAGES
WEBSITE_URL = 'https://example.com/jobs'  # Example website URL for test automation job postings

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        # Ignore messages sent in the channel, if needed
        pass

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')

    await send_job_notifications()

async def send_job_notifications():
    channel = client.get_channel(CHANNEL_ID)

    while True:
        try:
            # Send a GET request to the website and retrieve the page content
            response = requests.get(WEBSITE_URL)
            page_content = response.content

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(page_content, 'html.parser')

            # Find the job listings on the page and extract relevant information
            job_listings = soup.find_all('div', class_='job-listing')
            for job_listing in job_listings:
                # Extract job information (title, company, link, etc.)
                job_title = job_listing.find('h2', class_='job-title').text.strip()
                job_company = job_listing.find('span', class_='company').text.strip()
                job_link = job_listing.find('a')['href']

                # Customize the message content and format according to your needs
                notification_message = f'New test automation job posted:\nTitle: {job_title}\nCompany: {job_company}\nLink: {job_link}'
                await channel.send(notification_message)

        except requests.exceptions.RequestException as e:
            print(f'Error occurred while fetching job data: {e}')

        await asyncio.sleep(3600)  # Sleep for 1 hour before checking for new jobs again

client.run(TOKEN)
