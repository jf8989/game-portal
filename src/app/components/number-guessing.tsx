// src/app/components/NumberGuessingGamePage.tsx
import React, { useState, useEffect, KeyboardEvent } from "react";
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
        success?: boolean;
      }>("/api/guess", {
        guess: parseInt(guess),
      });
      setMessage(response.data.result);
      setAttempts(response.data.attempts);
      if (response.data.success) {
        setGameStarted(false);
        fetchHighScores();
        // Do not clear the guess input if the guess is correct
      } else {
        // Clear the guess input if the guess is incorrect
        setGuess("");
      }
    } catch {
      setMessage("Error submitting guess. Please try again.");
      // Clear the guess input in case of error
      setGuess("");
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleGuess();
    }
  };

  const resetGame = () => {
    setGameStarted(false);
    setGuess("");
    setMessage("Select difficulty to begin the game.");
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      {/* Background Gradient */}
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        {/* Main Content */}
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20 z-10">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl text-gray-700 font-semibold text-center mb-6">
                Number Guessing Game
              </h1>
            </div>
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <p className="text-center font-medium">{message}</p>
                {!gameStarted ? (
                  <div className="space-y-4">
                    <div className="flex justify-center space-x-4">
                      {["Easy", "Medium", "Hard"].map((level) => (
                        <label key={level} className="inline-flex items-center">
                          <input
                            type="radio"
                            className="form-radio text-cyan-600"
                            value={level}
                            checked={difficulty === level}
                            onChange={(e) => setDifficulty(e.target.value)}
                          />
                          <span className="ml-2">{level}</span>
                        </label>
                      ))}
                    </div>
                    <div className="text-center">
                      <button
                        onClick={startGame}
                        className="bg-cyan-500 text-white px-4 py-2 rounded-md hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-opacity-50"
                      >
                        Start Game
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <input
                      type="number"
                      value={guess}
                      onChange={(e) => setGuess(e.target.value)}
                      placeholder="Enter your guess"
                      onKeyPress={handleKeyPress}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-cyan-300 focus:ring focus:ring-cyan-200 focus:ring-opacity-50"
                    />
                    <div className="flex justify-center space-x-4">
                      <button
                        onClick={handleGuess}
                        className="bg-cyan-500 text-white px-4 py-2 rounded-md hover:bg-cyan-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-opacity-50"
                      >
                        Submit Guess
                      </button>
                      <button
                        onClick={resetGame}
                        className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50"
                      >
                        Change Difficulty
                      </button>
                    </div>
                  </div>
                )}
              </div>
              <div className="pt-6 text-base text-gray-500 leading-6 font-bold sm:text-lg sm:leading-7">
                <p className="text-center">High Scores</p>
                <div className="mt-2 flex justify-between text-sm">
                  <span>Easy: {highScores.Easy}</span>
                  <span>Medium: {highScores.Medium}</span>
                  <span>Hard: {highScores.Hard}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Adjusted z-index to ensure content is above the background */}
      </div>
    </div>
  );
};

export default NumberGuessingGamePage;
