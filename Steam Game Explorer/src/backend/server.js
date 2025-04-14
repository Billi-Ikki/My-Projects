const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const bodyParser = require('body-parser');
const connectDB = require('./config/db');
const authRoutes = require('./routes/auth');
const aboutUsRoutes = require('./routes/aboutUsRoutes');
const contactMessageRoutes = require('./routes/contactMessageRoutes');
const gameRoutes = require('./routes/gameRoutes');
const libraryRoutes = require('./routes/library');

dotenv.config();
connectDB();

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use('/api/auth', authRoutes);
app.use('/api/aboutus', aboutUsRoutes);
app.use('/api/contact-messages', contactMessageRoutes);
app.use('/api/games', gameRoutes);
app.use('/api/library', libraryRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
