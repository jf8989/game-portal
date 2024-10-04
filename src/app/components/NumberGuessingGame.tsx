//src/app/components/NumberGuessingGame.tsx
import React from "react";
import Link from "next/link";

const NumberGuessingGame = () => {
  return (
    <div className="game">
      <h2>Number Guessing Game</h2>
      <p>
        Test your skills by guessing the number within the given range. Select
        difficulty levels to make it more challenging!
      </p>
      <Link href="/number-guessing">
        <button>Play Now</button>
      </Link>
    </div>
  );
};

export default NumberGuessingGame;
