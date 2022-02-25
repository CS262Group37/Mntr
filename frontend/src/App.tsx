import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Login from "./Login";
import Register from "./Register";
import { Routes, Route } from "react-router-dom";
import DashboardMentee from "./DashboardMentee";
import DashboardMentor from "./DashboardMentor";
import BrowseMentors from "./BrowseMentors";
import Workshops from "./Workshops";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={ <Login /> } />
        <Route path="/register" element={ <Register /> } />
        <Route path="/dashboard-mentee" element={ <DashboardMentee /> } />
        <Route path="/browse-mentors" element={ <BrowseMentors /> } />
        <Route path="/workshops" element={ <Workshops /> } />
        <Route path="/dashboard-mentor" element={ <DashboardMentor /> } />
      </Routes>
    </div>
  );
}

export default App;
