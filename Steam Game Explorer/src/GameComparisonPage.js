import React, { useState, useEffect } from 'react';
import './GameComparisonPage.css';
import './Navbar_Footer.css';

function GameComparisonPage() {
  const [game1, setGame1] = useState('');
  const [game2, setGame2] = useState('');
  const [availableGames, setAvailableGames] = useState([]);
  const [selectedGames, setSelectedGames] = useState([]);
  const [showComparison, setShowComparison] = useState(false);

  useEffect(() => {
    // Fetch games from backend
    const fetchGames = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/games');
        const data = await response.json();
        setAvailableGames(data);
      } catch (error) {
        console.error('Failed to fetch games:', error);
      }
    };

    fetchGames();
  }, []);

  const handleCompare = () => {
    if (game1 === game2) {
      alert('Please select two different games.');
      return;
    }

    const selectedGame1 = availableGames.find((game) => game.title === game1);
    const selectedGame2 = availableGames.find((game) => game.title === game2);

    if (selectedGame1 && selectedGame2) {
      setSelectedGames([selectedGame1, selectedGame2]);
      setShowComparison(true);
    } else {
      alert('Please enter valid game titles.');
    }
  };

  const determineWinner = () => {
    if (selectedGames[0].rating > selectedGames[1].rating) return selectedGames[0].title;
    if (selectedGames[1].rating > selectedGames[0].rating) return selectedGames[1].title;
    return 'It’s a tie!';
  };

  return (
    <div className="gamecomparison-container">
      <h1 className="comparison-title">Compare Two Games</h1>

      <div className="game-inputs">
        <input
          type="text"
          placeholder="Enter first game title"
          value={game1}
          onChange={(e) => setGame1(e.target.value)}
          className="game-input"
          list="game-titles"
        />
        <input
          type="text"
          placeholder="Enter second game title"
          value={game2}
          onChange={(e) => setGame2(e.target.value)}
          className="game-input"
          list="game-titles"
        />
        <datalist id="game-titles">
          {availableGames.map((game) => (
            <option key={game._id} value={game.title} />
          ))}
        </datalist>
      </div>

      <button className="compare-button" onClick={handleCompare}>
        Compare
      </button>

      {showComparison && (
        <>
          <div className="comparison-content">
            {selectedGames.map((game, index) => (
              <div key={index} className="game-comparison-card">
                <h2>{game.title}</h2>
                <div className="game-image2">
                  <img src={game.image} alt={game.title} />
                </div>
                <p className="game-price">Price: ${game.price}</p>
                <p className="game-rating">Rating: {game.rating}★</p>
                <h3>System Requirements:</h3>
                <ul>
                  <li>OS: {game.systemSpecs.os}</li>
                  <li>Processor: {game.systemSpecs.processor}</li>
                  <li>Memory: {game.systemSpecs.memory}</li>
                  <li>Graphics: {game.systemSpecs.graphics}</li>
                  <li>Storage: {game.systemSpecs.storage}</li>
                </ul>
                <h3>Description</h3>
                <p>{game.description}</p>
              </div>
            ))}
          </div>
          <div className="winner-announcement">
            <h2>Winner: {determineWinner()}</h2>
          </div>
        </>
      )}
    </div>
  );
}

export default GameComparisonPage;
