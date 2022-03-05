import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBar from "./components/NavBar";

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
      <h1>{mentor.firstName + " " + mentor.lastName}</h1>
    </div>
  );
};

function BrowseMentors() {
  const [mentors, setMentors] = React.useState<UserData[]>([]);

  // Get recommended mentors
  useEffect(() => {
    axios.get("/api/matching/relation-recommendations").then((res) => {
      const newMentors: any[] = [];

      // Sort by compatibility
      res.data.sort((e1: any, e2: any) => {
        return e2.compatibility - e1.compatibility;
      });

      console.log(res.data);

      // Get user data for all mentors
      for (let i = 0; i < res.data.length; i++) {
        const element = res.data[i];

        const mentorID: number = element.userID;

        newMentors.push(
          axios
            .post("/api/users/get-user-data", { userID: mentorID })
            .then((res) => {
              return {
                email: res.data.email,
                firstName: res.data.firstname,
                lastName: res.data.lastname,
                avatar: res.data.profilepicture,
                role: res.data.role,
                businessArea: res.data.businessarea,
              };
            })
        );
      }
      Promise.all(newMentors).then((res: UserData[]) => {
        setMentors(res);
      });
    });
  }, []);

  return (
    <div className="fixed h-full w-full">
      <NavBar activeStr="Browse mentors" mentors={[]} />

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        {/* <div className="h-full w-full p-6 flex flex-col overflow-auto"> */}
        {mentors.map((mentor) => {
          console.log(mentors);
          console.log("bruh");
          return <MentorCard mentorData={mentor} />;
        })}
        {/* </div> */}
      </div>
    </div>
  );
}

export default BrowseMentors;
