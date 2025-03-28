import sqlite3
# this takes the scores from one player and returns points
def calculate_stableford(self, scores, course_id):
    stableford_points = 0
    self.cursor.execute("SELECT hole_number, par, handicap_rating FROM holes WHERE course_id = ?", (course_id,))
    holes = self.cursor.fetchall()
    hole_handicaps = {row[0]: (row[1], row[2]) for row in holes} # hold_number: (par, handicap_rating)

    for i, score in enumerate(scores, start=1):
        par, hole_handicap = hole_handicaps.get(i, (None, None))
        if par is not None:
            adjusted_score = score
            if adjusted_score <= par - 3: # albatross
                stableford_points += 10
            elif adjusted_score == par - 2: # eagle
                stableford_points += 6
            elif adjusted_score == par - 1: # birdie
                stableford_points += 4
            elif adjusted_score == par: # par
                stableford_points += 2
            elif adjusted_score == par + 1: # bogey
                stableford_points += 1
    return stableford_points