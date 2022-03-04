import React, { useEffect } from "react";
import "./App.css";
import { BiBriefcase, BiUser } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import Dropdown from "./components/Dropdown";
import LoginButton from "./components/LoginButton";
import axios from "axios";
import {
  Box,
  Checkbox,
  Chip,
  Input,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Select,
} from "@mui/material";

interface skillRating {
  name: string;
  rating: number;
}

function RegisterUser() {
  const [role, setRole] = React.useState<string>("mentor");

  const [area, setArea] = React.useState<string>("");
  const [selectedTopics, setSelectedTopics] = React.useState<string[]>([]);

  const [topics, setTopics] = React.useState<string[]>([]);
  const [areas, setAreas] = React.useState<string[]>([]);
  const [skills, setSkills] = React.useState<skillRating[]>([]);

  useEffect(() => {
    axios.get("/api/admin/get-skills").then((res: any) => {
      setSkills(
        res.data.map((skill: any) => ({ name: skill.name, rating: 0 }))
      );
    });
    axios.get("/api/admin/get-business-area").then((res: any) => {
      console.log(res.data);
      setAreas(res.data.map((area: any) => area.name));
    });
    axios.get("/api/admin/get-topics").then((res: any) => {
      console.log(res.data);
      setTopics(res.data.map((topic: any) => topic.name));
    });
  }, []);

  const [psword, setPsword] = React.useState<string>("");

  const register = () => {
    switch (role) {
      case "admin":
        axios
          .post("/api/auth/register-user", {
            role: "admin",
            adminPassword: psword,
          })
          .then((res: any) => {
            console.log(res);
          });
    }
  };

  const updateRating = (value: number, index: number) => {
    console.log(skills);
    console.log(value, index);
    const newSkills = [...skills];
    newSkills[index] = { name: skills[index].name, rating: value };
    setSkills(newSkills);
  };

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
      <Dropdown
        values={areas}
        labels={areas}
        onChange={(e: any) => {
          setArea(e.target.value);
        }}
        icon={<BiBriefcase className="text-4xl m-4 mr-0" />}
      ></Dropdown>
      <Select
        labelId="demo-multiple-chip-label"
        id="demo-multiple-chip"
        multiple
        value={selectedTopics}
        onChange={(e: any) => {
          setSelectedTopics(e.target.value);
        }}
        input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
        renderValue={(selected) => (
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
            {selected.map((value) => (
              <Chip key={value} label={value} />
            ))}
          </Box>
        )}
      >
        {topics.map((topic) => (
          <MenuItem key={topic} value={topic}>
            <Checkbox checked={selectedTopics.indexOf(topic) > -1} />
            <ListItemText primary={topic} />
          </MenuItem>
        ))}
      </Select>
    </div>
  );

  const RegisterMentee = (
    <div>
      <Dropdown
        values={areas}
        labels={areas}
        onChange={(e: any) => {
          setArea(e.target.value);
        }}
        icon={<BiBriefcase className="text-4xl m-4 mr-0" />}
      ></Dropdown>
      <Select
        labelId="demo-multiple-chip-label"
        id="demo-multiple-chip"
        multiple
        value={selectedTopics}
        onChange={(e: any) => {
          setSelectedTopics(e.target.value);
        }}
        input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
        renderValue={(selected) => (
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
            {selected.map((value) => (
              <Chip key={value} label={value} />
            ))}
          </Box>
        )}
      >
        {topics.map((topic) => (
          <MenuItem key={topic} value={topic}>
            <Checkbox checked={selectedTopics.indexOf(topic) > -1} />
            <ListItemText primary={topic} />
          </MenuItem>
        ))}
      </Select>
      {skills.map((skill, index) => (
        <div>
          <label>{skill.name}</label>
          <input
            key={index}
            type="number"
            value={skill.rating}
            onChange={(e: any) => {
              updateRating(e.target.value, index);
            }}
          ></input>
        </div>
      ))}
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
