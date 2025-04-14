import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ScrollToTop from './ScrollToTop';
import Layout from './Layout';
import LoginPage from './LoginPage';
import HomePage from './HomePage';
import SignUpPage from './SignUpPage';
import GameDetailsPage from './GameDetailsPage';
import AboutUs from './AboutUs';
import ContactUs from './ContactUs';
import GameComparisonPage from './GameComparisonPage';
import SearchResults from './SearchResults';
import FilterPage from './FilterPage';
import LibraryPage from './LibraryPage'
function ProtectedRoute({ children }) {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  return isLoggedIn ? children : <Navigate to="/" />;
}
const userId = localStorage.getItem('userId'); // Ensure this is a valid ObjectId

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />

      {/* Protected Routes */}

      <Route path="/filter" element={<Layout><FilterPage /></Layout>} />
      <Route path="/library" element={<Layout><LibraryPage /></Layout>} />

      <Route 
        path="/game/:id" 
        element={
        <Layout>
        <GameDetailsPage />
        </Layout>
        }
      />
      <Route 
        path="/search" 
        element={
          <Layout>
          <SearchResults />
          </Layout>
          } 
      />
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Layout>
              <HomePage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/about"
        element={
          <Layout>
            <AboutUs />
          </Layout>
        }
      />
      <Route
        path="/contact"
        element={
          <Layout>
            <ContactUs />
          </Layout>
        }
      />
      <Route
        path="/gamedetails"
        element={
          <Layout>
            <GameDetailsPage />
          </Layout>
        }
      />
      <Route
        path="/gamecomparison"
        element={
          <Layout>
            <GameComparisonPage />
          </Layout>
        }
      />
    </Routes>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <ScrollToTop />
      <App />
    </Router>
  );
}
