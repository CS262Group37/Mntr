import React from "react";
import "./App.css";
import axios from "axios";
import { BiUser, BiLockAlt, BiEnvelope } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import { Link } from "react-router-dom";
import LoginButton from "./components/LoginButton";

// TODO password confirmation

function Register() {
  const [email, setEmail] = React.useState<string>("");
  const [psword, setPsword] = React.useState<string>("");
  const [pswordConf, setPswordConf] = React.useState<string>("");
  const [firstName, setFirstName] = React.useState<string>("");
  const [lastName, setLastName] = React.useState<string>("");
  const [role, setRole] = React.useState<string>("");

  const register = async () => {
    const res = await axios.post("/api/auth/register-account", {
      email: email, 
      password: psword,
      firstName: firstName,
      lastName: lastName
    });
  };

  return(
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto pt-[5%] pb-[5%] flex text-prussianBlue overflow-scroll overflow-x-auto">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            <h2 className="text-4xl">
              Register to {" "}
              <span className="font-bold text-firebrick">Website Name</span>
            </h2>
            <p className="text-2xl">
              Here's where you can learn a new skill or share your knowledge
            </p>

            {/* Inputs */}
            <div className="flex flex-col space-y-8 pt-[8%]">
              {/* E-mail address input */}
              <TextInput
                type="text"
                value={email}
                onChange={(e: any) => {
                  setEmail(e.target.value);
                }}
                placeholder="E-mail address"
                icon={<BiEnvelope className="text-4xl m-4 mr-0" />}
              />

              {/* First name input */}
              <TextInput
                type="text"
                value={firstName}
                onChange={(e: any) => {
                  setFirstName(e.target.value);
                }}
                placeholder="First name"
                icon={<BiUser className="text-4xl m-4 mr-0" />}
              />

              {/* Last name input */}
              <TextInput
                type="text"
                value={lastName}
                onChange={(e: any) => {
                  setLastName(e.target.value);
                }}
                placeholder="Last name"
                icon={<BiUser className="text-4xl m-4 mr-0" />}
              />

              {/* Password input */}
              <TextInput
                type="password"
                value={psword}
                onChange={(e: any) => {
                  setPsword(e.target.value);
                }}
                placeholder="Password"
                icon={<BiLockAlt className="text-4xl m-4 mr-0" />}
              />

              {/* Password confirmation */}
              <TextInput
                type="password"
                value={pswordConf}
                onChange={(e: any) => {
                  setPswordConf(e.target.value);
                }}
                placeholder="Password confirmation"
                icon={<BiLockAlt className="text-4xl m-4 mr-0" />}
              />
            </div>

            <div className="pt-[32px]">
              <LoginButton 
                value="Register"
                onClick={register}
              />
            </div>

            {/* Registration link */}
            <p className="text-2xl underline m-auto pt-[10%]">
              <Link to="/">Back to login</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;