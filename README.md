<!-- PROJECT SHIELDS -->
[![Contributors](https://img.shields.io/github/contributors/raquel-amaral18/GroupT_Computation3)](https://github.com/raquel-amaral18/GroupT_Computation3/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/raquel-amaral18/GroupT_Computation3)](https://github.com/raquel-amaral18/GroupT_Computation3/issues)
[![MIT License](https://img.shields.io/github/license/raquel-amaral18/GroupT_Computation3)](https://github.com/raquel-amaral18/GroupT_Computation3/blob/main/LICENSE)

<!-- ABOUT THE PROJECT -->
## Rush Hour: The Race
<br />
<div>
    <img src="Images/interface.png" alt="Photo" width="80">

> Rush Hour: The Race is a fun and easy-to-play 2D car racing game. Your goal is to achieve the longest ride possible without colliding with incoming cars. During your drive, collect coins to increase your score or collide with different power-ups to receive a temporary advantage. Are you ready? Buckle up, step on the gas, and see how far you can go!
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Rush Hour: The Race">Rush Hour: The Race</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#How to Play">How to Play</a></li>
    <li><a href="#Open Issues">Open Issues</a></li>
    <li><a href="#Game Designers">Game Designers</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you can get a local copy of the game and run it on your computer

### Prerequisites
Before you begin, make sure you have the following:

- Python (version 3.6 or later)


### Installation

Please note that these instructions are tailored for Windows users. If you are using a different operating system, you may need to adapt the steps accordingly.

1. **Install Anaconda:**
   - Download and install Anaconda from the [Anaconda website](https://www.anaconda.com/products/distribution).

2. **Clone the Repository:**
   - Open Anaconda Prompt.
   - Navigate to the directory where you want to clone the repository using the `cd` command.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/raquel-amaral18/GroupT_Computation3.git
     ```

3. **Navigate to the Cloned Repository:**
   - Change to the directory of the cloned repository:
     ```bash
     cd GroupT_Computation3
     ```

4. **Create and Activate Virtual Environment:**
   - Create a new virtual environment (replace `your_environment_name` with your desired name):
     ```bash
     conda create --name your_environment_name python=3.8
     ```
   - Activate the virtual environment:
     ```bash
     conda activate your_environment_name
     ```

5. **Install Dependencies:**
   - Install Pygame:
     ```bash
     pip install pygame
     ```

6. **Run the Game:**
   - Execute the game using the following command:
     ```bash
     python main.py
     ```


<!-- USAGE EXAMPLES -->
## How to Play

#### Singleplayer mode:
- Use arrow keys keys to move your car in the desired direction.
- Other cars will be coming towards you from the opposite direction. To survive, you have to avoid colliding with them.
- Aside from cars, you might come across **coins** or **power-ups** as well. The more coins you collect, the higher your score will be. Collecting power-ups will grant you a **temporary** advantage.
- Only **1** power-up can be active at a time, so choose wisely.

#### Multiplayer mode:
In this mode, players have two exciting options to choose from:
1. **Single Road:**
   - **Player 1:** Use arrow keys to control your car. 
   - **Player 2:** Use 'WASD' keys to navigate your car.
   - Race against each other on a single highway, avoiding collisions and competing for survival.
   - Collect 10 coins and earn yourself an extra life.
   - Remember, **you can't overlap**, so strategic maneuvering is key.
   - No power-ups are available in this mode, making it a pure test of skill.

2. **Double Road:**
   - **Player 1:** Use arrow keys for your right highway.
   - **Player 2:** Use 'WASD' keys for your left highway.
   - Engage in a thrilling race where the goal is to outlast your opponent. In case one of the players crash, the other will be able to continue playing. The main goal will be to **survive longer** than the other player.
   - Two separate highways present different obstacles and opportunities for each player.
   - Use power-ups strategically, keeping in mind that only one power-up can be active at a time.
   - Each player starts with 3 lives, and the one who survives the longest emerges victorious.

  Invite a friend to play with you, and let the race begin! Will you be the ultimate champion of the roads?


<!--OPEN ISSUES -->
## Open Issues

These are areas where improvements or additional features could be considered. While they may not be critical for the fundamental functionality of the game, addressing these items could enhance the overall user experience and contribute to the project's growth:

- [x] Example 1
- [x] Example 2
- [x] Example 3
- [ ] Example 4
- [ ] Example 5


<!-- CONTRIBUTING -->
## Game Designers
This game was created as part of the course requirements for Computation III during the October semester 2023-2024. The project represents the collaborative effort of the following contributors:

- **Guilherme Marques**
  - *Student Number:* 20221780

- **Rafael Ribeiro**
  - *Student Number:* 20221853

- **Raquel Amaral**
  - *Student Number:* 20221844


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

