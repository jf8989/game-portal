// src/app/components/NumberGuessingGame.tsx
import React from "react";
import Link from "next/link";

const NumberGuessingGame = () => {
  return (
    <div
      className="text-center animate-slideUp"
      style={{ animationDelay: "0.5s" }}
    >
      <Link href="/number-guessing">
        <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-200">
          Play Now
        </button>
      </Link>
    </div>
  );
};

export default NumberGuessingGame;
