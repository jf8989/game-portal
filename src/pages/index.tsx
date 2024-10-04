// src/app/index.tsx
import React from "react";
import NumberGuessingGame from "../app/components/NumberGuessingGame";

const Home = () => {
  return (
    <div className="min-h-screen bg-indigo-500 p-8">
      <div className="max-w-6xl mx-auto animate-fadeIn">
        <h1 className="text-4xl font-bold mb-4 text-center text-white animate-slideUp">
          Welcome to the Game Portal
        </h1>
        <p
          className="text-xl mb-8 text-center text-white animate-slideUp"
          style={{ animationDelay: "0.1s" }}
        >
          Choose from a variety of games below to play and have fun!
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Number Guessing Game Card */}
          <div
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition-all hover:scale-105 animate-slideUp"
            style={{ animationDelay: "0.2s" }}
          >
            <div className="p-6">
              <h2 className="text-2xl font-semibold mb-2 text-gray-800">
                Number Guessing Game
              </h2>
              <p className="text-gray-600 mb-4 bg-gray-100 p-2 rounded-md">
                Test your skills by guessing the number within the given range.
                Select difficulty levels to make it more challenging!
              </p>
              <div className="mt-4">
                <NumberGuessingGame />
              </div>
            </div>
          </div>

          {/* Placeholder Game 1 Card */}
          <div
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition-all hover:scale-105 animate-slideUp"
            style={{ animationDelay: "0.3s" }}
          >
            <div className="p-6">
              <h2 className="text-2xl font-semibold mb-2 text-gray-800">
                Placeholder Game 1
              </h2>
              <p className="text-gray-600 mb-4 bg-gray-100 p-2 rounded-md">
                Coming Soon! Another exciting game to challenge your mind.
              </p>
              <div className="mt-4 text-center">
                <button
                  className="bg-gray-400 text-white font-bold py-2 px-4 rounded cursor-not-allowed"
                  disabled
                >
                  Coming Soon
                </button>
              </div>
            </div>
          </div>

          {/* Placeholder Game 2 Card */}
          <div
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition-all hover:scale-105 animate-slideUp"
            style={{ animationDelay: "0.4s" }}
          >
            <div className="p-6">
              <h2 className="text-2xl font-semibold mb-2 text-gray-800">
                Placeholder Game 2
              </h2>
              <p className="text-gray-600 mb-4 bg-gray-100 p-2 rounded-md">
                Coming Soon! Get ready for an adventurous experience.
              </p>
              <div className="mt-4 text-center">
                <button
                  className="bg-gray-400 text-white font-bold py-2 px-4 rounded cursor-not-allowed"
                  disabled
                >
                  Coming Soon
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
