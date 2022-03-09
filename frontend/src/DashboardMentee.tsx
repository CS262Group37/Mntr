import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBarMentee";
import PlanOfAction from "./components/PlanOfAction";
import { Link, Navigate, useLocation } from "react-router-dom";
import MeetingCard from "./components/MeetingCard";
import MentorDetails from "./components/MentorDetails";

interface UserData {
  relationID: number;
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics: string[];
  meetings: Meeting[];
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

function DashboardMentee() {
  const [mentors, setMentors] = React.useState<UserData[]>([]);

  // Get mentee-mentor relations and mentees' data
  useEffect(() => {
    axios.get("/api/relations/get-relations").then(async (res: any) => {
      var newMentors: UserData[] = [];

      for (const relationship of res.data) {
        let mentorTopics: string[];

        // Get topics
        await axios
          .post("/api/users/get-user-topics", { userID: relationship.mentorid })
          .then((res: any) => {
            mentorTopics = res.data.map((t: any) => t.topic);
          });

        // Get meetings
        let mentorMeetings: Meeting[] = [];
        await axios
          .post("/api/meetings/get-meetings", {
            relationID: relationship.relationid,
          })
          .then((res: any) => {
            mentorMeetings = res.data.map((m: any) => {
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

            mentorMeetings.sort((e1: any, e2: any) => {
              return e2.startTime - e1.startTime;
            });
          });

        // Get plan of action
        let goals: Goal[] = [];
        await axios
          .get("/api/plan/get-plan", { params: {relationID: relationship.relationid} })
          .then((res: any) => {
            console.log(res.data);

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
          .post("/api/users/get-user-data", { userID: relationship.mentorid })
          .then((res: any) => {
            const mentor: UserData = {
              relationID: relationship.relationid,
              id: relationship.mentorid,
              firstName: res.data.firstname,
              lastName: res.data.lastname,
              avatar: res.data.profilepicture,
              role: res.data.role,
              businessArea: res.data.businessarea,
              topics: mentorTopics,
              meetings: mentorMeetings,
              planOfAction: goals,
            };

            newMentors.push(mentor);
          });
      }

      setMentors(newMentors);
    });
  }, []);

  // Read the query string to get the mentee to render
  let query = useQuery();
  const currentMentorId = query.get("mentor");
  let currentMentorIdNum: number = -1;
  let currentMentor: UserData = {
    relationID: -1,
    firstName: "",
    lastName: "",
    avatar: "",
    role: "",
    businessArea: "",
    topics: [],
    meetings: [],
    planOfAction: [],
  };

  if (mentors.length > 0 && currentMentorId == null) {
    return <Navigate to={"/dashboard-mentee?mentor=" + mentors[0].id} />;
  }

  for (let i = 0; i < mentors.length; i++) {
    if (
      currentMentorId != null &&
      mentors[i].id === parseInt(currentMentorId)
    ) {
      currentMentorIdNum = parseInt(currentMentorId);
      currentMentor = mentors[i];
    }
  }

  console.log(currentMentor);

  return (
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="My mentors"
        activeMentorId={currentMentorIdNum}
        mentors={mentors}
      />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          <div className="flex flex-col w-[100%]">
            <MentorDetails mentorData={currentMentor} />

            <div className="w-[90%] flex flex-col mr-auto ml-auto pb-44">
              {currentMentor.meetings.map((meeting) => {
                return <MeetingCard meetingData={meeting} />;
              })}
            </div>
          </div>
        </div>

        {/* Plan of action */}
        <PlanOfAction goals={currentMentor.planOfAction} />
      </div>
    </div>
  );
}

export default DashboardMentee;