import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBarMentor";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent } from "react-icons/bi";
import { Avatar } from "@mui/material";
import { Navigate, useLocation } from "react-router-dom";

interface UserData {
  id?: number;
  email: string;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics: string[];
}

interface MenteeDetailsProps {
  firstName: string;
  lastName: string;
  avatar: string;
  topics: string[];
  nextMeeting: Date;
}

interface MeetingProps {
  date: Date;
  feedback: string;
}

// Mentor details component
const MenteeDetails: React.FC<MenteeDetailsProps> = (props) => {
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
            sx={{ width: 100, height: 100 }}
          />

          {/* Mentor name & topic */}
          <div className="flex flex-col text-left m-auto pl-4 space-y-1">
            <h2 className="font-semibold text-3xl">
              {props.firstName + " " + props.lastName}
            </h2>
            <h3 className="text-xl">
              {props.topics.map((topic, i, { length }) => {
                if (i === length - 1) {
                  return <span>{topic}</span>;
                } else return <span>{topic + ", "}</span>;
              })}
            </h3>
          </div>
        </div>

        {/* Schedule meeting button */}
        <button
          className="bg-prussianBlue text-cultured text-xl w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-2"
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

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function DashboardMentor() {
  // const [currentMentee, setCurrentMentee] = React.useState<UserData>({email: "", firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topic: []});
  const [mentees, setMentees] = React.useState<UserData[]>([]);

  // Get mentee-mentor relations and mentees' data
  useEffect(() => {
    axios.get("/api/relations/get-relations").then(async (res) => {
      var newMentees: any = [];
      var newTopics: string[][] = [];

      for (let i = 0; i < res.data.length; i++) {
        const element = res.data[i];
        const menteeID: number = element.menteeid;

        // Get mentee data
        await axios
          .post("/api/users/get-user-data", { userID: menteeID })
          .then((res) => {
            newMentees.push({
              id: menteeID,
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
          .post("/api/users/get-user-topics", { userID: menteeID })
          .then((res) => {
            const arr: string[] = [];
            res.data.map((t: any) => {
              arr.push(t.topic);
            });

            newTopics.push(arr);
          });
      }

      var newMenteesAll: UserData[] = [];
      for (let i = 0; i < newMentees.length; i++) {
        const element = newMentees[i];

        newMenteesAll.push({
          id: element.id,
          email: element.email,
          firstName: element.firstName,
          lastName: element.lastName,
          avatar: element.avatar,
          role: element.role,
          businessArea: element.businessArea,
          topics: newTopics[i],
        });
      }

      setMentees(newMenteesAll);
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

  // Read the query string to get the mentee to render
  let query = useQuery();
  const currentMenteeId = query.get("mentee");
  let currentMenteeIdNum: number = -1;
  let currentMentee: UserData = {email: "", firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topics: []};

  if (mentees.length > 0 && currentMenteeId == null) {
    return <Navigate to={"/dashboard-mentor?mentee=" + mentees[0].id} />;
  }

  for (let i = 0; i < mentees.length; i++) {
    if (currentMenteeId != null && mentees[i].id === parseInt(currentMenteeId)) {
      currentMenteeIdNum = parseInt(currentMenteeId);
      currentMentee = mentees[i];
    }
  }

  return (
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="My mentees"
        activeMenteeId={currentMenteeIdNum}
        mentees={mentees}
      />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          <div className="flex flex-col w-[100%]">
            <MenteeDetails
              firstName={currentMentee.firstName}
              lastName={currentMentee.lastName}
              topics={currentMentee.topics}
              avatar={currentMentee.avatar}
              nextMeeting={new Date("2022-02-25")}
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

export default DashboardMentor;
