import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Login from "./Login";
import Register from "./Register";
import { Routes, Route } from "react-router-dom";
import DashboardMentee from "./DashboardMentee";
import DashboardMentor from "./DashboardMentor";
import RegisterUser from "./RegisterUser";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={ <Login /> } />
        <Route path="/register" element={ <Register /> } />
        <Route path="/register-user" element={ <RegisterUser /> } />
        <Route path="/dbmentee" element={ <DashboardMentee /> } />
        <Route path="/dbmentor" element={ <DashboardMentor /> } />
      </Routes>
    </div>
  );
}

export default App;
