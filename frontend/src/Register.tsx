import { useState } from "react";
import "./App.css";
import axios from "axios";
import { BiUser, BiLockAlt, BiEnvelope } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import { Link } from "react-router-dom";
import LoginButton from "./components/LoginButton";
import {useNavigate} from 'react-router-dom';
import bcrypt from "bcryptjs";

function Register() {
  const [email, setEmail] = useState<string>("");
  const [psword, setPsword] = useState<string>("");
  const [pswordConf, setPswordConf] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");

  const [error1, setError1] = useState<boolean>(false);
  const [error2, setError2] = useState<boolean>(false);

  const navigate = useNavigate();

  const register = async () => {

    if (psword === pswordConf && email.includes("@")) {
      const res = await axios.post("/api/auth/register-account", {
        email: email, 
        password: psword,
        firstName: firstName,
        lastName: lastName,
      });
      navigate("/register-user");
    } else if (psword !== pswordConf) {
      console.log(`1: ${psword}, 2: ${pswordConf}`);
      setError1(true);
    } else {
      console.log(email);
      setError2(true);
    }
    
  };

  const iconCss = "text-4xl m-2 mt-6 text-prussianBlue";

  return(
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto pt-[5%] pb-[5%] flex text-prussianBlue overflow-auto text-center">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            <h2 className="text-4xl">
              Register to {" "}
              <span className="font-bold text-firebrick">Mntr</span>
            </h2>
            <p className="text-2xl">
              Here's where you can learn a new skill or share your knowledge
            </p>

            {/* Inputs */}
            <div className="flex flex-col space-y-8 pt-[8%]">
              {/* E-mail address input */}
              <TextInput
                type="email"
                value={email}
                onChange={(e: any) => {
                  setEmail(e.target.value);
                }}
                placeholder="E-mail address"
                icon={<BiEnvelope className={iconCss} />}
              />

              {/* First name input */}
              <TextInput
                type="text"
                value={firstName}
                onChange={(e: any) => {
                  setFirstName(e.target.value);
                }}
                placeholder="First name"
                icon={<BiUser className={iconCss} />}
              />

              {/* Last name input */}
              <TextInput
                type="text"
                value={lastName}
                onChange={(e: any) => {
                  setLastName(e.target.value);
                }}
                placeholder="Last name"
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

              {/* Password confirmation */}
              <TextInput
                type="password"
                value={pswordConf}
                onChange={(e: any) => {
                  setPswordConf(e.target.value);
                }}
                placeholder="Password confirmation"
                icon={<BiLockAlt className={iconCss} />}
              />
            </div>

            <div>
              <LoginButton value="Register" onClick={register} />
              {error1 && <h2 className="text-imperialRed font-semibold mt-2">Passwords do not match</h2>}
              {error2 && <h2 className="text-imperialRed font-semibold mt-2">Invalid e-mail address</h2>}
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