const mongoose = require('mongoose');

const aboutUsSchema = new mongoose.Schema({
  mission: { type: String, required: true },
  contactInfo: {
    email: { type: String, required: true },
    phone: { type: String, required: true },
    office: { type: String, required: true },
  },
  features: [
    {
      title: { type: String, required: true },
      description: { type: String, required: true },
      icon: { type: String, required: true },
    },
  ],
});

module.exports = mongoose.model('AboutUs', aboutUsSchema);
