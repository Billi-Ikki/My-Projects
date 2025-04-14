const Game = require('../models/Game');

// Get game details by ID
exports.getGameDetails = async (req, res) => {
  try {
    // Fetch the game by its ID
    const game = await Game.findById(req.params.id);
    if (!game) {
      return res.status(404).json({ message: 'Game not found' });
    }
    res.status(200).json(game); // Return the game details including reviews and comments
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// Add a review to a game
exports.addReview = async (req, res) => {
  try {
    const { gameId, stars, review } = req.body;

    // Find the game by ID
    const game = await Game.findById(gameId);
    if (!game) {
      return res.status(404).json({ message: 'Game not found' });
    }

    // Add the new review to the game's reviews array
    game.reviews.push({ stars, review });

    // Recalculate the rating of the game based on the reviews
    game.rating = (
      game.reviews.reduce((acc, rev) => acc + rev.stars, 0) / game.reviews.length
    ).toFixed(1); // Average rating to 1 decimal place

    // Save the updated game document
    await game.save();

    res.status(201).json(game); // Return the updated game data
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};

// Add a comment to a game
exports.addComment = async (req, res) => {
  try {
    const { gameId, comment } = req.body;

    // Find the game by ID
    const game = await Game.findById(gameId);
    if (!game) {
      return res.status(404).json({ message: 'Game not found' });
    }

    // Add the new comment to the game's comments array
    game.comments.push({ comment });

    // Save the updated game document
    await game.save();

    res.status(201).json(game); // Return the updated game data
  } catch (error) {
    res.status(500).json({ message: 'Server error', error: error.message });
  }
};
