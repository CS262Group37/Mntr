import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBarMentor";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent } from "react-icons/bi";
import { Avatar } from "@mui/material";
import { Navigate, useLocation } from "react-router-dom";
import MeetingCard from "./components/MeetingCard";
import MenteeDetails from "./components/MenteeDetails";

interface UserData {
  relationID: number;
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics: string[];
  goingAheadMeetings: Meeting[];
  pendingMeetings: Meeting[];
  completedMeetings: Meeting[];
  cancelledMeetings: Meeting[];
  missedMeetings: Meeting[];
  runningMeetings: Meeting[];
  planOfAction: Goal[];
}

interface Meeting {
  meetingID: number;
  title: string;
  description: string;
  feedback: string;
  status: string;
  startTime: Date;
  endTime: Date;
}

interface Goal {
  goalID?: number;
  title: string;
  description: string;
  creationDate?: Date;
  status: string;
}

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

// // Mentor details component
// const MenteeDetails: React.FC<MenteeDetailsProps> = (props) => {
//   // Next meeting date formatting
//   const weekday = props.nextMeeting.toLocaleString("default", {
//     weekday: "long",
//   });
//   const month = props.nextMeeting.getMonth() + 1;
//   const date =
//     weekday +
//     ", " +
//     props.nextMeeting.getDate() +
//     "." +
//     month +
//     "." +
//     props.nextMeeting.getFullYear();

//   return (
//     <div className="flex flex-col m-10 mb-2 text-firebrick font-display">
//       <div className="flex flex-row h-min">
//         <div className="flex">
//           {/* TODO Mentor profile pic */}
//           <Avatar
//             className="m-auto"
//             alt={props.firstName + " " + props.lastName}
//             src={props.avatar}
//             sx={{ width: 100, height: 100 }}
//           />

//           {/* Mentor name & topic */}
//           <div className="flex flex-col text-left m-auto pl-4 space-y-1">
//             <h2 className="font-semibold text-3xl">
//               {props.firstName + " " + props.lastName}
//             </h2>
//             <h3 className="text-xl">
//               {props.topics.map((topic, i, { length }) => {
//                 if (i === length - 1) {
//                   return <span>{topic}</span>;
//                 } else return <span>{topic + ", "}</span>;
//               })}
//             </h3>
//           </div>
//         </div>

//         {/* Schedule meeting button */}
//         <button className="bg-prussianBlue text-cultured text-xl w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-2">
//           Schedule a meeting
//         </button>
//       </div>

//       {/* Next meeting date */}
//       <div className="flex flex-row text-lg font-body m-5">
//         <BiCalendarEvent className="mt-auto mb-auto text-3xl mr-1" />
//         <p className="mt-auto mb-auto text-left">
//           Your next meeting with {props.firstName} is on{" "}
//           <span className="font-bold">{date}</span>
//         </p>
//       </div>
//     </div>
//   );
// };

// // Meeting component
// const Meeting: React.FC<MeetingProps> = (props) => {
//   const month = props.date.toLocaleString("default", { month: "long" });
//   const date =
//     month + " " + props.date.getDate() + ", " + props.date.getFullYear();

//   return (
//     <div className="flex flex-col bg-gray-300 bg-opacity-50 shadow-md mt-5 mb-5 w-[100%] text-prussianBlue p-4 rounded-xl">
//       {/* Heading & date */}
//       <div className="flex flex-row text-2xl border-b-2 border-imperialRed justify-between">
//         <h1 className="font-semibold mt-1 mb-3 ml-3 text-left">
//           Individual meeting
//         </h1>
//         <div className="flex flex-row mr-3 mt-1 mb-3 text-right">
//           <BiCalendarCheck className="text-3xl mr-1" />
//           <h1>{date}</h1>
//         </div>
//       </div>

//       {/* Mentor feedback */}
//       <div className="font-body text-lg text-justify m-3 mb-1">
//         <p>{props.feedback}</p>
//       </div>
//     </div>
//   );
// };

function parseDate(d: string) {
  const [date, time] = d.split(" ");
  const [day, month, year] = date.split("/");
  const [hour, min] = time.split(":");
  const fullYear = "20" + year;

  return new Date(
    new Date(
      parseInt(fullYear),
      parseInt(month) - 1,
      parseInt(day),
      parseInt(hour),
      parseInt(min)
    )
  );
}

