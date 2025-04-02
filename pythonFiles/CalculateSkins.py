import sqlite3
def calculate_skins(scores, course_id, money = 0): # scores dict key=int val=list[int]
    # returns a list of skins won, dict key=int, val=list[int]
    current_winning_id = 0
    current_lowest_score = 99
    is_a_tie = False
    total_skins = 0
    skins_won = {} # key is golfer_id and value is list of skins won -- 1 -> ["2,3,4"]
    points = {} #points should be a dictionary, key being golfer_id and value being amount of skins won -- 1 -> 3
    amount_of_skins_won = 1 # if there is a tie this should increment up by 1, then when someone wins, the skins should go to that person, then put this back to 1

    # start a counter at 0, and end at 17, each iteration, loop through dictionary and get the counter position in the list, 0th index is first hole score for each player
    for counter in range(18): # may want to change 18 to a variable that looks up course and checks how many holes it has
        for golfer_id, scoreline in scores.items():

            if current_lowest_score > scoreline[counter]: # if the golfers score is lower than our current lowest score then as of now there is no tie
                is_a_tie = False
                current_winning_id = golfer_id
            elif current_lowest_score == scoreline[counter]:
                is_a_tie = True
            
            if golfer_id not in skins_won:
                skins_won[golfer_id] = ""
            
            if golfer_id not in points:
                points[golfer_id] = 0

        if is_a_tie == False:
            skins_won[current_winning_id] += str(counter) + ","
            points[current_winning_id] += amount_of_skins_won
            total_skins += amount_of_skins_won
            #amount_of_skins_won = 1 # resets it back to 1 there were a bunch of ties before this hole    
        #else:
            #amount_of_skins_won += 1 # if there is a tie, then increment by 1
        
        current_lowest_score = 99
        current_winning_id = 0

    insert_data_into_db(self, skins_won, total_skins, money, scores, course_id)

    return points



# This function inputs all the data we gathered into the database
def insert_data_into_db(self, skins_won, total_skins, money, scores, course_id):
    scores_id = [] # this is for the games table, we need to put all the ids of the skins_score's inserted below into this
    month = self.calander.selectedDate().month()
    day = self.calander.selectedDate().day()
    if month < 10:
        month = f"0{self.calander.selectedDate().month()}"
    if day < 10:
        day = f"0{self.calander.selectedDate().day()}"
        
    week = f"{self.calander.selectedDate().year()}-{month}-{day}"

    # now we need to update skins_score table that has money, golfer_id, course_id, week, hole_scores, skins_points, holes_won
    for golfer_id, skins in skins_won.items():
        skins_amount = skins_won[golfer_id]
        money_made = round((skins_amount / total_skins) * money, 2)
        hole_scores = ", ".join(map(str, scores[golfer_id]))

        self.cursor.execute("INSERT into skins_score (golfer_id, money, course_id, week, hole_scores, skins_points, holes_won) VALUES (?,?,?,?,?,?,?)", (golfer_id, money_made, course_id, week, hole_scores, skins_amount, skins))
        self.conn.commit()

        scores_id.append(self.cursor.lastrowid) 
    
    score_ids_str = ",".join(str(id) for id in scores_id) # this makes the list of ids into a string of ids
    self.cursor.execute("INSERT INTO games(game_type, scores_ids) VALUES (?,?)", (1, score_ids_str,))
    self.conn.commit()

    game_id = self.cursor.lastrowid
    game_num = 1
    session_id = 0
    
    self.cursor.execute("SELECT * FROM sessions WHERE day = ?", (week,))
    results = self.cursor.fetchall()
    count = len(results)

    if (count > 0):
        session_id = results[0][1]
        game_num = count + 1
    else:
        self.cursor.execute("SELECT MAX(session_id) FROM sessions")
        result = self.cursor.fetchone()[0]  # This gets the max session_id
        session_id = (result if result is not None else 0) + 1  # Default to 1 if no entries exist

    # Insert data into sessions table
    self.cursor.execute("INSERT INTO sessions(session_id, game_num, day, game_type, game_id) VALUES (?,?,?,?,?)", (session_id, game_num, week, 1, game_id))
    self.conn.commit()

