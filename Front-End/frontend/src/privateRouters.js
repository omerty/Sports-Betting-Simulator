import React, { useContext } from 'react';
import { Route, Navigate } from 'react-router-dom';
import { AuthContext } from './Authentication'; // Ensure correct import path

const PrivateRoute = ({ element, ...rest }) => {
  const { auth } = useContext(AuthContext); // Destructure auth from context

  // Assuming isLoggedIn logic based on auth token presence
  const isLoggedIn = auth.token !== null && auth.username !== null;

  return (
    <Route
      {...rest}
      element={isLoggedIn ? element : <Navigate to="/login" />}
    />
  );
};

export default PrivateRoute;