function DashboardMentor() {
  const [mentees, setMentees] = React.useState<UserData[]>([]);

  const getMentees = () => {
    axios.get("/api/relations/get-relations").then(async (res: any) => {
      var newMentees: UserData[] = [];

      for (const relationship of res.data) {
        let menteeTopics: string[];

        // Get topics
        await axios
          .post("/api/users/get-user-topics", { userID: relationship.menteeid })
          .then((res: any) => {
            menteeTopics = res.data.map((t: any) => t.topic);
          });

        // Get meetings
        let menteeMeetings: Meeting[] = [];
        let goingAheadMeetings: Meeting[] = [];
        let pendingMeetings: Meeting[] = [];
        let completedMeetings: Meeting[] = [];
        let cancelledMeetings: Meeting[] = [];
        let missedMeetings: Meeting[] = [];
        let runningMeetings: Meeting[] = [];

        await axios
          .post("/api/meetings/get-meetings", {
            relationID: relationship.relationid,
          })
          .then((res: any) => {
            console.log(res.data);
            menteeMeetings = res.data.map((m: any) => {
              return {
                meetingID: m.meetingid,
                title: m.title,
                description: m.description,
                feedback: m.feedback,
                status: m.status,
                startTime: parseDate(m.starttime),
                endTime: parseDate(m.starttime),
              };
            });

            menteeMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });

            for (const meeting of menteeMeetings) {
              switch (meeting.status) {
                case "goingAhead":
                  goingAheadMeetings.push(meeting);
                  break;
                case "pending":
                  pendingMeetings.push(meeting);
                  break;
                case "completed":
                  completedMeetings.push(meeting);
                  break;
                case "cancelled":
                  cancelledMeetings.push(meeting);
                  break;
                case "missed":
                  missedMeetings.push(meeting);
                  break;
                case "running":
                  runningMeetings.push(meeting);
                  break;
              }
            }
          });

        // Get plan of action
        let goals: Goal[] = [];
        await axios
          .get("/api/plan/get-plan", {
            params: { relationID: relationship.relationid },
          })
          .then((res: any) => {
            goals = res.data.map((g: any) => {
              return {
                goalID: g.planofactionid,
                title: g.title,
                description: g.description,
                // creationDate: parseDate(g.creationdate),
                status: g.status,
              };
            });
          });

        await axios
          .post("/api/users/get-user-data", { userID: relationship.menteeid })
          .then((res: any) => {
            const mentee: UserData = {
              relationID: relationship.relationid,
              id: relationship.mentorid,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
              businessArea: res.data.businessarea,
              topics: menteeTopics,
              goingAheadMeetings: goingAheadMeetings,
              pendingMeetings: pendingMeetings,
              completedMeetings: completedMeetings,
              cancelledMeetings: cancelledMeetings,
              missedMeetings: missedMeetings,
              runningMeetings: runningMeetings,
              planOfAction: goals,
            };

            newMentees.push(mentee);
          });
      }

      setMentees(newMentees);
    });
  };

  // Get mentee-mentor relations and mentees' data
  useEffect(() => {
    getMentees();
  }, []);

  // Read the query string to get the mentee to render
  let query = useQuery();
  const currentMenteeId = query.get("mentee");
  let currentMenteeIdNum: number = -1;
  let currentMentee: UserData = {
    relationID: -1,
    firstName: "",
    lastName: "",
    avatar: "",
    role: "",
    businessArea: "",
    topics: [],
    goingAheadMeetings: [],
    pendingMeetings: [],
    completedMeetings: [],
    cancelledMeetings: [],
    missedMeetings: [],
    runningMeetings: [],
    planOfAction: [],
  };

  if (mentees.length > 0 && currentMenteeId == null) {
    return <Navigate to={"/dashboard-mentor?mentee=" + mentees[0].id} />;
  }

  for (let i = 0; i < mentees.length; i++) {
    if (
      currentMenteeId !== null &&
      mentees[i].id === parseInt(currentMenteeId)
    ) {
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
              menteeData={currentMentee}
              handleNewMeeting={getMentees}
              nextMeeting={
                currentMentee.goingAheadMeetings.length > 0
                  ? currentMentee.goingAheadMeetings[
                      currentMentee.goingAheadMeetings.length - 1
                    ].startTime
                  : null
              }
            />

            <div className="w-[94%] flex flex-col mr-auto ml-auto pb-44">
              {currentMentee.pendingMeetings.map((meeting) => {
                return <MeetingCard meetingData={meeting} />;
              })}

              {currentMentee.pendingMeetings.length > 0 &&
                (currentMentee.missedMeetings.length > 0 ||
                  currentMentee.completedMeetings.length > 0) && (
                  <h1 className="text-left pt-6 mt-6 pl-4 text-3xl text-firebrick border-t-[1.5px] border-gray-200"></h1>
                )}
              {/* <hr className="border-[0.5px]"></hr> */}
              {currentMentee.completedMeetings.map((meeting) => {
                return <MeetingCard meetingData={meeting} />;
              })}
              {currentMentee.missedMeetings.map((meeting) => {
                return <MeetingCard meetingData={meeting} />;
              })}
            </div>
          </div>
        </div>

        {/* Plan of action */}
        <PlanOfAction
          goals={currentMentee.planOfAction}
          relationID={currentMentee.relationID}
          handleNewGoal={getMentees}
        />
      </div>
    </div>
  );
}

export default DashboardMentor;
