const express = require('express');
const Game = require('../models/Game');
const router = express.Router();

// Fetch all games or search by title
router.get('/', async (req, res) => {
  const { query } = req.query;
  try {
    const games = query
      ? await Game.find({ title: { $regex: query, $options: 'i' } })
      : await Game.find();
    res.status(200).json(games);
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch games', error: err.message });
  }
});

// Fetch a game by title
router.get('/game/:title', async (req, res) => {
  try {
    const game = await Game.findOne({ title: req.params.title });
    if (!game) {
      return res.status(404).json({ message: 'Game not found' });
    }
    res.status(200).json(game);
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
});

// Fetch a single game by ID
router.get('/:id', async (req, res) => {
  try {
    const game = await Game.findById(req.params.id);
    if (!game) {
      return res.status(404).json({ message: 'Game not found' });
    }
    res.status(200).json(game);
  } catch (err) {
    res.status(500).json({ message: 'Failed to fetch game', error: err.message });
  }
});

// Add a new game
router.post('/', async (req, res) => {
  const gameData = req.body;
  try {
    const newGame = new Game(gameData);
    await newGame.save();
    res.status(201).json({ message: 'Game added successfully!', game: newGame });
  } catch (err) {
    res.status(500).json({ message: 'Error saving game', error: err.message });
  }
});

// Add a review based on game title
router.post('/review', async (req, res) => {
  const { title, stars, review } = req.body;
  try {
    const game = await Game.findOne({ title: title }); // Find game by title
    if (!game) return res.status(404).send('Game not found.');

    game.reviews.push({ stars, review });
    await game.save();
    res.send('Review added successfully!');
  } catch (err) {
    res.status(500).send('Error adding review.');
  }
});

// Add a comment based on game title
router.post('/comment', async (req, res) => {
  const { title, comment } = req.body;
  try {
    const game = await Game.findOne({ title: title }); // Find game by title
    if (!game) return res.status(404).send('Game not found.');

    game.comments.push({ comment });
    await game.save();
    res.send('Comment added successfully!');
  } catch (err) {
    res.status(500).send('Error adding comment.');
  }
});

module.exports = router;
