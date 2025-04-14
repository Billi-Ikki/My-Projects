import { useEffect, useState } from 'react';
import './LibraryPage.css';

function LibraryPage() {
  const [library, setLibrary] = useState([]);
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    const fetchLibrary = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/library/${userId}`);
        const data = await response.json();
        setLibrary(data);
      } catch (error) {
        console.error('Error fetching library:', error);
      }
    };

    fetchLibrary();
  }, [userId]);

  return (
    <div className="library-page">
      <h1>Your Library</h1>
      <div className="game-cards">
        {library.map((game) => (
          <div key={game._id} className="game-card">
            <img src={game.image} alt={game.title} />
            <h3>{game.title}</h3>
            <p>Rating: {'★'.repeat(game.rating)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LibraryPage;
