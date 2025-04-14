const express = require('express');
const mongoose = require('mongoose');
const router = express.Router();

// Example route
router.get('/library/:userId', async (req, res) => {
  const userId = req.params.userId;

  // Validate `userId`
  if (!mongoose.Types.ObjectId.isValid(userId)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }

  try {
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    console.error('Error fetching library:', err);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
