import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBarMentor from "./components/NavBarMentor";
import PlanOfAction from "./components/PlanOfAction";
import MeetingCardMentor from "./components/MeetingCardMentor";
import { Divider } from "@mui/material";

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
}

interface Meeting {
  meetingID: number;
  title: string;
  description: string;
  feedback: string;
  status: string;
  startTime: Date;
  endTime: Date;
  user: UserData;
}

interface MeetingObject {
  goingAheadMeetings: Meeting[];
  pendingMeetings: Meeting[];
  completedMeetings: Meeting[];
  cancelledMeetings: Meeting[];
  missedMeetings: Meeting[];
  runningMeetings: Meeting[];
}

function parseDateStr(d: string) {
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

function Meetings() {
  const [meetings, setMeetings] = React.useState<MeetingObject>({
    goingAheadMeetings: [],
    pendingMeetings: [],
    completedMeetings: [],
    cancelledMeetings: [],
    missedMeetings: [],
    runningMeetings: [],
  });

  const getMeetings = () => {
    axios.get("/api/relations/get-relations").then(async (res: any) => {
      var newGoingAheadMeetings: Meeting[] = [];
      var newPendingMeetings: Meeting[] = [];
      var newCompletedMeetings: Meeting[] = [];
      var newCancelledMeetings: Meeting[] = [];
      var newMissedMeetings: Meeting[] = [];
      var newRunningMeetings: Meeting[] = [];

      for (const relationship of res.data) {
        // Get mentee data
        let mentee: UserData;
        await axios
          .post("/api/users/get-user-data", { userID: relationship.menteeid })
          .then((res: any) => {
            mentee = {
              id: relationship.menteeid,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
            };
          });

        // Get meetings
        let menteeMeetings: Meeting[];
        await axios
          .post("/api/meetings/get-meetings", {
            relationID: relationship.relationid,
          })
          .then((res: any) => {
            menteeMeetings = res.data.map((m: any) => {
              return {
                meetingID: m.meetingid,
                title: m.title,
                description: m.description,
                feedback: m.feedback,
                status: m.status,
                startTime: parseDateStr(m.starttime),
                endTime: parseDateStr(m.starttime),
                user: mentee,
              };
            });

            menteeMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });

            for (const meeting of menteeMeetings) {
              switch (meeting.status) {
                case "going-ahead":
                  newGoingAheadMeetings.push(meeting);
                  break;
                case "pending":
                  newPendingMeetings.push(meeting);
                  break;
                case "completed":
                  newCompletedMeetings.push(meeting);
                  break;
                case "cancelled":
                  newCancelledMeetings.push(meeting);
                  break;
                case "missed":
                  newMissedMeetings.push(meeting);
                  break;
                case "running":
                  newRunningMeetings.push(meeting);
                  break;
              }
            }
          });
      }

      setMeetings({
        goingAheadMeetings: newGoingAheadMeetings,
        pendingMeetings: newPendingMeetings,
        completedMeetings: newCompletedMeetings,
        cancelledMeetings: newCancelledMeetings,
        missedMeetings: newMissedMeetings,
        runningMeetings: newRunningMeetings,
      });
    });
  };

  // Get mentee-mentor relations and mentees' data
  useEffect(() => {
    getMeetings();
    console.log(meetings);
  }, []);

  return (
    <div className="fixed h-full w-full">
      <NavBarMentor activeStr="Meetings" />

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        <div className="w-[94%] flex flex-col mr-auto ml-auto pb-44">
          {meetings.runningMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}

          {meetings.goingAheadMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}

          {meetings.pendingMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}

          {meetings.pendingMeetings.length > 0 &&
            (meetings.missedMeetings.length > 0 ||
              meetings.completedMeetings.length > 0) && (
              <Divider sx={{ marginTop: 3, marginBottom: 3 }} />
            )}

          {meetings.completedMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}
          {meetings.missedMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}

          {meetings.cancelledMeetings.length > 0 &&
            (meetings.missedMeetings.length > 0 ||
              meetings.completedMeetings.length > 0) && (
              <Divider sx={{ marginTop: 3, marginBottom: 3 }} />
            )}
          {meetings.cancelledMeetings.map((meeting) => {
            return (
              <MeetingCardMentor
                meetingData={meeting}
                handleNewMeeting={getMeetings}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default Meetings;
