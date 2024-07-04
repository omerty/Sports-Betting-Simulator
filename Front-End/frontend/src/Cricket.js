import React, { useEffect, useState } from 'react';
import './HomeScreen.css';
import 'boxicons/css/boxicons.min.css';
import { setupNavigation } from './navBar';

function CricketScreen() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [activeLink, setActiveLink] = useState('/Cricket'); // Initialize active link state

  const handleEventClick = (event) => {
    setSelectedEvent(event);
    document.getElementById('popup').style.display = 'block';
  };

  const closeModal = () => {
    document.getElementById('popup').style.display = 'none';
    setSelectedEvent(null);
  };

  useEffect(() => {
    fetch('http://localhost:5000/api/Cricket')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched events:', data);
        if (Array.isArray(data)) {
          setEvents(data);
        } else {
          console.error('Fetched data is not an array:', data);
        }
      })
      .catch(error => console.error('Error fetching sports data:', error));
  }, []);

  useEffect(() => {
    setupNavigation();
    setActiveLink(window.location.pathname);
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
            <a href="/Soccer" className={`nav__link ${activeLink === '/Soccer' ? 'active-link' : ''}`}>
              <i className='bx bx-football'></i>
              <span className="nav__name">Soccer</span>
            </a>

            <a href="/Football" className={`nav__link ${activeLink === '/Football' ? 'active-link' : ''}`}>
              <i className='bx bx-ball' ></i>
              <span className="nav__name">NFL</span>
            </a>

            <a href="/Hockey" className={`nav__link ${activeLink === '/Hockey' ? 'active-link' : ''}`}>
              <i className='bx bxs-circle'></i>
              <span className="nav__name">NHL</span>
            </a>

            <a href="/Cricket" className={`nav__link ${activeLink === '/Cricket' ? 'active-link' : ''}`}>
              <i className='bx bx-cricket-ball'></i>
              <span className="nav__name">Cricket</span>
            </a>

            <a href="#" className={`nav__link ${activeLink === '/Profile' ? 'active-link' : ''}`}>
              <i className='bx bx-cog'></i>
              <span className="nav__name">Profile</span>
            </a>
          </div>
        </nav>
      </div>

      {/* Main content */}
      <main className="container section">
        <div className="sports-section">
          <h1>Cricket</h1>
          {events.length === 0 ? (
            <p>No upcoming events</p>
          ) : (
            <div className="events-list">
              {events.map((event, index) => (
                <div key={index} className="event-item" onClick={() => handleEventClick(event)}>
                  <p className="teams">
                    <span className="main-team">{event.home_team}</span>
                    <span className="vs">vs</span>
                    <span className="away-team">{event.away_team}</span>
                  </p>
                  <p className="commence-time">
                    {new Date(event.commence_time).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        {/* Popup */}
        <div id="popup" className="popup">
          <div className="popup-content">
            <span className="close" onClick={closeModal}>&times;</span>
            {selectedEvent && (
              <div>
                <h2>Event Details</h2>
                <p><strong>Market:</strong> {selectedEvent.market}</p>
                <p><strong>Away Team:</strong> {selectedEvent.away_team}</p>
                <p><strong>Commence Time:</strong> {new Date(selectedEvent.commence_time).toLocaleString()}</p>
              </div>
            )}
          </div>
        </div>
        </div>
      </main>
    </div>
  );
}

export default CricketScreen;
