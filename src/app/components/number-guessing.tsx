//src/app/components/number-guessing.tsx
import React, { useState, useEffect } from "react";
import axios from "axios";

const NumberGuessingGamePage = () => {
  const [guess, setGuess] = useState("");
  const [message, setMessage] = useState(
    "Select difficulty to begin the game."
  );
  const [, setAttempts] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [difficulty, setDifficulty] = useState("Easy");
  const [highScores, setHighScores] = useState({
    Easy: 999,
    Medium: 999,
    Hard: 999,
  });

  useEffect(() => {
    fetchHighScores();
  }, []);

  const fetchHighScores = async () => {
    try {
      const response = await axios.get("/api/high-scores");
      const highScoresData = response.data as {
        Easy: number;
        Medium: number;
        Hard: number;
      };
      setHighScores(highScoresData);
    } catch (error) {
      console.error("Error fetching high scores:", error);
    }
  };

  const startGame = async () => {
    try {
      const response = await axios.post<{ message: string }>(
        "/api/start-game",
        { difficulty }
      );
      setMessage(response.data.message);
      setAttempts(0);
      setGameStarted(true);
      setGameStarted(true);
    } catch {
      setMessage("Error starting game. Please try again.");
    }
  };

  const handleGuess = async () => {
    if (!guess) {
      setMessage("Please enter a valid number.");
      return;
    }

    try {
      const response = await axios.post<{
        result: string;
        attempts: number;
        success: boolean;
      }>("/api/guess", {
        guess: parseInt(guess),
      });
      setMessage(response.data.result);
      setAttempts(response.data.attempts);
      if (response.data.success) {
        setGameStarted(false);
        fetchHighScores();
      }
    } catch {
      setMessage("Error submitting guess. Please try again.");
    }
    setGuess("");
  };

  return (
    <div className="number-guessing-game">
      <h1>Number Guessing Game</h1>
      <p>{message}</p>
      {!gameStarted ? (
        <>
          <div>
            <label>
              <input
                type="radio"
                value="Easy"
                checked={difficulty === "Easy"}
                onChange={(e) => setDifficulty(e.target.value)}
              />
              Easy (1-100)
            </label>
            <label>
              <input
                type="radio"
                value="Medium"
                checked={difficulty === "Medium"}
                onChange={(e) => setDifficulty(e.target.value)}
              />
              Medium (1-500)
            </label>
            <label>
              <input
                type="radio"
                value="Hard"
                checked={difficulty === "Hard"}
                onChange={(e) => setDifficulty(e.target.value)}
              />
              Hard (1-1000)
            </label>
          </div>
          <button onClick={startGame}>Start Game</button>
        </>
      ) : (
        <>
          <input
            type="number"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            placeholder="Enter your guess"
          />
          <button onClick={handleGuess}>Submit Guess</button>
        </>
      )}
      <div>
        <h2>High Scores</h2>
        <p>Easy: {highScores.Easy}</p>
        <p>Medium: {highScores.Medium}</p>
        <p>Hard: {highScores.Hard}</p>
      </div>
    </div>
  );
};

export default NumberGuessingGamePage;
