import React from "react";
import "./App.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { BiUser, BiLockAlt } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import LoginButton from "./components/LoginButton";
import Dropdown from "./components/Dropdown";
import bcrypt from "bcryptjs";
import {
  Box,
  FormControl,
  Input,
  InputAdornment,
  InputLabel,
  TextField,
} from "@mui/material";

// TODO print error message when user enters wrong credentials

function Login() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");
  const [role, setRole] = React.useState<string>("mentor");
  const [error, setError] = React.useState<boolean>(false);

  const navigate = useNavigate();

  const login = async () => {
    try {
      await axios.get("/api/auth/login2", { params: { email: email } }).then((res) => {
        console.log(res.data);
        const [hash, salt] = res.data;
        console.log(hash);
        console.log(salt);
      })
      navigate("/dashboard-" + role);
    } catch (error: any) {
      console.log(error.response);
      setError(true);
    }
  };

  const iconCss = "text-4xl m-2 mt-6 text-prussianBlue";

  return (
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto flex text-prussianBlue overflow-scroll overflow-x-auto">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10 text-center">
            <h2 className="text-4xl pt-[0%]">
              Welcome to <span className="font-bold text-firebrick">Mntr</span>
            </h2>
            <p className="text-2xl">
              Here's where you can learn a new skill or share your knowledge
            </p>

            {/* Inputs */}

            <div className="flex flex-col space-y-8 pt-[0%]">
              {/* Role input */}
              <FormControl variant="standard">
                <Dropdown
                  values={["mentor", "mentee", "admin"]}
                  labels={["Mentor", "Mentee", "Admin"]}
                  mainLabel="Role"
                  defaultVal={role}
                  onChange={(e: any) => {
                    setRole(e.target.value);
                  }}
                  icon={
                    <BiUser className="text-prussianBlue text-4xl m-auto ml-2 max-w-[33px]" />
                  }
                />
              </FormControl>

              {/* E-mail address input */}
              <TextInput
                type="email"
                value={email}
                onChange={(e: any) => {
                  setEmail(e.target.value);
                }}
                placeholder="E-mail address"
                icon={<BiUser className={iconCss} />}
              />

              {/* Password input */}
              <TextInput
                type="password"
                value={psword}
                onChange={(e: any) => {
                  setPsword(e.target.value);
                }}
                placeholder="Password"
                icon={<BiLockAlt className={iconCss} />}
              />

              {/* TODO Implement forget password feature. Might not be worth */}
              {/* <p className="text-right text-lg pt-1 underline">
                Forgot password?
              </p> */}
            </div>

            <div>
              <LoginButton value="Login" onClick={login} />
              {error && <h2 className="text-imperialRed font-semibold mt-2">Wrong e-mail, password or role</h2>}
            </div>

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
