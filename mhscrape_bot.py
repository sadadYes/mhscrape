import discord
from discord import app_commands
import requests

TOKEN = ''

class StudentInfoBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        await self.tree.sync()

client = StudentInfoBot()

@client.tree.command(name="search", description="Mencari informasi tentang mahasiswa")
@app_commands.describe(query="Nama mahsaiswa")
async def search(interaction: discord.Interaction, query: str):
    query = query.replace(' ', '%20')
    search_url = f"https://pddikti.kemdikbud.go.id/api/pencarian/mhs/{query}"
    response = requests.get(search_url)
    data = response.json()

    if data and 'id' in data[0]:
        student_id = data[0]['id']
        detail_url = f"https://pddikti.kemdikbud.go.id/api/detail/mhs/{student_id}"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()

        # Extract required fields
        nama = detail_data.get('nama', 'N/A')
        jenis_kelamin = detail_data.get('jenis_kelamin', 'N/A')
        nama_pt = detail_data.get('nama_pt', 'N/A')
        tahun_masuk = detail_data.get('tahun_masuk', 'N/A')
        jenjang = detail_data.get('jenjang', 'N/A')
        prodi = detail_data.get('prodi', 'N/A')
        nim = detail_data.get('nim', 'N/A')
        jenis_daftar = detail_data.get('jenis_daftar', 'N/A')
        status_saat_ini = detail_data.get('status_saat_ini', 'N/A')

        # Create the embed message
        embed = discord.Embed(title="Informasi Mahasiswa", color=discord.Color.blue())
        embed.add_field(name="Nama Mahasiswa", value=nama, inline=False)
        embed.add_field(name="Jenis Kelamin", value=jenis_kelamin, inline=False)
        embed.add_field(name="Perguruan Tinggi", value=nama_pt, inline=False)
        embed.add_field(name="Tahun Masuk", value=tahun_masuk, inline=False)
        embed.add_field(name="Jenjang - Program Studi", value=f"{jenjang} - {prodi}", inline=False)
        embed.add_field(name="Nomor Induk Mahasiswa", value=nim, inline=False)
        embed.add_field(name="Status Awal Mahasiswa", value=jenis_daftar, inline=False)
        embed.add_field(name="Status Akhir Mahasiswa", value=status_saat_ini, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No student data found or 'id' not present.", ephemeral=True)

client.run(TOKEN)
