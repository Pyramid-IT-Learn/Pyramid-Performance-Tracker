import pandas as pd

from cmrit_leaderboard.database import Database

def evaluate_leaderboard():
    db = Database()
    users = db.get_all_users()

    users = pd.DataFrame(users)

    users.fillna(0, inplace=True)

    print("Users loaded:", len(users))

    # Create a column for total rating
    users['TotalRating'] = users.get('codechefRating', 0) + users.get('codeforcesRating', 0) + users.get('geeksforgeeksWeeklyRating', 0) + users.get('geeksforgeeksPracticeRating', 0) + users.get('leetcodeRating', 0) + users.get('hackerrankRating', 0)

    print("TotalRating column added")

    try:
        max_codechef_rating = users.loc[users['codechefRating'].notnull(), 'codechefRating'].max()
    except KeyError:
        max_codechef_rating = 0

    print("Max codechef rating:", max_codechef_rating)

    try:
        max_codeforces_rating = users.loc[users['codeforcesRating'].notnull(), 'codeforcesRating'].max()
    except KeyError:
        max_codeforces_rating = 0

    print("Max codeforces rating:", max_codeforces_rating)

    try:
        max_geeksforgeeks_weekly_rating = users.loc[users['geeksforgeeksWeeklyRating'].notnull(), 'geeksforgeeksWeeklyRating'].max()
    except KeyError:
        max_geeksforgeeks_weekly_rating = 0

    print("Max geeksforgeeks weekly rating:", max_geeksforgeeks_weekly_rating)

    try:
        max_geeksforgeeks_practice_rating = users.loc[users['geeksforgeeksPracticeRating'].notnull(), 'geeksforgeeksPracticeRating'].max()
    except KeyError:
        max_geeksforgeeks_practice_rating = 0

    print("Max geeksforgeeks practice rating:", max_geeksforgeeks_practice_rating)

    try:
        max_leetcode_rating = users.loc[users['leetcodeRating'].notnull(), 'leetcodeRating'].max()
    except KeyError:
        max_leetcode_rating = 0

    print("Max leetcode rating:", max_leetcode_rating)

    try:
        max_hackerrank_rating = users.loc[users['hackerrankRating'].notnull(), 'hackerrankRating'].max()
    except KeyError:
        max_hackerrank_rating = 0

    print("Max hackerrank rating:", max_hackerrank_rating)

    for index, row in users.iterrows():
        cc = float(row.get('codechefRating', 0))
        cc = cc / max_codechef_rating * 100 if max_codechef_rating != 0 else 0
        cf = float(row.get('codeforcesRating', 0))
        cf = cf / max_codeforces_rating * 100 if max_codeforces_rating != 0 else 0
        ggw = float(row.get('geeksforgeeksWeeklyRating', 0))
        ggw = ggw / max_geeksforgeeks_weekly_rating * 100 if max_geeksforgeeks_weekly_rating != 0 else 0
        ggp = float(row.get('geeksforgeeksPracticeRating', 0))
        ggp = ggp / max_geeksforgeeks_practice_rating * 100 if max_geeksforgeeks_practice_rating != 0 else 0
        lc = float(row.get('leetcodeRating', 0))
        lc = lc / max_leetcode_rating * 100 if max_leetcode_rating != 0 else 0
        hr = float(row.get('hackerrankRating', 0))
        hr = hr / max_hackerrank_rating * 100 if max_hackerrank_rating != 0 else 0
        
        percentile = cc * 0.1 + cf * 0.3 + ggw * 0.3 + ggp * 0.1 + lc * 0.1 + hr * 0.1

        users.at[index, 'Percentile'] = percentile

    users.replace({' ': ''}, regex=True, inplace=True)

    print("Percentile column added")

    db.upload_to_db_with_df(users)
