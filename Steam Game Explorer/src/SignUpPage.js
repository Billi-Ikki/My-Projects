// Group Members
// 22i-1636 (M Bilal Ikram)
// 22i-1697 (Saif-Ur-Rehman)
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignUpPage.css';

function SignUpPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async (e) => {
  e.preventDefault();

  if (!username || !email || !password || !confirmPassword) {
    setError('All fields are required.');
    return;
  }

  if (password !== confirmPassword) {
    setError('Passwords do not match.');
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });

    if (!response.ok) {
      const data = await response.json();
      setError(data.message || 'Failed to sign up');
      return;
    }

    alert('Successfully Signed Up');
    navigate('/');
  } catch (err) {
    console.error(err);
    setError('An error occurred. Please try again later.');
  }
};


  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2 className="signup-title">Sign Up for Steam Game Explorer</h2>
        <form onSubmit={handleSignUp}>
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
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
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
          <div className="input-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
            />
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="signup-button">Sign Up</button>
        </form>
        <p className="footer-text">
          Already have an account? <button className="login-link" onClick={() => navigate('/')}>Login here</button>
        </p>
      </div>
    </div>
  );
}

export default SignUpPage;
