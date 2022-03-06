import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBarMentee";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent } from "react-icons/bi";
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

interface MentorObject {
  firstName: string;
  lastName: string;
  avatar: string;
  topic: string;
  nextMeeting: Date;
}

interface MeetingProps {
  date: Date;
  feedback: string;
}

// Mentor details component
const MentorDetails: React.FC<MentorObject> = (props) => {
  // TODO schedule a meeting function
  const schedule = () => {
    return;
  };

  // Next meeting date formatting
  const weekday = props.nextMeeting.toLocaleString("default", {
    weekday: "long",
  });
  const month = props.nextMeeting.getMonth() + 1;
  const date =
    weekday +
    ", " +
    props.nextMeeting.getDate() +
    "." +
    month +
    "." +
    props.nextMeeting.getFullYear();

  return (
    <div className="flex flex-col m-10 mb-2 text-firebrick font-display">
      <div className="flex flex-row h-min">
        <div className="flex">
          {/* TODO Mentor profile pic */}
          <Avatar
            className="m-auto"
            alt={props.firstName + " " + props.lastName}
            src={props.avatar}
            sx={{ width: 80, height: 80 }}
          />

          {/* Mentor name & topic */}
          <div className="flex flex-col text-left m-auto pl-4 space-y-1">
            <h2 className="font-semibold text-3xl">
              {props.firstName + " " + props.lastName}
            </h2>
            <h3 className="text-xl">{props.topic}</h3>
          </div>
        </div>

        {/* Schedule meeting button */}
        <button
          className="bg-prussianBlue text-cultured text-xl w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-2"
          onClick={schedule}
        >
          Schedule a meeting
        </button>
      </div>

      {/* Next meeting date */}
      <div className="flex flex-row text-lg font-body m-5">
        <BiCalendarEvent className="mt-auto mb-auto text-3xl mr-1" />
        <p className="mt-auto mb-auto text-left">
          Your next meeting with {props.firstName} is on{" "}
          <span className="font-bold">{date}</span>
        </p>
      </div>
    </div>
  );
};

// Meeting component
const Meeting: React.FC<MeetingProps> = (props) => {
  const month = props.date.toLocaleString("default", { month: "long" });
  const date =
    month + " " + props.date.getDate() + ", " + props.date.getFullYear();

  return (
    <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md mt-5 mb-5 w-[100%] text-prussianBlue p-4 rounded-xl">
      {/* Heading & date */}
      <div className="flex flex-row text-2xl border-b-2 border-imperialRed justify-between">
        <h1 className="font-semibold mt-1 mb-3 ml-3 text-left">
          Individual meeting
        </h1>
        <div className="flex flex-row mr-3 mt-1 mb-3 text-right">
          <BiCalendarCheck className="text-3xl mr-1" />
          <h1>{date}</h1>
        </div>
      </div>

      {/* Mentor feedback */}
      <div className="font-body text-lg text-justify m-3 mb-1">
        <p>{props.feedback}</p>
      </div>
    </div>
  );
};

function DashboardMentee() {
  const [currentMentor, setCurrentMentor] = React.useState<UserData>({email: "", firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topic: []});
  const [mentors, setMentors] = React.useState<UserData[]>([]);

  // Get mentee-mentor relations and mentors' data
  useEffect(() => {
    axios.get("/api/relations/get-relations").then((res) => {
      const newMentors: UserData[] = [];

      for (let i = 0; i < res.data.length; i++) {
        const element = res.data[i];
        
        const mentorID: number = element.mentorid;
      
        axios.post("/api/users/get-user-data", {userID: mentorID}).then((res) => {
          const newMentor: UserData = {
            email: res.data.email,
            firstName: res.data.firstname,
            lastName: res.data.lastname,
            avatar: res.data.profilepicture,
            role: res.data.role,
            businessArea: res.data.businessarea,
          }

          newMentors.push(newMentor);
          setMentors(newMentors);
        });
      };

      // setCurrentMentor(mentors[0]);
    });
  }, []);

  const dummyDate1 = new Date("2022-02-04");
  const dummyDate2 = new Date("2022-01-27");
  const dummyDate3 = new Date("2022-01-24");

  const dummyText1 =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ornare in ut iaculis sapien, id orci, pulvinar dui. Dui pulvinar eget varius et, et elit vitae, blandit. Nam in risus laoreet tellus. Pellentesque id ultrices rhoncus viverra nullam pretium tristique quam. Nibh felis posuere in non lectus est. Quis nullam porta sed pellentesque dui. Sed phasellus in vitae mi amet enim blandit. Eu neque viverra aenean porta cras.";
  const dummyText2 =
    "Aliquam rhoncus, faucibus imperdiet elementum. Ac praesent condimentum massa nam eu. Duis tellus aenean nunc id interdum. Mattis imperdiet fringilla purus tortor, egestas interdum. Eget posuere vel semper maecenas aliquet vulputate mattis aliquet.";
  const dummyText3 =
    "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?";

  const dummyAvatarMentor =
    "https://images.unsplash.com/photo-1600486913747-55e5470d6f40?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2340&q=80";

  const mentorData: MentorObject = {
    firstName: "John",
    lastName: "Doe",
    topic: "Random topic",
    avatar: dummyAvatarMentor,
    nextMeeting: new Date("2022-02-25"),
  };

  return (
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="My mentors"
        mentors={mentors}
      />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          <div className="flex flex-col w-[100%]">
            <MentorDetails
              firstName={mentorData.firstName}
              lastName={mentorData.lastName}
              topic={mentorData.topic}
              avatar={mentorData.avatar}
              nextMeeting={mentorData.nextMeeting}
            />

            <div className="w-[90%] flex flex-col mr-auto ml-auto pb-44">
              <Meeting date={dummyDate1} feedback={dummyText1.repeat(2)} />
              <Meeting date={dummyDate2} feedback={dummyText2.repeat(3)} />
              <Meeting date={dummyDate3} feedback={dummyText3.repeat(4)} />
            </div>
          </div>
        </div>

        {/* Plan of action */}
        <PlanOfAction />
      </div>
    </div>
  );
}

export default DashboardMentee;
