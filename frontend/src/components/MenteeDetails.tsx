import axios from "axios";
import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Avatar,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
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

interface MenteeProps {
  menteeData: UserData;
  nextMeeting: Date | null;
  handleNewMeeting: () => void;
}

function revParseDate(d: string) {
  const [date, time] = d.split("T");
  const [year, month, day] = date.split("-")
  return (`${parseInt(day)}/${parseInt(month)}/${year.slice(-2)} ${time}`)
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

// Mentee details component
const MenteeDetails: React.FC<MenteeProps> = (props) => {
  const [open, setOpen] = React.useState(false);

  const schedule = () => {
    console.log(
      `title: ${title}, descrip: ${descrip}, start: ${revParseDate(start)}, end: ${revParseDate(end)}`
    );

    axios
      .post("/api/meetings/create-meeting", {
        relationID: mentee.relationID,
        startTime: revParseDate(start),
        endTime: revParseDate(end),
        title: title,
        description: descrip,
      })
      .then((res: any) => {
        props.handleNewMeeting()
        
      });
      setOpen(false)
    return;
  };

  const mentee: UserData = props.menteeData;
  // const [nextMeeting, setNextMeeting] = useState<Date>(new Date());
  // const [hasNextMeeting, setHasNextMeeting] = useState<Boolean>(false);

  const [title, setTitle] = useState<string>("");
  const [descrip, setDescrip] = useState<string>("");
  const [start, setStart] = useState<string>(currentDate());
  const [end, setEnd] = useState<string>(currentDate());

  // useEffect(() => {
  //   console.log("here");
  //   axios
  //     .post("/api/meetings/get-next-meeting", { relationID: mentee.relationID })
  //     .then(async (res: any) => {
  //       // console.log(mentee.relationID)
  //       // console.log(res.data);
  //       if (!res.data.hasOwnProperty("error")) {
  //         console.log(res.data)
  //         setHasNextMeeting(true);
  //         setNextMeeting(new Date(parseDate(res.data.starttime)));
  //       }
  //     });
  // }, [mentee]);
  

  // Next meeting date formatting
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
            {/* TODO Mentee profile pic */}
            <Avatar
              className="m-auto"
              alt={mentee.firstName + " " + mentee.lastName}
              src={mentee.avatar}
              sx={{ width: 100, height: 100 }}
            />

            {/* Mentee name & topic */}
            <div className="flex flex-col text-left m-auto pl-4 space-y-1">
              <Link
                to={"/profile?id=" + mentee.id}
                className="font-semibold text-3xl hover:font-bold"
              >
                {mentee.firstName + " " + mentee.lastName}
              </Link>
              <h3 className="text-xl">
                {mentee.topics.map((topic, i, { length }) => {
                  if (i === length - 1) {
                    return <span>{topic}</span>;
                  } else return <span>{topic + ", "}</span>;
                })}
              </h3>
            </div>
          </div>
        </div>

        {/* Schedule meeting button */}
        {/* <button
          className="bg-prussianBlue text-cultured text-xl min-w-100 flex-none w-64 p-4 m-auto rounded-full shadow-md transition ease-in-out hover:bg-brightNavyBlue duration-200 mr-0"
          onClick={() => setOpen(true)}
        >
          Schedule a meeting
        </button> */}
        <Dialog
          fullWidth
          maxWidth="sm"
          onClose={() => setOpen(false)}
          open={open}
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
      </div>

      {/* Next meeting date */}
      { props.nextMeeting != null && (
        <div className="flex flex-row text-lg font-body m-5 mt-10 mb-0">
          <BiCalendarEvent className="mt-auto mb-auto text-3xl mr-1" />
          <p className="mt-auto mb-auto text-left">
            Your next meeting with {mentee.firstName} is on{" "}
            <span className="font-bold">{date}</span>
          </p>
        </div>
      )}
    </div>
  );
};

export default MenteeDetails;
