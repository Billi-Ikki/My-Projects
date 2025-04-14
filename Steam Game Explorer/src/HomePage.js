import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";
import "./Navbar_Footer.css";

function HomePage() {
  const [games, setGames] = useState([]);
  const navigate = useNavigate();

  // Fetch games from the backend on component mount
  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/games");
        const data = await response.json();
        setGames(data);  // Set the games data to state
      } catch (error) {
        console.error("Error fetching games:", error);
      }
    };

    fetchGames();  // Call the fetch function
  }, []);

  const handleCardClick = (game) => {
    // Pass game details via navigation state
    navigate(`/gamedetails`, { state: game });
  };

  return (
    <div className="homepage-container">
      <br></br>
      <div className="game-cards">
        {games.length > 0 ? (
          games.map((game) => (
            <div className="game-card" key={game._id} onClick={() => handleCardClick(game)}>
              <div className="game-image">
                <img
                  src={game.image || "https://via.placeholder.com/150"} // Use the image URL from DB or fallback to placeholder
                  alt={game.title}
                />
              </div>
              <div className="game-title">{game.title}</div>
              <div className="game-rating">{'★'.repeat(game.rating)}</div>
            </div>
          ))
        ) : (
          <p>Loading games...</p>
        )}
      </div>
      <br></br>
    </div>
  );
}

export default HomePage;
