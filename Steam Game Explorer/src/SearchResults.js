import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import './SearchResults.css';

function SearchResults() {
  const [games, setGames] = useState([]);
  const [searchParams] = useSearchParams();
  const query = searchParams.get('query');
  const navigate = useNavigate();

  useEffect(() => {
    if (query) {
      fetchGames(query);
    }
  }, [query]);

  const fetchGames = async (searchQuery) => {
    try {
      const response = await fetch(`http://localhost:5000/api/games?query=${searchQuery}`);
      const data = await response.json();
      setGames(data);
    } catch (err) {
      console.error('Error fetching games:', err);
    }
  };

  const handleCardClick = (game) => {
    navigate(`/game/${game._id}`, { state: game });
  };

  return (
    <div className="search-results-container">
      <h1>Search Results</h1>
      {games.length > 0 ? (
        <div className="game-cards">
          {games.map((game) => (
            <div
              key={game._id}
              className="game-card"
              onClick={() => handleCardClick(game)}
            >
              <img src={game.image} alt={game.title} />
              <h3>{game.title}</h3>
              <p>Rating: {'★'.repeat(game.rating)}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No games found for "{query}".</p>
      )}
    </div>
  );
}

export default SearchResults;
