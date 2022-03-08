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
  email: string;
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
  let hasNextMeeting: Boolean = false;

  useEffect(() => {
    axios
      .post("/api/meetings/get-next-meeting", { relationID: mentor.relationID })
      .then(async (res: any) => {
        console.log(res.data);

        if (!res.data.hasOwnProperty("error")) {
          hasNextMeeting = true;
          setNextMeeting(new Date(res.data.starttime));
        }
      });
  }, []);

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

function parseDate(d: string) {
  const [date, time] = d.split(" ");
  const [day, month, year] = date.split("/");
  const [hour, min] = time.split(":");
  let fullYear: string;

  if (parseInt(year) < 30) {
    fullYear = "20" + year;
  } else {
    fullYear = "19" + year;
  }

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
  const [mentor, setMentor] = React.useState<UserData>({
    relationID: -1,
    email: "",
    firstName: "",
    lastName: "",
    avatar: "",
    role: "",
    businessArea: "",
    topics: [],
    meetings: [],
  });

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
              email: res.data.email,
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
      setMentor(newMentors[0])
    });
  }, []);


  return (
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="My mentors"
        activeMentorId={mentor.id}
        mentors={mentors}
        setMentor={setMentor}
      />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          <div className="flex flex-col w-[100%]">
            <MentorDetails mentorData={mentor} />

            <div className="w-[90%] flex flex-col mr-auto ml-auto pb-44">
              {mentor.meetings.map((meeting) => {
                return <MeetingCard meetingData={meeting} />;
              })}
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
