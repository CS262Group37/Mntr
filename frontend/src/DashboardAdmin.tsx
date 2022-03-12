import React, { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import NavBarMentor from "./components/NavBarMentor";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent, BiCalendarPlus, BiPlus } from "react-icons/bi";
import { Avatar, Divider, TextField } from "@mui/material";
import { Navigate, useLocation } from "react-router-dom";
import MeetingCardMentor from "./components/MeetingCardMentor";
import MenteeDetails from "./components/MenteeDetails";

function DashboardAdmin() {
  const [skills, setSkills] = useState<string[]>([]);
  const [skill, setSkill] = useState<string>("");

  // useEffect(() => {

  // }, []);

  useEffect(() => getSkills, []);

  const getSkills = () => {
    axios.get("/api/admin/get-skills").then((res) => {
      const newSkills = res.data.map((skill: any) => skill.name);
      setSkills(newSkills);
    });
  };

  const addSkill = () => {
    axios
      .post("/api/admin/add-skill", { skillName: skill })
      .then((res) => getSkills());
  };

  return (
    <div className="fixed h-full w-full">
      {/* Main flexbox */}
      <div className="flex flex-row items-stretch  font-display p-4">
        <div className="flex flex-col space-y-1 border-2 rounded p-2">
          <h1 className="text-xl font-bold pb-2">Skills</h1>
          {skills.map((skill) => (
            <p>- {skill}</p>
          ))}
          <div> <TextField
          size="small"
            value={skill}
            onChange={(e: any) => setSkill(e.target.value)}
          ></TextField>
          <button
              className="bg-prussianBlue text-cultured text-xl ml-2 p-3 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
              onClick={addSkill}
            >
              <BiPlus className="h-4 w-4" />
            </button></div>
         
        </div>
      </div>
    </div>
  );
}

export default DashboardAdmin;
