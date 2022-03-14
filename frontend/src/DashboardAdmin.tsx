import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import {
  BiPlus,
} from "react-icons/bi";
import { TextField } from "@mui/material";

function DashboardAdmin() {
  const [skills, setSkills] = useState<string[]>([]);
  const [skill, setSkill] = useState<string>("");

  const [areas, setAreas] = useState<string[]>([]);
  const [area, setArea] = useState<string>("");

  const [topics, setTopics] = useState<string[]>([]);
  const [topic, setTopic] = useState<string>("");

  const [feedback, setFeedback] = useState<string[]>([]);

  useEffect(() => getSkills(), []);
  useEffect(() => getAreas(), []);
  useEffect(() => getTopics(), []);

  useEffect(() => getFeedback(), []);

  const getSkills = () => {
    axios.get("/api/admin/get-skills").then((res) => {
      const newSkills = res.data.map((skill: any) => skill.name);
      setSkills(newSkills);
    });
  };

  const getAreas = () => {
    axios.get("/api/admin/get-business-area").then((res) => {
      const newAreas = res.data.map((area: any) => area.name);
      setAreas(newAreas);
    });
  };

  const getTopics = () => {
    axios.get("/api/admin/get-topics").then((res) => {
      const newTopics = res.data.map((topic: any) => topic.name);
      setTopics(newTopics);
    });
  };

  const getFeedback = () => {
    axios.get("/api/admin/get-app-feedback").then((res) => {
      const newFeedback = res.data.map((feedback: any) => feedback.content);
      setFeedback(newFeedback);
    });
  };

  const addSkill = () => {
    axios
      .post("/api/admin/add-skill", { skillName: skill })
      .then((res) => getSkills());
  };
  const addArea = () => {
    axios
      .post("/api/admin/add-business-area", { businessAreaName: area })
      .then((res) => getAreas());
  };
  const addTopic = () => {
    axios
      .post("/api/admin/add-topic", { topicName: topic })
      .then((res) => getTopics());
  };

  return (
    <div className="grid grid-cols-3 gap-4 max-w-max mx-auto my-4">
      <h1 className="col-span-3 font-bold text-2xl px-1">Admin Dashboard</h1>
      {/* Skills */}
      <div className="flex flex-col space-y-1 border-2 rounded p-2">
        <h1 className="text-xl font-bold pb-2">Skills</h1>
        {skills.map((skill) => (
          <p>- {skill}</p>
        ))}
        <div>
          <TextField
            size="small"
            value={skill}
            onChange={(e: any) => setSkill(e.target.value)}
          ></TextField>
          <button
            className="bg-prussianBlue text-cultured text-xl ml-2 p-3 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
            onClick={addSkill}
          >
            <BiPlus className="h-4 w-4" />
          </button>
        </div>
      </div>
      {/* Areas */}
      <div className="flex flex-col space-y-1 border-2 rounded p-2">
        <h1 className="text-xl font-bold pb-2">Bussiness Areas</h1>
        {areas.map((area) => (
          <p>- {area}</p>
        ))}
        <div>
          <TextField
            size="small"
            value={area}
            onChange={(e: any) => setArea(e.target.value)}
          ></TextField>
          <button
            className="bg-prussianBlue text-cultured text-xl ml-2 p-3 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
            onClick={addArea}
          >
            <BiPlus className="h-4 w-4" />
          </button>
        </div>
      </div>
      {/* Topics */}
      <div className="flex flex-col space-y-1 border-2 rounded p-2">
        <h1 className="text-xl font-bold pb-2">Topics</h1>
        {topics.map((topic) => (
          <p>- {topic}</p>
        ))}
        <div>
          <TextField
            size="small"
            value={topic}
            onChange={(e: any) => setTopic(e.target.value)}
          ></TextField>
          <button
            className="bg-prussianBlue text-cultured text-xl ml-2 p-3 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
            onClick={addTopic}
          >
            <BiPlus className="h-4 w-4" />
          </button>
        </div>
      </div>
      {/* Feedback */}
      <div className="flex flex-col col-span-3 space-y-1 border-2 rounded p-2">
        <h1 className="font-bold text-xl pb-2">Feedback</h1>
        {feedback.map((f) => (
          <p>- {f}</p>
        ))}
      </div>
    </div>
  );
}

export default DashboardAdmin;
