import React from "react";
import "./App.css";
import { BiUser } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import Dropdown from "./components/Dropdown";

function RegisterMentor() {
  // TODO Fields to register mentor

  return (
    <div className="flex flex-col space-y-8 pt-[8%]">
        <Dropdown
          values={["mentor", "mentee", "admin"]}
          labels={["Mentor", "Mentee", "Admin"]}
          onChange={(e: any) => {
            //setRole(e.target.value);
          }}
          icon={<BiUser className="text-4xl m-4 mr-0" />}
        ></Dropdown>
        <TextInput
          type="text"
          value=""
          onChange={(e: any) => {}}
          placeholder="Mentee"
          icon={<BiUser className="text-4xl m-4 mr-0" />}
        />
        <TextInput
          type="text"
          value=""
          onChange={(e: any) => {}}
          placeholder="Mentee"
          icon={<BiUser className="text-4xl m-4 mr-0" />}
        />
      </div>
  );
}

export default RegisterMentor;
