import React, { useEffect, useState } from 'react';
import './HomeScreen.css';
import 'boxicons/css/boxicons.min.css';
import { setupNavigation } from './navBar';

function HomeScreen() {
  const [sports, setSports] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/sports')
      .then(response => response.json())
      .then(data => setSports(data))
      .catch(error => console.error('Error fetching sports data:', error));
  }, []);

  useEffect(() => {
    setupNavigation();
  }, []);

  return (
    <div className="HomeScreen">
      {/* Sidebar navigation */}
      <div className="nav" id="nav">
        <nav className="nav__content">
          <div className="nav__toggle" id="nav-toggle">
            <i className='bx bx-chevron-right'></i>
          </div>

          <a href="#" className="nav__logo">
            <i className='bx bxs-heart'></i>
            <span className="nav__logo-name">Sports</span>
          </a>

          <div className="nav__list">
            <a href="#" className="nav__link active-link">
              <i class='bx bx-football'></i>
              <span className="nav__name">Soccer</span>
            </a>

            <a href="#" className="nav__link">
              <i class='bx bx-ball' ></i>
              <span className="nav__name">NFL</span>
            </a>

            <a href="#" className="nav__link">
              <i class='bx bxs-circle'></i>
              <span className="nav__name">NHL</span>
            </a>

            <a href="#" className="nav__link">
              <i class='bx bx-cricket-ball'></i>
              <span className="nav__name">Cricket</span>
            </a>

            <a href="#" className="nav__link">
              <i className='bx bx-cog'></i>
              <span className="nav__name">Profile</span>
            </a>
          </div>
        </nav>
      </div>

      {/* Main content */}
      <main className="container section">
        <div className="sports-section">
          <div>
            <h1>Events</h1>
          </div>
        </div>
      </main>
    </div>
  );
}

export default HomeScreen;
