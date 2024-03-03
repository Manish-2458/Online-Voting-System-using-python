# Voting System 🗳️

## Description
This Python project implements a voting system with two interfaces:
1. Candidate registration interface for the election commissioner.
2. Login page for users/voters to select their candidate for two positions: MLA and MP.

## Features
- **Election Commissioner Interface**: Allows the election commissioner to register candidates for the election.
- **User/Voter Interface**: Allows users/voters to log in and cast their votes for MLA and MP positions.
- **Admin Password Protection**: Certain modules require the admin password to proceed, ensuring security and control.
- **Visualization of Results**: Utilizes Matplotlib to visualize the election results at the end.

## Dependencies
- Python 3.x
- PIL (Python Imaging Library)
- tkinter
- openpyxl
- shutil

## Installation
1. Clone or download this repository.
2. Ensure you have Python installed on your system.
3. Install dependencies using pip:

  Example:
  
  In terminal:pip install shutil
  
  For collab or kaggle notebooks:!pip install shutil

## Usage
1. Run the `voting_system.py` file.
2. Follow the prompts:
- If you're the election commissioner, register candidates with the admin password.
- If you're a user/voter, log in and cast your votes.
3. At the end of the voting period, the results will be displayed using Matplotlib.

## Files
- `voting_system.py`: Main Python script containing the implementation of the voting system.
- `candidates.csv`: CSV file storing the registered candidates.
- `users.csv`: CSV file storing the registered users/voters.

## Structure
- **Admin Module**:
- Register candidates with password protection.
- **User Module**:
- Log in.
- Cast votes for MLA and MP.
- **Results Module**:
- Visualize election results.

## Contributing
Contributions are welcome! Please feel free to fork this repository and submit pull requests to suggest improvements.

## License
This project is licensed under the [GNU GENERAL PUBLIC LICENSE 3.0](LICENSE).

![Vote Symbol](https://th.bing.com/th/id/R.497a04924609f9334839a7056dc87738?rik=UO94nCCwnf4Hxg&riu=http%3a%2f%2fpluspng.com%2fimg-png%2fvote-png-hd-free-voting-box-png-clipart-1024.png&ehk=nGNj%2ferSxyvUU0nT5i%2bRzF438Xl%2bRv9iB%2bCB4kgRwBg%3d&risl=&pid=ImgRaw)
