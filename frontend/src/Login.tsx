import React from "react";
import "./App.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { BiUser, BiLockAlt } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import LoginButton from "./components/LoginButton";
import Dropdown from "./components/Dropdown";

function Login() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");
  const [role, setRole] = React.useState<string>("mentor");

  const navigate = useNavigate();

  const login = async () => {

    try {
      const res = await axios.post("/api/auth/login", {
        email: email,
        password: psword,
        role: role,
      });
      navigate("/dashboard-" + role)
    } catch (error: any) {
      console.log(error.response);
    }
  };

  return (
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto flex text-prussianBlue overflow-scroll overflow-x-auto">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            <h2 className="text-4xl pt-[10%]">
              Welcome to <span className="font-bold text-firebrick">Mntr</span>
            </h2>
            <p className="text-2xl">
              Here's where you can learn a new skill or share your knowledge
            </p>

            {/* Inputs */}
            <div className="flex flex-col space-y-8 pt-[6%]">
              {/* Role input */}
              <Dropdown
                values={["mentor", "mentee", "admin"]}
                labels={["Mentor", "Mentee", "Admin"]}
                onChange={(e: any) => {
                  setRole(e.target.value);
                }}
                icon={<BiUser className="text-4xl m-4 mr-0" />}
              />

              {/* E-mail address input */}
              <TextInput
                type="email"
                value={email}
                onChange={(e: any) => {
                  setEmail(e.target.value);
                }}
                placeholder="E-mail address"
                icon={<BiUser className="text-4xl m-4 mr-0" />}
              />

              {/* Password input */}
              <div>
                <TextInput
                  type="password"
                  value={psword}
                  onChange={(e: any) => {
                    setPsword(e.target.value);
                  }}
                  placeholder="Password"
                  icon={<BiLockAlt className="text-4xl m-4 mr-0" />}
                />

                <p className="text-right text-lg pt-1 underline">
                  Forgot password?
                </p>
                <Dropdown
                  values={["mentor", "mentee", "admin"]}
                  labels={["Mentor", "Mentee", "Admin"]}
                  onChange={(e: any) => {
                    setRole(e.target.value);
                  }}
                  icon={<BiUser className="text-4xl m-4 mr-0" />}
                />
              </div>
            </div>

            <LoginButton value="Login" onClick={login} />

            {/* Registration link */}
            <p className="text-2xl m-auto pt-[5%]">
              Don't have an account yet?{" "}
              <span className="font-bold underline text-imperialRed">
                <Link to="/register">Register now!</Link>
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
