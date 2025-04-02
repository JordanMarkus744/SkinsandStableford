import sqlite3

def calculate_skins(scores, course_id, money=0, conn=None, cursor=None, calendar=None):
    current_winning_id = None
    current_lowest_score = float('inf')
    is_a_tie = False
    total_skins = 0
    skins_won = {}  # golfer_id -> list of holes won
    points = {}  # golfer_id -> number of skins won
    amount_of_skins_won = 1  # Skins accumulate if there's a tie

    for counter in range(18):  # Consider making this dynamic based on course
        current_winning_id = None
        current_lowest_score = float('inf')
        is_a_tie = False

        for golfer_id, scoreline in scores.items():
            if golfer_id not in skins_won:
                skins_won[golfer_id] = []
            if golfer_id not in points:
                points[golfer_id] = 0

            if scoreline[counter] < current_lowest_score:
                current_lowest_score = scoreline[counter]
                current_winning_id = golfer_id
                is_a_tie = False  # Reset tie if new lowest score is found
            elif scoreline[counter] == current_lowest_score:
                is_a_tie = True  # Tie detected

        if not is_a_tie and current_winning_id is not None:
            skins_won[current_winning_id].append(counter)
            points[current_winning_id] += amount_of_skins_won
            total_skins += amount_of_skins_won
            amount_of_skins_won = 1  # Reset skins count
        else:
            amount_of_skins_won += 1  # Carry over skins if tied

    if conn and cursor and calendar:
        insert_data_into_db(conn, cursor, calendar, skins_won, total_skins, money, scores, course_id)

    return points


def insert_data_into_db(conn, cursor, calendar, skins_won, total_skins, money, scores, course_id):
    scores_id = []
    selected_date = calendar.selectedDate()
    
    month = f"{selected_date.month():02d}"
    day = f"{selected_date.day():02d}"
    week = f"{selected_date.year()}-{month}-{day}"

    for golfer_id, holes in skins_won.items():
        skins_amount = len(holes)  # Now an integer, not a string
        money_made = round((skins_amount / total_skins) * money, 2) if total_skins > 0 else 0
        hole_scores = ", ".join(map(str, scores[golfer_id]))

        cursor.execute("""
            INSERT INTO skins_score (golfer_id, money, course_id, week, hole_scores, skins_points, holes_won)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (golfer_id, money_made, course_id, week, hole_scores, skins_amount, ",".join(map(str, holes))))
        conn.commit()

        scores_id.append(cursor.lastrowid)

    score_ids_str = ",".join(str(id) for id in scores_id)
    cursor.execute("INSERT INTO games (game_type, scores_ids) VALUES (?, ?)", (1, score_ids_str))
    conn.commit()

    game_id = cursor.lastrowid
    game_num = 1
    session_id = 0

    cursor.execute("SELECT * FROM sessions WHERE day = ?", (week,))
    results = cursor.fetchall()
    count = len(results)

    if count > 0:
        session_id = results[0][1]
        game_num = count + 1
    else:
        cursor.execute("SELECT MAX(session_id) FROM sessions")
        result = cursor.fetchone()[0]
        session_id = (result if result is not None else 0) + 1

    cursor.execute("""
        INSERT INTO sessions (session_id, game_num, day, game_type, game_id)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, game_num, week, 1, game_id))
    conn.commit()
