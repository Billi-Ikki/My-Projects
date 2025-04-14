import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './FilterPage.css';

function FilterPage() {
  const [selectedGenre, setSelectedGenre] = useState('');
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const genres = [
    'Action',
    'Adventure',
    'RPG',
    'Shooter',
    'Sports',
    'Simulation',
    'Platformer',
    'MMO',
    'Battle Royale',
    'Survival',
    'Sandbox',
    'MOBA' // Multiplayer Online Battle Arena
  ];
  
  

  const handleGenreSelect = async (genre) => {
    setSelectedGenre(genre);

    try {
      const response = await fetch(`http://localhost:5000/api/games/filter?genre=${genre}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error fetching games:', error);
      setResults([]); // Clear results if there's an error
    }
  };

  const handleCardClick = (game) => {
    // Navigate to the Game Details page and pass game data via state
    navigate(`/gamedetails`, { state: game });
  };

  return (
    <div className="filter-page">
      <h1 className="filter-page-header">Select a Genre</h1>
      <div className="genres-section">
        {genres.map((genre) => (
          <button
            key={genre}
            className={`genre-button ${selectedGenre === genre ? 'selected' : ''}`}
            onClick={() => handleGenreSelect(genre)}
          >
            {genre}
          </button>
        ))}
      </div>
      <div className="results-section">
        {selectedGenre && <h2>Results for "{selectedGenre}"</h2>}
        {results.length > 0 ? (
          <div className="game-cards">
            {results.map((game) => (
              <div className="game-card" key={game._id} onClick={() => handleCardClick(game)}>
                <div className="game-image">
                  <img
                    src={game.image || 'https://via.placeholder.com/150'} // Use game image or placeholder
                    alt={game.title}
                  />
                </div>
                <div className="game-title">{game.title}</div>
                <div className="game-rating">{'★'.repeat(game.rating)}</div>
              </div>
            ))}
          </div>
        ) : (
          selectedGenre && <p>No results found for this genre.</p>
        )}
      </div>
    </div>
  );
}

export default FilterPage;
