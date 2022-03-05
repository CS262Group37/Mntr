import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBar from "./components/NavBar";
import { Avatar } from "@mui/material";

interface UserData {
  email: string;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topic?: string[];
}

interface CardProps {
  mentorData: UserData;
}

const MentorCard: React.FC<CardProps> = (props) => {
  const mentor = props.mentorData;

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-6 rounded-xl text-left">
      {/* <h1>{mentor.firstName + " " + mentor.lastName}</h1> */}
      <div className="flex">
        <Avatar
          className="m-auto"
          alt={mentor.firstName + " " + mentor.lastName}
          src={mentor.avatar}
          sx={{ width: 80, height: 80 }}
        />
        {/* Mentor name & topic */}
        <div className="flex flex-col text-left m-auto pl-4 space-y-1">
          <h2 className="font-semibold text-3xl">
            {mentor.firstName + " " + mentor.lastName}
          </h2>
          <h3 className="text-xl">{mentor.topic}</h3>
        </div>
      </div>
    </div>
  );
};

function BrowseMentors() {
  const [mentors, setMentors] = React.useState<UserData[]>([]);
  const [topics, setTopics] = React.useState<string[][]>([]);
  const [ratings, setRatings] = React.useState<UserData[]>([]);

  // Get recommended mentors
  useEffect(() => {
    axios.get("/api/matching/relation-recommendations").then(async (res) => {
      var newMentors: UserData[] = [];
      var newTopics: string[][] = [];

      // Sort by compatibility
      res.data.sort((e1: any, e2: any) => {
        return e2.compatibility - e1.compatibility;
      });

      console.log(res.data);

      // Get user data for all mentors
      for (let i = 0; i < res.data.length; i++) {
        const element = res.data[i];

        const mentorID: number = element.userID;

        
        await axios
          .post("/api/users/get-user-data", { userID: mentorID })
          .then((res) => {
            newMentors.push({
              email: res.data.email,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
              businessArea: res.data.businessarea,
            });
          });

        await axios
          .post("/api/users/get-user-topics", { userID: mentorID })
          .then((res) => {
            const arr: string[] = [];
            res.data.map((t: any) => {
              arr.push(t.topic);
            })
            console.log(arr);
            newTopics.push(arr);
          });
      }

      var test:UserData[] = [];
      for (let i = 0; i < newMentors.length; i++) {
        const element = newMentors[i];
        console.log(element);
        console.log(newTopics[i]);
        
        test.push({
          email: element.email,
          firstName: element.firstName,
          lastName: element.lastName,
          avatar: element.avatar,
          role: element.role,
          businessArea: element.businessArea,
          topic: newTopics[i],
        })        
      }

      setMentors(test);
      console.log(mentors);
    });
  }, []);

  return (
    <div className="fixed h-full w-full">
      <NavBar activeStr="Browse mentors" mentors={[]} />

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        {mentors.map((mentor) => {
          return <MentorCard mentorData={mentor} />;
        })}
      </div>
    </div>
  );
}

export default BrowseMentors;
