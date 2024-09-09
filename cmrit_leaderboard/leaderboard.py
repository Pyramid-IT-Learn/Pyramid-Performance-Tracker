import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from cmrit_leaderboard.config import LEADERBOARD_REPORT_FILE
from cmrit_leaderboard.database import Database

class Leaderboard:
    def __init__(self):
        self.db = Database()

    def build_leaderboard(self):
        # Fetch all users
        users = self.db.get_all_users()
        data = []

        for user in users:
            data.append({
                'Hall Ticket No': user['hallTicketNo'],  # A
                'CodeChef Username': user.get('codechefUsername'),  # B
                'CodeChef Rating': user.get('codechefRating'),  # C
                'Codeforces Username': user.get('codeforcesUsername'),  # D
                'Codeforces Rating': user.get('codeforcesRating'),  # E
                'GeeksforGeeks Username': user.get('geeksforgeeksUsername'),    # F
                'GeeksforGeeks Weekly Rating': user.get('geeksforgeeksWeeklyRating'),    # G
                'GeeksforGeeks Practice Rating': user.get('geeksforgeeksPracticeRating'),    # H
                'Leetcode Username': user.get('leetcodeUsername'),    # I
                'Leetcode Rating': user.get('leetcodeRating'),    # J
                'Hackerrank Username': user.get('hackerrankUsername'),    # K
                'Hackerrank Rating': user.get('hackerrankRating'),    # L
                'Codechef Status': user.get('codechefStatus'),    # M
                'Codeforces Status': user.get('codeforcesStatus'),    # N
                'GeeksforGeeks Status': user.get('geeksforgeeksStatus'),    # O
                'Leetcode Status': user.get('leetcodeStatus'),    # P
                'Hackerrank Status': user.get('hackerrankStatus'),    # Q
                'Total Rating': user.get('TotalRating'),    # R
                'Percentile': user.get('Percentile'),    # S
            })

        df = pd.DataFrame(data)

        df = df.sort_values(by='Percentile', ascending=False)

        writer = pd.ExcelWriter(LEADERBOARD_REPORT_FILE, engine='openpyxl')
        df.to_excel(writer, index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Define styles
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        bad_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
        border = Border(left=Side(style='thin', color='D3D3D3'), right=Side(style='thin', color='D3D3D3'), top=Side(style='thin', color='D3D3D3'), bottom=Side(style='thin', color='D3D3D3'))
        # Apply styles to header
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
            cell.border = border

        # Apply column widths
        column_widths = []
        for row in data:
            for i, cell in enumerate(row):
                cell_length = len(str(cell)) if cell else 0
                if len(column_widths) > i:
                    if cell_length > column_widths[i]:
                        column_widths[i] = cell_length
                else:
                    column_widths.append(cell_length)
        
        for i, column_width in enumerate(column_widths, 1):
            worksheet.column_dimensions[get_column_letter(i)].width = column_width + 2

        # Apply conditional formatting (Bad style)
        for row in worksheet.iter_rows(min_row=2):  # Skip header row
            # Check statuses
            if row[12].value == False:  # Codechef Status column (M)
                for cell in row[1:3]:  # CodeChef Username (B) and Rating (C)
                    cell.fill = bad_fill
                    cell.border = border
                    cell.font = Font(color="9C0006")

            if row[13].value == False:  # Codeforces Status column (N)
                for cell in row[3:5]:  # Codeforces Username (D) and Rating (E)
                    cell.fill = bad_fill
                    cell.border = border
                    cell.font = Font(color="9C0006")

            if row[14].value == False:  # GeeksforGeeks Status column (O)
                for cell in row[5:8]:  # GeeksforGeeks Username (F), Weekly Rating (G), Practice Rating (H)
                    cell.fill = bad_fill
                    cell.border = border
                    cell.font = Font(color="9C0006")

            if row[15].value == False:  # Leetcode Status column (P)
                for cell in row[8:10]:  # Leetcode Username (I) and Rating (J)
                    cell.fill = bad_fill
                    cell.border = border
                    cell.font = Font(color="9C0006")

            if row[16].value == False:  # Hackerrank Status column (Q)
                for cell in row[10:12]:  # Hackerrank Username (K) and Rating (L)
                    cell.fill = bad_fill
                    cell.border = border
                    cell.font = Font(color="9C0006")

        # Hide Status columns
        for i in range(13, 18):
            worksheet.column_dimensions[get_column_letter(i)].hidden = True

        writer._save()

    def get_users(self):
        return self.db.get_all_users()
