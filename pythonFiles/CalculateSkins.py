import sqlite3
def calculate_skins(self, scores, course_id, money = 0): # scores dict key=int val=list[int]
    # returns a list of skins won, dict key=int, val=list[int]
    current_winning_id = 0
    current_lowest_score = 99
    is_a_tie = False
    counter = 0
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
            amount_of_skins_won = 1 # resets it back to 1 there were a bunch of ties before this hole    
        else:
            amount_of_skins_won += 1 # if there is a tie, then increment by 1
        
        current_lowest_score = 99
        current_winning_id = 0


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


        self.cursor.execute("INSERT into skins_score (golfer_id, money, course_id, week, hole_scores, skins_points, holes_won) VALUES (?,?,?,?,?,?,?)"(golfer_id, money_made, course_id, week, hole_scores, skins_amount, skins))
        self.conn.commit()
        scores_id.append(self.cursor.lastrowid)
    



    return points
