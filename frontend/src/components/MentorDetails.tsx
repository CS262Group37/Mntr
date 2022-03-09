import axios from "axios";
import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Avatar,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Modal,
  TextField,
} from "@mui/material";
import { BiCalendarEvent } from "react-icons/bi";

interface UserData {
  relationID: number;
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics: string[];
}

interface MentorProps {
  mentorData: UserData;
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
  const [hasNextMeeting, setHasNextMeeting] = React.useState<Boolean>(false);

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
            <div className="flex flex-col space-y-3">
            <TextField label="Title"></TextField>
            <TextField label="Description" multiline></TextField>
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={schedule} sx={{ color: "#0E2A47" }}>
              Schedule
            </Button>
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

export default MentorDetails;
