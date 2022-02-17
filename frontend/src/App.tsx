import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";

function App() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");
  const [token, setToken] = React.useState<string>("");

  const login = async () => {
    const res = await axios.post("/api/auth/login", {
      email: email,
      password: psword,
    });
    setToken(res.headers.authorization);
  };

  const getUsers = async () => {
    const headers = {
      authorization: token,
    };
    const res = await axios.get("/api/auth/users", { headers });
    console.log(res);
  };

  return (
    <div className="App">
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
      <p>{token}</p>
      <button onClick={getUsers}>Users</button>
    </div>
  );
}

export default App;
