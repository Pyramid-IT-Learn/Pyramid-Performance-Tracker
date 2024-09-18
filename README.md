# CMRIT Leaderboard 🏆

Welcome to the **CMRIT Leaderboard** project! This application tracks and displays competitive programming performance across various platforms for students of CMRIT.

## 🚀 Features

- Scrapes data from multiple platforms: CodeChef, Codeforces, GeeksforGeeks, HackerRank, and LeetCode.
- Generates a comprehensive leaderboard in Excel and CSV formats.
- Allows real-time updates and viewing of participants’ performance.

Here’s the updated Table of Contents to match the content of your README:

## 📋 Table of Contents

- [Installation](#-installation)
- [Environment Setup](#-environment-setup)
- [Configuration Setup](#-database-configuration)
- [Usage](#-usage)
- [Viewing Leaderboards](#-viewing-leaderboards)
- [Workflows](#-workflows)
- [Credits](#-credits)

## 💻 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dog-broad/cmrit_leaderboard.git
   cd cmrit_leaderboard
   ```

2. **Create a Virtual Environment**:
   Make sure you have Python and `venv` installed:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - **On Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**:
   Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Environment Setup

To configure the application, you'll need to set several environment variables. You can create a `.env` file in the root directory or set these variables in your environment:

```plaintext
CODEFORCES_KEY=your_codeforces_api_key
CODEFORCES_SECRET=your_codeforces_api_secret
GIT_USERNAME=your_github_username
GIT_PASSWORD=your_github_password
GFG_USERNAME=your_geeksforgeeks_username
GFG_PASSWORD=your_geeksforgeeks_password
CODECHEF_CLIENT_ID=your_codechef_client_id
CODECHEF_CLIENT_SECRET=your_codechef_client_secret
DB_PASSWORD=your_mongodb_password
```

### 📊 Database Configuration

- **MongoDB Connection**:
  ```plaintext
  mongodb://myUserAdmin:<DB_PASSWORD>@103.172.179.23:27017
  ```
- **DB_NAME**: Keep it as `CMRIT` unless you need to change it for a different college.
- **USERS_COLLECTION**: Change this name for different batches; currently set to `CMRIT-2026-LEADERBOARD`.

## 📈 Usage

To manage the CMRIT Leaderboard, follow these steps:

1. **Verify Users**: This will download the CSV file specified in the config if it doesn't exist.
   ```bash
   python main.py --verify all
   ```

2. **Upload Data to Database**:
   ```bash
   python main.py --upload
   ```

3. **Scrape Data**: Collect data from all platforms.
   ```bash
   python main.py --scrape all
   ```

4. **Clear Logs and Reports** (optional):
   ```bash
   python main.py --clear
   ```

Ensure you run the verification and upload steps before scraping to keep your data updated!

This will fetch user data and generate reports in the `reports` directory.

## 🌐 Viewing Leaderboards

You can view the latest leaderboards and track participant performance at [Pyramid Leaderboards](https://dog-broad.github.io/pyramid-leaderboards/).

## 🔄 Workflows

The CMRIT Leaderboard project uses GitHub Actions to automate key tasks:

### 1. **Leaderboard Builder**
- **Trigger**: Manually.
- **Purpose**: Scrapes user data from coding platforms and builds the leaderboard report.

### 2. **Manual Scrape & Build Leaderboard**
- **Trigger**: Manually select platforms.
- **Purpose**: Scrapes data from specific platforms (CodeChef, Codeforces, etc.) or all at once.

### 3. **Manual Verify & Upload Users** 
> Needs to be performed first.
- **Trigger**: Manually select platforms.
- **Purpose**: Verifies user handles and uploads the data to the database.

### 4. **Leaderboard Builder**
- **Purpose**: To generate the leaderboard report of the current content in the database.

To trigger workflows, go to the GitHub Actions tab in your repository and select the desired workflow.

## 🙏 Credits

A massive shoutout to the incredible [gabyah92](https://www.instagram.com/gabyah92) for their brilliant vision and exceptional contributions! 🎉 Your original project laid the foundation for this leaderboard, and your dedication to the coding community inspires us all. Thank you for sharing your knowledge and creativity—this project wouldn’t be possible without you! 🌟
