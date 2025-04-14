import React, { useEffect, useState } from 'react';
import './Navbar_Footer.css';
import './AboutUs.css';

function AboutUs() {
  const [aboutUs, setAboutUs] = useState(null);

  useEffect(() => {
    const fetchAboutUs = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/aboutus');
        const data = await response.json();
        setAboutUs(data);
      } catch (err) {
        console.error('Error fetching About Us data:', err);
      }
    };

    fetchAboutUs();
  }, []);

  if (!aboutUs) {
    return <div>Loading...</div>;
  }

  return (
    <div className="about-us-container">
      <h2>About Us</h2>
      <p>{aboutUs.mission}</p>

      <section className="features-section">
        <h3>Features</h3>
        <p>We are constantly working to bring new updates and features to Steam, such as:</p>
        <div className="features-grid">
          {aboutUs.features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h4>{feature.title}</h4>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="contact-info">
        <h3>Contact Information</h3>
        <p>Email: {aboutUs.contactInfo.email}</p>
        <p>Phone: {aboutUs.contactInfo.phone}</p>
        <p>Office Location: {aboutUs.contactInfo.office}</p>
      </section>
    </div>
  );
}

export default AboutUs;
