import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import './GameDetailsPage.css';
import './Navbar_Footer.css';

function GameDetailsPage() {
  const location = useLocation();
  const { state: gameDataFromState } = location;
  const { id } = useParams();

  const [gameData, setGameData] = useState(gameDataFromState || null);
  const [userStars, setUserStars] = useState(0);
  const [userReview, setUserReview] = useState('');
  const [userComment, setUserComment] = useState('');
  const [loading, setLoading] = useState(!gameDataFromState);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!gameDataFromState) {
      fetchGameDetails(id);
    }
  }, [id, gameDataFromState]);

  const fetchGameDetails = async (gameId) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`http://localhost:5000/api/games/${gameId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch game details: ${response.status}`);
      }
      const data = await response.json();
      setGameData(data);
    } catch (err) {
      console.error('Error fetching game details:', err);
      setError('Unable to load game details. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddReview = async () => {
    if (!userReview && userStars === 0) {
      alert('Please add a review or select a star rating.');
      return;
    }
    try {
      const response = await fetch(`http://localhost:5000/api/games/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: gameData.title,
          stars: userStars,
          review: userReview,
        }),
      });
      if (!response.ok) {
        throw new Error(`Failed to add review: ${response.status}`);
      }
      const message = await response.text();
      alert(message);
      setUserReview('');
      setUserStars(0);
      fetchGameDetails(id); // Refresh game details
    } catch (err) {
      console.error('Error adding review:', err);
      alert('Failed to add review. Please try again.');
    }
  };

  const handleAddComment = async () => {
    if (!userComment) {
      alert('Please enter a comment.');
      return;
    }
    try {
      const response = await fetch(`http://localhost:5000/api/games/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: gameData.title, comment: userComment }),
      });
      if (!response.ok) {
        throw new Error(`Failed to add comment: ${response.status}`);
      }
      const message = await response.text();
      alert(message);
      setUserComment('');
      fetchGameDetails(id); // Refresh game details
    } catch (err) {
      console.error('Error adding comment:', err);
      alert('Failed to add comment. Please try again.');
    }
  };

  if (loading) {
    return <p>Loading game details...</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  const {
    title,
    image,
    price,
    rating,
    description,
    systemSpecs = {},
    reviews = [],
    comments = [],
  } = gameData;

  return (
    <div className="gamedetails-container">
      <div className="game-content">
        <h1 className="game-title1">{title}</h1>
        <div className="game-info">
          <div className="game-image1">
            <img src={image} alt={title} />
          </div>
          <div className="game-details">
            <p className="game-price">Price: ${price}</p>
            <p className="game-rating1">Rating: {'★'.repeat(rating)}</p>
            <h3>System Requirements:</h3>
            <ul>
              <li>OS: {systemSpecs.os}</li>
              <li>Processor: {systemSpecs.processor}</li>
              <li>Memory: {systemSpecs.memory}</li>
              <li>Graphics: {systemSpecs.graphics}</li>
              <li>Storage: {systemSpecs.storage}</li>
            </ul>
          </div>
        </div>

        <div className="game-description">
          <h2>Description</h2>
          <p>{description}</p>
        </div>

        <div className="reviews-section">
          <h2>Reviews</h2>
          <ul>
            {reviews.map((review, index) => (
              <li key={index}>
                {'★'.repeat(review.stars)} - {review.review}
              </li>
            ))}
          </ul>
          <div className="user-rating">
            {[1, 2, 3, 4, 5].map((star) => (
              <span
                key={star}
                onClick={() => setUserStars(star)}
                style={{ cursor: 'pointer', color: star <= userStars ? 'gold' : 'gray' }}
              >
                ★
              </span>
            ))}
          </div>
          <textarea
            value={userReview}
            onChange={(e) => setUserReview(e.target.value)}
            placeholder="Write your review..."
            className="input-area"
          ></textarea>
          <button onClick={handleAddReview} className="submit-button">
            Submit Review
          </button>
        </div>

        <div className="comments-section">
          <h2>Community Comments</h2>
          <ul>
            {comments.map((comment, index) => (
              <li key={index}>{comment.comment}</li>
            ))}
          </ul>
          <textarea
            value={userComment}
            onChange={(e) => setUserComment(e.target.value)}
            placeholder="Add a comment..."
            className="input-area"
          ></textarea>
          <button onClick={handleAddComment} className="submit-button">
            Add Comment
          </button>
        </div>
      </div>
    </div>
  );
}

export default GameDetailsPage;
