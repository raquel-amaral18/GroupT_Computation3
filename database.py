def highscore(playername, score, coins):
    """
        This function updates the high score file with the latest score and coins for a given player.

        Parameters
        ---------
            playername : str
                the name of the player
            score : int
                score the player got in the game
            coins : int
                coins that the player got in the game
    """
    # Load the existing high scores from the file
    try:
        with open('hscore.txt', 'r') as f:
            dict = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        dict = {}  # Initialize a new dictionary if file doesn't exist or is empty

    # Update the dictionary with the new score, coins, inventory cars, and selected car
    if playername in dict:
        # If the player already exists, update their score, coins, inventory cars, and selected car
        existing_score_coins, existing_cars, existing_selected_car = dict[playername]
        existing_score, existing_coins = existing_score_coins
        updated_score_coins = (max(score, existing_score), existing_coins + coins)

        # Username : (Highscore, coins), ( owned cars), current car
        dict[playername] = (updated_score_coins, existing_cars, existing_selected_car)
    else:
        # If the player is new, add them to the dictionary with car 0 selected automatically
        dict[playername] = ((score, coins), (0,), 0)

    # Write the updated dictionary back to the file
    with open('hscore.txt', 'w') as f:
        f.write(repr(dict))


def read_highscores():
    """
        This function will open the file, read the highscore from all the players and return it.

        Return:
        ------
            dict:
                a dictionary containing player names as keys and their corresponding high scores.
                If the file is not found or a syntax error occurs it returns an empty dictionary.

    """
    try:
        with open('hscore.txt', 'r') as f:
            return eval(f.read())
    except (FileNotFoundError, SyntaxError):
        return {}


print(read_highscores())
