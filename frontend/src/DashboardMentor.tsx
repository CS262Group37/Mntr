import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBarMentor from "./components/NavBarMentor";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent } from "react-icons/bi";
import { Avatar, Divider } from "@mui/material";
import { Navigate, useLocation } from "react-router-dom";
import MeetingCardMentor from "./components/MeetingCardMentor";
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
                case "going-ahead":
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

            // Sorting meetings - future from closest to most distant, past from most recent
            runningMeetings.sort((e1: any, e2: any) => {
              return e1.startTime - e2.startTime;
            });
            goingAheadMeetings.sort((e1: any, e2: any) => {
              return e1.startTime - e2.startTime;
            });
            pendingMeetings.sort((e1: any, e2: any) => {
              return e1.startTime - e2.startTime;
            });

            completedMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });
            missedMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });
            cancelledMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });
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
              id: relationship.menteeid,
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

  if (mentees.length > 0 && currentMenteeId === null) {
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
      <NavBarMentor
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
                  ? currentMentee.goingAheadMeetings[0].startTime
                  : null
              }
            />

            <div className="w-[94%] flex flex-col mr-auto ml-auto pb-44">
              {currentMentee.pendingMeetings.map((meeting) => {
                return (
                  <MeetingCardMentor
                    meetingData={meeting}
                    handleNewMeeting={getMentees}
                  />
                );
              })}

{currentMentee.runningMeetings.map((meeting) => {
                return (
                  <MeetingCardMentor
                    meetingData={meeting}
                    handleNewMeeting={getMentees}
                  />
                );
              })}

{currentMentee.runningMeetings.length > 0 &&
                (currentMentee.missedMeetings.length > 0 ||
                  currentMentee.completedMeetings.length > 0) && (
                  <Divider sx={{ marginTop: 3, marginBottom: 3 }} />
                )}
              {currentMentee.completedMeetings.map((meeting) => {
                return (
                  <MeetingCardMentor
                    meetingData={meeting}
                    handleNewMeeting={getMentees}
                  />
                );
              })}
              {currentMentee.missedMeetings.map((meeting) => {
                return (
                  <MeetingCardMentor
                    meetingData={meeting}
                    handleNewMeeting={getMentees}
                  />
                );
              })}

              {currentMentee.cancelledMeetings.length > 0 &&
                (currentMentee.missedMeetings.length > 0 ||
                  currentMentee.completedMeetings.length > 0) && (
                  <Divider sx={{ marginTop: 3, marginBottom: 3 }} />
                )}
              {currentMentee.cancelledMeetings.map((meeting) => {
                return (
                  <MeetingCardMentor
                    meetingData={meeting}
                    handleNewMeeting={getMentees}
                  />
                );
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
