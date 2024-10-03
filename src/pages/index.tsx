import React from "react";
import Link from "next/link";
import NumberGuessingGame from "../app/components/NumberGuessingGame";
import PlaceholderGame1 from "../app/components/PlaceholderGame1";
import PlaceholderGame2 from "../app/components/PlaceholderGame2";

const Home = () => {
  return (
    <div className="home">
      <h1>Welcome to the Game Portal</h1>
      <p>Choose from a variety of games below to play and have fun!</p>
      <div className="games-list">
        <NumberGuessingGame />
        <PlaceholderGame1 />
        <PlaceholderGame2 />
      </div>
    </div>
  );
};

export default Home;
