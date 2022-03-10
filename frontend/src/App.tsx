import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Login from "./Login";
import Register from "./Register";
import { Routes, Route } from "react-router-dom";
import DashboardMentee from "./DashboardMentee";
import DashboardMentor from "./DashboardMentor";
import BrowseMentors from "./BrowseMentors";
import WorkshopsMentee from "./WorkshopsMentee";
import WorkshopsMentor from "./WorkshopsMentor";
import RegisterUser from "./RegisterUser"
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Profile from "./Profile";
import Meetings from "./Meetings";

declare module '@mui/material/styles' {
  interface Palette {
    cultured: Palette['primary'];
  }
  interface PaletteOptions {
    cultured: PaletteOptions['primary'];
  }
}

const theme = createTheme({
  palette: {
    // Light: imperial Red, Main: firebrick
    primary: {
      light: '#F02D3A',
      main: '#BB0A21',
    },
    // Light: Bright Navy Blue, Main: prussian blue
    secondary: {
      light: '#3379C2',
      main: '#0E2A47',
    },
    cultured: {
      main: '#F4F5F6',
    },
  },
  shape: {
    borderRadius: "0.75rem",
  },
});

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <Routes>
          <Route path="/" element={ <Login /> } />
          <Route path="/register" element={ <Register /> } />
          <Route path="/dashboard-mentee" element={ <DashboardMentee /> } />
          <Route path="/browse-mentors" element={ <BrowseMentors /> } />
          <Route path="/workshops-mentee" element={ <WorkshopsMentee /> } />
          <Route path="/dashboard-mentor" element={ <DashboardMentor /> } />
          <Route path="/meetings" element={ <Meetings /> } />
          <Route path="/workshops-mentor" element={ <WorkshopsMentor /> } />
          <Route path="/register-user" element={ <RegisterUser /> } />
          <Route path="/profile" element={ <Profile /> } />
        </Routes>
      </ThemeProvider>
    </div>
  );
}

export default App;
