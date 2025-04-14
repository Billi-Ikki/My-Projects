// Group Members
// 22i-1636 (M Bilal Ikram)
// 22i-1697 (Saif-Ur-Rehman)
import React, { useState } from 'react';
import './ContactUs.css';
import { useNavigate, Link } from 'react-router-dom';
import './Navbar_Footer.css';

function ContactUs() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    messageType: 'Feedback',
    message: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const response = await fetch('http://localhost:5000/api/contact-messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
  
      if (response.ok) {
        alert("Thank you for reaching out! We'll get back to you shortly.");
        setFormData({ name: '', email: '', messageType: 'Feedback', message: '' });
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (err) {
      console.error('Error sending message:', err);
      alert('An error occurred while sending your message. Please try again later.');
    }
  };
  
  return (
    <div className="contact-us-container">
      <h2>Contact Us</h2>
      <div className="contact-content">
        <form className="contact-form" onSubmit={handleSubmit}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Your Name"
              required
            />
          </label>

          <label>
            Email:
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Your Email"
              required
            />
          </label>

          <label>
            Type of Message:
            <select
              name="messageType"
              value={formData.messageType}
              onChange={handleInputChange}
            >
              <option value="Feedback">Feedback</option>
              <option value="Issue/Problem">Issue/Problem</option>
              <option value="Question">Question</option>
              <option value="Other">Other</option>
            </select>
          </label>

          <label>
            Message:
            <textarea
              name="message"
              value={formData.message}
              onChange={handleInputChange}
              placeholder="Write your message here..."
              required
            />
          </label>

          <button type="submit">Send Message</button>
        </form>

        <div className="contact-details">
          <h3>Our Contact Information</h3>
          <p><strong>Email:</strong> support@steamexplorer.com</p>
          <p><strong>Phone:</strong> +1 (555) 123-4567</p>
          <p><strong>Office Location:</strong> 1234 Game St, Suite 500, San Francisco, CA 94103</p>
          <p><strong>Working Hours:</strong> Monday - Friday, 9:00 AM - 5:00 PM</p>

          <div className="social-media">
            <h4>Follow Us</h4>
            <a href="https://twitter.com/SteamExplorer" target="_blank" rel="noopener noreferrer">Twitter</a>
            <a href="https://facebook.com/SteamExplorer" target="_blank" rel="noopener noreferrer">Facebook</a>
            <a href="https://instagram.com/SteamExplorer" target="_blank" rel="noopener noreferrer">Instagram</a>
          </div>
        </div>
      </div>

    </div>
  );
}

export default ContactUs;
