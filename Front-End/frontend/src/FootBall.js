import React, { useEffect, useState } from 'react';
import './HomeScreen.css';
import 'boxicons/css/boxicons.min.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { setupNavigation } from './navBar';

function FootballScreen() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [activeLink, setActiveLink] = useState('/FootBall'); // Initialize active link state
  const [selectedOdds, setSelectedOdds] = useState(null); // State for selected odds
  const [betAmount, setBetAmount] = useState(''); // State for bet amount
  const [selectedBetOption, setSelectedBetOption] = useState(''); // State for selected bet option
  const [message, setMessage] = useState('');
  const [userCoins, setUserCoins] = useState(0);
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  
  const handleEventClick = (event) => {
    setSelectedEvent(event);
    document.getElementById('popup').style.display = 'block';
  };

  const handleSubmit = async () => {
    try {
      // Example: Post bet data with authorization header
      const response = await axios.post('http://localhost:5000/placeBet', {
        eventID: selectedEvent.id, 
        betAmount,
        selectedBetOption
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log('Response:', response.data); // Log or use the response data
    } catch (error) {
      console.error('Error placing bet:', error);
    }
  };

  const closeModal = () => {
    document.getElementById('popup').style.display = 'none';
    setSelectedEvent(null);
  };

  const handleOddsClick = (odds) => {
    setSelectedOdds(odds);
    document.getElementById('bet-popup').style.display = 'block';
  };

  const closeBetModal = () => {
    document.getElementById('bet-popup').style.display = 'none';
    setSelectedOdds(null);
    setBetAmount('');
    setSelectedBetOption('');
  };

  const handleBetAmountChange = (event) => {
    setBetAmount(event.target.value);
  };

  const handleBetOptionChange = (event) => {
    setSelectedBetOption(event.target.value);
  };

  const handleConfirmBet = () => {
    if (!betAmount || !selectedBetOption) {
      alert("Please enter a bet amount and select an outcome.");
      return;
    }

    // Add logic to handle the bet placement here
    handleSubmit();
    console.log("Bet Amount:", betAmount);
    console.log("Selected Bet Option:", selectedBetOption);

    // Close the modal after confirming the bet
    closeBetModal();
  };

  useEffect(() => {
    // Check if user is authenticated (example: check if token exists)
    const token = localStorage.getItem('token');
    if (!token) {
      // Redirect to login page if token does not exist
      navigate('/login'); // Adjust the route according to your app's routes
      return;
    }

    // Axios request interceptor to add token to headers
    axios.interceptors.request.use(
      (config) => {
        config.headers.Authorization = `Bearer ${token}`;
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    axios.get('http://localhost:5000/api/userCoins', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      console.log('Fetched user coins:', response.data);
      setUserCoins(response.data.coins);
    })
    .catch(error => {
      console.error('Error fetching user coins:', error);
    });

    // Fetch events using Axios
    axios.get('http://localhost:5000/api/Cricket')
      .then(response => {
        console.log('Fetched events:', response.data);
        setEvents(response.data);
      })
      .catch(error => {
        console.error('Error fetching sports data:', error);
      });

    // Setup navigation and set active link based on current pathname
    setupNavigation();
    setActiveLink(window.location.pathname);

  }, [navigate]); // Include navigate in dependencies to prevent warnings

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

            <a href="/Setting" className={`nav__link ${activeLink === '/Profile' ? 'active-link' : ''}`}>
              <i className='bx bx-cog'></i>
              <span className="nav__name">Profile</span>
            </a>
          </div>
        </nav>
      </div>

      {/* Main content */}
      <main className="container section">
        <div className="sports-section">
          <h1>FootBall</h1>
          <h2>Coins: {userCoins}</h2>
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
                  <h2>Betting Details</h2>
                  <div>
                    {/* Render event odds here */}
                    <h3>Event Odds</h3>
                    {selectedEvent.event_odds.slice(0, 15).map((outcome, idx) => (
                      <div key={idx} style={{ position: 'relative' }}>
                        {(idx % 3 === 0) && <p>Event {Math.floor(idx / 3) + 1}</p>}
                        {(idx % 3 === 0) && <button className="ButtonBet" onClick={() => handleOddsClick(selectedEvent.event_odds.slice(idx, idx + 3))}>Place Bet on Event {Math.floor(idx / 3) + 1}</button>}
                        <p><strong>{outcome.name}:</strong> {outcome.price}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
          {/* Bet Popup */}
          <div id="bet-popup" className="popup">
            <div className="popup-content">
              <span className="close" onClick={closeBetModal}>&times;</span>
              {selectedOdds && (
                <div>
                  <h2>Place Your Bet</h2>
                  <div>
                    <label>Bet Amount:</label>
                    <input
                      type="number"
                      value={betAmount}
                      onChange={handleBetAmountChange}
                      placeholder="Enter bet amount"
                    />
                  </div>
                  <div>
                    <label>Select Outcome:</label>
                    <select value={selectedBetOption} onChange={handleBetOptionChange}>
                      <option value="">Select an outcome</option>
                      {selectedOdds.map((odds, idx) => (
                        <option key={idx} value={odds.name}>{odds.name}</option>
                      ))}
                    </select>
                  </div>
                  <button onClick={handleConfirmBet}>Confirm Bet</button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default FootballScreen;
