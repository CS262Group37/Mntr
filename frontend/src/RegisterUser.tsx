import React from "react";
import "./App.css";
import { BiUser } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import Dropdown from "./components/Dropdown";

function RegisterUser() {
  const [role, setRole] = React.useState<string>("mentor");

  var x = (
    <div className="flex flex-col space-y-8 pt-[8%]">
      <Dropdown
        values={["mentor", "mentee", "admin"]}
        labels={["Mentor", "Mentee", "Admin"]}
        onChange={(e: any) => {
          setRole(e.target.value);
        }}
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      ></Dropdown>
    </div>
  );
  if (role === "mentor") {
    x = (
      <div className="flex flex-col space-y-8 pt-[8%]">
        <Dropdown
          values={["mentor", "mentee", "admin"]}
          labels={["Mentor", "Mentee", "Admin"]}
          onChange={(e: any) => {
            setRole(e.target.value);
          }}
          icon={<BiUser className="text-4xl m-4 mr-0" />}
        ></Dropdown>
        <TextInput
          type="text"
          value=""
          onChange={(e: any) => {}}
          placeholder="Mentor"
          icon={<BiUser className="text-4xl m-4 mr-0" />}
        />
      </div>
    );
  } else if (role === "mentee") {
    x = (
      <div className="flex flex-col space-y-8 pt-[8%]">
        <Dropdown
          values={["mentor", "mentee", "admin"]}
          labels={["Mentor", "Mentee", "Admin"]}
          onChange={(e: any) => {
            setRole(e.target.value);
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
  } else if (role === "admin") {
    x = (<div className="flex flex-col space-y-8 pt-[8%]">
    <Dropdown
      values={["mentor", "mentee", "admin"]}
      labels={["Mentor", "Mentee", "Admin"]}
      onChange={(e: any) => {
        setRole(e.target.value);
      }}
      icon={<BiUser className="text-4xl m-4 mr-0" />}
    ></Dropdown>
      <TextInput
        type="text"
        value=""
        onChange={(e: any) => {}}
        placeholder="Admin"
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      />
      </div>
    );
  }

  return (
    <div className="fixed h-full w-full">
      <div className="flex flex-row items-stretch h-full align-middle font-display">
        <LeftPanel />

        {/* White half */}
        <div className="bg-cultured h-full w-3/5 m-auto pt-[5%] pb-[5%] flex text-prussianBlue overflow-scroll overflow-x-auto">
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            {/* Inputs */}
            {x}
            <div className="pt-[32px]"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterUser;
