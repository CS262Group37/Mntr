import React, { useEffect } from "react";
import "./App.css";
import { BiUser } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import Dropdown from "./components/Dropdown";
import LoginButton from "./components/LoginButton";
import axios from "axios";

function RegisterUser() {
  const [role, setRole] = React.useState<string>("mentor");

  const [bizArea, setBizArea] = React.useState<string>("mentor");
  const [topics, setTopics] = React.useState<string[]>();
  const [ratings, setRatings] = React.useState<number[]>();

  useEffect(() => {
    axios.get("/api/admin/get-skills").then((res: any) => {
      const skills = res.data;
      console.log(skills);
    });
  }, []);

  const [psword, setPsword] = React.useState<string>("");

  const register = () => {};

  const RegisterAdmin = (
    <div>
      <TextInput
        type="password"
        value={psword}
        onChange={(e: any) => {
          setPsword(e.target.value);
        }}
        placeholder="Admin Password"
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      />
    </div>
  );

  const RegisterMentor = (
    <div>
      <TextInput
        type="password"
        value={psword}
        onChange={(e: any) => {
          setPsword(e.target.value);
        }}
        placeholder="Mentor Password"
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      />
    </div>
  );

  const RegisterMentee = (
    <div>
      <TextInput
        type="password"
        value={psword}
        onChange={(e: any) => {
          setPsword(e.target.value);
        }}
        placeholder="Mentee Password"
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      />
    </div>
  );

  var userFields = <div></div>;

  switch (role) {
    case "mentor": {
      userFields = RegisterMentor;
      break;
    }

    case "mentee": {
      userFields = RegisterMentee;
      break;
    }

    case "admin": {
      userFields = RegisterAdmin;
      break;
    }
  }

  return (
    <div className="fixed h-full w-full">
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto pt-[5%] pb-[5%] flex text-prussianBlue overflow-scroll overflow-x-auto">
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            {/* Inputs */}
            <div className="flex flex-col space-y-8 pt-[8%]">
              <Dropdown
                values={["mentor", "mentee", "admin"]}
                labels={["Mentor", "Mentee", "Admin"]}
                onChange={(e: any) => {
                  setRole(e.target.value);
                }}
                icon={<BiUser className="text-4xl m-4 mr-0" />}
              ></Dropdown>
              {userFields}
            </div>

            <div className="pt-[32px]">
              <div className="pt-[32px]">
                <LoginButton value="Register" onClick={register} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterUser;
