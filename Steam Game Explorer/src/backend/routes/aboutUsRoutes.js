const express = require('express');
const AboutUs = require('../models/AboutUs');
const router = express.Router();

// Get About Us data
router.get('/', async (req, res) => {
  try {
    const aboutUs = await AboutUs.findOne();
    res.status(200).json(aboutUs);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ message: 'Server error' });
  }
});

// Add or Update About Us data
router.post('/', async (req, res) => {
  const { mission, contactInfo, features } = req.body;

  try {
    let aboutUs = await AboutUs.findOne();

    if (aboutUs) {
      // Update existing data
      aboutUs.mission = mission;
      aboutUs.contactInfo = contactInfo;
      aboutUs.features = features;
    } else {
      // Create new data
      aboutUs = new AboutUs({
        mission,
        contactInfo,
        features,
      });
    }

    await aboutUs.save();
    res.status(200).json({ message: 'About Us data saved successfully', aboutUs });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ message: 'Server error' });
  }
});

module.exports = router;
