const mongoose = require('mongoose');

const gameSchema = new mongoose.Schema({
  title: { type: String, required: true },
  image: { type: String, required: true },
  rating: { type: Number, required: true },
  genre: { type: String, required: true }, 
  description: { type: String, required: true },
  price: { type: String, required: true },
  systemSpecs: {
    os: String,
    processor: String,
    memory: String,
    graphics: String,
    storage: String,
  },
  reviews: [
    {
      stars: { type: Number, required: true },
      review: { type: String, required: true },
    },
  ],
  comments: [
    {
      comment: { type: String, required: true },
    },
  ],
});

const Game = mongoose.model('Game', gameSchema);
module.exports = Game;
