const express = require('express');
const ContactMessage = require('../models/ContactMessage');
const router = express.Router();

// Save a contact message
router.post('/', async (req, res) => {
  const { name, email, messageType, message } = req.body;

  try {
    const newMessage = new ContactMessage({
      name,
      email,
      messageType,
      message
    });

    await newMessage.save();
    res.status(201).json({ message: 'Message sent successfully!' });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get all contact messages (optional, for admin purposes)
router.get('/', async (req, res) => {
  try {
    const messages = await ContactMessage.find().sort({ date: -1 });
    res.status(200).json(messages);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
