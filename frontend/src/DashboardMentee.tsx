import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import NavBar from "./components/NavBarMentee";
import PlanOfAction from "./components/PlanOfAction";
import { BiCalendarCheck, BiCalendarEvent } from "react-icons/bi";
import {
  Avatar,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Modal,
} from "@mui/material";
import { Link, Navigate, useLocation } from "react-router-dom";
import MeetingCard from "./components/MeetingCard";
import { setSyntheticLeadingComments } from "typescript";

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

interface MentorProps {
  mentorData: UserData;
}

// Mentor details component
const MentorDetails: React.FC<MentorProps> = (props) => {
  const [open, setOpen] = React.useState(false);

  // TODO schedule a meeting function
  const schedule = () => {
    console.log("SCHEDULE");
    return;
  };

  const mentor: UserData = props.mentorData;
  const [nextMeeting, setNextMeeting] = React.useState<Date>(new Date());
  const [hasNextMeeting, setHasNextMeeting]=  React.useState<Boolean>(false);

  useEffect(() => {
    // console.log("here");
    axios
      .post("/api/meetings/get-next-meeting", { relationID: mentor.relationID })
      .then(async (res: any) => {
        // console.log(mentor.relationID)
        // console.log(res.data);
        if (!res.data.hasOwnProperty("error")) {
          setHasNextMeeting(true);
          setNextMeeting(new Date(parseDate(res.data.starttime)));
        }
      });
  }, [mentor]);

  // Next meeting date formatting
  // TODO check formatting
  const weekday = nextMeeting.toLocaleString("default", {
    weekday: "long",
  });
  const month = nextMeeting.getMonth() + 1;
  const date =
    weekday +
    ", " +
    nextMeeting.getDate() +
    "." +
    month +
    "." +
    nextMeeting.getFullYear();

  return (
    <div className="flex flex-col m-10 mb-6 text-firebrick font-display">
      <div className="flex flex-row h-min">
        <div className="flex flex-row">
          <div className="flex flex-row mr-4">
            {/* TODO Mentor profile pic */}
            <Avatar
              className="m-auto"
              alt={mentor.firstName + " " + mentor.lastName}
              src={mentor.avatar}
              sx={{ width: 100, height: 100 }}
            />

            {/* Mentor name & topic */}
            <div className="flex flex-col text-left m-auto pl-4 space-y-1">
              <Link
                to={"/profile?id=" + mentor.id}
                className="font-semibold text-3xl hover:font-bold"
              >
                {mentor.firstName + " " + mentor.lastName}
              </Link>
              <h3 className="text-xl">
                {mentor.topics.map((topic, i, { length }) => {
                  if (i === length - 1) {
                    return <span>{topic}</span>;
                  } else return <span>{topic + ", "}</span>;
                })}
              </h3>
            </div>
          </div>
        </div>

        {/* Schedule meeting button */}
        <button
          className="bg-prussianBlue text-cultured text-xl min-w-100 flex-none w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
          onClick={() => setOpen(true)}
        >
          Schedule a meeting
        </button>
        <Dialog onClose={() => setOpen(false)} open={open}>
          <DialogTitle>Subscribe</DialogTitle>
          <DialogContent>
            <DialogContentText>
              To subscribe to this website, please enter your email address
              here. We will send updates occasionally.
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={schedule}>Schedule</Button>
          </DialogActions>
        </Dialog>
      </div>

      {/* Next meeting date */}
      {/* //! BROKEN */}
      {hasNextMeeting && (
        <div className="flex flex-row text-lg font-body m-5 mr-2 mb-0">
          <BiCalendarEvent className="mt-auto mb-auto text-3xl mr-1" />
          <p className="mt-auto mb-auto text-left">
            Your next meeting with {mentor.firstName} is on{" "}
            <span className="font-bold">{date}</span>
          </p>
        </div>
      )}
    </div>
  );
};

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

        await axios
          .post("/api/users/get-user-topics", { userID: relationship.mentorid })
          .then((res: any) => {
            mentorTopics = res.data.map((t: any) => t.topic);
          });

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
        <PlanOfAction relationID={currentMentor.relationID} />
      </div>
    </div>
  );
}

export default DashboardMentee;