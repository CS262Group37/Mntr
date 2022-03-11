import React from "react";
import "./App.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { BiUser, BiLockAlt } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import LoginButton from "./components/LoginButton";
import Dropdown from "./components/Dropdown";
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

  const navigate = useNavigate();

  const login = async () => {
    try {
      const res = await axios.post("/api/auth/login", {
        email: email,
        password: psword,
        role: role,
      });
      navigate("/dashboard-" + role);
    } catch (error: any) {
      console.log(error.response);
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
              {/* <Box sx={{ "& > :not(style)": { m: 1 } }}> */}
              {/* <FormControl variant="standard">
                <InputLabel htmlFor="email">E-mail address</InputLabel>
                <Input
                  id="email"
                  startAdornment={
                    <InputAdornment position="start">
                      <BiUser className="font-xl" />
                    </InputAdornment>
                  }
                />
              </FormControl>
              <TextField
                id="input-with-icon-textfield"
                label="TextField"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <BiUser className="text-3xl" />
                    </InputAdornment>
                  ),
                }}
                variant="standard"
              />
              <Box
                sx={{
                  display: "flex",
                  alignItems: "flex-end",
                  fontFamily: "Nunito",
                  fontSize: 20,
                }}
              >
                <TextField
                  required
                  id="input-with-sx"
                  label="E-mail address"
                  variant="standard"
                  color="primary"
                  InputProps={
                    {
                      startAdornment: <BiUser className="text-4xl m-2 mt-6 text-prussianBlue" />
                    }
                  }
                  sx={{
                    input: {
                      color: "#0E2A47",
                      fontFamily: "Nunito",
                      fontSize: 20,
                      padding: 2,
                      marginTop: 2,
                      paddingLeft: 0,
                    },
                    label: {
                      color: "#0E2A47",
                      fontFamily: "Nunito",
                      fontSize: 20,
                      padding: 2,
                      paddingLeft: 1,
                    },
                  }}
                  fullWidth
                />
              </Box> */}

              {/* <FormControl variant="standard"> */}
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
              {/* </FormControl> */}

              {/* TODO Implement forget password feature. Might not be worth */}
              {/* <p className="text-right text-lg pt-1 underline">
                Forgot password?
              </p> */}
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
