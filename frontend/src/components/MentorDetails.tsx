import axios from "axios";
import React, { useEffect, useState } from "react";
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
  Rating,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";

import {
  BiCalendarEvent,
  BiCalendarPlus,
  BiPlus,
  BiStar,
} from "react-icons/bi";

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
  nextMeeting: Date | null;
  handleNewMeeting: () => void;
}

interface SkillRating {
  name: string;
  rating: number;
}

function revParseDate(d: string) {
  const [date, time] = d.split("T");
  const [year, month, day] = date.split("-");
  return `${parseInt(day)}/${parseInt(month)}/${year.slice(-2)} ${time}`;
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

const currentDate = () => {
  const dateNow = new Date(); // Creating a new date object with the current date and time
  const year = dateNow.getFullYear(); // Getting current year from the created Date object
  const monthWithOffset = dateNow.getUTCMonth() + 1; // January is 0 by default in JS. Offsetting +1 to fix date for calendar.
  const month = // Setting current Month number from current Date object
    monthWithOffset.toString().length < 2 // Checking if month is < 10 and pre-prending 0 to adjust for date input.
      ? `0${monthWithOffset}`
      : monthWithOffset;
  const day =
    dateNow.getUTCDate().toString().length < 2 // Checking if date is < 10 and pre-prending 0 if not to adjust for date input.
      ? `0${dateNow.getUTCDate()}`
      : dateNow.getUTCDate();
  const hour =
    dateNow.getHours().toString().length < 2
      ? `0${dateNow.getHours()}`
      : dateNow.getHours();

  const mins =
    dateNow.getMinutes().toString().length < 2
      ? `0${dateNow.getMinutes()}`
      : dateNow.getMinutes();

  return `${year}-${month}-${day}T${hour}:${mins}`;
};

// Mentor details component
const MentorDetails: React.FC<MentorProps> = (props) => {
  const [schedulerOpen, setSchedulerOpen] = useState(false);
  const [raterOpen, setRaterOpen] = useState(false);
  const [skills, setSkills] = useState<SkillRating[]>([]);

  useEffect(() => {
    axios.get("/api/admin/get-skills").then((res) => {
      const newSkills = res.data.map((skill: any) => ({
        name: skill.name,
        rating: 0,
      }));
      setSkills(newSkills);
    });
  }, []);

  // TODO schedule a meeting function
  const schedule = () => {
    console.log(
      `title: ${title}, descrip: ${descrip}, start: ${revParseDate(
        start
      )}, end: ${revParseDate(end)}`
    );

    axios
      .post("/api/meetings/create-meeting", {
        relationID: mentor.relationID,
        startTime: revParseDate(start),
        endTime: revParseDate(end),
        title: title,
        description: descrip,
      })
      .then((res: any) => {
        props.handleNewMeeting();
      });
    setSchedulerOpen(false);
    return;
  };

  const rateMentor = () => {
    console.log(skills);
    axios.post("/api/relations/rate-mentor", {
      mentorID: mentor.id,
      skills: skills.map((skill) => skill.name),
      ratings: skills.map((skill) => Math.round(skill.rating*2))
    }).then((res) => {
      console.log(res);
      setRaterOpen(false);
    })
  };

  const updateRating = (value: number, index: number) => {
    const newSkills = [...skills];
    newSkills[index] = { name: skills[index].name, rating: value };
    setSkills(newSkills);
  };

  const mentor: UserData = props.mentorData;

  const [title, setTitle] = useState<string>("");
  const [descrip, setDescrip] = useState<string>("");
  const [start, setStart] = useState<string>(currentDate());
  const [end, setEnd] = useState<string>(currentDate());

  // Next meeting date formatting
  // TODO check formatting
  let date: string = "";

  if (props.nextMeeting != null) {
    const weekday = props.nextMeeting.toLocaleString("default", {
      weekday: "long",
    });
    const month = props.nextMeeting.getMonth() + 1;
    date =
      weekday +
      ", " +
      props.nextMeeting.getDate() +
      "." +
      month +
      "." +
      props.nextMeeting.getFullYear();
  }

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
        <div className="flex m-auto mr-3 space-x-4">
          {/* Schedule meeting button */}
          <Tooltip title="Schedule Meeting" arrow>
            <button
              className="bg-prussianBlue text-cultured text-xl  p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
              onClick={() => setSchedulerOpen(true)}
            >
              <BiCalendarPlus className="h-12 w-12 p-2" />
            </button>
          </Tooltip>
          <Dialog
            fullWidth
            maxWidth="sm"
            onClose={() => setSchedulerOpen(false)}
            open={schedulerOpen}
          >
            <div>
              <DialogTitle>Schedule Meeting</DialogTitle>
              <DialogContent>
                <div className="flex flex-col space-y-3 pt-2">
                  <TextField
                    label="Title"
                    value={title}
                    onChange={(e: any) => setTitle(e.target.value)}
                  ></TextField>
                  <TextField
                    label="Description"
                    value={descrip}
                    multiline
                    onChange={(e: any) => setDescrip(e.target.value)}
                  ></TextField>
                  <TextField
                    label="Start time"
                    type="datetime-local"
                    value={start}
                    defaultValue={currentDate()}
                    onChange={(e: any) => setStart(e.target.value)}
                  ></TextField>
                  <TextField
                    label="End time"
                    type="datetime-local"
                    value={end}
                    defaultValue={currentDate()}
                    onChange={(e: any) => setEnd(e.target.value)}
                  ></TextField>
                </div>
              </DialogContent>
              <DialogActions>
                <Button onClick={schedule} sx={{ color: "#0E2A47" }}>
                  Schedule
                </Button>
              </DialogActions>
            </div>
          </Dialog>

          {/* Rate mentor button */}
          <Tooltip title="Rate Mentor" arrow>
            <button
              className="bg-firebrick text-cultured text-xl  p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-imperialRed duration-200 mr-0"
              onClick={() => setRaterOpen(true)}
            >
              <BiStar className="h-12 w-12 p-2" />
            </button>
          </Tooltip>
          <Dialog
            fullWidth
            maxWidth="xs"
            onClose={() => setRaterOpen(false)}
            open={raterOpen}
          >
            <div>
              <DialogTitle>Rate Mentor</DialogTitle>
              <DialogContent>
                <div className="flex flex-col space-y-3 pt-2">
                  {skills.map((skill, index) => (
                    <div key={index}>
                      <Typography component="legend">{skill.name}</Typography>
                      <Rating
                        precision={0.5}
                        onChange={(e: any) => {
                          updateRating(e.target.value, index);
                        }}
                      ></Rating>
                    </div>
                  ))}
                </div>
              </DialogContent>
              <DialogActions>
                <Button onClick={rateMentor} sx={{ color: "#0E2A47" }}>
                  Rate
                </Button>
              </DialogActions>
            </div>
          </Dialog>
        </div>
      </div>

      {/* Next meeting date */}
      {/* //! BROKEN */}
      {props.nextMeeting != null && (
        <div className="flex flex-row text-lg font-body m-5 mt-10 mb-0">
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
