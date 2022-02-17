import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";

function App() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");
  const [firstName, setFirstName] = React.useState<string>("");
  const [lastName, setLastName] = React.useState<string>("");
  const [role, setRole] = React.useState<string>("");

  const login = async () => {
    const res = await axios.post("/api/auth/login", {
      email: email,
      password: psword,
    });
  };

  const register = async () => {
    const res = await axios.post("/api/auth/register", {
      email: email,
      password: psword,
      firstName: firstName,
      lastName: lastName,
      role: role
    });
  };

  const getUsers = async () => {
    const res = await axios.get("/api/auth/users");
    console.log(res);
  };

  return (
    <div className="App">
      <button onClick={register}>Register</button>
      <input
        onChange={(e) => {
          setEmail(e.target.value);
        }}
      ></input>
      <input
        onChange={(e) => {
          setPsword(e.target.value);
        }}
      ></input>
      <input
        onChange={(e) => {
          setFirstName(e.target.value);
        }}
      ></input>
      <input
        onChange={(e) => {
          setLastName(e.target.value);
        }}
      ></input>
      <input
        onChange={(e) => {
          setRole(e.target.value);
        }}
      ></input>
      <button onClick={login}>Login</button>
      <input
        onChange={(e) => {
          setEmail(e.target.value);
        }}
      ></input>
      <input
        onChange={(e) => {
          setPsword(e.target.value);
        }}
      ></input>
      <button onClick={getUsers}>Users</button>
    </div>
  );
}

export default App;
