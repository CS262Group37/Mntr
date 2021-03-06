import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import NavBarMentee from "./components/NavBarMentee";
import { Avatar, Rating, Typography } from "@mui/material";
import { BiPlus } from "react-icons/bi";

interface UserData {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics?: string[];
  ratings?: Rating[];
}

interface Rating {
  skill: string;
  rating: number;
}

interface CardProps {
  mentorData: UserData;
}

const MentorCard: React.FC<CardProps> = (props) => {
  const navigate = useNavigate();
  const mentor = props.mentorData;

  // TODO connect to a mentor function
  const connectMentor = () => {
    console.log(mentor.id);
    axios
      .post("/api/relations/create-relation", { mentorID: mentor.id })
      .then((res: any) => {
        console.log(res);
        navigate(`/dashboard-mentee?mentor=${mentor.id}`);
      });
    return;
  };

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md m-auto mt-5 mb-5 w-[70%] text-prussianBlue p-8 rounded-xl text-left">
      <div className="flex flex-row mb-6 justify-between">
        <Avatar
          className="m-2"
          alt={mentor.firstName + " " + mentor.lastName}
          src={mentor.avatar}
          sx={{ width: 130, height: 130 }}
        />
        {/* Mentor name & topics */}
        <div className="flex flex-col text-left m-auto ml-0 pl-4 space-y-1">
          <Link
            to={"/profile?id=" + mentor.id}
            className="font-semibold hover:font-bold text-3xl"
          >
            {mentor.firstName + " " + mentor.lastName}
          </Link>

          {/* Topics */}
          <p className="text-lg font-body">
            {mentor.topics?.map((topic, i, { length }) => {
              if (i === length - 1) {
                return <span>{topic}</span>;
              } else return <span>{topic + ", "}</span>;
            })}
          </p>
          <p className="font-body">{mentor.businessArea}</p>
        </div>

        <button
          className="bg-firebrick text-cultured text-xl min-w-80 p-4 m-auto mt-2 mr-2 ml-5 rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200"
          onClick={connectMentor}
        >
          <BiPlus className="h-12 w-12 p-2" />
        </button>
      </div>

      {/* Ratings */}
      <div className="flex flex-row justify-evenly overflow-clip flex-wrap">
        {mentor.ratings?.map((rating) => {
          return (
            <div className="p-1">
              <Typography component="legend">{rating.skill}</Typography>
              <Rating name="read-only" value={rating.rating} readOnly />
            </div>
          );
        })}
      </div>
    </div>
  );
};

function BrowseMentors() {
  const [mentors, setMentors] = React.useState<UserData[]>([]);
  const [mentor, setMentor] = React.useState<UserData[]>([]);

  // Get recommended mentors
  useEffect(() => {
    axios.get("/api/matching/relation-recommendations").then(async (res) => {
      console.log(res.data);
      var newMentors: UserData[] = [];
      var newTopics: string[][] = [];
      var newRatings: Rating[][] = [];

      // Sort recommended mentors by compatibility
      res.data.sort((e1: any, e2: any) => {
        return e2.compatibility - e1.compatibility;
      });

      // Get user data for all mentors
      for (let i = 0; i < res.data.length; i++) {
        const element = res.data[i];

        const mentorID: number = element.userID;

        // Get mentor data
        await axios
          .post("/api/users/get-user-data", { userID: mentorID })
          .then((res) => {
            newMentors.push({
              id: mentorID,
              email: res.data.email,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
              businessArea: res.data.businessarea,
            });
          });

        // Get topics
        await axios
          .post("/api/users/get-user-topics", { userID: mentorID })
          .then((res) => {
            const arr = res.data.map((t: any) => t.topic);
            newTopics.push(arr);
          });

        // Get ratings
        await axios
          .post("/api/users/get-user-ratings", { userID: mentorID })
          .then((res) => {
            const arr = res.data;
            // Sort alphabetically by skill
            arr.sort((e1: any, e2: any) => {
              return e2.skill > e1.skill ? -1 : 1;;
            });

            console.log(arr);

            newRatings.push(res.data);
          });
      }

      var newMentorsAll: UserData[] = [];
      for (let i = 0; i < newMentors.length; i++) {
        const element = newMentors[i];

        newMentorsAll.push({
          id: element.id,
          email: element.email,
          firstName: element.firstName,
          lastName: element.lastName,
          avatar: element.avatar,
          role: element.role,
          businessArea: element.businessArea,
          topics: newTopics[i],
          ratings: newRatings[i],
        });
      }

      setMentors(newMentorsAll);
    });
  }, []);

  return (
    <div className="fixed h-full w-full">
      <NavBarMentee activeStr="Browse mentors" />

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
