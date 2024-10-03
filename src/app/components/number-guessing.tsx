import React from "react";

const NumberGuessingGamePage = () => {
  return (
    <div className="number-guessing-game">
      <h1>Number Guessing Game</h1>
      <p>
        Currently, the Number Guessing Game is available as a standalone
        deployment. Please click the button below to play it.
      </p>
      <a
        href="https://number-guessing-game.vercel.app"
        target="_blank"
        rel="noopener noreferrer"
      >
        <button>Play Number Guessing Game</button>
      </a>
    </div>
  );
};

export default NumberGuessingGamePage;
