const express = require('express');
const router = express.Router(); 
const { loginUser, registerUser } = require('../controllers/authController');

// Existing signup route
router.post('/signup', registerUser);

// New login route
router.post('/login', loginUser);

module.exports = router;
