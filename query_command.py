import discord
from discord import app_commands
import requests

# A class to handle button interactions and pagination
class StudentSelectView(discord.ui.View):
    def __init__(self, students, current_page, total_pages):
        super().__init__(timeout=None)
        self.students = students
        self.current_page = current_page
        self.total_pages = total_pages

        for i in range(10):
            if i + (current_page * 10) < len(students):
                student = students[i + (current_page * 10)]
                self.add_item(StudentButton(student, i + 1))

        if current_page > 0:
            self.add_item(PreviousPageButton())
        if current_page < total_pages - 1:
            self.add_item(NextPageButton())

    async def update_page(self, interaction, new_page):
        self.clear_items()

        self.current_page = new_page
        for i in range(10):
            if i + (new_page * 10) < len(self.students):
                student = self.students[i + (new_page * 10)]
                self.add_item(StudentButton(student, i + 1))

        if new_page > 0:
            self.add_item(PreviousPageButton())
        if new_page < self.total_pages - 1:
            self.add_item(NextPageButton())

        embed = discord.Embed(title="Select a Student", color=discord.Color.blue())
        start_idx = new_page * 10
        for i, student in enumerate(self.students[start_idx:start_idx + 10]):
            embed.add_field(
                name=f"{i + 1}. {student['nama']}",
                value=f"PT: {student['nama_pt']} | Prodi: {student['nama_prodi']}",
                inline=False
            )
        embed.set_footer(text=f"Page {new_page + 1} of {self.total_pages}")
        await interaction.response.edit_message(embed=embed, view=self)

# Button to select a student and view their details
class StudentButton(discord.ui.Button):
    def __init__(self, student, index):
        super().__init__(label=str(index), style=discord.ButtonStyle.primary)
        self.student = student

    async def callback(self, interaction: discord.Interaction):
        student_id = self.student['id']
        detail_url = f"https://pddikti.kemdikbud.go.id/api/detail/mhs/{student_id}"
        headers = {"x-api-key": "3ed297db-db1c-4266-8bf4-a89f21c01317"}
        detail_response = requests.get(detail_url, headers=headers)
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
        embed = discord.Embed(title="Informasi Mahasiswa", color=discord.Color.green())
        embed.add_field(name="Nama Mahasiswa", value=nama, inline=False)
        embed.add_field(name="Jenis Kelamin", value=jenis_kelamin, inline=False)
        embed.add_field(name="Perguruan Tinggi", value=nama_pt, inline=False)
        embed.add_field(name="Tahun Masuk", value=tahun_masuk, inline=False)
        embed.add_field(name="Jenjang - Program Studi", value=f"{jenjang} - {prodi}", inline=False)
        embed.add_field(name="Nomor Induk Mahasiswa", value=nim, inline=False)
        embed.add_field(name="Status Awal Mahasiswa", value=jenis_daftar, inline=False)
        embed.add_field(name="Status Akhir Mahasiswa", value=status_saat_ini, inline=False)

        await interaction.response.edit_message(embed=embed, view=None)

# Button to go to the previous page
class PreviousPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Previous", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        current_page = view.current_page
        if current_page > 0:
            new_page = current_page - 1
            await view.update_page(interaction, new_page)

# Button to go to the next page
class NextPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Next", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        current_page = view.current_page
        if current_page < view.total_pages - 1:
            new_page = current_page + 1
            await view.update_page(interaction, new_page)

# Main query command
def setup_query(client):
    @client.tree.command(name="query", description="Mencari mahasiswa di daftar dan melihat detail mahasiswa yang dipilih")
    @app_commands.describe(nama="Nama mahasiswa")
    async def query(interaction: discord.Interaction, name: str):
        name = name.replace(' ', '%20')
        search_url = f"https://pddikti.kemdikbud.go.id/api/pencarian/mhs/{name}"
        headers = {"x-api-key": "3ed297db-db1c-4266-8bf4-a89f21c01317"}
        response = requests.get(search_url, headers=headers)
        data = response.json()

        if data:
            total_pages = (len(data) + 9) // 10
            current_page = 0
            view = StudentSelectView(data, current_page, total_pages)

            embed = discord.Embed(title="Select a Student", color=discord.Color.blue())
            for i, student in enumerate(data[:10]):
                embed.add_field(
                    name=f"{i+1}. {student['nama']}",
                    value=f"PT: {student['nama_pt']} | Prodi: {student['nama_prodi']}",
                    inline=False
                )
            embed.set_footer(text=f"Page 1 of {total_pages}")

            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("Data mahasiswa tidak dapat ditemukan.", ephemeral=True)

