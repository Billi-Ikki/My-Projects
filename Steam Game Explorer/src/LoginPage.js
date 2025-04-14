// Group Members
// 22i-1636 (M Bilal Ikram)
// 22i-1697 (Saif-Ur-Rehman)
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is already logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (isLoggedIn) {
      navigate('/home'); // Redirect to home if logged in
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
  
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        setError(data.message || 'Failed to log in');
        return;
      }
  
      // Store token and login status
      localStorage.setItem('token', data.token);
      localStorage.setItem('userId', data._id); // Store user ID in localStorage
      localStorage.setItem('isLoggedIn', 'true');
      navigate('/home'); // Redirect to the homepage
    } catch (err) {
      console.error(err);
      setError('An error occurred. Please try again later.');
    }
  };
  

  const handleSignUp = () => {
    navigate('/signup'); // Navigate to the signup page
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">Steam Game Explorer</h2>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="login-button">Login</button>
        </form>
        <div className="signup-option">
          <p className="signup-text">Don't have an account?</p>
          <button className="signup-button" onClick={handleSignUp}>
            Sign Up
          </button>
        </div>
        <p className="footer-text">
          © 2023 Steam Game Explorer. All rights reserved.
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
