# Frontend - Trivia API

## Getting Setup

> This frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. Make sure that your **backend is up and running** before running it.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
#### For all types of shell
```shell
npm install
```
---
## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode, use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.
#### For all types of shell
```shell
npm start
```
---
## Game Play Mechanics

Currently, when an user plays the game, he/she plays up to the number of questions on the chosen category. The app will display your scores (aka the result of the game) when all questions are played in the selected category and you will need to replay by clicking on the `Play Again?` button
#### Example :
- Let's say that the `Science` category has been selected
- The `Science` category has `3` questions
- After the user played all `3 questions`, the result of the game will be displayed
- If you wish to continue the game, you will need to click on replay button
---
