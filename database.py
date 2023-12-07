def highscore(playername, score, coins):
    # Load the existing high scores from the file
    try:
        with open('hscore.txt', 'r') as f:
            d = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        d = {}  # Initialize a new dictionary if file doesn't exist or is empty

    # Update the dictionary with the new score, coins, and additional value
    if playername in d:
        # If the player already exists, update their score, coins, and additional value
        existing_score_coins, existing_numbers, existing_additional_value = d[playername]
        existing_score, existing_coins = existing_score_coins
        updated_score_coins = (max(score, existing_score), existing_coins + coins)
        # Update the player's data, keeping the existing additional value
        d[playername] = (updated_score_coins, existing_numbers, existing_additional_value)
    else:
        # If the player is new, add them to the dictionary with the additional value initialized to 1
        d[playername] = ((score, coins), (1,), 1)  # Additional value starts as 1

    # Write the updated dictionary back to the file
    with open('hscore.txt', 'w') as f:
        f.write(repr(d))

def read_highscores():
    try:
        with open('hscore.txt', 'r') as f:
            return eval(f.read())
    except (FileNotFoundError, SyntaxError):
        return {}

print(read_highscores())

