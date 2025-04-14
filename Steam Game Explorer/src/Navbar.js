import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Navbar_Footer.css';

function Navbar() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const navigate = useNavigate();

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  const handleLogout = () => {
    localStorage.setItem('isLoggedIn', 'false');
    alert('Logged out successfully!');
    window.location.href = '/'; // Redirect to login page
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?query=${searchQuery}&genre=${selectedGenre}`); // Navigate to search results with genre filter
    }
  };

  return (
    <>
      <header className="header">
        <div className="logo">
          <Link to="/home" className="logo-link">
            Steam Explorer
          </Link>
        </div>
        <div className="search-bar-container">
          <form className="search-bar" onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="Search games..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="search-button" type="submit">
              Search
            </button>
            <button
              type="button"
              className="filter-button"
              onClick={() => navigate('/filter')}
            >
              Filter
            </button>
          </form>
        </div>
        <button className="sidebar-toggle" onClick={toggleSidebar}>
          ☰
        </button>
      </header>

      {/* Sidebar */}
      <div className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <button className="sidebar-close" onClick={toggleSidebar}>
          ✖
        </button>
        <ul className="sidebar-links">
          <li>
            <Link to="/home" onClick={toggleSidebar}>
              Home
            </Link>
          </li>
          <li>
            <Link to="/gamecomparison" onClick={toggleSidebar}>
              Compare Games
            </Link>
          </li>
          <li>
            <Link to="/contact" onClick={toggleSidebar}>
              Contact Us
            </Link>
          </li>
          <li>
            <Link to="/about" onClick={toggleSidebar}>
              About Us
            </Link>
          </li>
          
          <li>
            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </li>
        </ul>
      </div>
    </>
  );
}

export default Navbar;
