import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios from "axios";

function App() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");


  const login = () => {
    axios
      .post("/api/auth/login", {
        email: email,
        password: psword,
      })
      .then((res) => console.log(res));
  };

  return (
    <div className="App">
      <button onClick={login}>Login</button>
      <input onChange={(e) => {setEmail(e.target.value)}}></input>
      <input onChange={(e) => {setPsword(e.target.value)}}></input>
    </div>
  );
}

export default App;
