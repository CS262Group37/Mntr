import React from "react";
import "./App.css";
import axios from "axios";
import { Route, Link } from "react-router-dom"
import { BiUser, BiLockAlt } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";

function Login() {
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
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto flex text-prussianBlue">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-between space-y-10">
            <h2 className="text-4xl">Welcome to <span className="font-bold text-firebrick">Website Name</span></h2>
            <p className="text-2xl">Here's where you can learn a new skill or share your knowledge</p>

            {/* E-mail address input */}
            <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
              <BiUser className="text-4xl m-4 mr-0" />
              <input
                className="bg-cultured bg-opacity-0 text-2xl p-4 pl-3 text-prussianBlue w-full"
                placeholder="E-mail address"
                onChange={(e) => {
                  setEmail(e.target.value);
                }}
              ></input>
            </div>

            {/* Password input */}
            <div>
              <div className="flex flex-row bg-cultured text-2xl text-prussianBlue w-full border-b-2 border-imperialRed">
                <BiLockAlt className="text-4xl m-4 mr-0" />
                <input
                  className="bg-cultured bg-opacity-0 text-2xl p-4 pl-3 text-prussianBlue w-full"
                  placeholder="Password"
                  type="password"
                  onChange={(e) => {
                    setPsword(e.target.value);
                  }}
                ></input>
              </div>
              <p className="text-right text-lg pt-1 underline">Forgot password?</p>
            </div>
            
            {/* Login button */}
            <button
              className="bg-firebrick text-cultured text-2xl w-48 p-4 m-auto rounded-full shadow-md"
              onClick={login}
            >Login</button>

            <p className="text-2xl m-auto">Don't have an account yet? <span className="font-bold underline text-imperialRed"><Link to="/register">Register now!</Link></span></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;