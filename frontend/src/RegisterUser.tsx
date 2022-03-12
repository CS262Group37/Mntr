import React, { useEffect } from "react";
import "./App.css";
import { BiBriefcase, BiUser, BiClipboard } from "react-icons/bi";
import LeftPanel from "./components/LeftPanel";
import TextInput from "./components/TextInput";
import Dropdown from "./components/Dropdown";
import LoginButton from "./components/LoginButton";
import axios from "axios";
import {
  Box,
  Checkbox,
  Chip,
  FormControl,
  Input,
  InputLabel,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Select,
  Slider,
  TextField,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

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

  const [psword, setPsword] = React.useState<string>("");

  const navigate = useNavigate();

  const iconCss = "text-prussianBlue text-4xl m-auto ml-2 max-w-[33px]";

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

  useEffect(() => {
    setArea(areas[0]);
  }, [areas]);

  const register = () => {
    switch (role) {
      case "admin":
        try {
          axios
            .post("/api/auth/register-user", {
              role: "admin",
              adminPassword: psword,
            })
            .then((res: any) => {
              navigate("/dashboard-admin");
            });
        } catch (e) {
          console.log(e);
        }

        break;

      case "mentor":
        try {
          axios
            .post("/api/auth/register-user", {
              role: "mentor",
              businessArea: area,
              topics: selectedTopics,
            })
            .then((res: any) => {
              navigate("/dashboard-mentor");
            });
        } catch (e) {
          console.log(e);
        }

        break;

      case "mentee":
        try {
          axios
            .post("/api/auth/register-user", {
              role: "mentee",
              businessArea: area,
              topics: selectedTopics,
              skills: skills.map((skill) => skill.name),
              ratings: skills.map((skill) => skill.rating),
            })
            .then((res: any) => {
              navigate("/dashboard-mentee");
            });
        } catch (e) {
          console.log(e);
        }

        break;
    }
  };

  const updateRating = (value: number, index: number) => {
    const newSkills = [...skills];
    newSkills[index] = { name: skills[index].name, rating: value };
    setSkills(newSkills);
  };

  const RegisterAdmin = (
    <>
      <TextInput
        type="password"
        value={psword}
        onChange={(e: any) => {
          setPsword(e.target.value);
        }}
        placeholder="Admin Password"
        icon={<BiUser className="text-4xl m-4 mr-0" />}
      />
    </>
  );

  const RegisterMentor = (
    <>
      <FormControl variant="standard">
        <Dropdown
          values={areas}
          labels={areas}
          mainLabel="Business area"
          defaultVal={area}
          onChange={(e: any) => {
            setArea(e.target.value);
          }}
          icon={<BiBriefcase className={iconCss} />}
        />
      </FormControl>

      <FormControl variant="standard">
        <InputLabel id="select-topics-label">
          <div className="flex flex-row">
            {/* <BiClipboard className="text-prussianBlue text-3xl m-auto ml-2 max-w-[33px]" /> */}
            <h1 className="font-display text-prussianBlue text-xl m-auto ml-3">
              Select topics
            </h1>
          </div>
        </InputLabel>
        <Select
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={selectedTopics}
          onChange={(e: any) => {
            setSelectedTopics(e.target.value);
          }}
          sx={{
            color: "#0E2A47",
            padding: 1,
            paddingLeft: 0,
          }}
          input={<Input id="select-multiple-chip" />}
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
      </FormControl>
    </>
  );

  const RegisterMentee = (
    <>
      <FormControl variant="standard">
        <Dropdown
          values={areas}
          labels={areas}
          mainLabel="Business area"
          defaultVal={area}
          onChange={(e: any) => {
            setArea(e.target.value);
          }}
          icon={<BiBriefcase className={iconCss} />}
        />
      </FormControl>

      <FormControl variant="standard">
        <InputLabel id="select-topics-label">
          <div className="flex flex-row">
            {/* <BiClipboard className="text-prussianBlue text-3xl m-auto ml-2 max-w-[33px]" /> */}
            <h1 className="font-display text-prussianBlue text-xl m-auto ml-3">
              Select topics
            </h1>
          </div>
        </InputLabel>
        {/* <InputLabel id="select-topics-label">Select topics</InputLabel> */}
        <Select
          labelId="select-topics-label"
          id="select-topics"
          variant="filled"
          multiple
          value={selectedTopics}
          onChange={(e: any) => {
            setSelectedTopics(e.target.value);
          }}
          sx={{
            color: "#0E2A47",
            padding: 1,
            paddingLeft: 0,
          }}
          input={<Input id="select-multiple-chip" />}
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
      </FormControl>

      <div className="flex flex-col space-y-4">
        {skills.map((skill, index) => (
          <div className="flex flex-col">
            <label className="text-xl m-auto ml-0 mr-3">{skill.name}: </label>
            {/* <input
              key={index}
              type="number"
              min={0}
              max={10}
              value={skill.rating}
              onChange={(e: any) => {
                updateRating(e.target.value, index);
              }}
            ></input> */}
            <Slider
              defaultValue={0}
              // getAriaValueText={valuetext}
              step={1}
              marks
              min={0}
              max={10}
              valueLabelDisplay="auto"
              onChange={(e: any) => {
                updateRating(e.target.value, index);
              }}
              className="m-1 ml-3 mr-3"
            />
            {/* <TextField
              inputProps={{ inputMode: "numeric", pattern: "[0-9]*" }}
            /> */}
          </div>
        ))}
      </div>
    </>
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
            <div className="flex flex-col space-y-10 pt-[8%]">
              <FormControl variant="standard">
                <Dropdown
                  values={["mentor", "mentee", "admin"]}
                  labels={["Mentor", "Mentee", "Admin"]}
                  mainLabel="Role"
                  defaultVal={role}
                  onChange={(e: any) => {
                    setRole(e.target.value);
                  }}
                  icon={<BiUser className={iconCss} />}
                />
              </FormControl>
              {userFields}
            </div>

            <div className="pt-[32px] m-auto">
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
