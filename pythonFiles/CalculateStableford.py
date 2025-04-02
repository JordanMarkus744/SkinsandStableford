import sqlite3

def calculate_stableford(db_conn, scores, course_id):
    stableford_points = 0
    cursor = db_conn.cursor()

    # Fetch hole information from the database
    cursor.execute("SELECT hole_number, par, handicap_rating FROM holes WHERE course_id = ?", (course_id,))
    holes = cursor.fetchall()
    
    # Create a dictionary of hole info
    hole_handicaps = {row[0]: (row[1], row[2]) for row in holes}  # hole_number: (par, handicap_rating)

    for i, score in enumerate(scores, start=1):
        if i not in hole_handicaps:
            continue  # Skip holes that are not found in the database

        par, hole_handicap = hole_handicaps[i]
        
        if par is not None:  # Ensure par is valid
            adjusted_score = score
            if adjusted_score <= par - 3:  # Albatross
                stableford_points += 10
            elif adjusted_score == par - 2:  # Eagle
                stableford_points += 6
            elif adjusted_score == par - 1:  # Birdie
                stableford_points += 4
            elif adjusted_score == par:  # Par
                stableford_points += 2
            elif adjusted_score == par + 1:  # Bogey
                stableford_points += 1
            else:  # Double bogey or worse (optional, but explicit)
                stableford_points += 0  # No points

    return stableford_points
