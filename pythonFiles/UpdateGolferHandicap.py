import sqlite3
def update_handicap(self, golfer_id, stableford_points):
    self.cursor.execute("SELECT handicap FROM golfers WHERE id = ?", (golfer_id,))
    handicap = self.cursor.fetchone()

    difference = stableford_points - handicap
    if difference >= 3:
        movement = difference // 3
        handicap += movement
    else:
        if difference <= -3:
            handicap -= 1
    
    self.cursor.execute("UPDATE golfers SET handicap = ? WHERE id = ?", (handicap, golfer_id,))
    self.conn.commit()